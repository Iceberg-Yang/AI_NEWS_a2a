from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import requests
from config import GNEWS_URL, NEWS_ANALYZER_URL, ALLOWED_ORIGINS

app = FastAPI()

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载静态文件目录
app.mount("/static", StaticFiles(directory="static"), name="static")

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
    
@app.get("/")
async def read_root():
    return {"message": "Welcome to AI News Analysis System"}

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
        result = response.json()
        return {
            "status": "success",
            "analysis_result": {
                "raw_news": raw_news,
                "raw_analysis": result["content"].get("raw_analysis", "无分析结果")
            }
        }
    else:
        return {
            "status": "error",
            "message": "Failed to communicate with NewsAnalyzerAgent"
        }
