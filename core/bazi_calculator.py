"""
不认命 App - 八字计算核心算法
"""
from datetime import datetime
from typing import Dict, Tuple, List


# ========== 基础数据 ==========

TIANGAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
DIZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

TIANGAN_WUXING = {
    "甲": "木", "乙": "木",
    "丙": "火", "丁": "火",
    "戊": "土", "己": "土",
    "庚": "金", "辛": "金",
    "壬": "水", "癸": "水"
}

DIZHI_WUXING = {
    "子": "水",
    "丑": "土", "寅": "木", "卯": "木",
    "辰": "土", "巳": "火", "午": "火",
    "未": "土", "申": "金", "酉": "金",
    "戌": "土", "亥": "水"
}


def get_year_ganzhi(year: int) -> Tuple[str, str]:
    """获取年柱"""
    tiangan_idx = year % 10
    dizhi_idx = (year - 4) % 12
    return TIANGAN[tiangan_idx], DIZHI[dizhi_idx]


def get_month_ganzhi(year: int, month: int) -> Tuple[str, str]:
    """获取月柱（简化版）"""
    dizhi_idx = (month + 2) % 12
    dizhi = DIZHI[dizhi_idx]
    
    tiangan_map = {
        "甲": 2, "己": 2,
        "乙": 4, "庚": 4,
        "丙": 6, "辛": 6,
        "丁": 8, "壬": 8,
        "戊": 0, "癸": 0
    }
    
    year_tiangan, _ = get_year_ganzhi(year)
    start_idx = tiangan_map.get(year_tiangan, 0)
    tiangan_idx = (start_idx + month - 1) % 10
    
    return TIANGAN[tiangan_idx], dizhi


def get_day_ganzhi(year: int, month: int, day: int) -> Tuple[str, str]:
    """获取日柱（简化计算）"""
    base_date = datetime(2000, 1, 1)
    target_date = datetime(year, month, day)
    days_diff = (target_date - base_date).days
    
    ganzhi_idx = days_diff % 60
    tiangan_idx = ganzhi_idx % 10
    dizhi_idx = ganzhi_idx % 12
    
    return TIANGAN[tiangan_idx], DIZHI[dizhi_idx]


def get_hour_ganzhi(hour: int) -> Tuple[str, str]:
    """获取时柱（简化版）"""
    hour_dizhi_idx = ((hour + 1) % 24) // 2
    dizhi = DIZHI[hour_dizhi_idx]
    tiangan_idx = (hour_dizhi_idx * 2) % 10
    tiangan = TIANGAN[tiangan_idx]
    
    return tiangan, dizhi


def calculate_bazi(year: int, month: int, day: int, hour: int) -> Dict:
    """
    计算八字
    
    Args:
        year: 出生年份（公历）
        month: 出生月份
        day: 出生日期
        hour: 出生时辰（24 小时制）
    
    Returns:
        八字信息字典
    """
    # 获取四柱
    year_tiangan, year_dizhi = get_year_ganzhi(year)
    month_tiangan, month_dizhi = get_month_ganzhi(year, month)
    day_tiangan, day_dizhi = get_day_ganzhi(year, month, day)
    hour_tiangan, hour_dizhi = get_hour_ganzhi(hour)
    
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
    
    # 日主
    day_master = day_tiangan
    day_master_wuxing = TIANGAN_WUXING[day_tiangan]
    
    # 五行强弱
    strong_wuxing = max(wuxing_count, key=wuxing_count.get)
    weak_wuxing = min(wuxing_count, key=wuxing_count.get)
    
    # 喜用神（取最弱的五行）
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
