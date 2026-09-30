#!/usr/bin/env python3
"""Prepara entradas da primeira fase da revisão, sem modificar o repositório.

Uso: python review_inputs.py <registro.md> <task-id>

JSON na saída: metadados mínimos, inventário, diffs filtrados e arquivos novos
permitidos para leitura. Relatos e Observações nunca são emitidos. Os estados
incompleta/finalizada das revisões são metadados, não suas conclusões.
Não atribui mudanças à task, não faz revisão e não autoriza commits.
"""

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

# Importar o validador compartilhado não deve criar __pycache__ na skill.
sys.dont_write_bytecode = True
from update_registro import FULL_HASH, HEADER_CELLS, INTEGRATION_MARKER, cells, find_task

NARRATIVE = re.compile(r"task-.+-(?:relatorio|revisao-[1-9][0-9]*)\.md")
REVIEW_STATE = re.compile(r"^Estado: (incompleta|finalizada)$", re.MULTILINE)


def git(root, *args):
    result = subprocess.run(
        ["git", "--no-pager", "-C", str(root), *args],
        capture_output=True, env={**os.environ, "GIT_OPTIONAL_LOCKS": "0"},
    )
    if result.returncode:
        # Não ecoar stderr arbitrário de comandos/configurações no contexto.
        raise ValueError(f"comando Git falhou: {args[0]}")
    return result.stdout


def name_changes(raw):
    fields = raw.decode("utf-8", errors="surrogateescape").split("\0")
    i = 0
    while i < len(fields) and fields[i]:
        status = fields[i]
        count = 2 if status.startswith(("R", "C")) else 1
        paths = fields[i + 1:i + 1 + count]
        if len(paths) != count or not all(paths):
            raise ValueError("inventário Git incompleto")
        yield status, paths
        i += count + 1


def metadata(row):
    if row[3] != "-" and not re.fullmatch(r"[0-9a-fA-F]{7,40}", row[3]):
        raise ValueError("hash funcional malformado no registro")
    links = [part.strip() for part in row[5].split(";") if "Integração:" in part]
    integration = None
    if links:
        if (len(links) != 1 or not links[0].startswith(INTEGRATION_MARKER)
                or not FULL_HASH.fullmatch(links[0][len(INTEGRATION_MARKER):])):
            raise ValueError("vínculo de integração malformado no registro")
        integration = links[0][len(INTEGRATION_MARKER):].lower()
    return {"task": row[0], "marco": row[1], "status": row[2],
            "commit": row[3], "updated_at": row[4], "integration": integration}


