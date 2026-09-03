#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# IdeaLab 工具调用脚本 — 通过 TBMCP 网关调用 IdeaLab 工具，将 JSON 结果输出到 stdout。
#
# 用法示例:
#   python3 this_script.py '{"request": {"query": "hello"}}'
#   python3 this_script.py '{"param1": "value1"}'
#
# 入参: 第一个 CLI 参数为 JSON 对象，包含工具所需的业务参数（直接透传，不提取 systemParams）。
# 输出: 成功时将工具返回的 JSON 数据打印到 stdout；错误和进度信息输出到 stderr。
# 依赖: 仅使用 Python 3 标准库，无需 pip install。
# 退出码: 0=成功, 1=失败（鉴权/网络/工具执行错误/超时）。

import json
import os
import sys
import urllib.request
import urllib.error

# 工具身份常量（生成时注入）
TOOL_CODE = "6ea22dc3-1941-455e-8114-7ea8ff4025a4"
TOOL_NAME = "钉钉文档读取"
TOOL_VERSION = "*"
TOOL_TECH_TYPE = 7
SKILL_CODE = "skill_8d966pgyjd"
SKILL_VERSION = "draft"
ACTION_CODE = "6ea22dc3-1941-455e-8114-7ea8ff4025a4"
SKILL_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJza2lsbElkIjoyNTU2MSwic2tpbGxDb2RlIjoic2tpbGxfOGQ5NjZwZ3lqZCIsInNraWxsVmVyc2lvbiI6ImRyYWZ0IiwiYWN0aW9ucyI6eyJpZGVhbGFiX3Rvb2wiOlt7ImNvZGUiOiI2ZWEyMmRjMy0xOTQxLTQ1NWUtODExNC03ZWE4ZmY0MDI1YTQiLCJ2ZXJzaW9uIjoiKiJ9LHsiY29kZSI6ImU2M2EzYWU4LTEwZDQtNDJiNC04YWU0LTc1M2Q0OTQ0MDg2MiIsInZlcnNpb24iOiIxLjAuNCJ9XX19.vhzWNEue7stCWb1JlC_7N1viq6pvnF8o6YvHOOkk9Ec"
IS_ASYNC = False
BASE_URL = "https://tbmcp.alibaba-inc.com"

# 系统参数（运行时从同目录 system_params.json 加载）
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_SYSTEM_PARAMS_FILE = os.path.join(_SCRIPT_DIR, "system_params.json")

def _load_system_params():
    if os.path.exists(_SYSTEM_PARAMS_FILE):
        with open(_SYSTEM_PARAMS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

DEFAULT_SYSTEM_PARAMS = _load_system_params()

# 网络请求与异步轮询配置
REQUEST_TIMEOUT = 120


def invoke_tool(params):
    """
    调用 TBMCP 工具接口。

    Args:
        params: dict, 工具业务参数。

    Returns:
        dict — 响应 JSON 中的 "data" 字段。

    失败时打印错误到 stderr 并 sys.exit(1)。
    """
    if SKILL_TOKEN:
        url = f"{BASE_URL}/api/skill/tool/invoke"
    else:
        url = f"{BASE_URL}/api/tool/invoke"
    payload = {
        "toolName": TOOL_NAME,
        "toolCode": TOOL_CODE,
        "toolVersion": TOOL_VERSION,
        "toolTechType": TOOL_TECH_TYPE,
        "params": params,
        "systemParams": DEFAULT_SYSTEM_PARAMS,
        "platformParams": {
            "skillCode": SKILL_CODE,
            "skillVersion": SKILL_VERSION,
            "actionCode": ACTION_CODE
        }
    }

    data = json.dumps(payload).encode("utf-8")
    headers = {"Content-Type": "application/json; charset=utf-8"}
    if SKILL_TOKEN:
        headers["X-Skill-Token"] = SKILL_TOKEN
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
            trace_id = resp.headers.get("EagleEye-TraceId", "")
            body = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        trace_id = e.headers.get("EagleEye-TraceId", "") if e.headers else ""
        print(f"[ERROR] HTTP {e.code}, traceId={trace_id}", file=sys.stderr)
        try:
            print(e.read().decode("utf-8"), file=sys.stderr)
        except Exception:
            pass
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"[ERROR] Request failed: {e.reason}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Request failed: {e}", file=sys.stderr)
        sys.exit(1)

    if not body.get("success"):
        err_code = body.get("errCode", "UNKNOWN")
        err_msg = body.get("errMsg", "unknown error")
        print(f"[ERROR] Tool invocation failed: [{err_code}] {err_msg}, traceId={trace_id}", file=sys.stderr)
        sys.exit(1)

    return body.get("data")


def main():
    if len(sys.argv) < 2:
        print(f"Usage: python3 {sys.argv[0]} '<json_params>'", file=sys.stderr)
        sys.exit(1)

    try:
        params = json.loads(sys.argv[1])
    except json.JSONDecodeError as e:
        print(f"[ERROR] Invalid JSON input: {e}", file=sys.stderr)
        sys.exit(1)

    result = invoke_tool(params)

    if result is not None:
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

