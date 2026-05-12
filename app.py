from utils.excel_exporter import export_to_excel
from utils.json_parser import parse_json
from services.title_generator import generate_title
from services.seo_generator import generate_keywords
from services.title_generator import regenerate_title
product_info = {
    "name": "Pet Water Fountain",
    "feature": "Ultra Silent, Automatic Circulation",
    "region": "US"
}

title_result = regenerate_title(product_info)
#josn转换为python对象
title_data=parse_json(title_result)

print("生成的标题：")
print(title_data)

seo_keywords = generate_keywords(product_info)
seo_data=parse_json(seo_keywords)

print("生成的SEO关键词：")
print(seo_data)
#导出excel
export_to_excel(title_data, seo_data)