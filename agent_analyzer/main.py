from fastapi import FastAPI, Request
import uuid
import requests
from config import DEEPSEEK_API_KEY, DEEPSEEK_URL

app = FastAPI()

def call_deepseek(raw_news):
    news_text = "\n".join([f"- {item['title']}: {item['content']}" for item in raw_news])
    prompt = f"""你是一个智能新闻分析助手，请对以下新闻进行详细分析。\n\n新闻内容：\n{news_text}\n\n请对新闻进行总结、情感倾向分析和风险等级评估，并给出你的理由。\n"""
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }
    resp = requests.post(DEEPSEEK_URL, headers=headers, json=payload)
    if resp.status_code == 200:
        content = resp.json()["choices"][0]["message"]["content"]
        print("大模型原始输出：", content)
        return {"raw_analysis": content}
    else:
        print("大模型原始输出：DeepSeek 分析失败")
        return {"raw_analysis": "DeepSeek 分析失败"}

@app.get("/collect")
@app.post("/a2a/message")
async def analyze_news(request: Request):
    data = await request.json()
    task = data.get("task")
    if task != "ANALYZE_NEWS":
        return {"error": "Unsupported task"}
    raw_news = data["content"].get("raw_news", [])
    result = call_deepseek(raw_news)
    response = {
        "message_id": str(uuid.uuid4()),
        "sender": "NewsAnalyzerAgent",
        "receiver": data["sender"],
        "task": "ANALYSIS_RESULT",
        "content": result
    }
    return response

# 启动命令（终端中）
# uvicorn main:app --reload --port 8001
