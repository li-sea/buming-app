"""
不认命 App - 寺庙匹配算法
"""
from typing import Dict, List


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


def calculate_temple_score(temple: Dict, user_bazi: Dict) -> float:
    """
    计算寺庙匹配分数
    
    Args:
        temple: 寺庙信息
        user_bazi: 用户八字信息
    
    Returns:
        匹配分数（0-100）
    """
    score = 50.0
    
    xishen = user_bazi.get("xishen", "")
    temple_type = temple.get("temple_type", "")
    main_deity = temple.get("main_deity", "")
    prayer_directions = temple.get("prayer_directions", [])
    rating = temple.get("rating", 4.0)
    
    # 1. 五行匹配（最高 20 分）
    if xishen in XISHEN_RECOMMEND:
        recommend = XISHEN_RECOMMEND[xishen]
        
        for rec_temple in recommend["temples"]:
            if rec_temple in temple_type:
                score += 15
                break
        
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


def match_temples(temples: List[Dict], user_bazi: Dict, limit: int = 10, city: str = None) -> List[Dict]:
    """
    为用户匹配最适合的寺庙
    
    Args:
        temples: 寺庙列表
        user_bazi: 用户八字信息
        limit: 返回数量
        city: 限制城市
    
    Returns:
        匹配结果列表
    """
    scored_temples = []
    
    for temple in temples:
        # 城市过滤
        if city and temple.get("city") != city:
            continue
        
        score = calculate_temple_score(temple, user_bazi)
        temple_with_score = temple.copy()
        temple_with_score["match_score"] = score
        scored_temples.append(temple_with_score)
    
    # 按分数降序排序
    scored_temples.sort(key=lambda x: x["match_score"], reverse=True)
    
    return scored_temples[:limit]


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
    day_master_wuxing = user_bazi.get("day_master_wuxing", "")
    
    recommendation = {
        "day_master": f"日主：{day_master}（{day_master_wuxing}）",
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
