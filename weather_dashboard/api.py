import requests
import pandas as pd
from config import API_BASE_URL, PAST_DAYS, FORECAST_DAYS


def fetch_weather(city_name: str, lat: float, lon: float) -> pd.DataFrame:
    """
    从 Open-Meteo API 获取指定城市的天气数据。
    返回包含日期、最高/最低温度、降水量、风速的 DataFrame。
    """
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": [
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_sum",
            "windspeed_10m_max",
        ],
        "timezone": "auto",
        "past_days": PAST_DAYS,
        "forecast_days": FORECAST_DAYS,
    }

    try:
        resp = requests.get(API_BASE_URL, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except requests.RequestException as e:
        raise RuntimeError(f"获取 {city_name} 数据失败: {e}")

    daily = data.get("daily", {})
    df = pd.DataFrame({
        "日期":     pd.to_datetime(daily["time"]),
        "最高温度": daily["temperature_2m_max"],
        "最低温度": daily["temperature_2m_min"],
        "降水量":   daily["precipitation_sum"],
        "最大风速": daily["windspeed_10m_max"],
        "城市":     city_name,
    })
    return df


def fetch_multiple(cities: dict) -> pd.DataFrame:
    """
    批量获取多个城市的天气数据，合并为一个 DataFrame。
    cities: {城市名: {"lat": ..., "lon": ...}}
    """
    frames = []
    for name, coords in cities.items():
        df = fetch_weather(name, coords["lat"], coords["lon"])
        frames.append(df)
    return pd.concat(frames, ignore_index=True)
