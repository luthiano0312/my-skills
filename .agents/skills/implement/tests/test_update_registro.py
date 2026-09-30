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


if __name__ == "__main__":
    unittest.main()
