#!/usr/bin/env bash
# Cria a estrutura docs/ + um arquivo de entrada num projeto novo.
# Uso: scaffold_docs.sh [diretorio-alvo] [AGENTS.md|CLAUDE.md]
# Padrão: diretório atual e AGENTS.md. Preserva arquivo de entrada existente.

set -euo pipefail

TARGET="${1:-.}"
ENTRY_FILE="${2:-AGENTS.md}"
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [ "$ENTRY_FILE" != 'AGENTS.md' ] && [ "$ENTRY_FILE" != 'CLAUDE.md' ]; then
  echo 'Arquivo de entrada deve ser AGENTS.md ou CLAUDE.md' >&2
  exit 2
fi

# Não crie duas cópias do mapa de documentação/execução: preserve o que o
# projeto já usa. Se ambos existirem, peça reconciliação manual do conteúdo.
if [ -f "$TARGET/AGENTS.md" ] && [ -f "$TARGET/CLAUDE.md" ]; then
  ENTRY_FILE=''
  echo 'AGENTS.md e CLAUDE.md já existem; mantidos sem alterações. Confira se os mapas concordam.'
elif [ -f "$TARGET/AGENTS.md" ]; then
  ENTRY_FILE='AGENTS.md'
elif [ -f "$TARGET/CLAUDE.md" ]; then
  ENTRY_FILE='CLAUDE.md'
fi

mkdir -p "$TARGET/docs/01-requisitos/casos-de-uso"
mkdir -p "$TARGET/docs/02-design/apis"
mkdir -p "$TARGET/docs/02-design/ui-ux"
mkdir -p "$TARGET/docs/02-design/adr/archive"
mkdir -p "$TARGET/docs/how-to"
mkdir -p "$TARGET/docs/reference"
mkdir -p "$TARGET/docs/explanation"

# .gitkeep nas pastas que começam vazias, pra não sumir no git
for d in \
  "$TARGET/docs/01-requisitos/casos-de-uso" \
  "$TARGET/docs/02-design/apis" \
  "$TARGET/docs/02-design/ui-ux" \
  "$TARGET/docs/02-design/adr" \
  "$TARGET/docs/02-design/adr/archive" \
  "$TARGET/docs/how-to" \
  "$TARGET/docs/reference" \
  "$TARGET/docs/explanation"
do
  [ -z "$(ls -A "$d" 2>/dev/null)" ] && touch "$d/.gitkeep"
done

# Copia os templates só se ainda não existir o arquivo (não sobrescreve trabalho já feito)
copy_if_absent() {
  local src="$1" dest="$2"
  if [ ! -f "$dest" ]; then
    cp "$src" "$dest"
    echo "criado: $dest"
  else
    echo "já existe, mantido: $dest"
  fi
}

copy_if_absent "$SKILL_DIR/assets/templates/escopo.md" "$TARGET/docs/01-requisitos/escopo.md"
if [ -n "$ENTRY_FILE" ]; then
  if [ -f "$TARGET/$ENTRY_FILE" ]; then
    echo "já existe, mantido: $TARGET/$ENTRY_FILE"
  else
    template="$(<"$SKILL_DIR/assets/templates/agent-entrypoint.md")"
    printf '%s\n' "${template//__ENTRY_FILE__/$ENTRY_FILE}" > "$TARGET/$ENTRY_FILE"
    echo "criado: $TARGET/$ENTRY_FILE"
  fi
fi

echo ""
echo "Estrutura criada em: $TARGET/docs/"
echo "Próximo passo: decidir SRS vs. backlog (ver references/requisitos-levantamento.md) e preencher o arquivo de entrada escolhido."
