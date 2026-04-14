#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
不认命 App - 寺庙数据清洗脚本
功能：筛选真正的宗教场所，去除公园、酒店等假数据
创建时间：2026-04-14
"""

import json
from datetime import datetime

# 输入输出文件
INPUT_FILE = "/Users/apple/.openclaw/workspace/program-shrimp/temples_amap_raw.json"
OUTPUT_FILE = "/Users/apple/.openclaw/workspace/program-shrimp/temples_cleaned.json"

# 需要排除的关键词（非宗教场所）
EXCLUDE_KEYWORDS = [
    # 住宿餐饮
    "酒店", "宾馆", "旅馆", "客栈", "民宿", "公寓", "招待所",
    "餐厅", "饭店", "酒楼", "餐馆", "咖啡", "奶茶", "酒吧",
    
    # 购物
    "商场", "超市", "市场", "商店", "店铺", "购物", "广场",
    
    # 娱乐
    "KTV", "网吧", "游戏", "影院", "电影院", "剧场", "公园", "乐园",
    "景区", "风景区", "动物园", "植物园", "游乐场",
    
    # 教育
    "学校", "幼儿园", "学院", "大学", "中学", "小学", "培训",
    
    # 医疗
    "医院", "诊所", "药店", "药房", "卫生", "医疗",
    
    # 交通
    "地铁", "车站", "机场", "港口", "码头", "停车场",
    
    # 金融
    "银行", "信用社", "证券", "保险", "ATM",
    
    # 政府机构
    "政府", "公安局", "派出所", "法院", "检察院", "税务", "工商",
    "街道办", "居委会", "村委会",
    
    # 公司企业
    "公司", "企业", "工厂", "园区", "写字楼", "大厦", "中心",
    
    # 其他
    "小区", "社区", "家园", "花园", "新村", "别墅",
    "健身", "美容", "美发", "洗浴", "桑拿", "按摩",
    "快递", "物流", "仓库", "建材", "汽车", "4S"
]

# 需要保留的关键词（宗教相关）
INCLUDE_KEYWORDS = [
    "寺", "庙", "观", "宫", "庵", "祠", "堂", "院",
    "佛", "菩萨", "观音", "如来", "罗汉", "佛陀",
    "道", "道教", "道士", "真人", "天尊",
    "清真", "伊斯兰", "穆斯林", "安拉",
    "天主", "基督", "教堂", "礼拜", "牧师",
    "文庙", "孔庙", "学宫", "书院",
    "城隍", "土地", "财神", "关帝", "妈祖", "天后",
    "冼太", "冼夫人", "龙王", "药王", "月老",
    "塔", "阁", "殿", "龛", "窟", "石窟",
    "僧", "尼", "和尚", "喇嘛", "活佛"
]

# 宗教类型分类
RELIGION_MAP = {
    "佛教": ["寺", "庙", "庵", "院", "佛", "菩萨", "观音", "如来", "罗汉", "僧", "尼", "和尚", "喇嘛", "活佛"],
    "道教": ["观", "宫", "道", "道士", "真人", "天尊", "阁", "殿"],
    "伊斯兰教": ["清真", "伊斯兰", "穆斯林", "安拉"],
    "基督教": ["天主", "基督", "教堂", "礼拜", "牧师"],
    "儒教": ["文庙", "孔庙", "学宫", "书院", "孔子"],
    "民间信仰": ["城隍", "土地", "财神", "关帝", "妈祖", "天后", "冼太", "冼夫人", "龙王", "药王", "月老", "祠", "堂", "塔", "龛", "窟", "石窟"]
}


def should_exclude(name):
    """检查是否应该排除"""
    name_upper = name.upper()
    for keyword in EXCLUDE_KEYWORDS:
        if keyword.upper() in name_upper:
            return True
    return False


def should_include(name):
    """检查是否应该保留"""
    for keyword in INCLUDE_KEYWORDS:
        if keyword in name:
            return True
    return False


def classify_religion(name, temple_type=""):
    """分类宗教类型"""
    # 先检查已有分类
    if temple_type:
        return temple_type
    
    # 根据名称分类
    for religion, keywords in RELIGION_MAP.items():
        for keyword in keywords:
            if keyword in name:
                return religion
    
    return "其他"


def clean_data():
    """主清洗流程"""
    print("🧹 开始清洗寺庙数据...")
    print(f"📂 输入文件：{INPUT_FILE}")
    print(f"📂 输出文件：{OUTPUT_FILE}")
    print("-" * 50)
    
    # 读取数据
    print("📖 读取原始数据...")
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    original_count = data.get("total", len(data.get("temples", [])))
    print(f"✅ 原始数据：{original_count} 条")
    
    # 清洗数据
    print("🔍 开始筛选...")
    cleaned_temples = []
    excluded_count = 0
    excluded_reasons = {}
    
    for temple in data.get("temples", []):
        name = temple.get("name", "")
        
        # 1. 检查是否应该排除
        if should_exclude(name):
            excluded_count += 1
            # 记录排除原因
            for keyword in EXCLUDE_KEYWORDS:
                if keyword.upper() in name.upper():
                    reason = keyword
                    excluded_reasons[reason] = excluded_reasons.get(reason, 0) + 1
                    break
            continue
        
        # 2. 检查是否应该保留（有宗教关键词）
        if not should_include(name):
            excluded_count += 1
            reason = "无宗教关键词"
            excluded_reasons[reason] = excluded_reasons.get(reason, 0) + 1
            continue
        
        # 3. 清洗和标准化数据
        cleaned_temple = {
            "name": name,
            "location": temple.get("location", ""),
            "latitude": temple.get("latitude"),
            "longitude": temple.get("longitude"),
            "city": temple.get("city", ""),
            "province": temple.get("province", "") or get_province_from_city(temple.get("city", "")),
            "district": temple.get("district", ""),
            "temple_type": classify_religion(name, temple.get("temple_type", "")),
            "telephone": temple.get("telephone", "") if temple.get("telephone") and not isinstance(temple.get("telephone"), list) else "",
            "source": "高德地图",
            "crawl_time": temple.get("crawl_time", ""),
            "tags": temple.get("tags", []),
            "data_level": "standard"  # 数据等级：standard（标准）
        }
        
        cleaned_temples.append(cleaned_temple)
    
    # 统计
    print(f"✅ 清洗后：{len(cleaned_temples)} 条")
    print(f"❌ 已排除：{excluded_count} 条")
    print(f"📊 保留率：{len(cleaned_temples)/original_count*100:.1f}%")
    
    # 显示排除原因 Top 10
    if excluded_reasons:
        print("\n🗑️  排除原因 Top 10:")
        sorted_reasons = sorted(excluded_reasons.items(), key=lambda x: x[1], reverse=True)[:10]
        for reason, count in sorted_reasons:
            print(f"   - {reason}: {count} 条")
    
    # 统计宗教类型分布
    print("\n📊 宗教类型分布:")
    religion_count = {}
    for temple in cleaned_temples:
        religion = temple.get("temple_type", "其他")
        religion_count[religion] = religion_count.get(religion, 0) + 1
    
    for religion, count in sorted(religion_count.items(), key=lambda x: x[1], reverse=True):
        print(f"   - {religion}: {count} 座 ({count/len(cleaned_temples)*100:.1f}%)")
    
    # 统计城市分布 Top 10
    print("\n🏙️  城市分布 Top 10:")
    city_count = {}
    for temple in cleaned_temples:
        city = temple.get("city", "未知")
        city_count[city] = city_count.get(city, 0) + 1
    
    for city, count in sorted(city_count.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"   - {city}: {count} 座")
    
    # 保存结果
    print(f"\n💾 保存清洗后的数据...")
    output_data = {
        "total": len(cleaned_temples),
        "original_total": original_count,
        "excluded_count": excluded_count,
        "crawl_time": datetime.now().isoformat(),
        "source": "高德地图 API（已清洗）",
        "temples": cleaned_temples
    }
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 数据已保存至：{OUTPUT_FILE}")
    print(f"📊 文件大小：{len(json.dumps(output_data, ensure_ascii=False))/1024/1024:.2f} MB")
    print("\n🎉 清洗完成！")


def get_province_from_city(city):
    """根据城市名推断省份"""
    province_map = {
        "北京": "北京市", "上海": "上海市", "天津": "天津市", "重庆": "重庆市",
        "南京": "江苏省", "杭州": "浙江省", "成都": "四川省", "武汉": "湖北省",
        "西安": "陕西省", "苏州": "江苏省", "郑州": "河南省", "长沙": "湖南省",
        "沈阳": "辽宁省", "青岛": "山东省", "宁波": "浙江省", "昆明": "云南省",
        "福州": "福建省", "厦门": "福建省", "合肥": "安徽省", "南昌": "江西省",
        "贵阳": "贵州省", "南宁": "广西壮族自治区", "石家庄": "河北省",
        "太原": "山西省", "呼和浩特": "内蒙古自治区", "长春": "吉林省",
        "哈尔滨": "黑龙江省", "济南": "山东省", "海口": "海南省",
        "拉萨": "西藏自治区", "西宁": "青海省", "银川": "宁夏回族自治区",
        "乌鲁木齐": "新疆维吾尔自治区", "香港": "香港特别行政区",
        "澳门": "澳门特别行政区", "台北": "台湾省"
    }
    return province_map.get(city, "")


if __name__ == "__main__":
    clean_data()
