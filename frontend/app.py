import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from frontend.components.sidebar import render_sidebar
from frontend.components.stat_cards import render_stat_cards
from frontend.api_client import api_get_stats

st.set_page_config(page_title="CrossBorder AI Agent", page_icon="🤖", layout="wide")
st.markdown("""
<style>
.block-container {padding-top: 2rem; padding-bottom: 2rem; max-width: 1400px;}
.page-title {font-size: 36px; font-weight: 800; color: #111827; margin-bottom: 4px;}
.page-subtitle {font-size: 14px; color: #6b7280; margin-bottom: 28px;}
.section-title {font-size: 20px; font-weight: 700; margin-top: 28px; margin-bottom: 14px; color: #111827;}
.tag-title {display:inline-block;background:#dbeafe;color:#1d4ed8;padding:2px 10px;border-radius:6px;font-size:12px;font-weight:600;}
.tag-seo {display:inline-block;background:#fef3c7;color:#b45309;padding:2px 10px;border-radius:6px;font-size:12px;font-weight:600;}
.tag-desc {display:inline-block;background:#ede9fe;color:#7c3aed;padding:2px 10px;border-radius:6px;font-size:12px;font-weight:600;}
.badge-pending {display:inline-block;background:#fef3c7;color:#92400e;padding:2px 10px;border-radius:6px;font-size:12px;font-weight:600;}
.badge-approved {display:inline-block;background:#d1fae5;color:#065f46;padding:2px 10px;border-radius:6px;font-size:12px;font-weight:600;}
.badge-rejected {display:inline-block;background:#fee2e2;color:#991b1b;padding:2px 10px;border-radius:6px;font-size:12px;font-weight:600;}
.review-row {background:white;border-radius:12px;padding:14px 18px;margin-bottom:8px;border:1px solid #e5e7eb;transition:box-shadow 0.15s;}
.review-row:hover {box-shadow:0 2px 8px rgba(0,0,0,0.06);}
.content-text {font-size:14px;color:#374151;line-height:1.5;word-break:break-word;}
.stButton > button {border-radius:10px;font-weight:600;transition:all 0.15s;}
.stButton > button:hover {transform:translateY(-1px);box-shadow:0 2px 6px rgba(0,0,0,0.1);}
.btn-approve > button {background:#059669 !important;color:white !important;border:none !important;}
.btn-reject > button {background:#dc2626 !important;color:white !important;border:none !important;}
.btn-restore > button {background:#6b7280 !important;color:white !important;border:none !important;}
.btn-batch-approve > button {background:#059669 !important;color:white !important;border:none !important;height:48px !important;font-size:16px !important;}
.btn-batch-reject > button {background:#dc2626 !important;color:white !important;border:none !important;height:48px !important;font-size:16px !important;}
</style>
""", unsafe_allow_html=True)

render_sidebar()

st.markdown('<div class="page-title">🤖 CrossBorder AI Agent</div>', unsafe_allow_html=True)
st.markdown('<div class="page-subtitle">AI跨境电商运营助手 · 多模型 · 多平台 · 内容审核 · Excel导出</div>', unsafe_allow_html=True)

stats = api_get_stats()
st.markdown('<div class="section-title">📊 运营数据</div>', unsafe_allow_html=True)
render_stat_cards(stats)

st.markdown("---")
st.markdown("### 📌 快速开始")
st.markdown("使用左侧导航栏或下方按钮进入各功能模块：")

col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("📝 内容生成", use_container_width=True):
        st.switch_page("pages/1_generate.py")
with col2:
    if st.button("✅ 内容审核", use_container_width=True):
        st.switch_page("pages/2_review.py")
with col3:
    if st.button("📋 历史记录", use_container_width=True):
        st.switch_page("pages/3_history.py")
with col4:
    if st.button("⚙️ 系统设置", use_container_width=True):
        st.switch_page("pages/4_settings.py")
