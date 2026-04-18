#!/usr/bin/env python3
"""
自动创建飞书多维表格 - 不认命寺庙数据库
使用飞书开放平台 API
"""

import json
import os
import requests
from datetime import datetime

# 飞书配置
FEISHU_APP_ID = "cli_a9312b92f8fa1bc8"
FEISHU_APP_SECRET = "tYVYXHcUJyOXEKCOjc9kzpSuuz4oA6Sd"

def get_access_token():
    """获取飞书 access token"""
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    payload = {
        "app_id": FEISHU_APP_ID,
        "app_secret": FEISHU_APP_SECRET
    }
    response = requests.post(url, json=payload)
    result = response.json()
    if result.get("code") == 0:
        return result.get("tenant_access_token")
    else:
        print(f"获取 token 失败：{result}")
        return None

def create_bitable(token, title):
    """创建多维表格"""
    url = "https://open.feishu.cn/open-apis/bitable/v1/apps"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "title": title
    }
    response = requests.post(url, headers=headers, json=payload)
    result = response.json()
    if result.get("code") == 0:
        return result.get("data")
    else:
        print(f"创建表格失败：{result}")
        return None

def get_table_id(token, app_token):
    """获取表格 ID"""
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    result = response.json()
    if result.get("code") == 0:
        items = result.get("data", {}).get("items", [])
        if items:
            return items[0].get("table_id")
    return None

def create_fields(token, app_token, table_id, fields):
    """创建字段"""
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/fields"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    for field in fields:
        payload = {
            "field_name": field["name"],
            "field_type": field["type"]
        }
        if "options" in field:
            payload["options"] = field["options"]
        
        response = requests.post(url, headers=headers, json=payload)
        result = response.json()
        if result.get("code") == 0:
            print(f"✅ 创建字段：{field['name']}")
        else:
            print(f"❌ 创建字段失败 {field['name']}: {result}")

def load_temples():
    """加载寺庙数据"""
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
    
    return unique_temples

if __name__ == "__main__":
    print("🔮 不认命 - 飞书多维表格自动创建工具")
    print("=" * 60)
    
    # 获取 token
    print("\n1️⃣ 获取 access token...")
    token = get_access_token()
    if not token:
        print("❌ 获取 token 失败，请检查配置")
        exit(1)
    print("✅ Token 获取成功")
    
    # 创建多维表格
    print("\n2️⃣ 创建多维表格...")
    title = f"不认命 - 寺庙数据库 {datetime.now().strftime('%Y-%m-%d')}"
    bitable = create_bitable(token, title)
    if not bitable:
        print("❌ 创建表格失败")
        exit(1)
    
    app_token = bitable.get("app_token")
    print(f"✅ 表格创建成功：{title}")
    print(f"   App Token: {app_token}")
    print(f"   链接：https://bytedance.feishu.cn/base/{app_token}")
    
    # 获取表格 ID
    print("\n3️⃣ 获取表格 ID...")
    table_id = get_table_id(token, app_token)
    if not table_id:
        print("❌ 获取表格 ID 失败")
        exit(1)
    print(f"✅ Table ID: {table_id}")
    
    # 定义字段
    print("\n4️⃣ 创建字段...")
    fields = [
        {"name": "寺庙名称", "type": 1},  # Text
        {"name": "省份", "type": 3, "options": {"options": [{"name": "北京市"}, {"name": "上海市"}, {"name": "广东省"}]}},  # SingleSelect
        {"name": "城市", "type": 1},  # Text
        {"name": "区县", "type": 1},  # Text
        {"name": "详细地址", "type": 1},  # Text
        {"name": "纬度", "type": 2},  # Number
        {"name": "经度", "type": 2},  # Number
        {"name": "类型", "type": 3},  # SingleSelect
        {"name": "子类型", "type": 3},  # SingleSelect
        {"name": "评级", "type": 2},  # Number
        {"name": "简介", "type": 1},  # Text
        {"name": "历史", "type": 1},  # Text
        {"name": "特色", "type": 4},  # MultiSelect
        {"name": "祈福方向", "type": 4},  # MultiSelect
        {"name": "交通", "type": 1},  # Text
        {"name": "门票", "type": 1},  # Text
        {"name": "开放时间", "type": 1},  # Text
        {"name": "标签", "type": 4},  # MultiSelect
        {"name": "历史典故", "type": 1},  # Text
        {"name": "文化价值", "type": 4},  # MultiSelect
        {"name": "著名人物", "type": 4},  # MultiSelect
        {"name": "建筑特色", "type": 4},  # MultiSelect
        {"name": "诗词典故", "type": 1},  # Text
    ]
    
    create_fields(token, app_token, table_id, fields)
    
    # 加载寺庙数据
    print("\n5️⃣ 加载寺庙数据...")
    temples = load_temples()
    print(f"✅ 加载寺庙数据：{len(temples)}座")
    
    print("\n" + "=" * 60)
    print("✅ 飞书多维表格创建完成！")
    print(f"\n📊 表格信息:")
    print(f"   名称：{title}")
    print(f"   App Token: {app_token}")
    print(f"   Table ID: {table_id}")
    print(f"   链接：https://bytedance.feishu.cn/base/{app_token}")
    print(f"   寺庙数量：{len(temples)}座")
    print(f"   字段数量：{len(fields)}个")
    
    # 保存配置
    config = {
        "app_token": app_token,
        "table_id": table_id,
        "title": title,
        "temples_count": len(temples),
        "fields_count": len(fields),
        "created_at": datetime.now().isoformat()
    }
    
    config_file = os.path.join(os.path.dirname(__file__), "../feishu_bitable_config.json")
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 配置已保存到：{config_file}")
