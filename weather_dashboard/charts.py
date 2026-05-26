import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


def temperature_trend(df: pd.DataFrame) -> go.Figure:
    """折线图：各城市最高/最低温度趋势"""
    fig = go.Figure()
    colors = px.colors.qualitative.Set2

    for i, city in enumerate(df["城市"].unique()):
        city_df = df[df["城市"] == city]
        color = colors[i % len(colors)]

        fig.add_trace(go.Scatter(
            x=city_df["日期"], y=city_df["最高温度"],
            name=f"{city} 最高",
            line=dict(color=color, width=2),
            mode="lines+markers",
        ))
        fig.add_trace(go.Scatter(
            x=city_df["日期"], y=city_df["最低温度"],
            name=f"{city} 最低",
            line=dict(color=color, width=1.5, dash="dot"),
            mode="lines+markers",
        ))

    fig.update_layout(
        title="温度趋势（°C）",
        xaxis_title="日期",
        yaxis_title="温度 (°C)",
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        template="plotly_white",
    )
    return fig


def precipitation_bar(df: pd.DataFrame) -> go.Figure:
    """柱状图：各城市每日降水量"""
    fig = px.bar(
        df, x="日期", y="降水量", color="城市",
        barmode="group",
        labels={"降水量": "降水量 (mm)"},
        title="每日降水量 (mm)",
        template="plotly_white",
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    fig.update_layout(
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
    )
    return fig


def windspeed_box(df: pd.DataFrame) -> go.Figure:
    """箱线图：各城市风速分布"""
    fig = px.box(
        df, x="城市", y="最大风速", color="城市",
        labels={"最大风速": "最大风速 (km/h)"},
        title="风速分布 (km/h)",
        template="plotly_white",
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    fig.update_layout(showlegend=False)
    return fig


def heatmap_temperature(df: pd.DataFrame) -> go.Figure:
    """热力图：城市 × 日期 的最高温度"""
    pivot = df.pivot_table(index="城市", columns="日期", values="最高温度")
    pivot.columns = [d.strftime("%m-%d") for d in pivot.columns]

    fig = go.Figure(data=go.Heatmap(
        z=pivot.values,
        x=pivot.columns.tolist(),
        y=pivot.index.tolist(),
        colorscale="RdYlBu_r",
        colorbar=dict(title="°C"),
        hoverongaps=False,
    ))
    fig.update_layout(
        title="最高温度热力图 (°C)",
        xaxis_title="日期",
        yaxis_title="城市",
        template="plotly_white",
    )
    return fig
