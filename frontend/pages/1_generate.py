import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st
from frontend.api_client import api_generate
from frontend.components.stat_cards import render_stat_cards
from frontend.components.sidebar import render_sidebar

st.set_page_config(page_title="内容生成", page_icon="📝", layout="wide")
render_sidebar()

st.markdown("## 📝 内容生成")
st.markdown("输入商品信息，AI自动生成运营内容")

col1, col2, col3 = st.columns([2, 1, 2])
with col1:
    product_name = st.text_input("商品名称", placeholder="例如：降噪耳机", key="gen_name")
with col2:
    region = st.text_input("目标地区", placeholder="例如：US", key="gen_region")
with col3:
    product_feature = st.text_input("商品特点", placeholder="例如：续航长、主动降噪", key="gen_feature")

col1, col2 = st.columns(2)
with col1:
    platform = st.selectbox("目标平台", ["amazon", "ebay", "shopify"], key="gen_platform")
with col2:
    provider = st.selectbox("AI模型", ["minimax", "openai", "ollama"], key="gen_provider")

content_types = st.multiselect(
    "生成内容类型",
    ["title", "seo", "description"],
    default=["title", "seo"],
    format_func=lambda x: {"title": "商品标题", "seo": "SEO关键词", "description": "商品描述"}[x],
)

if st.button("🚀 一键生成运营内容", use_container_width=True, type="primary"):
    if not product_name or not product_feature:
        st.warning("请填写商品名称和特点")
    elif not content_types:
        st.warning("请至少选择一种内容类型")
    else:
        product = {
            "name": product_name,
            "feature": product_feature,
            "region": region or "US",
            "platform": platform,
        }
        with st.spinner(f"AI正在生成内容（{provider}）..."):
            result = api_generate(product, content_types, provider)
        if result:
            st.session_state["last_result"] = result
            st.success(f"生成成功！共 {len(result['items'])} 项内容")
            st.balloons()

if "last_result" in st.session_state:
    result = st.session_state["last_result"]
    st.markdown(f"**批次ID**: `{result['batch_id']}` | **模型**: {result['provider']} | **时间**: {result['created_at']}")
    st.markdown("---")

    type_labels = {"Title": "商品标题", "SEO Keyword": "SEO关键词", "Description": "商品描述"}
    type_tags = {"Title": "tag-title", "SEO Keyword": "tag-seo", "Description": "tag-desc"}

    for item in result["items"]:
        tag_class = type_tags.get(item["item_type"], "tag-title")
        label = type_labels.get(item["item_type"], item["item_type"])
        st.markdown(f"""
        <div class="review-row" style="border-left:3px solid #f59e0b;">
            <div style="display:flex;align-items:center;gap:12px;">
                <span class="{tag_class}">{label}</span>
                <span class="badge-pending">⏳ 待审核</span>
                <span class="content-text" style="flex:1;">{item['content']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
