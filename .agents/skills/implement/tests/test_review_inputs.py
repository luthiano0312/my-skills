"""Testes do filtro: saída segura e repositórios Git exclusivamente temporários."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "review_inputs.py"
PRIVATE = "NARRATIVA_NAO_DEVE_ENTRAR_NO_CONTEXTO"


class ReviewInputsTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.git("init", "-b", "main")
        self.git("config", "user.name", "Fixture")
        self.git("config", "user.email", "fixture@example.invalid")
        self.registro = self.root / "docs/03-execucao/registro.md"
        self.setup_layout(self.registro)
        self.write("src/login.py", "BEFORE\n")
        self.git("add", "--", ".")
        self.git("commit", "-m", "baseline temporario")

    def git(self, *args):
        result = subprocess.run(["git", "-C", str(self.root), *args],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout

    def write(self, relative, content):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def setup_layout(self, registro):
        registro.parent.mkdir(parents=True, exist_ok=True)
        registro.write_text(
            "|Task|Marco|Status|Commit|Atualizado em|Observações|\n"
            "| :--- | ---: | :----: | --- | --- | --- |\n"
            "| M01-T03 | M01 | aguardando revisão | - | 2026-09-30T14:20:00-03:00 | "
            + PRIVATE + " |\n", encoding="utf-8")
        self.findings = registro.parent / "achados"
        self.findings.mkdir(parents=True, exist_ok=True)

    def run_script(self, task="M01-T03"):
        return subprocess.run([sys.executable, str(SCRIPT), str(self.registro), task],
                              capture_output=True, text=True)

    def assert_safe(self, result):
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn(PRIVATE, result.stdout + result.stderr)
        return json.loads(result.stdout)

    def test_untracked_reports_are_filtered_but_code_tests_and_docs_remain_visible(self):
        self.write("src/login.py", "STAGED_CODE\n")
        self.git("add", "--", "src/login.py")
        self.write("src/login.py", "WORKTREE_CODE\n")
        self.write("tests/login.py", "NEW_TEST_CODE\n")
        self.write("docs/reference/autenticacao.md", "DOC_DELIVERABLE\n")
        (self.findings / "task-M01-T03-relatorio.md").write_text(PRIVATE, encoding="utf-8")
        before_status = self.git("status", "--porcelain")
        before_index = self.git("ls-files", "--stage")
        before_files = {path.relative_to(self.root): path.read_bytes()
                        for path in self.root.rglob("*") if path.is_file() and ".git" not in path.parts}
        output = self.assert_safe(self.run_script())
        self.assertIn("WORKTREE_CODE", output["diffs"]["HEAD"])
        self.assertIn("STAGED_CODE", output["diffs"]["staged"])
        self.assertIn("WORKTREE_CODE", output["diffs"]["unstaged"])
        self.assertEqual(output["untracked_allowed"],
                         ["docs/reference/autenticacao.md", "tests/login.py"])
        self.assertIn("docs/03-execucao/achados/task-M01-T03-relatorio.md", output["deferred_changed"])
        self.assertEqual(self.git("status", "--porcelain"), before_status)
        self.assertEqual(self.git("ls-files", "--stage"), before_index)
        after_files = {path.relative_to(self.root): path.read_bytes()
                       for path in self.root.rglob("*") if path.is_file() and ".git" not in path.parts}
        self.assertEqual(after_files, before_files)

    def test_tracked_staged_and_unstaged_narratives_and_record_are_filtered(self):
        report = self.findings / "task-M01-T03-relatorio.md"
        report.write_text(PRIVATE + " BEFORE", encoding="utf-8")
        self.git("add", "--", str(report))
        self.git("commit", "-m", "relato temporario")
        report.write_text(PRIVATE + " STAGED", encoding="utf-8")
        self.git("add", "--", str(report))
        report.write_text(PRIVATE + " UNSTAGED", encoding="utf-8")
        self.registro.write_text(self.registro.read_text(encoding="utf-8").replace(PRIVATE, PRIVATE + " EDIT"),
                                 encoding="utf-8")
        self.write("src/login.py", "DELIVERED_CODE\n")
        review = self.findings / "task-M01-T03-revisao-1.md"
        review.write_text("Estado: finalizada\n" + PRIVATE, encoding="utf-8")
        (self.findings / "task-M01-T03-revisao-2.md").write_text(
            "Estado: incompleta\n" + PRIVATE, encoding="utf-8")
        output = self.assert_safe(self.run_script())
        self.assertIn("DELIVERED_CODE", output["diffs"]["HEAD"])
        self.assertEqual([(entry["round"], entry["state"]) for entry in output["reviews"]],
                         [(1, "finalizada"), (2, "incompleta")])
        for diff in output["diffs"].values():
            self.assertNotIn("Observações", diff)
            self.assertNotIn("relatorio.md", diff)
            self.assertNotIn("revisao-", diff)

    def test_metadata_only_changes_produce_empty_diffs_not_an_unfiltered_fallback(self):
        (self.findings / "task-M01-T03-relatorio.md").write_text(PRIVATE, encoding="utf-8")
        output = self.assert_safe(self.run_script())
        self.assertTrue(all(not diff for diff in output["diffs"].values()))
        self.assertEqual(output["untracked_allowed"], [])

    def test_recolhe_layout_is_discovered_from_the_supplied_record(self):
        self.registro = self.root / "docs_sistema_recolhe/execucao/registro.md"
        self.setup_layout(self.registro)
        (self.findings / "task-M01-T03-relatorio.md").write_text(PRIVATE, encoding="utf-8")
        self.write("docs_sistema_recolhe/reference/manual.md", "MANUAL\n")
        output = self.assert_safe(self.run_script())
        self.assertEqual(output["achados"], "docs_sistema_recolhe/execucao/achados")
        self.assertIn("docs_sistema_recolhe/reference/manual.md", output["untracked_allowed"])
        # O registro do outro layout não é metadado deste fluxo: não excluir docs/ inteira.
        self.assertNotIn("docs/03-execucao/registro.md", output["deferred_changed"])

    def test_unknown_artifact_in_findings_stops_without_emitting_content(self):
        (self.findings / "manual-entregavel.md").write_text(PRIVATE, encoding="utf-8")
        result = self.run_script()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertNotIn(PRIVATE, result.stderr)
        self.assertIn("não reconhecido", result.stderr)

    def test_rename_across_narrative_boundary_stops_before_content(self):
        report = self.findings / "task-M01-T03-relatorio.md"
        report.write_text(PRIVATE, encoding="utf-8")
        self.git("add", "--", str(report))
        self.git("commit", "-m", "relato temporario")
        (self.root / "docs/reference").mkdir(parents=True)
        self.git("mv", "--", str(report), "docs/reference/manual.md")
        result = self.run_script()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertNotIn(PRIVATE, result.stderr)
        self.assertIn("cruza", result.stderr)

    def test_symbolic_alias_to_narrative_is_not_allowed_for_reading(self):
        report = self.findings / "task-M01-T03-relatorio.md"
        report.write_text(PRIVATE, encoding="utf-8")
        try:
            (self.root / "manual.md").symlink_to(report)
        except OSError:
            self.skipTest("ambiente sem permissão para criar symlinks")
        result = self.run_script()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertNotIn(PRIVATE, result.stderr)

    def test_invalid_record_or_task_does_not_emit_observations(self):
        for task in ("M99-T99", "../M01-T03"):
            with self.subTest(task=task):
                result = self.run_script(task)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(result.stdout, "")
                self.assertNotIn(PRIVATE, result.stderr)

    def test_legacy_review_is_identified_without_emitting_its_conclusion(self):
        (self.findings / "task-M01-T03-revisao-1.md").write_text(PRIVATE, encoding="utf-8")
        output = self.assert_safe(self.run_script())
        self.assertEqual(output["reviews"][0]["state"], "não identificado")

    def test_snapshot_tracks_untracked_content_but_not_narrative_edits(self):
        code = self.write("tests/new.py", "FIRST_CODE\n")
        report = self.findings / "task-M01-T03-relatorio.md"
        report.write_text(PRIVATE, encoding="utf-8")
        first = self.assert_safe(self.run_script())["snapshot"]
        report.write_text(PRIVATE + " EDIT", encoding="utf-8")
        self.assertEqual(self.assert_safe(self.run_script())["snapshot"], first)
        code.write_text("SECOND_CODE\n", encoding="utf-8")
        self.assertNotEqual(self.assert_safe(self.run_script())["snapshot"], first)

    def test_new_task_id_does_not_inherit_four_reviews_from_replaced_task(self):
        old_files = []
        for number in range(1, 5):
            path = self.findings / f"task-M01-T03-revisao-{number}.md"
            path.write_text("Estado: finalizada\n" + PRIVATE, encoding="utf-8")
            old_files.append(path)
        record = self.registro.read_text(encoding="utf-8").replace(
            "aguardando revisão", "substituída"
        )
        record += "| M01-T07 | M01 | não iniciada | - | 2026-10-02T09:00:00-03:00 | origem: M01-T03 |\n"
        self.registro.write_text(record, encoding="utf-8")
        output = self.assert_safe(self.run_script("M01-T07"))
        self.assertEqual(output["reviews"], [])
        self.assertTrue(all(path.read_text(encoding="utf-8").endswith(PRIVATE) for path in old_files))
        review = self.findings / "task-M01-T07-revisao-1.md"
        review.write_text("Estado: incompleta\n" + PRIVATE, encoding="utf-8")
        output = self.assert_safe(self.run_script("M01-T07"))
        self.assertEqual([(entry["round"], entry["state"]) for entry in output["reviews"]],
                         [(1, "incompleta")])

    def test_integration_metadata_is_emitted_without_other_observations(self):
        integration = "b" * 40
        content = self.registro.read_text(encoding="utf-8").replace(
            "aguardando revisão | - |", "concluída | a1b2c3d |"
        ).replace(PRIVATE, PRIVATE + "; Integração: " + integration)
        self.registro.write_text(content, encoding="utf-8")
        output = self.assert_safe(self.run_script())
        self.assertEqual(output["integration"], integration)
        self.assertEqual(output["commit"], "a1b2c3d")
        self.assertEqual(output["registro_tasks"][0]["integration"], integration)

    def test_duplicate_review_state_markers_stop_without_emitting_narrative(self):
        review = self.findings / "task-M01-T03-revisao-1.md"
        review.write_text("Estado: incompleta\n" + PRIVATE + "\nEstado: finalizada\n",
                          encoding="utf-8")
        result = self.run_script()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertNotIn(PRIVATE, result.stderr)


if __name__ == "__main__":
    unittest.main()
