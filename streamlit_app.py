import streamlit as st
from datetime import datetime

from services.title_generator import regenerate_title
from services.seo_generator import generate_keywords
from utils.json_parser import parse_json
from utils.review_manager import load_review_status, save_review_status
from utils.excel_exporter import export_to_excel, update_excel_status
from utils.history_manager import add_history
from utils.db_manager import (
    init_db,
    save_task,
    save_items,
    get_recent_tasks,
    get_items_by_batch,
    search_tasks,
    update_item_status,
    get_dashboard_stats
)

st.set_page_config(page_title="CrossBorder AI Agent", page_icon="🤖", layout="wide")
st.markdown("""
<style>
.block-container {padding-top: 2rem; padding-bottom: 2rem; max-width: 1400px;}

.page-title {font-size: 36px; font-weight: 800; color: #111827; margin-bottom: 4px;}
.page-subtitle {font-size: 14px; color: #6b7280; margin-bottom: 28px;}

.stat-card {
    background: white; border-radius: 14px; padding: 20px 24px;
    border: 1px solid #e5e7eb; box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    text-align: center;
}
.stat-number {font-size: 32px; font-weight: 800; line-height: 1.2;}
.stat-label {font-size: 13px; color: #6b7280; margin-top: 4px;}

.section-title {font-size: 20px; font-weight: 700; margin-top: 28px; margin-bottom: 14px; color: #111827;}

.tag-title {
    display: inline-block; background: #dbeafe; color: #1d4ed8;
    padding: 2px 10px; border-radius: 6px; font-size: 12px; font-weight: 600;
}
.tag-seo {
    display: inline-block; background: #fef3c7; color: #b45309;
    padding: 2px 10px; border-radius: 6px; font-size: 12px; font-weight: 600;
}

.badge-pending {
    display: inline-block; background: #fef3c7; color: #92400e;
    padding: 2px 10px; border-radius: 6px; font-size: 12px; font-weight: 600;
}
.badge-approved {
    display: inline-block; background: #d1fae5; color: #065f46;
    padding: 2px 10px; border-radius: 6px; font-size: 12px; font-weight: 600;
}
.badge-rejected {
    display: inline-block; background: #fee2e2; color: #991b1b;
    padding: 2px 10px; border-radius: 6px; font-size: 12px; font-weight: 600;
}

.review-row {
    background: white; border-radius: 12px; padding: 14px 18px; margin-bottom: 8px;
    border: 1px solid #e5e7eb; transition: box-shadow 0.15s;
}
.review-row:hover {box-shadow: 0 2px 8px rgba(0,0,0,0.06);}

.content-text {font-size: 14px; color: #374151; line-height: 1.5; word-break: break-word;}

.batch-bar {
    position: sticky; bottom: 0; background: white; border-top: 1px solid #e5e7eb;
    padding: 14px 20px; border-radius: 14px; margin-top: 12px;
    box-shadow: 0 -2px 10px rgba(0,0,0,0.06); z-index: 100;
}

.stButton > button {border-radius: 10px; font-weight: 600; transition: all 0.15s;}
.stButton > button:hover {transform: translateY(-1px); box-shadow: 0 2px 6px rgba(0,0,0,0.1);}
.btn-approve > button {background: #059669 !important; color: white !important; border: none !important;}
.btn-reject > button {background: #dc2626 !important; color: white !important; border: none !important;}
.btn-restore > button {background: #6b7280 !important; color: white !important; border: none !important;}
.btn-batch-approve > button {background: #059669 !important; color: white !important; border: none !important; height: 48px !important; font-size: 16px !important;}
.btn-batch-reject > button {background: #dc2626 !important; color: white !important; border: none !important; height: 48px !important; font-size: 16px !important;}
</style>
""", unsafe_allow_html=True)

init_db()

for key in ["title_data", "seo_data", "items", "excel_path"]:
    if key not in st.session_state:
        st.session_state[key] = None

if "selected_items" not in st.session_state:
    st.session_state["selected_items"] = set()
if "filter_status" not in st.session_state:
    st.session_state["filter_status"] = "全部"
if "filter_type" not in st.session_state:
    st.session_state["filter_type"] = "全部"

st.markdown('<div class="page-title">🤖 CrossBorder AI Agent</div>', unsafe_allow_html=True)
st.markdown('<div class="page-subtitle">AI跨境电商运营助手 · 商品标题生成 · SEO优化 · 内容审核 · Excel导出</div>', unsafe_allow_html=True)

review_data_global = load_review_status()
if st.session_state["items"]:
    pending_count = sum(1 for item in st.session_state["items"] if review_data_global.get(item["item_id"], "Pending") == "Pending")
    approved_count = sum(1 for item in st.session_state["items"] if review_data_global.get(item["item_id"], "Pending") == "Approved")
    rejected_count = sum(1 for item in st.session_state["items"] if review_data_global.get(item["item_id"], "Pending") == "Rejected")
else:
    pending_count = approved_count = rejected_count = 0

