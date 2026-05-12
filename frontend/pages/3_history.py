import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st
from frontend.api_client import api_get_tasks, api_search_tasks, api_get_items, api_export_excel
from frontend.components.sidebar import render_sidebar

st.set_page_config(page_title="历史记录", page_icon="📋", layout="wide")
render_sidebar()

st.markdown("## 📋 历史记录")

keyword = st.text_input("🔍 搜索商品名称", placeholder="输入关键词搜索", key="hist_search")
if keyword:
    tasks = api_search_tasks(keyword)
else:
    tasks = api_get_tasks(limit=50)

if not tasks:
    st.info("暂无历史任务")
    st.stop()

for task in tasks:
    status_emoji = "🟡" if task["pending_count"] > 0 else "🟢"
    with st.expander(
        f"{status_emoji} {task['product_name']} - {task['region']} - {task['platform']} ({task['created_at']})"
    ):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("总内容", task["total_items"])
        with col2:
            st.metric("待审核", task["pending_count"])
        with col3:
            st.metric("已通过", task["approved_count"])
        with col4:
            st.metric("已拒绝", task["rejected_count"])

        if st.button(f"查看详情", key=f"view_{task['batch_id']}"):
            items = api_get_items(task["batch_id"])
            if items:
                type_labels = {"Title": "商品标题", "SEO Keyword": "SEO关键词", "Description": "商品描述"}
                for item in items:
                    label = type_labels.get(item["item_type"], item["item_type"])
                    status_icon = {"Pending": "⏳", "Approved": "✅", "Rejected": "❌"}.get(item["status"], "?")
                    st.markdown(f"**{label}** {status_icon} `{item['status']}`")
                    st.markdown(f"> {item['content']}")
                    st.markdown("---")

        excel_data = api_export_excel(task["batch_id"])
        if excel_data:
            st.download_button(
                "📥 下载Excel",
                excel_data,
                file_name=f"{task['batch_id']}.xlsx",
                key=f"dl_{task['batch_id']}",
            )
