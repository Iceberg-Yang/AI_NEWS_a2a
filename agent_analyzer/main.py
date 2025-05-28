from fastapi import FastAPI, Request
import uuid
import requests

app = FastAPI()

DEEPSEEK_API_KEY = "sk-05ebc3ce5203464fa7a59c4b3579b539"  # 替换成你的 DeepSeek key
DEEPSEEK_URL = "https://api.deepseek.com/v1/chat/completions"

def call_deepseek(raw_news):
    news_text = "\n".join([f"- {item['title']}: {item['content']}" for item in raw_news])
    prompt = f"""你是一个智能新闻分析助手，请对以下新闻进行总结、情感倾向分析、并判断是否存在风险信息。

新闻内容：
{news_text}

请用如下结构返回：
总结：...
情感倾向：积极 / 中性 / 消极
风险等级：高 / 中 / 低
"""

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
        return parse_deepseek_response(content)
    else:
        return {
            "summary": "DeepSeek 分析失败",
            "sentiment": "未知",
            "risk_level": "未知"
        }

def parse_deepseek_response(text):
    lines = text.strip().splitlines()
    summary = ""
    sentiment = ""
    risk = ""
    for line in lines:
        if "总结" in line:
            summary = line.split("：", 1)[-1].strip()
        elif "情感" in line:
            sentiment = line.split("：", 1)[-1].strip()
        elif "风险" in line:
            risk = line.split("：", 1)[-1].strip()
    return {
        "summary": summary,
        "sentiment": sentiment,
        "risk_level": risk
    }

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
