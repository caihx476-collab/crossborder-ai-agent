import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st
from frontend.components.sidebar import render_sidebar
from backend.config import settings

st.set_page_config(page_title="系统设置", page_icon="⚙️", layout="wide")
render_sidebar()

st.markdown("## ⚙️ 系统设置")

st.markdown("### 🤖 AI模型配置")
st.markdown("当前配置从 `.env` 文件读取，修改后需重启服务生效")

col1, col2 = st.columns(2)
with col1:
    st.text_input("当前AI模型", value=settings.AI_PROVIDER, disabled=True)
    st.text_input("MiniMax模型", value=settings.MINIMAX_MODEL, disabled=True)
with col2:
    st.text_input("OpenAI模型", value=settings.OPENAI_MODEL, disabled=True)
    st.text_input("Ollama模型", value=settings.OLLAMA_MODEL, disabled=True)

st.markdown("---")
st.markdown("### 🔑 API密钥状态")

col1, col2, col3 = st.columns(3)
with col1:
    has_key = "✅ 已配置" if settings.MINIMAX_API_KEY else "❌ 未配置"
    st.markdown(f"**MiniMax**: {has_key}")
with col2:
    has_key = "✅ 已配置" if settings.OPENAI_API_KEY else "❌ 未配置"
    st.markdown(f"**OpenAI**: {has_key}")
with col3:
    st.markdown(f"**Ollama地址**: `{settings.OLLAMA_BASE_URL}`")

st.markdown("---")
st.markdown("### 🗄️ 数据库配置（MySQL）")
col1, col2 = st.columns(2)
with col1:
    st.text_input("主机", value=settings.DB_HOST, disabled=True)
    st.text_input("用户", value=settings.DB_USER, disabled=True)
with col2:
    st.text_input("端口", value=str(settings.DB_PORT), disabled=True)
    st.text_input("数据库", value=settings.DB_NAME, disabled=True)
st.text_input("日志级别", value=settings.LOG_LEVEL, disabled=True)

st.markdown("---")
st.markdown("### 📖 使用说明")
st.markdown("""
1. 复制 `.env.example` 为 `.env`，填入API密钥和MySQL配置
2. 确保MySQL服务已启动，并创建好数据库（后端启动时自动创建）
3. 启动后端：`uvicorn backend.main:app --reload`
4. 启动前端：`streamlit run frontend/app.py`
5. 在「内容生成」页面输入商品信息并生成
6. 在「内容审核」页面审核生成的内容
7. 在「历史记录」页面查看和导出历史任务
""")