stats = get_dashboard_stats()
st.markdown('<div class="section-title">📊 运营数据</div>', unsafe_allow_html=True)
c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    st.markdown(f'<div class="stat-card"><div class="stat-number" style="color:#3b82f6">{stats["total_tasks"]}</div><div class="stat-label">总任务</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="stat-card"><div class="stat-number" style="color:#8b5cf6">{stats["total_items"]}</div><div class="stat-label">总内容</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="stat-card"><div class="stat-number" style="color:#f59e0b">{pending_count}</div><div class="stat-label">⏳ 待审核</div></div>', unsafe_allow_html=True)
with c4:
    st.markdown(f'<div class="stat-card"><div class="stat-number" style="color:#10b981">{approved_count}</div><div class="stat-label">✅ 已通过</div></div>', unsafe_allow_html=True)
with c5:
    st.markdown(f'<div class="stat-card"><div class="stat-number" style="color:#ef4444">{rejected_count}</div><div class="stat-label">❌ 已拒绝</div></div>', unsafe_allow_html=True)

st.markdown('<div class="section-title">📦 商品信息</div>', unsafe_allow_html=True)
col1, col2, col3 = st.columns([2, 1, 2])
with col1: product_name = st.text_input("商品名称", placeholder="例如：降噪耳机")
with col2: region = st.text_input("目标地区", placeholder="例如：美国")
with col3: product_feature = st.text_input("商品特点", placeholder="例如：续航长、主动降噪、佩戴舒适")

generate_button = st.button("🚀 一键生成运营内容", use_container_width=True, type="primary")

if generate_button:
    product_info = {"name": product_name, "feature": product_feature, "region": region}
    if not product_name or not product_feature or not region:
        st.warning("请填写完整商品信息")
    else:
        with st.spinner("AI正在生成内容，请稍等..."):
            title_result = regenerate_title(product_info)
            seo_result = generate_keywords(product_info)
            st.session_state["title_data"] = parse_json(title_result)
            st.session_state["seo_data"] = parse_json(seo_result)
            batch_id = datetime.now().strftime("%Y%m%d_%H%M%S")
            items = []
            for i, title in enumerate(st.session_state["title_data"].get("titles", [])):
                items.append({"item_id": f"{batch_id}_title_{i+1}", "type": "Title", "content": title, "status": "Pending"})
            for i, keyword in enumerate(st.session_state["seo_data"].get("keywords", [])):
                items.append({"item_id": f"{batch_id}_keyword_{i+1}", "type": "SEO Keyword", "content": keyword, "status": "Pending"})
            items.sort(key=lambda x: x["status"] != "Pending")
            st.session_state["items"] = items
            excel_path = export_to_excel(items, product_info["name"])
            if excel_path:
                st.session_state["excel_path"] = excel_path
                created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                save_task(batch_id, product_info, excel_path, created_at)
                save_items(items, batch_id)
                add_history(batch_id, product_info, items, excel_path)
                st.success("AI内容生成成功！请在下方审核内容。")
            else:
                st.error("Excel导出失败，请关闭Excel文件后重试")

