#!/bin/zsh
# 知域 · 小红书动向 每日更新入口（macOS 双击即可运行）
#
# 流程：拉起专用 Chrome → 探测登录态（失效时等你扫码）→ 逐博主增量抓取
#       → 校验数据 → 提交并推送 data/xhs → 发送系统通知。
#
# 环境变量：
#   XHS_NO_PUSH=1        只提交不推送
#   XHS_NO_COMMIT=1      只抓取不提交（自己审阅后再提交）
#   XHS_FETCH_ARGS="..." 追加传给 scripts/xhs/fetch.py 的参数，例如 "--dump-state"
#   XHS_DIGEST=1         可选：抓取后运行 scripts/xhs/digest.py 生成摘要归档（默认关闭，网页不展示）
#   XHS_DIGEST_ARGS="..."追加传给 scripts/xhs/digest.py 的参数，例如 "--backend openai --model gpt-4o-mini"
#   XHS_LLM_API_KEY / XHS_LLM_BASE_URL / XHS_LLM_MODEL  摘要用的 OpenAI 兼容接口（不设则尝试 codex CLI，再退回启发式）

set -u
setopt pipefail 2>/dev/null

REPO="$(cd "$(dirname "$0")" && pwd)"
cd "$REPO" || exit 1

STATE_DIR="${XHS_STATE_DIR:-$HOME/.zhiyu/xhs}"
mkdir -p "$STATE_DIR"
LOG="$STATE_DIR/update-$(date +%Y%m%d-%H%M%S).log"
TODAY="$(date +%Y-%m-%d)"

notify() {
  osascript -e "display notification \"$2\" with title \"$1\"" >/dev/null 2>&1 || true
}

finish() {
  echo
  echo "日志：$LOG"
  if [[ -t 0 ]]; then
    echo "按回车关闭窗口…"
    read -r _
  fi
}

fail() {
  echo "✗ $1" | tee -a "$LOG"
  notify "知域 · 小红书动向" "$1"
  finish
  exit 1
}

exec > >(tee -a "$LOG") 2>&1

echo "== 知域 · 小红书动向 · $TODAY =="
test -f index.html && test -d scripts || fail "当前目录不是知域仓库根目录：$REPO"

if [[ -n "$(git status --porcelain -- data/xhs data/xhs_watchlist.json)" ]]; then
  echo "提示：data/xhs 下已有未提交修改，本次结果会与其一并提交。"
fi

echo "-- 抓取"
python3 scripts/xhs/fetch.py ${=XHS_FETCH_ARGS:-}
FETCH_STATUS=$?
if [[ $FETCH_STATUS -ne 0 && $FETCH_STATUS -ne 2 ]]; then
  fail "抓取脚本异常退出（$FETCH_STATUS），详见日志"
fi

if [[ "${XHS_DIGEST:-0}" == "1" ]]; then
  # 可选：生成 data/xhs/digests.json 归档（网页暂不展示）。
  echo "-- 摘要（可选）"
  python3 scripts/xhs/digest.py ${=XHS_DIGEST_ARGS:-} || echo "摘要生成失败（不影响抓取数据），继续。"
fi

echo "-- 校验"
python3 scripts/validate_xhs.py || fail "数据校验失败，未提交。请查看日志。"

SUMMARY="$STATE_DIR/last_run.json"
NEW_NOTES=0
RUN_STATUS="unknown"
if [[ -f "$SUMMARY" ]]; then
  NEW_NOTES="$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1])).get("new_notes",0))' "$SUMMARY")"
  RUN_STATUS="$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1])).get("status","unknown"))' "$SUMMARY")"
fi

if [[ -z "$(git status --porcelain -- data/xhs)" ]]; then
  echo "没有新数据，无需提交。"
  notify "知域 · 小红书动向" "今日无新增笔记（状态 $RUN_STATUS）"
  finish
  exit 0
fi

if [[ "${XHS_NO_COMMIT:-0}" == "1" ]]; then
  echo "XHS_NO_COMMIT=1：已抓取 $NEW_NOTES 条新笔记，留待人工提交。"
  notify "知域 · 小红书动向" "新增 $NEW_NOTES 条，等待人工提交"
  finish
  exit 0
fi

echo "-- 提交"
git add data/xhs
git commit -m "xhs: daily update $TODAY (+$NEW_NOTES notes, $RUN_STATUS)" || fail "git commit 失败"

if [[ "${XHS_NO_PUSH:-0}" == "1" ]]; then
  echo "XHS_NO_PUSH=1：已提交，未推送。"
  notify "知域 · 小红书动向" "新增 $NEW_NOTES 条，已提交未推送"
  finish
  exit 0
fi

echo "-- 推送"
if git push; then
  notify "知域 · 小红书动向" "新增 $NEW_NOTES 条笔记，已推送（状态 $RUN_STATUS）"
  echo "✓ 完成：新增 $NEW_NOTES 条，状态 $RUN_STATUS"
else
  fail "git push 失败，提交已保留在本地，稍后手动 git push 即可"
fi

finish
