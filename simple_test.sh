#!/bin/bash
# 不认命 App - 简化测试脚本
# 每 30 秒测试一次，持续 8 小时

LOG_FILE="/tmp/burenmng_test.log"
API_BASE="http://localhost:8001"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "🚀 开始测试，日志文件：$LOG_FILE"

TEST_DATA=(
    '{"year":1990,"month":3,"day":15,"hour":11,"gender":"male","prayer_focus":"事业"}'
    '{"year":1985,"month":7,"day":22,"hour":9,"gender":"female","prayer_focus":"财运"}'
    '{"year":1992,"month":1,"day":8,"hour":23,"gender":"male","prayer_focus":"姻缘"}'
    '{"year":1988,"month":11,"day":30,"hour":5,"gender":"female","prayer_focus":"健康"}'
    '{"year":1995,"month":6,"day":18,"hour":13,"gender":"male","prayer_focus":"学业"}'
)

SUCCESS=0
FAIL=0
ROUND=0

while true; do
    ROUND=$((ROUND + 1))
    
    # 随机选择测试数据
    DATA=${TEST_DATA[$RANDOM % ${#TEST_DATA[@]}]}
    
    # 测试 API
    RESPONSE=$(curl -s -X POST "$API_BASE/api/match" \
        -H "Content-Type: application/json" \
        -d "$DATA" \
        --max-time 10)
    
    # 使用 Python 解析 JSON
    RESULT=$(echo "$RESPONSE" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    temples = len(data.get('temples', []))
    faqi = len(data.get('faqi', []))
    if temples > 0 and faqi > 0:
        print(f'OK:{temples}:{faqi}')
    else:
        print(f'EMPTY:{temples}:{faqi}')
except Exception as e:
    print(f'ERROR:{e}')
" 2>&1)
    
    STATUS=$(echo "$RESULT" | cut -d: -f1)
    
    if [ "$STATUS" = "OK" ]; then
        TEMPLES=$(echo "$RESULT" | cut -d: -f2)
        FAQI=$(echo "$RESULT" | cut -d: -f3)
        SUCCESS=$((SUCCESS + 1))
        log "✅ Round $ROUND: OK (temples:$TEMPLES faqi:$FAQI) [成功:$SUCCESS 失败:$FAIL]"
    else
        FAIL=$((FAIL + 1))
        log "❌ Round $ROUND: $RESULT [成功:$SUCCESS 失败:$FAIL]"
    fi
    
    # 休息 30 秒
    sleep 30
done
