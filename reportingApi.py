# coding=utf-8
import streamlit as st
import hashlib
import time
import requests
import pandas as pd
from datetime import datetime, timedelta

# ==========================================
# Pangle 工具类
# ==========================================

class PangleMediaUtil:
    user_id = ""
    role_id = ""
    secure_key = ""

    version = "2.0"
    sign_type_md5 = "MD5"

    KEY_USER_ID = "user_id"
    KEY_ROLE_ID = "role_id"
    KEY_VERSION = "version"
    KEY_SIGN_TYPE = "sign_type"

    PANGLE_HOST = "https://open-api.pangleglobal.com"

    @classmethod
    def sign_gen(cls, params):
        result = {"sign": "", "url": ""}

        params = params.copy()

        params[cls.KEY_USER_ID] = cls.user_id
        params[cls.KEY_ROLE_ID] = cls.role_id
        params[cls.KEY_VERSION] = cls.version
        params[cls.KEY_SIGN_TYPE] = cls.sign_type_md5

        # timestamp为空 → 自动生成
        if not params.get("timestamp"):
            params["timestamp"] = int(time.time())

        param_orders = sorted(params.items(), key=lambda x: x[0])

        raw_str = ""
        for k, v in param_orders:
            if v == "":
                continue
            raw_str += f"{k}={v}&"

        sign_str = raw_str[:-1] + cls.secure_key
        sign = hashlib.md5(sign_str.encode()).hexdigest()

        result["sign"] = sign
        result["url"] = raw_str + "sign=" + sign

        return result

    @classmethod
    def get_media_rt_income(cls, params):
        url = cls.sign_gen(params).get("url", "")
        return cls.PANGLE_HOST + "/union_pangle/open/api/rt/income?" + url


# ==========================================
# JSON → DataFrame 转换
# ==========================================

def json_to_dataframe(api_json):

    if "Data" not in api_json:
        return pd.DataFrame()

    rows = []

    for date, records in api_json["Data"].items():
        for r in records:
            row = {"date": date}
            row.update(r)
            rows.append(row)

    return pd.DataFrame(rows)


# ==========================================
# Streamlit UI
# ==========================================

st.set_page_config(page_title="Pangle API V2 工具", page_icon="🚀")
st.title("🚀 Pangle Reporting API V2 工具")

# ✅ 默认日期 = 昨天
default_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

# ------------------------
# 账号信息
# ------------------------
st.subheader("账号信息")

user_id = st.text_input("User ID")
role_id = st.text_input("Role ID")
secure_key = st.text_input("Secure Key", type="password")

# ------------------------
# 基础参数
# ------------------------
st.subheader("基础参数")

date = st.text_input(
    "date (YYYY-MM-DD)",
    value=default_date
)

time_zone = st.number_input("time_zone", value=8)
currency = st.text_input("currency", "usd")

# ✅ timestamp 默认空
timestamp = st.text_input("timestamp (可留空)", "")

# ------------------------
# 可选参数
# ------------------------
st.subheader("可选参数")

app_id = st.text_input("app_id", "")
region = st.text_input("region", "")
dimensions = st.text_input("dimensions", "is_bidding")
bidding_type = st.text_input("bidding_type", "")
ad_slot_type = st.text_input("ad_slot_type", "")
media_name = st.text_input("media_name", "")

# ==========================================
# 主按钮
# ==========================================

if st.button("生成并获取数据 ✅"):

    if not user_id or not role_id or not secure_key:
        st.error("请填写全部账号信息")
        st.stop()

    # 设置账号
    PangleMediaUtil.user_id = user_id
    PangleMediaUtil.role_id = role_id
    PangleMediaUtil.secure_key = secure_key

    params = {
        "date": date,
        "time_zone": time_zone,
        "currency": currency,
        "timestamp": timestamp,
        "app_id": app_id,
        "region": region,
        "dimensions": dimensions,
        "bidding_type": bidding_type,
        "ad_slot_type": ad_slot_type,
        "media_name": media_name,
    }

    # 生成 URL
    url = PangleMediaUtil.get_media_rt_income(params)

    st.success("API URL 已生成")
    st.code(url, language="text")

    # ==========================
    # 请求 API
    # ==========================
    with st.spinner("请求 API 数据中..."):

        try:
            response = requests.get(url, timeout=30)
            data = response.json()

        except Exception as e:
            st.error(f"请求失败: {e}")
            st.stop()

    # 显示原始 JSON
    st.subheader("原始 JSON")
    st.json(data)

    # ==========================
    # JSON → CSV
    # ==========================
    df = json_to_dataframe(data)

    if df.empty:
        st.warning("没有可转换的数据")
        st.stop()

    st.subheader("转换后的数据表")

    st.dataframe(df, use_container_width=True)

    # ==========================
    # CSV 下载
    # ==========================
    csv = df.to_csv(index=False).encode("utf-8-sig")

    st.download_button(
        label="⬇️ 下载 CSV",
        data=csv,
        file_name=f"pangle_report_{date}.csv",
        mime="text/csv",
    )