if st.session_state["items"]:
    st.markdown('<div class="section-title">✅ 内容审核</div>', unsafe_allow_html=True)
    review_data = load_review_status()

    items_sorted = sorted(
        st.session_state["items"],
        key=lambda x: (review_data.get(x["item_id"], "Pending") != "Pending", x["type"] != "Title")
    )

    def handle_single_action(item_id, action):
        rd = load_review_status()
        rd[item_id] = action
        update_item_status(item_id, action)
        update_excel_status(st.session_state["excel_path"], item_id, action)
        save_review_status(rd)
        st.session_state["selected_items"].discard(item_id)

    def handle_select_all():
        all_ids = [item["item_id"] for item in st.session_state["items"]]
        current_selected = st.session_state.get("selected_items", set())
        all_already_selected = all(iid in current_selected for iid in all_ids) and len(all_ids) > 0
        if all_already_selected:
            for iid in all_ids:
                st.session_state[f"select_{iid}"] = False
            st.session_state["selected_items"] = set()
        else:
            selected_set = set()
            for iid in all_ids:
                selected_set.add(iid)
                st.session_state[f"select_{iid}"] = True
            st.session_state["selected_items"] = selected_set

    def handle_batch_action(action):
        selected = st.session_state.get("selected_items", set()).copy()
        if not selected:
            return
        rd = load_review_status()
        for sid in selected:
            rd[sid] = action
            update_item_status(sid, action)
            update_excel_status(st.session_state["excel_path"], sid, action)
        save_review_status(rd)
        action_label = "通过" if action == "Approved" else "拒绝"
        st.session_state["batch_msg"] = f"成功{action_label} {len(selected)} 项内容"
        st.session_state["selected_items"] = set()

    if "batch_msg" in st.session_state:
        st.success(st.session_state.pop("batch_msg"))

    filter_col1, filter_col2, filter_col3, filter_col4 = st.columns([1, 1, 2, 1])
    with filter_col1:
        filter_status = st.selectbox("筛选状态", ["全部", "⏳ 待审核", "✅ 已通过", "❌ 已拒绝"], key="sb_status")
    with filter_col2:
        filter_type = st.selectbox("筛选类型", ["全部", "商品标题", "SEO关键词"], key="sb_type")
    with filter_col3:
        st.markdown("")
    with filter_col4:
        st.button("☑️ 全选/取消", use_container_width=True, help="全选或取消全选", on_click=handle_select_all)

    status_filter_map = {"全部": None, "⏳ 待审核": "Pending", "✅ 已通过": "Approved", "❌ 已拒绝": "Rejected"}
    type_filter_map = {"全部": None, "商品标题": "Title", "SEO关键词": "SEO Keyword"}
    active_status_filter = status_filter_map.get(filter_status)
    active_type_filter = type_filter_map.get(filter_type)

    filtered_items = []
    for item in items_sorted:
        item_id = item["item_id"]
        current_status = review_data.get(item_id, "Pending")
        if active_status_filter and current_status != active_status_filter:
            continue
        if active_type_filter and item["type"] != active_type_filter:
            continue
        filtered_items.append(item)

    st.markdown(f"<div style='color:#6b7280; font-size:13px; margin-bottom:8px;'>共 {len(filtered_items)} 项</div>", unsafe_allow_html=True)

    for item in filtered_items:
        item_id = item["item_id"]
        item_type = item["type"]
        content = item["content"]
        current_status = review_data.get(item_id, "Pending")

        is_selected = item_id in st.session_state.get("selected_items", set())

        type_tag = '<span class="tag-title">商品标题</span>' if item_type == "Title" else '<span class="tag-seo">SEO关键词</span>'
        status_badge_map = {
            "Pending": '<span class="badge-pending">⏳ 待审核</span>',
            "Approved": '<span class="badge-approved">✅ 已通过</span>',
            "Rejected": '<span class="badge-rejected">❌ 已拒绝</span>'
        }
        status_badge = status_badge_map.get(current_status, current_status)

        row_bg = ""
        if current_status == "Approved":
            row_bg = "border-left: 3px solid #10b981;"
        elif current_status == "Rejected":
            row_bg = "border-left: 3px solid #ef4444;"
        else:
            row_bg = "border-left: 3px solid #f59e0b;"

        st.markdown(f"""
        <div class="review-row" style="{row_bg}">
            <div style="display:flex; align-items:center; justify-content:space-between; gap:12px;">
                <div style="flex:0 0 auto;">{type_tag} {status_badge}</div>
                <div class="content-text" style="flex:1; margin:0 12px;">{content}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns([1, 3, 1, 1])
        with col1:
            new_selection = st.checkbox("选择", value=is_selected, key=f"select_{item_id}", label_visibility="collapsed")
            current_selected = st.session_state.get("selected_items", set())
            if new_selection and item_id not in current_selected:
                current_selected.add(item_id)
            elif not new_selection and item_id in current_selected:
                current_selected.discard(item_id)
            st.session_state["selected_items"] = current_selected

        with col2:
            pass

        with col3:
            pass

        with col4:
            if current_status == "Pending":
                st.markdown('<div class="btn-approve">', unsafe_allow_html=True)
                st.button("通过", key=f"approve_{item_id}", help="标记为通过", on_click=handle_single_action, args=(item_id, "Approved"))
                st.markdown('</div>', unsafe_allow_html=True)
            elif current_status == "Approved":
                st.markdown('<div class="btn-reject">', unsafe_allow_html=True)
                st.button("拒绝", key=f"reject_{item_id}", help="标记为拒绝", on_click=handle_single_action, args=(item_id, "Rejected"))
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="btn-restore">', unsafe_allow_html=True)
                st.button("恢复", key=f"restore_{item_id}", help="恢复为待审核", on_click=handle_single_action, args=(item_id, "Pending"))
                st.markdown('</div>', unsafe_allow_html=True)

    selected_count = len(st.session_state.get("selected_items", set()))

    if selected_count > 0:
        st.markdown(f"""
        <div class="batch-bar">
            <div style="display:flex; align-items:center; justify-content:space-between;">
                <span style="font-weight:600; font-size:15px;">已选择 <span style="color:#3b82f6;">{selected_count}</span> 项</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        bc1, bc2, bc3 = st.columns([1, 1, 2])
        with bc1:
            st.markdown('<div class="btn-batch-approve">', unsafe_allow_html=True)
            st.button(f"✅ 批量通过 ({selected_count})", use_container_width=True, on_click=handle_batch_action, args=("Approved",))
            st.markdown('</div>', unsafe_allow_html=True)
        with bc2:
            st.markdown('<div class="btn-batch-reject">', unsafe_allow_html=True)
            st.button(f"❌ 批量拒绝 ({selected_count})", use_container_width=True, on_click=handle_batch_action, args=("Rejected",))
            st.markdown('</div>', unsafe_allow_html=True)
        with bc3:
            if st.session_state.get("excel_path"):
                with open(st.session_state["excel_path"], "rb") as f:
                    st.download_button("📥 下载Excel", f, file_name=st.session_state["excel_path"].split("/")[-1].split("\\")[-1], use_container_width=True)
