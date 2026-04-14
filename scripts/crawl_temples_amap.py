#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
不认命 App - 寺庙数据批量获取脚本
数据源：高德地图 API
创建时间：2026-04-14
"""

import requests
import json
import time
from datetime import datetime

# ========== 配置区域 ==========
# 需要替换为你的高德 API Key
# 注册地址：https://lbs.amap.com/
AMAP_API_KEY = "a05aeef67f77dd2c50fd310f0c8449ff"  # 海哥的新 Key

# 输出文件
OUTPUT_FILE = "temples_amap_raw.json"

# 搜索关键词
KEYWORDS = [
    "寺庙",
    "寺院", 
    "佛教",
    "道观",
    "道教",
    "清真寺",
    "伊斯兰",
    "文庙",
    "孔庙",
    "城隍庙",
    "祠堂",
    "妈祖庙",
    "天后宫",
    "关帝庙",
    "观音庙",
    "龙王庙",
    "财神庙",
    "月老庙",
    "药王庙",
    "冼太庙"
]

# 重点城市（全部 38 个）
CITIES = [
    "北京", "上海", "广州", "深圳", "天津", "重庆",
    "南京", "杭州", "成都", "武汉", "西安", "苏州",
    "郑州", "长沙", "沈阳", "青岛", "宁波", "昆明",
    "福州", "厦门", "合肥", "南昌", "贵阳", "南宁",
    "石家庄", "太原", "呼和浩特", "长春", "哈尔滨",
    "济南", "海口", "拉萨", "西宁", "银川", "乌鲁木齐",
    "香港", "澳门", "台北"
]

# ========== API 调用函数 ==========

def search_places(keyword, city, page=1, offset=25):
    """
    搜索 POI 数据
    https://lbs.amap.com/api/webservice/guide/api/search
    """
    url = "https://restapi.amap.com/v3/place/text"
    params = {
        "keywords": keyword,
        "types": "110000",  # 宗教场所
        "city": city,
        "key": AMAP_API_KEY,
        "offset": offset,
        "page": page,
        "extensions": "all"  # 返回详细信息
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        return data
    except Exception as e:
        print(f"❌ 请求失败：{e}")
        return None


def parse_poi(poi, keyword, city):
    """
    解析单个 POI 数据
    """
    return {
        "name": poi.get("name", ""),
        "location": poi.get("address", ""),
        "latitude": float(poi.get("location", ",").split(",")[1]) if poi.get("location") else None,
        "longitude": float(poi.get("location", ",").split(",")[0]) if poi.get("location") else None,
        "city": city,
        "province": poi.get("province", ""),
        "district": poi.get("district", ""),
        "temple_type": categorize_temple(poi.get("name", ""), keyword),
        "rating": None,  # 临时简化
        "telephone": poi.get("tel", ""),
        "source": "高德地图",
        "crawl_time": datetime.now().isoformat(),
        "tags": [keyword]
    }


def categorize_temple(name, keyword):
    """
    根据名称和关键词分类寺庙类型
    """
    if any(x in name for x in ["寺", "佛", "观音", "菩萨"]):
        return "佛教"
    elif any(x in name for x in ["观", "道", "宫", "殿"]):
        return "道教"
    elif any(x in name for x in ["清真", "伊斯兰", "穆斯林"]):
        return "伊斯兰教"
    elif any(x in name for x in ["妈祖", "天后"]):
        return "民间信仰/妈祖"
    elif any(x in name for x in ["关帝", "关公"]):
        return "民间信仰/关帝"
    elif "文庙" in name or "孔庙" in name:
        return "儒教"
    elif "城隍" in name:
        return "道教/民间信仰"
    elif "祠" in name or "堂" in name:
        return "祠堂"
    elif "冼太" in name or "冼夫人" in name:
        return "民间信仰/冼太夫人"
    else:
        return "民间信仰"


# ========== 主流程 ==========

def main():
    print("🚀 开始获取寺庙数据...")
    print(f"📍 数据源：高德地图 API")
    print(f"📊 关键词：{len(KEYWORDS)} 个")
    print(f"🏙️  城市：{len(CITIES)} 个")
    print("-" * 50)
    
    all_temples = []
    total_count = 0
    
    for city in CITIES:
        print(f"\n📍 正在搜索：{city}")
        
        for keyword in KEYWORDS:
            # 每个城市 + 关键词组合，获取前 3 页（约 75 条数据）
            for page in range(1, 4):
                data = search_places(keyword, city, page)
                
                if not data or data.get("status") != "1":
                    if data and data.get("info") != "OK":
                        print(f"  ⚠️  {keyword} - {data.get('info', '未知错误')}")
                    break
                
                pois = data.get("pois", [])
                if not pois:
                    break
                
                for poi in pois:
                    temple = parse_poi(poi, keyword, city)
                    if temple["latitude"] and temple["longitude"]:
                        all_temples.append(temple)
                        total_count += 1
                
                # 控制频率，避免触发限流
                time.sleep(0.2)
            
            # 每完成一个关键词，休息一下
            time.sleep(0.5)
        
        print(f"  ✅ {city} 完成，当前累计：{total_count} 座")
        
        # 每完成一个城市，保存一次进度
        save_progress(all_temples)
    
    # 最终保存
    save_progress(all_temples)
    print(f"\n🎉 全部完成！共获取 {total_count} 座寺庙")
    print(f"💾 数据已保存至：{OUTPUT_FILE}")


def save_progress(temples):
    """保存进度"""
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump({
            "total": len(temples),
            "crawl_time": datetime.now().isoformat(),
            "source": "高德地图 API",
            "temples": temples
        }, f, ensure_ascii=False, indent=2)
    print(f"  💾 已保存进度：{len(temples)} 座")


if __name__ == "__main__":
    # 检查 API Key
    if AMAP_API_KEY == "你的高德 API Key":
        print("❌ 请先配置高德 API Key！")
        print("📝 注册地址：https://lbs.amap.com/")
        print("📖 配置方法：")
        print("   1. 注册高德开放平台账号")
        print("   2. 创建应用（选择 Web 服务）")
        print("   3. 获取 Key 并替换脚本中的 AMAP_API_KEY")
        exit(1)
    
    main()
