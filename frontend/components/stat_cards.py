import streamlit as st


def render_stat_cards(stats: dict):
    cols = st.columns(5)
    cards = [
        ("总任务", stats.get("total_tasks", 0), "#3b82f6"),
        ("总内容", stats.get("total_items", 0), "#8b5cf6"),
        ("⏳ 待审核", stats.get("pending_count", 0), "#f59e0b"),
        ("✅ 已通过", stats.get("approved_count", 0), "#10b981"),
        ("❌ 已拒绝", stats.get("rejected_count", 0), "#ef4444"),
    ]
    for col, (label, value, color) in zip(cols, cards):
        with col:
            st.markdown(
                f'<div style="background:white;border-radius:14px;padding:20px 24px;'
                f'border:1px solid #e5e7eb;box-shadow:0 1px 3px rgba(0,0,0,0.04);text-align:center;">'
                f'<div style="font-size:32px;font-weight:800;color:{color};line-height:1.2;">{value}</div>'
                f'<div style="font-size:13px;color:#6b7280;margin-top:4px;">{label}</div></div>',
                unsafe_allow_html=True,
            )
