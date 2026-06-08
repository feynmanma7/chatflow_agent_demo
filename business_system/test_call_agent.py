"""
理财营销助手 - 下游业务系统

提供前端对话页面，理财经理可以提问并调用 MCP HTTP 服务获取推荐结果。
每轮对话（用户提问 + 返回结果）自动保存为 JSON 文件。
"""
import json
import os
from datetime import datetime

import requests
from flask import Flask, jsonify, render_template, request

from config import HISTORY_DIR, MCP_HTTP_URL

app = Flask(__name__)

# 确保历史记录目录存在
os.makedirs(HISTORY_DIR, exist_ok=True)

# 取消标志：{user_id: cancel_flag}
cancel_flags = {}


# =========================
# 保存对话历史
# =========================

def save_conversation_round(user_id: str, manager_id: str, query: str, answer: str):
    """
    将每轮对话保存为独立的 JSON 文件。

    文件名格式：{user_id}_{timestamp}.json
    保存内容：用户ID、经理ID、提问时间、问题、回答
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    filename = f"{user_id}_{timestamp}.json"
    filepath = os.path.join(HISTORY_DIR, filename)

    record = {
        "user_id": user_id,
        "manager_id": manager_id,
        "timestamp": datetime.now().isoformat(),
        "query": query,
        "answer": answer
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)

    print(f"[历史记录] 已保存: {filepath}")


# =========================
# 静态资源（favicon 等）
# =========================

@app.route("/favicon.ico")
def favicon():
    """返回空响应避免 404"""
    return "", 204


# =========================
# 页面路由
# =========================

@app.route("/")
def index():
    """渲染前端对话页面"""
    return render_template("index.html")


# =========================
# 提问接口
# =========================

@app.route("/ask", methods=["POST"])
def ask():
    """
    接收前端提问，转发给 MCP HTTP 服务，返回结果并保存历史记录。

    请求体：
    {
        "user_id": "manager001",
        "manager_id": "10001",
        "query": "请帮我推荐理财类的客户。"
    }

    返回：
    {
        "success": true,
        "answer": "...",
        "conversation_id": "..."
    }
    """
    data = request.get_json()

    user_id = data.get("user_id", "anonymous")
    manager_id = data.get("manager_id", "unknown")
    query = data.get("query", "")

    if not query.strip():
        return jsonify({"success": False, "detail": "问题不能为空"}), 400

    # 重置取消标志
    cancel_flags[user_id] = False

    try:
        # 调用 MCP HTTP 服务
        resp = requests.post(
            MCP_HTTP_URL,
            json={
                "user_id": user_id,
                "manager_id": manager_id,
                "query": query
            },
            timeout=60
        )

        # 检查是否被取消
        if cancel_flags.get(user_id):
            return jsonify({
                "success": False,
                "detail": "用户取消了请求"
            }), 499

        resp.raise_for_status()
        result = resp.json()

        answer = result.get("answer", "")

        # 保存本轮对话历史
        save_conversation_round(user_id, manager_id, query, answer)

        return jsonify({
            "success": True,
            "answer": answer,
            "conversation_id": result.get("conversation_id")
        })

    except requests.exceptions.ConnectionError:
        return jsonify({
            "success": False,
            "detail": "无法连接到 MCP HTTP 服务，请确认服务已启动在 localhost:9000"
        }), 503

    except requests.exceptions.Timeout:
        return jsonify({
            "success": False,
            "detail": "请求超时，请稍后重试"
        }), 504

    except Exception as e:
        return jsonify({
            "success": False,
            "detail": str(e)
        }), 500


# =========================
# 取消请求接口
# =========================

@app.route("/cancel", methods=["POST"])
def cancel():
    """
    取消当前用户正在进行的请求。
    """
    data = request.get_json()
    user_id = data.get("user_id", "")
    if user_id:
        cancel_flags[user_id] = True
        print(f"[取消] 用户 {user_id} 取消了当前请求")
    return jsonify({"success": True})


# =========================
# 启动
# =========================

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5050)
