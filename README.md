# AI News Analysis System

这是一个基于AI的新闻分析系统，可以自动获取新闻并使用AI进行分析。

## 功能特点

- 自动获取最新中文新闻
- 使用AI进行新闻分析和情感评估
- 实时展示分析结果
- 美观的Web界面

## 系统要求

- Python 3.8+
- pip（Python包管理器）

## 安装步骤

1. 克隆项目到本地：
```bash
git clone [项目地址]
cd [项目目录]
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 配置环境变量：
   - 复制 `.env.example` 文件并重命名为 `.env`
   - 在 `.env` 文件中填入你的API密钥：
     - GNEWS_API_KEY：从 [GNews](https://gnews.io/) 获取
     - DEEPSEEK_API_KEY：从 [DeepSeek](https://deepseek.com/) 获取

## 运行项目

1. 启动新闻收集服务：
```bash
cd agent_collector
uvicorn main:app --port 8000
```

2. 启动新闻分析服务：
```bash
cd agent_analyzer
uvicorn main:app --port 8001
```

3. 在浏览器中访问：
```
http://localhost:8000/static/index.html
```

## 使用说明

1. 打开网页后，点击"获取最新新闻"按钮
2. 系统会自动获取最新新闻并使用AI进行分析
3. 分析结果会实时显示在右侧面板中

## 注意事项

- 请确保在使用前正确配置了API密钥
- 建议在本地开发环境中运行
- 如需修改端口号，可以在 `.env` 文件中配置

## 许可证

[添加许可证信息] 