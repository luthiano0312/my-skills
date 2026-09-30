#!/usr/bin/env python3
"""
Atualiza (ou cria) a linha de uma task na tabela docs_sistema_recolhe/execucao/registro.md,
sem arriscar quebrar a formatação markdown ao editar manualmente.

Uso:
  python3 update_registro.py <caminho_registro.md> <task> <status> [--commit HASH] [--data YYYY-MM-DD] [--obs "texto"]

Exemplos:
  python3 update_registro.py docs_sistema_recolhe/execucao/registro.md 8.3 "implementação em andamento"
  python3 update_registro.py docs_sistema_recolhe/execucao/registro.md 8.3 "concluída" --commit a1b2c3d --data 2026-09-29 --obs "-"

Se o arquivo não existir, ele é criado com o cabeçalho padrão.
Se a task ainda não tem linha, uma linha nova é adicionada.
Se já tem, a linha é substituída (nunca duplicada).
Campos não passados mantêm o valor anterior (ou "-" se a linha é nova).
"""
import argparse
import os
import sys
from datetime import datetime, timezone

HEADER = (
    "# Registro de Execução\n\n"
    "Tabela central de status das tasks do `plano.md`. Cada task tem no máximo uma linha, "
    "atualizada — nunca duplicada — por `scripts/update_registro.py`.\n\n"
    "Status possíveis: `implementação em andamento`, `aguardando revisão`, `em correção`, "
    "`concluída`, `pausada`.\n\n"
    "| Task | Status | Commit | Data | Observações |\n"
    "|---|---|---|---|---|\n"
)


def parse_table(lines):
    """Retorna (linhas_antes_da_tabela, header_linhas, dict task->linha_completa, ordem_das_tasks)."""
    rows = {}
    order = []
    table_start = None
    for i, line in enumerate(lines):
        if line.strip().startswith("| Task"):
            table_start = i
            break
    if table_start is None:
        return lines, [], rows, order

    pre = lines[: table_start + 2]  # inclui a linha de separador |---|---|
    for line in lines[table_start + 2 :]:
        if not line.strip().startswith("|"):
            continue
        cols = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cols) < 1 or not cols[0]:
            continue
        task_id = cols[0]
        rows[task_id] = line.rstrip("\n")
        order.append(task_id)
    return pre, [], rows, order


def format_row(task, status, commit, data, obs):
    return f"| {task} | {status} | {commit} | {data} | {obs} |"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("registro_path")
    ap.add_argument("task")
    ap.add_argument("status")
    ap.add_argument("--commit", default=None)
    ap.add_argument("--data", default=None)
    ap.add_argument("--obs", default=None)
    args = ap.parse_args()

    path = args.registro_path
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)

    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write(HEADER)
        pre_lines = HEADER.splitlines(keepends=True)
    else:
        with open(path, "r", encoding="utf-8") as f:
            pre_lines = f.readlines()

    pre, _, rows, order = parse_table(pre_lines)

    existing = rows.get(args.task)
    if existing:
        cols = [c.strip() for c in existing.strip().strip("|").split("|")]
        # cols: [task, status, commit, data, obs]
        prev_commit = cols[2] if len(cols) > 2 else "-"
        prev_data = cols[3] if len(cols) > 3 else "-"
        prev_obs = cols[4] if len(cols) > 4 else "-"
    else:
        prev_commit, prev_data, prev_obs = "-", "-", "-"
        order.append(args.task)

    commit = args.commit if args.commit is not None else prev_commit
    data = args.data if args.data is not None else (
        prev_data if existing else datetime.now(timezone.utc).strftime("%Y-%m-%d")
    )
    obs = args.obs if args.obs is not None else prev_obs

    rows[args.task] = format_row(args.task, args.status, commit, data, obs)

    with open(path, "w", encoding="utf-8") as f:
        f.writelines(pre)
        for task_id in order:
            f.write(rows[task_id] + "\n")

    print(f"OK: task {args.task} -> status='{args.status}' commit='{commit}' data='{data}' obs='{obs}'")


if __name__ == "__main__":
    sys.exit(main())
