#!/bin/bash
#
# =======================================
# CREWAI/GPT CONTEXT EXPORT SCRIPT v2.0
# =======================================
#
# Этот скрипт не только экспортирует файлы проекта, но и
# рассказывает, зачем он это делает, что такое "чанк", и как
# устроена передача контекста для AI/LLM/crewAI.
#
# Пиши: ./crewai_export.sh [папка] [шаблон_файлов]
# Например: ./crewai_export.sh ./src '*.py'
#
# Всё экспортируется в context_output.md
#
# Автор: YOU, 2025
# ---------------------------------------

# НАСТРОЙКИ
MAX_CHUNK_SIZE=15000
OUTPUT_FILE="context_output.md"
SCAN_DIR="${1:-.}"
FILE_PATTERN="${2:-*}"

# Список папок, которые не надо включать (типа .git, node_modules)
EXCLUDE_DIRS=("node_modules" ".git" ".venv" "__pycache__" "build" "dist")

# Функция — строка exclude для find
gen_exclude_expr() {
  local expr=""
  for d in "${EXCLUDE_DIRS[@]}"; do
    expr+=" -path \"*/$d/*\" -prune -o"
  done
  # убираем последний -o
  expr="${expr::-2}"
  echo "$expr"
}

# ==== ВСТАВЛЯЕМ ПРОЛОГ ====

cat > "$OUTPUT_FILE" <<END
# 📦 CREWAI/AI-КОНТЕКСТ: ПРОЕКТНЫЕ ФАЙЛЫ

Это экспорт файлов из проекта для передачи искусственному интеллекту или агенту (например, LLM или crewAI).  
Здесь каждый файл разбит на **чанки** — отдельные куски данных, чтобы AI мог эффективно читать, анализировать и строить ответы на их основе.

---

### 🤖 Зачем это нужно?

- Большой проект невозможно отправить AI-агенту целиком — его "контекстное окно" ограничено.
- Файлы делятся на логические части ("чанки").
- У каждого чанка есть метаданные: роль, путь, тип, номер чанка.
- В таком виде проект можно анализировать, рефакторить, строить документацию или делать автотесты силами ИИ.

---

### 🧩 Что такое "чанк"?

**Чанк** — это кусок файла ограниченного размера.  
Так проще пересылать и обрабатывать большие данные.

---

### ⚙️ Как устроен этот экспорт?

- Пробегаемся по проекту, исключая техпапки (.git, node_modules, ...).
- Для каждого файла определяем его роль по расширению.
- Если файл большой — делим на чанки.
- Каждый чанк оформлен в markdown с подписями.

---

END

# ==== ФУНКЦИЯ: Определить роль ====
detect_role() {
  case "$1" in
    *.md) echo "documentation" ;;
    *.txt) echo "text" ;;
    *.py) echo "code-python" ;;
    *.js) echo "code-js" ;;
    *.sh) echo "script-bash" ;;
    *.yaml|*.yml) echo "config-yaml" ;;
    *.json) echo "config-json" ;;
    *.env) echo "env-config" ;;
    *) echo "file" ;;
  esac
}

# ==== ФУНКЦИЯ: "find" с исключением папок ====
find_cmd="find \"$SCAN_DIR\" "
for d in "${EXCLUDE_DIRS[@]}"; do
  find_cmd+=" -path \"$SCAN_DIR/$d\" -prune -o"
done
find_cmd+=" -type f -name \"$FILE_PATTERN\" -print"

# ==== ЦИКЛ: Обработка файлов ====
eval $find_cmd | while read -r FILE
do
  ROLE=$(detect_role "$FILE")
  BASENAME=$(basename "$FILE")
  CONTENT=$(cat "$FILE")
  TOTAL_LEN=${#CONTENT}
  if [ $TOTAL_LEN -le $MAX_CHUNK_SIZE ]; then
    CHUNKS=1
  else
    CHUNKS=$(( (TOTAL_LEN + MAX_CHUNK_SIZE - 1) / MAX_CHUNK_SIZE ))
  fi

  for ((i=0; i<CHUNKS; i++))
  do
    START=$(( i * MAX_CHUNK_SIZE ))
    LEN=$(( MAX_CHUNK_SIZE ))
    CHUNK_CONTENT=$(echo -n "$CONTENT" | cut -c $((START+1))-$((START+LEN)))
    {
      echo "-------------------------------------------"
      echo "**role:** $ROLE"
      echo "**file:** $FILE"
      echo "**chunk:** $((i+1))/$CHUNKS"
      echo ""
      echo '```'
      echo "$CHUNK_CONTENT"
      echo '```'
      echo ""
    } >> "$OUTPUT_FILE"
  done
done

echo "✅ Готово! Смотри результат в $OUTPUT_FILE"
