# 全球天气可视化仪表板

基于 Open-Meteo 免费天气 API，使用 Streamlit + Plotly 构建的交互式天气数据可视化仪表板。

## 功能

- 支持全球 10 个预设城市，最多同时对比 6 个
- 展示过去 7 天 + 未来 7 天的天气数据
- 4 种交互式图表：温度趋势、每日降水、风速分布、温度热力图
- 支持缩放、悬停查看数据、点击图例显示/隐藏

## 项目结构

```
weather_dashboard/
├── app.py           # Streamlit 主界面
├── api.py           # Open-Meteo API 数据获取
├── charts.py        # Plotly 图表定义
├── config.py        # 城市列表与 API 配置
└── requirements.txt # 依赖列表
```

## 环境要求

- Python 3.8+
- 网络连接（用于调用 Open-Meteo API）

## 安装

```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 启动方式

**方式一：PyCharm**
直接右键 `app.py` → Run

**方式二：命令行**
```bash
python -m streamlit run app.py
```

启动后浏览器自动打开 `http://localhost:8501`

## 数据来源

[Open-Meteo](https://open-meteo.com/) — 免费开放的天气预报 API，无需注册或 API Key。
