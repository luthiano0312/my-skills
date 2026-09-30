#!/usr/bin/env python3
"""Atualiza uma task de um registro já inicializado pela skill plan.

Uso: python update_registro.py <registro.md> <task-id> <status>
     [--commit HASH] [--obs "motivo ou links"]

A tabela tem seis colunas fixas. Em caso de formato, ID ou transição inválida,
não modifica o arquivo. `Atualizado em` muda apenas quando o status muda.
"""

import argparse
import os
import re
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

HEADER = "| Task | Marco | Status | Commit | Atualizado em | Observações |"
SEPARATOR = "|---|---|---|---|---|---|"
STATES = {
    "não iniciada": {"em andamento", "pausada", "substituída"},
    "em andamento": {"aguardando revisão", "pausada", "substituída"},
    "aguardando revisão": {"em correção", "concluída", "pausada", "substituída"},
    "em correção": {"aguardando revisão", "pausada", "substituída"},
    "pausada": {"em andamento", "aguardando revisão", "em correção", "substituída"},
    "concluída": set(),
    "substituída": set(),
}


def cells(line):
    text = line.strip()
    if not (text.startswith("|") and text.endswith("|")):
        raise ValueError("linha da tabela malformada")
    values = [c.strip() for c in text[1:-1].split("|")]
    if len(values) != 6:
        raise ValueError("o registro deve ter exatamente seis colunas; não use '|' em Observações")
    return values


def find_task(lines, task_id):
    indices = [i for i, line in enumerate(lines) if line.strip() == HEADER]
    if len(indices) != 1:
        raise ValueError("cabeçalho do registro ausente, duplicado ou incompatível")
    start = indices[0]
    if start + 1 >= len(lines) or lines[start + 1].strip() != SEPARATOR:
        raise ValueError("separador da tabela incompatível")

    found = None
    seen = set()
    for i in range(start + 2, len(lines)):
        if not lines[i].lstrip().startswith("|"):
            break
        row = cells(lines[i])
        if not row[0] or not row[1]:
            raise ValueError("Task e Marco são obrigatórios")
        if row[0] in seen:
            raise ValueError(f"ID duplicado no registro: {row[0]}")
        if row[2] not in STATES:
            raise ValueError(f"status desconhecido em {row[0]}: {row[2]}")
        try:
            updated_at = datetime.fromisoformat(row[4])
        except ValueError as exc:
            raise ValueError(f"data/hora inválida em {row[0]}") from exc
        if updated_at.tzinfo is None or updated_at.utcoffset() is None:
            raise ValueError(f"fuso ausente em Atualizado em da task {row[0]}")
        seen.add(row[0])
        if row[0] == task_id:
            found = (i, row)
    if found is None:
        raise ValueError(f"task {task_id} não encontrada; peça à skill plan para inicializar o registro")
    return found


def update(path, task_id, status, commit=None, obs=None):
    if not path.is_file():
        raise ValueError(f"registro ausente: {path}; a skill implement não cria registros")
    if status not in STATES:
        raise ValueError(f"status inválido: {status}")
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    index, row = find_task(lines, task_id)
    old_status = row[2]
    if old_status in {"concluída", "substituída"}:
        raise ValueError(f"task em estado final: {old_status}")
    if status != old_status and status not in STATES[old_status]:
        raise ValueError(f"transição inválida: {old_status} → {status}")
    if status == "concluída":
        if not commit or not re.fullmatch(r"[0-9a-fA-F]{7,40}", commit):
            raise ValueError("conclusão exige hash do commit (7 a 40 caracteres hexadecimais)")
    elif commit is not None:
        raise ValueError("o hash só pode ser registrado ao concluir a task")
    if status in {"pausada", "substituída"} and (not obs or obs == "-"):
        raise ValueError(f"{status} exige motivo/vínculo nas Observações")
    if old_status == "pausada" and status != old_status and (not obs or obs == "-"):
        raise ValueError("retomar task pausada exige motivo nas Observações")
    if obs is not None and ("|" in obs or "\n" in obs or "\r" in obs):
        raise ValueError("Observações não podem conter '|' nem quebras de linha")

    row[2] = status
    if commit is not None:
        row[3] = commit
    if status != old_status:
        row[4] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    if obs is not None:
        row[5] = obs
    newline = "\r\n" if lines[index].endswith("\r\n") else "\n"
    lines[index] = "| " + " | ".join(row) + " |" + newline

    # Só substitui o arquivo depois de todas as validações; preserve notas fora da tabela.
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", newline="", dir=path.parent,
                                         prefix=".registro-", delete=False) as tmp:
            tmp_path = Path(tmp.name)
            tmp.writelines(lines)
        os.replace(tmp_path, path)
    finally:
        if tmp_path is not None and tmp_path.exists():
            tmp_path.unlink()
    return row


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("registro_path", type=Path)
    parser.add_argument("task")
    parser.add_argument("status")
    parser.add_argument("--commit", default=None)
    parser.add_argument("--obs", default=None)
    args = parser.parse_args()
    try:
        row = update(args.registro_path, args.task, args.status, args.commit, args.obs)
    except (ValueError, OSError) as exc:
        parser.exit(2, f"Erro: {exc}\n")
    print(f"OK: {row[0]} ({row[1]}) -> {row[2]} em {row[4]}")


if __name__ == "__main__":
    sys.exit(main())
