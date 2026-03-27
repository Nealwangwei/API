# coding=utf-8
import streamlit as st
import hashlib
import time

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
    KEY_SIGN = "sign"
    KEY_SIGN_TYPE = "sign_type"
    PANGLE_HOST = "https://open-api.pangleglobal.com"

    @classmethod
    def sign_gen(cls, params):
        result = {"sign": "", "url": ""}

        if not isinstance(params, dict):
            return result

        params[cls.KEY_USER_ID] = cls.user_id
        params[cls.KEY_ROLE_ID] = cls.role_id
        params[cls.KEY_VERSION] = cls.version
        params[cls.KEY_SIGN_TYPE] = cls.sign_type_md5

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
    def get_signed_url(cls, params):
        return cls.sign_gen(params).get("url", "")

    @classmethod
    def get_media_rt_income(cls, params):
        url = cls.get_signed_url(params)
        if url == "":
            return ""
        return cls.PANGLE_HOST + "/union_pangle/open/api/rt/income?" + url


# ==========================================
# Streamlit UI
# ==========================================
st.set_page_config(page_title="Pangle API V2 工具", page_icon="🚀")
st.title("🚀 Pangle Reporting API V2 工具")

st.subheader("账号信息")
user_id = st.text_input("User ID")
role_id = st.text_input("Role ID")
secure_key = st.text_input("Secure Key", type="password")

st.subheader("基础参数")
date = st.text_input("date (YYYY-MM-DD)", "2026-03-24")
time_zone = st.number_input("time_zone", value=8)
currency = st.text_input("currency", "usd")
timestamp = st.text_input("timestamp (可留空, 默认当前)", str(int(time.time())))

st.subheader("可选参数")
app_id = st.text_input("app_id (多个用逗号分隔)", "")
region = st.text_input("region (国家码, 如CN, US)", "")
dimensions = st.text_input("dimensions (多个用逗号分隔)", "is_bidding")
bidding_type = st.text_input("bidding_type (可选)", "")
ad_slot_type = st.text_input("ad_slot_type (可选)", "")
media_name = st.text_input("media_name (可选)", "")

if st.button("生成 API URL ✅"):

    if not user_id or not role_id or not secure_key:
        st.error("请填写全部账号信息")
    else:
        # 设置账号信息
        PangleMediaUtil.user_id = user_id
        PangleMediaUtil.role_id = role_id
        PangleMediaUtil.secure_key = secure_key

        # 生成参数字典
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

        url = PangleMediaUtil.get_media_rt_income(params)

        st.success("生成成功！")
        st.code(url, language="text")
