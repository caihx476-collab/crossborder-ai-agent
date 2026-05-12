import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st
from frontend.api_client import api_get_tasks, api_get_items, api_update_status, api_batch_review, api_export_excel
from frontend.components.sidebar import render_sidebar

st.set_page_config(page_title="内容审核", page_icon="✅", layout="wide")
render_sidebar()

st.markdown("## ✅ 内容审核")

tasks = api_get_tasks(limit=50)
if not tasks:
    st.info("暂无任务，请先生成内容")
    st.stop()

task_options = {f"{t['product_name']} ({t['batch_id'][:15]}...) - {t['pending_count']}待审核": t["batch_id"] for t in tasks}
selected_label = st.selectbox("选择任务", list(task_options.keys()))
batch_id = task_options[selected_label]

items = api_get_items(batch_id)
if not items:
    st.warning("该任务无内容")
    st.stop()

if "selected_items" not in st.session_state:
    st.session_state["selected_items"] = set()

col1, col2, col3 = st.columns([1, 1, 2])
with col1:
    filter_status = st.selectbox("筛选状态", ["全部", "⏳ 待审核", "✅ 已通过", "❌ 已拒绝"], key="rev_status")
with col2:
    filter_type = st.selectbox("筛选类型", ["全部", "商品标题", "SEO关键词", "商品描述"], key="rev_type")
with col3:
    if st.button("☑️ 全选/取消", use_container_width=True):
        all_ids = [item["item_id"] for item in items]
        current = st.session_state.get("selected_items", set())
        if all(iid in current for iid in all_ids) and all_ids:
            for iid in all_ids:
                st.session_state[f"sel_{iid}"] = False
            st.session_state["selected_items"] = set()
        else:
            for iid in all_ids:
                st.session_state[f"sel_{iid}"] = True
            st.session_state["selected_items"] = set(all_ids)

status_map = {"全部": None, "⏳ 待审核": "Pending", "✅ 已通过": "Approved", "❌ 已拒绝": "Rejected"}
type_map = {"全部": None, "商品标题": "Title", "SEO关键词": "SEO Keyword", "商品描述": "Description"}

filtered = []
for item in items:
    if status_map[filter_status] and item["status"] != status_map[filter_status]:
        continue
    if type_map[filter_type] and item["item_type"] != type_map[filter_type]:
        continue
    filtered.append(item)

st.markdown(f"<div style='color:#6b7280;font-size:13px;'>共 {len(filtered)} 项</div>", unsafe_allow_html=True)

type_tags = {"Title": "tag-title", "SEO Keyword": "tag-seo", "Description": "tag-desc"}
type_labels = {"Title": "商品标题", "SEO Keyword": "SEO关键词", "Description": "商品描述"}
status_badges = {
    "Pending": '<span class="badge-pending">⏳ 待审核</span>',
    "Approved": '<span class="badge-approved">✅ 已通过</span>',
    "Rejected": '<span class="badge-rejected">❌ 已拒绝</span>',
}
border_colors = {"Pending": "#f59e0b", "Approved": "#10b981", "Rejected": "#ef4444"}

for item in filtered:
    item_id = item["item_id"]
    current_status = item["status"]
    tag_class = type_tags.get(item["item_type"], "tag-title")
    label = type_labels.get(item["item_type"], item["item_type"])
    badge = status_badges.get(current_status, current_status)
    border = border_colors.get(current_status, "#e5e7eb")

    st.markdown(f"""
    <div class="review-row" style="border-left:3px solid {border};">
        <div style="display:flex;align-items:center;gap:12px;">
            <span class="{tag_class}">{label}</span> {badge}
            <span class="content-text" style="flex:1;">{item['content']}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns([1, 3, 1, 1])
    with col1:
        is_selected = item_id in st.session_state.get("selected_items", set())
        new_sel = st.checkbox("选择", value=is_selected, key=f"sel_{item_id}", label_visibility="collapsed")
        current_selected = st.session_state.get("selected_items", set())
        if new_sel and item_id not in current_selected:
            current_selected.add(item_id)
        elif not new_sel and item_id in current_selected:
            current_selected.discard(item_id)
        st.session_state["selected_items"] = current_selected

    with col4:
        if current_status == "Pending":
            st.markdown('<div class="btn-approve">', unsafe_allow_html=True)
            if st.button("通过", key=f"appr_{item_id}"):
                api_update_status(item_id, "approve")
                st.success("已通过")
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        elif current_status == "Approved":
            st.markdown('<div class="btn-reject">', unsafe_allow_html=True)
            if st.button("拒绝", key=f"rej_{item_id}"):
                api_update_status(item_id, "reject")
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="btn-restore">', unsafe_allow_html=True)
            if st.button("恢复", key=f"rest_{item_id}"):
                api_update_status(item_id, "restore")
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

selected_count = len(st.session_state.get("selected_items", set()))
if selected_count > 0:
    st.markdown(f"**已选择 {selected_count} 项**")
    bc1, bc2, bc3 = st.columns([1, 1, 2])
    with bc1:
        st.markdown('<div class="btn-batch-approve">', unsafe_allow_html=True)
        if st.button(f"✅ 批量通过 ({selected_count})", use_container_width=True):
            review_items = [{"item_id": iid, "action": "approve"} for iid in st.session_state["selected_items"]]
            api_batch_review(review_items)
            st.session_state["selected_items"] = set()
            st.success("批量通过成功")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with bc2:
        st.markdown('<div class="btn-batch-reject">', unsafe_allow_html=True)
        if st.button(f"❌ 批量拒绝 ({selected_count})", use_container_width=True):
            review_items = [{"item_id": iid, "action": "reject"} for iid in st.session_state["selected_items"]]
            api_batch_review(review_items)
            st.session_state["selected_items"] = set()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with bc3:
        excel_data = api_export_excel(batch_id)
        if excel_data:
            filename = f"{batch_id}.xlsx"
            st.download_button("📥 下载Excel", excel_data, file_name=filename, use_container_width=True)
