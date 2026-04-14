#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
不认命 App - 八字计算与寺庙匹配算法
功能：根据生辰八字计算五行，匹配适合的寺庙
创建时间：2026-04-14
"""

import json
from datetime import datetime
from typing import Dict, List, Tuple

# ========== 基础数据 ==========

# 天干
TIANGAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]

# 地支
DIZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

# 天干五行
TIANGAN_WUXING = {
    "甲": "木", "乙": "木",
    "丙": "火", "丁": "火",
    "戊": "土", "己": "土",
    "庚": "金", "辛": "金",
    "壬": "水", "癸": "水"
}

# 地支五行
DIZHI_WUXING = {
    "子": "水",
    "丑": "土", "寅": "木", "卯": "木",
    "辰": "土", "巳": "火", "午": "火",
    "未": "土", "申": "金", "酉": "金",
    "戌": "土", "亥": "水"
}

# 五行相生
WUXING_SHENG = {
    "木": "火",
    "火": "土",
    "土": "金",
    "金": "水",
    "水": "木"
}

# 五行相克
WUXING_KE = {
    "木": "土",
    "土": "水",
    "水": "火",
    "火": "金",
    "金": "木"
}

# 五行喜用神推荐
XISHEN_RECOMMEND = {
    "木": {
        "temples": ["佛教", "道教"],
        "directions": ["东方", "东南方"],
        "colors": ["绿色", "青色"],
        "deities": ["观音菩萨", "文殊菩萨", "文昌帝君"]
    },
    "火": {
        "temples": ["佛教", "道教", "民间信仰"],
        "directions": ["南方"],
        "colors": ["红色", "紫色"],
        "deities": ["关帝", "财神", "观音菩萨"]
    },
    "土": {
        "temples": ["佛教", "道教", "祠堂"],
        "directions": ["中央", "西南", "东北"],
        "colors": ["黄色", "棕色"],
        "deities": ["土地公", "城隍爷", "祖先"]
    },
    "金": {
        "temples": ["佛教", "道教", "儒教"],
        "directions": ["西方", "西北方"],
        "colors": ["白色", "金色"],
        "deities": ["释迦牟尼佛", "孔子", "财神"]
    },
    "水": {
        "temples": ["佛教", "道教", "民间信仰"],
        "directions": ["北方"],
        "colors": ["黑色", "蓝色"],
        "deities": ["观音菩萨", "妈祖", "龙王"]
    }
}


# ========== 八字计算 ==========

def get_year_ganzhi(year: int) -> Tuple[str, str]:
    """获取年柱（天干地支）"""
    # 天干：年份尾数对应
    tiangan_idx = year % 10
    # 地支：(年份 - 4) % 12
    dizhi_idx = (year - 4) % 12
    
    return TIANGAN[tiangan_idx], DIZHI[dizhi_idx]


def get_month_ganzhi(year: int, month: int) -> Tuple[str, str]:
    """获取月柱（简化版，按节气划分）"""
    # 月地支固定：寅月（立春 - 惊蛰）、卯月（惊蛰 - 清明）等
    # 简化处理：1 月寅、2 月卯、3 月辰...
    dizhi_idx = (month + 2) % 12
    dizhi = DIZHI[dizhi_idx]
    
    # 月天干根据年天干推算（五虎遁）
    tiangan_map = {
        "甲": 2, "己": 2,  # 甲己之年丙作首
        "乙": 4, "庚": 4,  # 乙庚之岁戊为头
        "丙": 6, "辛": 6,  # 丙辛必定寻庚起
        "丁": 8, "壬": 8,  # 丁壬壬位顺行流
        "戊": 0, "癸": 0   # 若问戊癸何方发，甲寅之上好追求
    }
    
    year_tiangan, _ = get_year_ganzhi(year)
    start_idx = tiangan_map.get(year_tiangan, 0)
    tiangan_idx = (start_idx + month - 1) % 10
    
    return TIANGAN[tiangan_idx], dizhi


def get_day_ganzhi(year: int, month: int, day: int) -> Tuple[str, str]:
    """获取日柱（简化计算）"""
    # 实际应用中应使用专业历法库（如 lunar_python）
    # 这里使用简化算法
    base_date = datetime(2000, 1, 1)
    target_date = datetime(year, month, day)
    days_diff = (target_date - base_date).days
    
    # 60 甲子循环
    ganzhi_idx = days_diff % 60
    
    tiangan_idx = ganzhi_idx % 10
    dizhi_idx = ganzhi_idx % 12
    
    return TIANGAN[tiangan_idx], DIZHI[dizhi_idx]


def get_hour_ganzhi(hour: int, day: int = None) -> Tuple[str, str]:
    """获取时柱（简化版）"""
    # 时辰地支：子时（23-1 点）、丑时（1-3 点）等
    hour_dizhi_idx = ((hour + 1) % 24) // 2
    dizhi = DIZHI[hour_dizhi_idx]
    
    # 时天干根据日天干推算（五鼠遁）
    # 简化处理，假设日天干为甲
    tiangan_idx = (hour_dizhi_idx * 2) % 10
    tiangan = TIANGAN[tiangan_idx]
    
    return tiangan, dizhi


def calculate_bazi(year: int, month: int, day: int, hour: int) -> Dict:
    """
    计算八字
    
    Args:
        year: 出生年份（公历）
        month: 出生月份（公历）
        day: 出生日期（公历）
        hour: 出生时辰（24 小时制）
    
    Returns:
        八字信息字典
    """
    # 获取四柱
    year_tiangan, year_dizhi = get_year_ganzhi(year)
    month_tiangan, month_dizhi = get_month_ganzhi(year, month)
    day_tiangan, day_dizhi = get_day_ganzhi(year, month, day)
    hour_tiangan, hour_dizhi = get_hour_ganzhi(hour, day)
    
    # 八字
    bazi = {
        "year": f"{year_tiangan}{year_dizhi}",
        "month": f"{month_tiangan}{month_dizhi}",
        "day": f"{day_tiangan}{day_dizhi}",
        "hour": f"{hour_tiangan}{hour_dizhi}",
        "full": f"{year_tiangan}{year_dizhi} {month_tiangan}{month_dizhi} {day_tiangan}{day_dizhi} {hour_tiangan}{hour_dizhi}"
    }
    
    # 五行统计
    wuxing_list = [
        TIANGAN_WUXING[year_tiangan],
        TIANGAN_WUXING[month_tiangan],
        TIANGAN_WUXING[day_tiangan],
        TIANGAN_WUXING[hour_tiangan],
        DIZHI_WUXING[year_dizhi],
        DIZHI_WUXING[month_dizhi],
        DIZHI_WUXING[day_dizhi],
        DIZHI_WUXING[hour_dizhi]
    ]
    
    wuxing_count = {
        "木": wuxing_list.count("木"),
        "火": wuxing_list.count("火"),
        "土": wuxing_list.count("土"),
        "金": wuxing_list.count("金"),
        "水": wuxing_list.count("水")
    }
    
    # 日主（日干）
    day_master = day_tiangan
    day_master_wuxing = TIANGAN_WUXING[day_tiangan]
    
    # 五行强弱分析
    strong_wuxing = max(wuxing_count, key=wuxing_count.get)
    weak_wuxing = min(wuxing_count, key=wuxing_count.get)
    
    # 喜用神（简化：取最弱的五行为喜用）
    xishen = weak_wuxing
    
    return {
        "bazi": bazi,
        "wuxing": wuxing_count,
        "day_master": day_master,
        "day_master_wuxing": day_master_wuxing,
        "strong_wuxing": strong_wuxing,
        "weak_wuxing": weak_wuxing,
        "xishen": xishen
    }


# ========== 寺庙匹配算法 ==========

def calculate_temple_score(temple: Dict, user_bazi: Dict) -> float:
    """
    计算寺庙匹配分数
    
    Args:
        temple: 寺庙信息
        user_bazi: 用户八字信息
    
    Returns:
        匹配分数（0-100）
    """
    score = 50.0  # 基础分
    
    xishen = user_bazi.get("xishen", "")
    temple_type = temple.get("temple_type", "")
    main_deity = temple.get("main_deity", "")
    prayer_directions = temple.get("prayer_directions", [])
    rating = temple.get("rating", 4.0)
    
    # 1. 五行匹配（最高 20 分）
    if xishen in XISHEN_RECOMMEND:
        recommend = XISHEN_RECOMMEND[xishen]
        
        # 寺庙类型匹配
        for rec_temple in recommend["temples"]:
            if rec_temple in temple_type:
                score += 15
                break
        
        # 神祇匹配
        for rec_deity in recommend["deities"]:
            if rec_deity in main_deity:
                score += 10
                break
    
    # 2. 评分加成（最高 10 分）
    if rating >= 4.8:
        score += 10
    elif rating >= 4.5:
        score += 7
    elif rating >= 4.0:
        score += 5
    
    # 3. 祈福方向匹配（最高 10 分）
    # 根据五行推荐祈福方向
    prayer_map = {
        "木": ["求学业", "求智慧", "求事业"],
        "火": ["求财运", "求事业", "求平安"],
        "土": ["求健康", "求平安", "求家庭"],
        "金": ["求事业", "求财运", "求学业"],
        "水": ["求平安", "求健康", "求姻缘"]
    }
    
    if xishen in prayer_map:
        for prayer in prayer_map[xishen]:
            if prayer in prayer_directions:
                score += 5
                break
    
    # 4. 著名寺庙加成（最高 10 分）
    if temple.get("is_famous", False):
        score += 10
    
    # 5. 数据等级加成（最高 10 分）
    data_level = temple.get("data_level", "basic")
    if data_level == "premium":
        score += 10
    elif data_level == "standard":
        score += 5
    
    return min(score, 100.0)


def match_temples(temples: List[Dict], user_bazi: Dict, top_n: int = 10) -> List[Dict]:
    """
    为用户匹配最适合的寺庙
    
    Args:
        temples: 寺庙列表
        user_bazi: 用户八字信息
        top_n: 返回前 N 个匹配结果
    
    Returns:
        匹配结果列表（按分数排序）
    """
    scored_temples = []
    
    for temple in temples:
        score = calculate_temple_score(temple, user_bazi)
        temple_with_score = temple.copy()
        temple_with_score["match_score"] = score
        scored_temples.append(temple_with_score)
    
    # 按分数降序排序
    scored_temples.sort(key=lambda x: x["match_score"], reverse=True)
    
    return scored_temples[:top_n]


def generate_recommendation(user_bazi: Dict, matched_temples: List[Dict]) -> Dict:
    """
    生成推荐说明
    
    Args:
        user_bazi: 用户八字信息
        matched_temples: 匹配的寺庙列表
    
    Returns:
        推荐说明字典
    """
    xishen = user_bazi.get("xishen", "")
    day_master = user_bazi.get("day_master", "")
    
    recommendation = {
        "day_master": f"日主：{day_master}（{TIANGAN_WUXING.get(day_master, '')}）",
        "xishen": f"喜用神：{xishen}",
        "analysis": f"五行中{xishen}较弱，宜补{xishen}",
        "temples_recommendation": [],
        "prayer_advice": []
    }
    
    # 寺庙推荐
    for i, temple in enumerate(matched_temples[:5], 1):
        recommendation["temples_recommendation"].append({
            "rank": i,
            "name": temple.get("name", ""),
            "score": temple.get("match_score", 0),
            "type": temple.get("temple_type", ""),
            "location": temple.get("location", "")
        })
    
    # 祈福建议
    if xishen in XISHEN_RECOMMEND:
        rec = XISHEN_RECOMMEND[xishen]
        recommendation["prayer_advice"] = [
            f"宜往{', '.join(rec['directions'])}方位参拜",
            f"宜穿{', '.join(rec['colors'])}色衣物",
            f"宜拜{', '.join(rec['deities'])}"
        ]
    
    return recommendation


# ========== 主流程 ==========

def main():
    print("🔮 不认命 App - 八字计算与寺庙匹配算法")
    print("=" * 60)
    
    # 示例：测试用户
    print("\n📝 测试用户信息:")
    test_user = {
        "name": "海哥",
        "birth_year": 1990,
        "birth_month": 5,
        "birth_day": 15,
        "birth_hour": 10
    }
    
    print(f"  姓名：{test_user['name']}")
    print(f"  生日：{test_user['birth_year']}年{test_user['birth_month']}月{test_user['birth_day']}日")
    print(f"  时辰：{test_user['birth_hour']}点")
    
    # 计算八字
    print("\n🔮 计算八字...")
    bazi_result = calculate_bazi(
        test_user["birth_year"],
        test_user["birth_month"],
        test_user["birth_day"],
        test_user["birth_hour"]
    )
    
    print(f"  八字：{bazi_result['bazi']['full']}")
    print(f"  日主：{bazi_result['day_master']}（{bazi_result['day_master_wuxing']}）")
    print(f"  五行统计:")
    for wuxing, count in bazi_result['wuxing'].items():
        print(f"    {wuxing}: {count}")
    print(f"  喜用神：{bazi_result['xishen']}")
    
    # 加载寺庙数据
    print("\n📖 加载寺庙数据...")
    with open("/Users/apple/.openclaw/workspace/program-shrimp/temples_with_history.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    temples = data.get("temples", [])
    print(f"  ✅ 加载寺庙：{len(temples)} 座")
    
    # 匹配寺庙
    print("\n🎯 开始匹配寺庙...")
    matched = match_temples(temples, bazi_result, top_n=10)
    
    print(f"\n🏆 匹配结果 Top 10:")
    for i, temple in enumerate(matched, 1):
        print(f"  {i}. {temple['name']} - {temple['match_score']:.1f}分")
        print(f"     类型：{temple['temple_type']}")
        print(f"     位置：{temple['location']}")
        print(f"     主祀：{temple.get('main_deity', '未知')}")
    
    # 生成推荐
    print("\n📋 生成推荐说明...")
    recommendation = generate_recommendation(bazi_result, matched)
    
    print(f"\n  {recommendation['day_master']}")
    print(f"  {recommendation['xishen']}")
    print(f"  {recommendation['analysis']}")
    print(f"\n  祈福建议:")
    for advice in recommendation['prayer_advice']:
        print(f"    - {advice}")
    
    print("\n" + "=" * 60)
    print("✅ 算法测试完成！")
    
    # 保存测试结果
    output = {
        "user": test_user,
        "bazi": bazi_result,
        "matched_temples": matched,
        "recommendation": recommendation,
        "test_time": datetime.now().isoformat()
    }
    
    with open("/Users/apple/.openclaw/workspace/burenmng/test_bazi_match.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"💾 测试结果已保存：/Users/apple/.openclaw/workspace/burenmng/test_bazi_match.json")


if __name__ == "__main__":
    main()
