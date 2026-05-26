import streamlit as st
import pandas as pd
from config import CITIES
from api import fetch_multiple
from charts import temperature_trend, precipitation_bar, windspeed_box, heatmap_temperature

st.set_page_config(
    page_title="全球天气可视化仪表板",
    page_icon="🌤",
    layout="wide",
)

st.title("🌤 全球天气可视化仪表板")
st.caption("数据来源：Open-Meteo 免费天气 API · 过去 7 天 + 未来 7 天")

# ── 侧边栏：城市选择 ──────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ 设置")
    selected = st.multiselect(
        "选择城市（最多 6 个）",
        options=list(CITIES.keys()),
        default=["北京", "上海", "东京", "纽约"],
        max_selections=6,
    )
    st.divider()
    st.markdown("**图表说明**")
    st.markdown("- 折线图：温度趋势\n- 柱状图：每日降水\n- 箱线图：风速分布\n- 热力图：温度对比")

# ── 数据加载 ──────────────────────────────────────────────────
if not selected:
    st.warning("请在左侧至少选择一个城市。")
    st.stop()

cities_to_fetch = {name: CITIES[name] for name in selected}

with st.spinner("正在获取天气数据..."):
    try:
        df = fetch_multiple(cities_to_fetch)
    except RuntimeError as e:
        st.error(str(e))
        st.stop()

# ── 数据概览 ──────────────────────────────────────────────────
st.subheader("📊 数据概览")
cols = st.columns(len(selected))
for col, city in zip(cols, selected):
    city_df = df[df["城市"] == city]
    today = city_df.iloc[len(city_df) // 2]  # 取中间行近似今日
    col.metric(
        label=city,
        value=f"{today['最高温度']:.1f} °C",
        delta=f"最低 {today['最低温度']:.1f} °C",
    )

st.divider()

# ── 图表区域 ──────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["🌡 温度趋势", "🌧 降水量", "💨 风速分布", "🗺 热力图"])

with tab1:
    st.plotly_chart(temperature_trend(df), use_container_width=True)

with tab2:
    st.plotly_chart(precipitation_bar(df), use_container_width=True)

with tab3:
    st.plotly_chart(windspeed_box(df), use_container_width=True)

with tab4:
    st.plotly_chart(heatmap_temperature(df), use_container_width=True)

# ── 原始数据表 ────────────────────────────────────────────────
with st.expander("📋 查看原始数据"):
    st.dataframe(
        df.sort_values(["城市", "日期"]).reset_index(drop=True),
        use_container_width=True,
    )

if __name__ == "__main__":
    import os, subprocess, sys
    if os.environ.get("_STREAMLIT_RUNNING") != "1":
        env = os.environ.copy()
        env["_STREAMLIT_RUNNING"] = "1"
        subprocess.run([sys.executable, "-m", "streamlit", "run", __file__], env=env)
