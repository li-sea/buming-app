#!/usr/bin/env python3
"""
创建飞书多维表格 - 不认命寺庙数据库
"""

import json
import os
import sys

# 飞书配置
FEISHU_APP_ID = "cli_a9312b92f8fa1bc8"
FEISHU_APP_SECRET = "tYVYXHcUJyOXEKCOjc9kzpSuuz4oA6Sd"

def load_temples():
    """加载所有寺庙数据"""
    temples = []
    data_dir = os.path.join(os.path.dirname(__file__), "../data")
    
    for filename in os.listdir(data_dir):
        if filename.endswith(".json") and filename.startswith("temples_"):
            filepath = os.path.join(data_dir, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        temples.extend(data)
                    elif isinstance(data, dict) and 'temples' in data:
                        temples.extend(data['temples'])
            except Exception as e:
                print(f"Error loading {filename}: {e}")
    
    # 去重
    seen = set()
    unique_temples = []
    for temple in temples:
        key = f"{temple.get('name', '')}_{temple.get('province', '')}"
        if key not in seen:
            seen.add(key)
            unique_temples.append(temple)
    
    print(f"Loaded {len(unique_temples)} unique temples")
    return unique_temples

def create_bitable_structure():
    """创建飞书多维表格结构"""
    # 这里应该调用飞书 API 创建多维表格
    # 由于需要实际 API 调用，这里只提供结构定义
    
    table_structure = {
        "name": "不认命 - 寺庙数据库",
        "tables": [
            {
                "name": "寺庙信息",
                "fields": [
                    {"name": "寺庙名称", "type": "text"},
                    {"name": "省份", "type": "single_select"},
                    {"name": "城市", "type": "text"},
                    {"name": "区县", "type": "text"},
                    {"name": "详细地址", "type": "text"},
                    {"name": "纬度", "type": "number"},
                    {"name": "经度", "type": "number"},
                    {"name": "类型", "type": "single_select"},
                    {"name": "子类型", "type": "single_select"},
                    {"name": "评级", "type": "number"},
                    {"name": "简介", "type": "text"},
                    {"name": "历史", "type": "text"},
                    {"name": "特色", "type": "multi_select"},
                    {"name": "祈福方向", "type": "multi_select"},
                    {"name": "交通", "type": "text"},
                    {"name": "门票", "type": "text"},
                    {"name": "开放时间", "type": "text"},
                    {"name": "标签", "type": "multi_select"}
                ]
            },
            {
                "name": "用户数据",
                "fields": [
                    {"name": "用户 ID", "type": "text"},
                    {"name": "姓名", "type": "text"},
                    {"name": "性别", "type": "single_select"},
                    {"name": "出生年月日时", "type": "text"},
                    {"name": "八字", "type": "text"},
                    {"name": "五行分布", "type": "text"},
                    {"name": "最弱五行", "type": "single_select"},
                    {"name": "喜用神", "type": "text"},
                    {"name": "推荐寺庙", "type": "text"},
                    {"name": "推荐法器", "type": "text"},
                    {"name": "创建时间", "type": "datetime"}
                ]
            },
            {
                "name": "法器商品",
                "fields": [
                    {"name": "法器名称", "type": "text"},
                    {"name": "五行属性", "type": "single_select"},
                    {"name": "描述", "type": "text"},
                    {"name": "价格范围", "type": "text"},
                    {"name": "淘宝链接", "type": "url"},
                    {"name": "图片", "type": "attachment"},
                    {"name": "佣金比例", "type": "number"},
                    {"name": "状态", "type": "single_select"}
                ]
            }
        ]
    }
    
    return table_structure

if __name__ == "__main__":
    print("🔮 不认命 - 飞书多维表格创建工具")
    print("=" * 50)
    
    # 加载寺庙数据
    temples = load_temples()
    
    # 创建表格结构
    structure = create_bitable_structure()
    
    print(f"\n✅ 寺庙数据加载完成：{len(temples)}座")
    print(f"✅ 表格结构定义完成：{len(structure['tables'])}个表")
    
    print("\n📋 表格结构:")
    for table in structure['tables']:
        print(f"  - {table['name']}: {len(table['fields'])}个字段")
    
    print("\n⚠️  注意：实际创建需要调用飞书 API")
    print("请手动在飞书中创建多维表格，或配置 API 凭证后自动创建")
    
    # 保存结构定义
    output_file = os.path.join(os.path.dirname(__file__), "../feishu_bitable_structure.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(structure, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 结构定义已保存到：{output_file}")
