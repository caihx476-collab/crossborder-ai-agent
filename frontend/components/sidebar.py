import streamlit as st
from frontend.api_client import api_get_stats


def render_sidebar():
    with st.sidebar:
        st.markdown("## 🤖 CrossBorder AI")
        st.markdown("---")
        stats = api_get_stats()
        st.metric("总任务", stats.get("total_tasks", 0))
        st.metric("待审核", stats.get("pending_count", 0))
        st.markdown("---")
        st.markdown("### 📋 导航")
        st.markdown("- [内容生成](#内容生成)")
        st.markdown("- [内容审核](#内容审核)")
        st.markdown("- [历史记录](#历史记录)")
        st.markdown("- [系统设置](#系统设置)")
        st.markdown("---")
        st.caption("v2.0.0 · AI跨境电商运营助手")
