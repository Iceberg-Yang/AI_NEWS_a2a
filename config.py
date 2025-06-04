import os
from dotenv import load_dotenv

# 加载.env文件中的环境变量
load_dotenv()

# API配置
GNEWS_API_KEY = os.getenv('GNEWS_API_KEY')
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')

# API URLs
GNEWS_URL = f"https://gnews.io/api/v4/top-headlines?token={GNEWS_API_KEY}&lang=zh&country=cn&max=5"
DEEPSEEK_URL = "https://api.deepseek.com/v1/chat/completions"

# 服务配置
NEWS_ANALYZER_URL = os.getenv('NEWS_ANALYZER_URL', 'http://localhost:8001/a2a/message')
COLLECTOR_PORT = int(os.getenv('COLLECTOR_PORT', '8000'))
ANALYZER_PORT = int(os.getenv('ANALYZER_PORT', '8001'))

# CORS配置
ALLOWED_ORIGINS = os.getenv('ALLOWED_ORIGINS', '*').split(',') 