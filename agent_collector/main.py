from fastapi import FastAPI
import requests

app = FastAPI()

# GNews 配置
GNEWS_API_KEY = "7b1a790f8c7a63b72165650a18822f0e"  # 请替换为你自己的 key
GNEWS_URL = f"https://gnews.io/api/v4/top-headlines?token={GNEWS_API_KEY}&lang=zh&country=cn&max=5"
NEWS_ANALYZER_URL = "http://localhost:8001/a2a/message"  # 指向分析端


# 从 GNews 获取新闻
def fetch_news_from_gnews():
    try:
        response = requests.get(GNEWS_URL)
        data = response.json()
        if data.get("articles"):
            raw_news = []
            for article in data["articles"]:
                raw_news.append({
                    "title": article.get("title"),
                    "content": article.get("description") or article.get("content") or ""
                })
            print("📰 获取到的新闻内容：", raw_news) 
            return raw_news
        else:
            print("GNews 返回为空")
            return None
    except Exception as e:
        print(f"获取 GNews 新闻失败: {e}")
        return None
    
@app.get("/collect")
@app.get("/collect")
async def collect_news_and_send():
    # 获取真实新闻
    raw_news = fetch_news_from_gnews()

    if not raw_news:
        return {
            "status": "error",
            "message": "无法从 GNews 获取新闻"
        }
    
    # 构建A2A请求数据
    payload = {
        "message_id": "123",  # 这个可以替换为 UUID 等唯一标识
        "sender": "NewsCollectorAgent",
        "receiver": "NewsAnalyzerAgent",
        "task": "ANALYZE_NEWS",
        "content": {
            "raw_news": raw_news
        }
    }

    # 发起请求到分析端
    response = requests.post(NEWS_ANALYZER_URL, json=payload)

    if response.status_code == 200:
        # 解析 DeepSeek 返回的分析结果
        result = response.json()
        return {
            "status": "success",
            "analysis_result": result["content"]
        }
    else:
        return {
            "status": "error",
            "message": "Failed to communicate with NewsAnalyzerAgent"
        }