def prepare(registro, task_id):
    if (not task_id or task_id in {".", ".."}
            or any(char in task_id for char in "/\\\0\r\n")):
        raise ValueError("ID incompatível com os nomes dos arquivos de execução")
    registro = registro.absolute()
    if not registro.is_file() or registro.is_symlink():
        raise ValueError("registro ausente ou caminho simbólico; esclareça o mapa")
    root = Path(os.fsdecode(git(registro.parent, "rev-parse", "--show-toplevel")).strip()).resolve()
    try:
        registro = registro.resolve()
        register_path = registro.relative_to(root).as_posix()
    except ValueError as exc:
        raise ValueError("registro fora da raiz do repositório") from exc
    findings = registro.parent / "achados"
    if findings.resolve() != findings or (findings.exists() and not findings.is_dir()):
        raise ValueError("pasta de achados ambígua; esclareça o mapa")
    findings_path = findings.relative_to(root)
    lines = registro.read_text(encoding="utf-8").splitlines()
    _, row = find_task(lines, task_id)
    register_tasks = []
    in_table = False
    for line in lines:
        if not in_table:
            try:
                in_table = cells(line) == HEADER_CELLS
            except ValueError:
                pass
            continue
        if not line.lstrip().startswith("|"):
            break
        values = cells(line)
        if all(re.fullmatch(r":?-{3,}:?", value) for value in values):
            continue
        register_tasks.append(metadata(values))

    def category(path):
        relative = Path(path)
        if relative.is_absolute() or ".." in relative.parts:
            raise ValueError("caminho Git fora da raiz")
        if path == register_path:
            return "registro"
        if findings_path in relative.parents:
            if relative.parent == findings_path and NARRATIVE.fullmatch(relative.name):
                return "narrativa"
            raise ValueError(f"arquivo não reconhecido na área de achados: {path}")
        return "entregavel"

    changes = {}

    def remember(path, source, status):
        kind = category(path)
        changes.setdefault(path, {"path": path, "kind": kind, "changes": []})
        changes[path]["changes"].append({"source": source, "status": status})
        return kind

    modes = [("HEAD", ["HEAD"]), ("staged", ["--cached"]), ("unstaged", [])]
    for source, arguments in modes:
        raw = git(root, "diff", "--no-ext-diff", "--no-textconv",
                  "--name-status", "-z", "--find-renames", *arguments, "--")
        for status, paths in name_changes(raw):
            kinds = [remember(path, source, status) for path in paths]
            if len(set(kinds)) > 1:
                raise ValueError("renomeação/cópia cruza entregáveis e metadados; esclareça antes da leitura")
    untracked = [os.fsdecode(path) for path in
                 git(root, "ls-files", "--others", "--exclude-standard", "-z").split(b"\0") if path]
    for path in untracked:
        remember(path, "untracked", "?")

    allowed = sorted(path for path, entry in changes.items() if entry["kind"] == "entregavel")
    deferred = sorted(path for path, entry in changes.items() if entry["kind"] != "entregavel")
    for path in allowed:
        target = (root / path).resolve()
        try:
            target_path = target.relative_to(root).as_posix()
        except ValueError as exc:
            raise ValueError(f"entregável aponta para fora da raiz: {path}") from exc
        if category(target_path) != "entregavel":
            raise ValueError(f"entregável aponta para metadados: {path}")

    # Exclusões adicionais impedem que um pathspec de arquivo removido, hoje
    # ancestral de uma pasta, inclua os metadados dessa pasta por prefixo.
    pathspecs = ([f":(top,literal){path}" for path in allowed]
                 + [f":(top,literal,exclude){path}" for path in deferred])
    diffs = {}
    for source, arguments in modes:
        diffs[source] = (git(root, "diff", "--no-ext-diff", "--no-textconv",
                            "--no-color", "--find-renames", *arguments, "--", *pathspecs)
                         .decode("utf-8", errors="replace") if allowed else "")

    # Ler estes arquivos internamente serve somente para extrair o marcador
    # de estado. Nunca devolver sua narrativa ou decisão ao agente nesta fase.
    reviews = []
    review_name = re.compile(r"task-" + re.escape(task_id) + r"-revisao-([1-9][0-9]*)\.md")
    if findings.exists():
        for path in findings.iterdir():
            match = review_name.fullmatch(path.name)
            if not match:
                continue
            if path.is_symlink() or not path.is_file():
                raise ValueError("revisão com caminho ambíguo")
            states = REVIEW_STATE.findall(path.read_text(encoding="utf-8"))
            if len(states) > 1:
                raise ValueError("revisão com marcadores de estado duplicados")
            reviews.append({"round": int(match[1]), "path": path.relative_to(root).as_posix(),
                            "state": states[0] if states else "não identificado"})

    working = [(path, hashlib.sha256((root / path).read_bytes()).hexdigest()
                if (root / path).is_file() else None) for path in allowed]
    fingerprint = {"head": git(root, "rev-parse", "HEAD").decode("ascii").strip(),
                   "inventory": [changes[path] for path in allowed],
                   "diffs": diffs, "working": working}
    snapshot = hashlib.sha256(json.dumps(fingerprint, ensure_ascii=True, sort_keys=True)
                              .encode("utf-8")).hexdigest()

    return {
        "snapshot": snapshot,
        **metadata(row), "registro_tasks": register_tasks,
        "registro": register_path, "achados": findings_path.as_posix(),
        "relatorio": (findings_path / f"task-{task_id}-relatorio.md").as_posix(),
        "inventory": [changes[path] for path in sorted(changes)],
        "diffs": diffs,
        "untracked_allowed": sorted(path for path in untracked if category(path) == "entregavel"),
        "deferred_changed": deferred,
        "reviews": sorted(reviews, key=lambda review: review["round"]),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("registro", type=Path)
    parser.add_argument("task")
    args = parser.parse_args()
    try:
        result = prepare(args.registro, args.task)
    except (ValueError, OSError, UnicodeError) as exc:
        parser.exit(2, f"Erro: {exc}\n")
    # ASCII escapado funciona também em consoles Windows sem UTF-8.
    print(json.dumps(result, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    main()
