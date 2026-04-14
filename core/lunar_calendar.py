"""
不认命 App - 万年历与农历转换
"""
from lunar_python import Solar, Lunar
from datetime import datetime
from typing import Dict


def solar_to_lunar(year: int, month: int, day: int, hour: int = 0) -> Dict:
    """
    阳历转农历
    
    Args:
        year: 阳历年
        month: 阳历月
        day: 阳历日
        hour: 时辰（0-23）
    
    Returns:
        农历信息字典
    """
    # 创建阳历对象
    solar_obj = Solar.fromYmdHms(year, month, day, hour, 0, 0)
    
    # 转农历
    lunar_obj = solar_obj.getLunar()
    
    # 获取八字
    ba_zi = lunar_obj.getEightChar()
    
    return {
        "solar": {
            "year": year,
            "month": month,
            "day": day,
            "hour": hour,
            "weekday": solar_obj.getWeekInChinese(),
            "date_str": f"{year}年{month}月{day}日"
        },
        "lunar": {
            "year": lunar_obj.getYear(),
            "month": lunar_obj.getMonth(),
            "day": lunar_obj.getDay(),
            "year_gan_zhi": lunar_obj.getYearInGanZhi(),
            "month_gan_zhi": lunar_obj.getMonthInGanZhi(),
            "day_gan_zhi": lunar_obj.getDayInGanZhi(),
            "hour_gan_zhi": ba_zi.getTime(),
            "month_leap": False,  # lunar_obj.isLeap() if needed
            "date_str": lunar_obj.toString(),
            "full_str": f"{lunar_obj.getYearInGanZhi()}年 {lunar_obj.getMonthInGanZhi()}月 {lunar_obj.getDayInGanZhi()}日"
        },
        "bazi": {
            "year": ba_zi.getYear(),
            "month": ba_zi.getMonth(),
            "day": ba_zi.getDay(),
            "hour": ba_zi.getTime(),
            "full": f"{ba_zi.getYear()} {ba_zi.getMonth()} {ba_zi.getDay()} {ba_zi.getTime()}"
        },
        "wuxing": {
            "year": ba_zi.getYearWuXing(),
            "month": ba_zi.getMonthWuXing(),
            "day": ba_zi.getDayWuXing(),
            "hour": ba_zi.getTimeWuXing()
        },
        "shengxiao": lunar_obj.getYearShengXiao(),
        "jieqi": lunar_obj.getJieQi()
    }


def lunar_to_solar(year: int, month: int, day: int, is_leap_month: bool = False) -> Dict:
    """
    农历转阳历
    
    Args:
        year: 农历年
        month: 农历月
        day: 农历日
        is_leap_month: 是否闰月
    
    Returns:
        阳历信息字典
    """
    # 创建农历对象
    lunar_obj = Lunar.fromYmd(year, month, day)
    
    # 转阳历
    solar_obj = lunar_obj.getSolar()
    
    return {
        "lunar": {
            "year": year,
            "month": month,
            "day": day,
            "is_leap": is_leap_month,
            "date_str": f"{year}年{month}月{day}日"
        },
        "solar": {
            "year": solar_obj.getYear(),
            "month": solar_obj.getMonth(),
            "day": solar_obj.getDay(),
            "weekday": solar_obj.getWeekInChinese(),
            "date_str": f"{solar_obj.getYear()}年{solar_obj.getMonth()}月{solar_obj.getDay()}日"
        }
    }


def get_today_info() -> Dict:
    """
    获取今日信息
    
    Returns:
        今日阴阳历信息
    """
    now = datetime.now()
    return solar_to_lunar(now.year, now.month, now.day, now.hour)


def get_zodiac(year: int) -> str:
    """
    获取生肖
    
    Args:
        year: 年份
    
    Returns:
        生肖
    """
    zodiacs = ["鼠", "牛", "虎", "兔", "龙", "蛇", "马", "羊", "猴", "鸡", "狗", "猪"]
    return zodiacs[(year - 4) % 12]
