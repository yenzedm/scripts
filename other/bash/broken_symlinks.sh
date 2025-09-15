#!/bin/bash
# Использование: broken_symlinks.sh [ROOT]
ROOT="${1:-/}"
LOG_FILE="/var/log/broken_symlinks.log"

echo "🔗 Scan broken symlinks in ${ROOT} — $(date)" | tee -a "$LOG_FILE"

# -xdev: не уходить на другие файловые системы (уберите, если нужно везде)
# -xtype l: «битые» ссылки, у которых цель недоступна
FOUND=$(mktemp)
sudo find "$ROOT" -xdev -xtype l -print 2>/dev/null | sort -u | tee "$FOUND" | tee -a "$LOG_FILE"

COUNT=$(wc -l < "$FOUND")
[ "$COUNT" -eq 0 ] && echo "✅ Не найдено" | tee -a "$LOG_FILE" || echo "⚠️ Найдено: $COUNT" | tee -a "$LOG_FILE"

# (опционально) удалить найденные ссылки — раскомментируйте следующую строку:
# xargs -0 -r rm -v < <(tr '\n' '\0' < "$FOUND") | tee -a "$LOG_FILE"

rm -f "$FOUND"
# test
