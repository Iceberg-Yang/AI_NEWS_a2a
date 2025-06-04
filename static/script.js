document.addEventListener('DOMContentLoaded', function() {
    const fetchNewsButton = document.getElementById('fetchNews');
    const newsList = document.getElementById('newsList');
    const analysisResult = document.getElementById('analysisResult');

    fetchNewsButton.addEventListener('click', async function() {
        // 显示加载状态
        showLoading();
        
        try {
            // 调用后端API
            const response = await fetch('http://localhost:8000/collect');
            const data = await response.json();

            if (data.status === 'success') {
                // 显示新闻列表
                displayNews(data.analysis_result.raw_news);
                // 显示分析结果
                displayAnalysis(data.analysis_result);
            } else {
                showError('获取新闻失败：' + data.message);
            }
        } catch (error) {
            showError('系统错误：' + error.message);
        } finally {
            // 隐藏加载状态
            hideLoading();
        }
    });

    function showLoading() {
        newsList.innerHTML = `
            <div class="loading">
                <div class="spinner-border loading-spinner text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
                <p class="mt-2">正在获取新闻...</p>
            </div>
        `;
        analysisResult.innerHTML = `
            <div class="loading">
                <div class="spinner-border loading-spinner text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
                <p class="mt-2">正在分析新闻...</p>
            </div>
        `;
    }

    function hideLoading() {
        const loadingElements = document.querySelectorAll('.loading');
        loadingElements.forEach(el => el.style.display = 'none');
    }

    function showError(message) {
        analysisResult.innerHTML = `
            <div class="alert alert-danger">
                ${message}
            </div>
        `;
    }

    function displayNews(news) {
        newsList.innerHTML = news.map(item => `
            <div class="news-item">
                <div class="news-title">${item.title}</div>
                <div class="news-content">${item.content}</div>
            </div>
        `).join('');
    }

    function displayAnalysis(result) {
        analysisResult.innerHTML = `
            <div class="analysis-section">
                <h6>分析结果</h6>
                <pre class="analysis-text" style="white-space: pre-wrap;">${result.raw_analysis}</pre>
            </div>
        `;
    }
}); 