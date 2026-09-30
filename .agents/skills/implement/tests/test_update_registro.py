"""Testes do contrato de registro compartilhado por plan e implement.

Rodar: python -m unittest discover -s .agents/skills/implement/tests -v
"""

import subprocess
import sys
import tempfile
import unittest
from datetime import datetime
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "update_registro.py"
REGISTER = (
    "# Registro\n\n"
    "| Task | Marco | Status | Commit | Atualizado em | Observações |\n"
    "|---|---|---|---|---|---|\n"
    "| M01-T01 | M01 | não iniciada | - | 2026-09-30T14:20:00-03:00 | - |\n"
    "| M02-T01 | M02 | não iniciada | - | 2026-10-01T09:00:00-03:00 | - |\n"
    "\nNota preservada depois da tabela.\n"
)


class UpdateRegistroTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "registro.md"
        self.path.write_text(REGISTER, encoding="utf-8")

    def run_script(self, *args):
        return subprocess.run(
            [sys.executable, str(SCRIPT), str(self.path), "M01-T01", *args],
            capture_output=True, text=True,
        )

    def test_updates_only_selected_task_and_preserves_marco_and_notes(self):
        result = self.run_script("em andamento")
        self.assertEqual(result.returncode, 0, result.stderr)
        content = self.path.read_text(encoding="utf-8")
        self.assertIn("| M02-T01 | M02 | não iniciada | - | 2026-10-01T09:00:00-03:00 | - |", content)
        self.assertIn("Nota preservada depois da tabela.", content)
        changed = next(line for line in content.splitlines() if line.startswith("| M01-T01 |"))
        fields = [part.strip() for part in changed.strip("|").split("|")]
        self.assertEqual(fields[:4], ["M01-T01", "M01", "em andamento", "-"])
        self.assertEqual(fields[5], "-")
        self.assertIsNotNone(datetime.fromisoformat(fields[4]).tzinfo)

    def test_same_status_only_updates_observation_not_timestamp(self):
        self.assertEqual(self.run_script("em andamento").returncode, 0)
        before = next(line for line in self.path.read_text(encoding="utf-8").splitlines() if line.startswith("| M01-T01 |"))
        result = self.run_script("em andamento", "--obs", "preparando testes")
        self.assertEqual(result.returncode, 0, result.stderr)
        after = next(line for line in self.path.read_text(encoding="utf-8").splitlines() if line.startswith("| M01-T01 |"))
        self.assertEqual(before.split("|")[5], after.split("|")[5])
        self.assertIn("preparando testes", after)

    def test_rejects_old_schema_without_modifying_file(self):
        old = REGISTER.replace(
            "| Task | Marco | Status | Commit | Atualizado em | Observações |",
            "| Task | Status | Commit | Data | Observações |",
        )
        self.path.write_text(old, encoding="utf-8")
        result = self.run_script("em andamento")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.path.read_text(encoding="utf-8"), old)

    def test_rejects_timestamp_without_timezone(self):
        invalid = REGISTER.replace("2026-09-30T14:20:00-03:00", "2026-09-30T14:20:00")
        self.path.write_text(invalid, encoding="utf-8")
        self.assertNotEqual(self.run_script("em andamento").returncode, 0)
        self.assertEqual(self.path.read_text(encoding="utf-8"), invalid)

    def test_rejects_invalid_transition_and_completed_task(self):
        before = self.path.read_text(encoding="utf-8")
        result = self.run_script("concluída", "--commit", "a1b2c3d")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.path.read_text(encoding="utf-8"), before)
        self.assertEqual(self.run_script("em andamento").returncode, 0)
        self.assertEqual(self.run_script("aguardando revisão").returncode, 0)
        self.assertEqual(self.run_script("concluída", "--commit", "a1b2c3d").returncode, 0)
        finished = self.path.read_text(encoding="utf-8")
        self.assertIn("| M01-T01 | M01 | concluída | a1b2c3d |", finished)
        self.assertNotEqual(self.run_script("em andamento").returncode, 0)
        self.assertEqual(self.path.read_text(encoding="utf-8"), finished)

    def test_missing_record_and_duplicate_ids_do_not_create_or_rewrite(self):
        self.path.unlink()
        self.assertNotEqual(self.run_script("em andamento").returncode, 0)
        self.assertFalse(self.path.exists())
        duplicate = REGISTER.replace(
            "| M02-T01 | M02 |", "| M01-T01 | M02 |"
        )
        self.path.write_text(duplicate, encoding="utf-8")
        self.assertNotEqual(self.run_script("em andamento").returncode, 0)
        self.assertEqual(self.path.read_text(encoding="utf-8"), duplicate)

    def test_paused_or_superseded_requires_observation(self):
        before = self.path.read_text(encoding="utf-8")
        self.assertNotEqual(self.run_script("pausada").returncode, 0)
        self.assertEqual(self.path.read_text(encoding="utf-8"), before)
        self.assertEqual(self.run_script("pausada", "--obs", "aguarda ADR-0005").returncode, 0)
        self.assertNotEqual(self.run_script("em andamento").returncode, 0)
        self.assertEqual(self.run_script("em andamento", "--obs", "ADR-0005 resolvida").returncode, 0)

    def test_accepts_spacing_alignment_and_more_hyphens_without_reformatting_table(self):
        headers = [
            "|Task|Marco|Status|Commit|Atualizado em|Observações|",
            "|  Task  | Marco |Status| Commit | Atualizado em |  Observações  |",
        ]
        separators = [
            "| --- | --- | --- | --- | --- | --- |",
            "| :--- | ---: | :---: | ---- | :----- | -----: |",
        ]
        for header in headers:
            for separator in separators:
                with self.subTest(header=header, separator=separator):
                    content = REGISTER.replace(
                        "| Task | Marco | Status | Commit | Atualizado em | Observações |", header
                    ).replace("|---|---|---|---|---|---|", separator)
                    self.path.write_text(content, encoding="utf-8")
                    result = self.run_script("em andamento")
                    self.assertEqual(result.returncode, 0, result.stderr)
                    changed = self.path.read_text(encoding="utf-8").splitlines(keepends=True)
                    original = content.splitlines(keepends=True)
                    self.assertEqual(changed[:4], original[:4])
                    self.assertEqual(changed[5:], original[5:])

    def test_rejects_invalid_headers_and_separators_without_rewriting(self):
        invalid_headers = [
            "| Task | Status | Marco | Commit | Atualizado em | Observações |",
            "| Task | Marco | Status | Commit | Atualizado em | Observações | Extra |",
            "| task | Marco | Status | Commit | Atualizado em | Observações |",
            "Task | Marco | Status | Commit | Atualizado em | Observações",
        ]
        invalid_separators = [
            "| --- | --- | --- | --- | --- |",
            "| --- | --- | --- | --- | --- | --- | --- |",
            "| -- | --- | --- | --- | --- | --- |",
            "| :--: | --- | --- | --- | --- | --- |",
            "| --- | texto | --- | --- | --- | --- |",
            "| --- | ::--- | --- | --- | --- | --- |",
            "--- | --- | --- | --- | --- | ---",
        ]
        cases = [REGISTER.replace(
            "| Task | Marco | Status | Commit | Atualizado em | Observações |", header
        ) for header in invalid_headers]
        cases += [REGISTER.replace("|---|---|---|---|---|---|", separator)
                  for separator in invalid_separators]
        for content in cases:
            with self.subTest(content=content):
                self.path.write_text(content, encoding="utf-8")
                before = self.path.read_bytes()
                self.assertNotEqual(self.run_script("em andamento").returncode, 0)
                self.assertEqual(self.path.read_bytes(), before)

    def test_duplicate_semantic_headers_are_rejected(self):
        duplicate = REGISTER + "\n|Task|Marco|Status|Commit|Atualizado em|Observações|\n"
        self.path.write_text(duplicate, encoding="utf-8")
        self.assertNotEqual(self.run_script("em andamento").returncode, 0)
        self.assertEqual(self.path.read_text(encoding="utf-8"), duplicate)

    def test_preserves_crlf_in_untouched_lines(self):
        self.path.write_bytes(REGISTER.replace("\n", "\r\n").encode("utf-8"))
        before = self.path.read_bytes().splitlines(keepends=True)
        result = self.run_script("em andamento")
        self.assertEqual(result.returncode, 0, result.stderr)
        after = self.path.read_bytes().splitlines(keepends=True)
        self.assertEqual(after[:4], before[:4])
        self.assertEqual(after[5:], before[5:])
        self.assertTrue(after[4].endswith(b"\r\n"))

    def complete_task(self, obs=None):
        self.assertEqual(self.run_script("em andamento").returncode, 0)
        self.assertEqual(self.run_script("aguardando revisão").returncode, 0)
        args = ["concluída", "--commit", "a1b2c3d"]
        if obs is not None:
            args += ["--obs", obs]
        result = self.run_script(*args)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_integration_only_appends_link_preserving_commit_status_timestamp_and_notes(self):
        self.complete_task("relatório: achados/task-M01-T01-revisao-1.md")
        before_lines = self.path.read_text(encoding="utf-8").splitlines()
        before = [cell.strip() for cell in before_lines[4].strip("|").split("|")]
        integration = "b" * 40
        result = self.run_script("concluída", "--integration", integration)
        self.assertEqual(result.returncode, 0, result.stderr)
        after_lines = self.path.read_text(encoding="utf-8").splitlines()
        after = [cell.strip() for cell in after_lines[4].strip("|").split("|")]
        self.assertEqual(before[:5], after[:5])
        self.assertEqual(after[5], before[5] + "; Integração: " + integration)
        self.assertEqual(before_lines[:4], after_lines[:4])
        self.assertEqual(before_lines[5:], after_lines[5:])

    def test_integration_is_idempotent_but_cannot_replace_existing_link(self):
        self.complete_task()
        integration = "B" * 40
        self.assertEqual(self.run_script("concluída", "--integration", integration).returncode, 0)
        before = self.path.read_bytes()
        self.assertEqual(self.run_script("concluída", "--integration", integration.lower()).returncode, 0)
        self.assertEqual(self.path.read_bytes(), before)
        self.assertNotEqual(self.run_script("concluída", "--integration", "c" * 40).returncode, 0)
        self.assertEqual(self.path.read_bytes(), before)

    def test_integration_does_not_conclude_reopen_or_accept_other_changes(self):
        self.assertNotEqual(self.run_script("não iniciada", "--integration", "b" * 40).returncode, 0)
        self.complete_task()
        before = self.path.read_bytes()
        invalid = [
            ["em andamento", "--integration", "b" * 40],
            ["concluída", "--integration", "a1b2c3d"],
            ["concluída", "--integration", "z" * 40],
            ["concluída", "--integration", "b" * 40, "--commit", "a1b2c3d"],
            ["concluída", "--integration", "b" * 40, "--obs", "substitui notas"],
            ["concluída", "--obs", "alteração comum não autorizada"],
        ]
        for args in invalid:
            with self.subTest(args=args):
                self.assertNotEqual(self.run_script(*args).returncode, 0)
                self.assertEqual(self.path.read_bytes(), before)

    def test_malformed_or_duplicate_integration_markers_are_not_overwritten(self):
        for obs in ("Integração: inválida", "nota Integração: " + "b" * 40,
                    "Integração: " + "b" * 40 + "; Integração: " + "b" * 40):
            with self.subTest(obs=obs):
                self.path.write_text(REGISTER, encoding="utf-8")
                self.complete_task(obs)
                before = self.path.read_bytes()
                self.assertNotEqual(self.run_script("concluída", "--integration", "b" * 40).returncode, 0)
                self.assertEqual(self.path.read_bytes(), before)

    def test_replacement_preserves_old_id_and_does_not_reopen_it(self):
        self.assertEqual(self.run_script("pausada", "--obs", "revisão 4 sem convergência").returncode, 0)
        self.assertEqual(self.run_script("substituída", "--obs", "substituída por M01-T07").returncode, 0)
        content = self.path.read_text(encoding="utf-8")
        new_row = "| M01-T07 | M01 | não iniciada | - | 2026-10-02T09:00:00-03:00 | origem: M01-T01 |\n"
        # Simula a linha nova inicializada pela plan; o atualizador não a cria.
        content = content.replace("\nNota preservada", new_row + "\nNota preservada")
        self.path.write_text(content, encoding="utf-8")
        self.assertNotEqual(self.run_script("em andamento", "--obs", "tenta reset").returncode, 0)
        self.assertNotEqual(self.run_script("substituída", "--integration", "b" * 40).returncode, 0)
        self.assertEqual(self.path.read_text(encoding="utf-8"), content)
        result = subprocess.run(
            [sys.executable, str(SCRIPT), str(self.path), "M01-T07", "em andamento"],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        changed = self.path.read_text(encoding="utf-8")
        self.assertIn("| M01-T01 | M01 | substituída |", changed)
        self.assertIn("| M01-T07 | M01 | em andamento |", changed)

    def test_squash_link_is_available_in_fresh_clone_without_original_commits(self):
        root = self.path.parent

        def git(cwd, *args, check=True):
            result = subprocess.run(
                ["git", "-c", "commit.gpgSign=false", "-c", "core.hooksPath=" + str(root / "no-hooks"),
                 "-C", str(cwd), *args], capture_output=True, text=True,
            )
            if check:
                self.assertEqual(result.returncode, 0, result.stderr)
            return result

        git(root, "init", "-b", "main")
        git(root, "config", "user.name", "Fixture")
        git(root, "config", "user.email", "fixture@example.invalid")
        git(root, "add", "--", "registro.md")
        git(root, "commit", "-m", "baseline temporario")
        git(root, "switch", "-c", "task")
        self.assertEqual(self.run_script("em andamento").returncode, 0)
        self.assertEqual(self.run_script("aguardando revisão").returncode, 0)
        code = root / "login.py"
        code.write_text("DELIVERED_CODE\n", encoding="utf-8")
        findings = root / "achados"
        findings.mkdir()
        review = findings / "task-M01-T01-revisao-1.md"
        review.write_text("Estado: finalizada\n## Decisão final\nAprovada.\n", encoding="utf-8")
        git(root, "add", "--", "login.py", "achados/task-M01-T01-revisao-1.md")
        git(root, "commit", "-m", "feat(M01-T01): entrega temporaria")
        functional = git(root, "rev-parse", "HEAD").stdout.strip()
        self.assertEqual(self.run_script("concluída", "--commit", functional).returncode, 0)
        git(root, "add", "--", "registro.md")
        git(root, "commit", "-m", "docs: registro temporario")
        metadata = git(root, "rev-parse", "HEAD").stdout.strip()
        git(root, "switch", "main")
        git(root, "merge", "--squash", "task")
        git(root, "commit", "-m", "feat: integracao temporaria")
        integration = git(root, "rev-parse", "HEAD").stdout.strip()
        self.assertEqual(self.run_script("concluída", "--integration", integration).returncode, 0)
        git(root, "add", "--", "registro.md")
        git(root, "commit", "-m", "docs: vinculo de integracao temporario")
        git(root, "branch", "-D", "task")
        with tempfile.TemporaryDirectory() as clone_dir:
            clone = Path(clone_dir) / "fresh"
            git(root, "clone", "--no-local", "--single-branch", "--branch", "main", str(root), str(clone))
            content = (clone / "registro.md").read_text(encoding="utf-8")
            self.assertIn("| M01-T01 | M01 | concluída | " + functional + " |", content)
            self.assertIn("Integração: " + integration, content)
            git(clone, "merge-base", "--is-ancestor", integration, "HEAD")
            self.assertIn("Aprovada.", git(clone, "show", integration + ":achados/task-M01-T01-revisao-1.md").stdout)
            self.assertIn("DELIVERED_CODE", git(clone, "show", integration + ":login.py").stdout)
            for original in (functional, metadata):
                self.assertNotEqual(git(clone, "cat-file", "-e", original + "^{commit}", check=False).returncode, 0)


if __name__ == "__main__":
    unittest.main()
