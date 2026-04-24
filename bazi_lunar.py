"""
不认命 App - 八字计算模块（使用 lunar-python 专业库）
"""

from lunar_python import Lunar, Solar
from typing import Dict, List, Any

# 五行映射
GAN_WUXING = {
    "甲": "木", "乙": "木",
    "丙": "火", "丁": "火",
    "戊": "土", "己": "土",
    "庚": "金", "辛": "金",
    "壬": "水", "癸": "水"
}

ZHI_WUXING = {
    "子": "水",
    "丑": "土",
    "寅": "木",
    "卯": "木",
    "辰": "土",
    "巳": "火",
    "午": "火",
    "未": "土",
    "申": "金",
    "酉": "金",
    "戌": "土",
    "亥": "水"
}

class BaziCalculator:
    """八字计算器 - 专业版"""
    
    def __init__(self):
        pass
    
    def calculate(self, year: int, month: int, day: int, hour: int, minute: int = 0, gender: str = "male") -> Dict[str, Any]:
        """
        计算八字
        
        Args:
            year: 公历年份
            month: 公历月份
            day: 公历日期
            hour: 时辰（0-23）
            minute: 分钟
            gender: 性别（male/female）
        
        Returns:
            八字计算结果
        """
        # 创建阳历对象
        solar = Solar.fromYmdHms(year, month, day, hour, minute, 0)
        
        # 转换为农历
        lunar = solar.getLunar()
        
        # 获取八字
        ba_zi = lunar.getEightChar()
        
        # 年柱、月柱、日柱、时柱
        year_gan = ba_zi.getYearGan()  # 年干
        year_zhi = ba_zi.getYearZhi()  # 年支
        month_gan = ba_zi.getMonthGan()  # 月干
        month_zhi = ba_zi.getMonthZhi()  # 月支
        day_gan = ba_zi.getDayGan()  # 日干
        day_zhi = ba_zi.getDayZhi()  # 日支
        hour_gan = ba_zi.getTimeGan()  # 时干
        hour_zhi = ba_zi.getTimeZhi()  # 时支
        
        # 五行
        wuxing = {
            "年柱": {
                "干": year_gan,
                "支": year_zhi,
                "干五行": GAN_WUXING.get(year_gan, "未知"),
                "支五行": ZHI_WUXING.get(year_zhi, "未知")
            },
            "月柱": {
                "干": month_gan,
                "支": month_zhi,
                "干五行": GAN_WUXING.get(month_gan, "未知"),
                "支五行": ZHI_WUXING.get(month_zhi, "未知")
            },
            "日柱": {
                "干": day_gan,
                "支": day_zhi,
                "干五行": GAN_WUXING.get(day_gan, "未知"),
                "支五行": ZHI_WUXING.get(day_zhi, "未知")
            },
            "时柱": {
                "干": hour_gan,
                "支": hour_zhi,
                "干五行": GAN_WUXING.get(hour_gan, "未知"),
                "支五行": ZHI_WUXING.get(hour_zhi, "未知")
            }
        }
        
        # 统计五行数量
        wuxing_count = {"金": 0, "木": 0, "水": 0, "火": 0, "土": 0}
        for pillar in wuxing.values():
            wuxing_count[pillar["干五行"]] += 1
            wuxing_count[pillar["支五行"]] += 1
        
        # 找出最弱和最强的五行
        weakest = min(wuxing_count, key=wuxing_count.get)
        strongest = max(wuxing_count, key=wuxing_count.get)
        
        # 纳音
        na_yin = {
            "年柱": ba_zi.getYearNaYin(),
            "月柱": ba_zi.getMonthNaYin(),
            "日柱": ba_zi.getDayNaYin(),
            "时柱": ba_zi.getTimeNaYin()
        }
        
        # 生肖
        zodiac = lunar.getYearShengXiao()
        
        # 星座
        constellation = solar.getXingZuo()
        
        # 大运（简化版）
        da_yun = []
        try:
            yun = ba_zi.getYun(1 if gender == "female" else 0)
            for i in range(8):
                da_yun.append({
                    "序号": i + 1,
                    "干支": yun.getGanZhi(i),
                    "起始年龄": yun.getStartYear(i)
                })
        except:
            da_yun = [{"提示": "大运计算需要更详细信息"}]
        
        # 流年（近 10 年）
        current_year = 2026
        liu_nian = []
        for i in range(10):
            year_num = current_year + i
            year_lunar = Solar.fromYmd(year_num, 1, 1).getLunar()
            year_ba_zi = year_lunar.getEightChar()
            liu_nian.append({
                "年份": year_num,
                "干支": f"{year_ba_zi.getYearGan()}{year_ba_zi.getYearZhi()}",
                "生肖": year_lunar.getYearShengXiao()
            })
        
        # 五行喜用神
        xi_yong = self._calculate_xi_yong(wuxing_count, weakest, strongest)
        
        # 命卦
        ming_gua = self._calculate_ming_gua(year, gender)
        
        return {
            "基本信息": {
                "公历": f"{year}年{month}月{day}日 {hour}时{minute}分",
                "农历": lunar.toString(),
                "生肖": zodiac,
                "星座": constellation,
                "性别": "男" if gender == "male" else "女"
            },
            "八字": {
                "年柱": f"{year_gan}{year_zhi}",
                "月柱": f"{month_gan}{month_zhi}",
                "日柱": f"{day_gan}{day_zhi}",
                "时柱": f"{hour_gan}{hour_zhi}",
                "完整": f"{year_gan}{year_zhi} {month_gan}{month_zhi} {day_gan}{day_zhi} {hour_gan}{hour_zhi}"
            },
            "五行": {
                "分布": wuxing_count,
                "最弱": weakest,
                "最强": strongest,
                "统计": f"金{wuxing_count['金']} 木{wuxing_count['木']} 水{wuxing_count['水']} 火{wuxing_count['火']} 土{wuxing_count['土']}"
            },
            "纳音": na_yin,
            "大运": da_yun,
            "流年": liu_nian,
            "喜用神": xi_yong,
            "命卦": ming_gua,
            "建议": self._get_advice(weakest, xi_yong)
        }
    
    def _calculate_xi_yong(self, wuxing_count: Dict[str, int], weakest: str, strongest: str) -> Dict[str, str]:
        """计算喜用神（简化版）"""
        wuxing_generate = {
            "金": "水",
            "水": "木",
            "木": "火",
            "火": "土",
            "土": "金"
        }
        
        xi_shen = None
        for k, v in wuxing_generate.items():
            if v == weakest:
                xi_shen = k
                break
        
        return {
            "喜神": xi_shen or weakest,
            "用神": weakest,
            "忌神": strongest,
            "说明": f"五行{weakest}较弱，需要补充；{strongest}过旺，需要克制"
        }
    
    def _calculate_ming_gua(self, year: int, gender: str) -> Dict[str, str]:
        """计算命卦（简化版）"""
        last_digit = year % 10
        
        if gender == "male":
            gua_map = {
                0: "巽", 1: "坎", 2: "离", 3: "艮", 4: "兑",
                5: "乾", 6: "坤", 7: "艮", 8: "巽", 9: "震"
            }
        else:
            gua_map = {
                0: "坤", 1: "震", 2: "坤", 3: "坎", 4: "离",
                5: "艮", 6: "乾", 7: "兑", 8: "艮", 9: "坤"
            }
        
        ming_gua = gua_map.get(last_digit, "坤")
        
        dong_si = ["坎", "离", "震", "巽"]
        xi_si = ["乾", "坤", "艮", "兑"]
        
        return {
            "卦": ming_gua,
            "类型": "东四命" if ming_gua in dong_si else "西四命",
            "吉利方位": self._get_lucky_direction(ming_gua)
        }
    
    def _get_lucky_direction(self, gua: str) -> str:
        """获取吉利方位"""
        directions = {
            "坎": "北方、东方、东南方、南方",
            "离": "南方、北方、东方、东南方",
            "震": "东方、南方、东南方、北方",
            "巽": "东南方、北方、南方、东方",
            "乾": "西北方、西方、东北方、西南方",
            "坤": "西南方、西北方、西方、东北方",
            "艮": "东北方、西南方、西北方、西方",
            "兑": "西方、东北方、西南方、西北方"
        }
        return directions.get(gua, "吉利方位需详细计算")
    
    def _get_advice(self, weakest: str, xi_yong: Dict[str, str]) -> List[str]:
        """根据五行给出传统文化角度的说明（仅供文化参考）"""
        advice_map = {
            "金": [
                "传统文化中，金象征坚定与清晰",
                "传统方位文化中，西方与金元素相关",
                "传统文化认为金融、法律等行业与金相关",
                "传统色彩文化中，白色、金色属金"
            ],
            "木": [
                "传统文化中，木象征生长与发展",
                "传统方位文化中，东方与木元素相关",
                "传统文化认为教育、文化等行业与木相关",
                "传统色彩文化中，绿色、青色属木"
            ],
            "水": [
                "传统文化中，水象征智慧与流动",
                "传统方位文化中，北方与水元素相关",
                "传统文化认为贸易、旅游等行业与水相关",
                "传统色彩文化中，黑色、蓝色属水"
            ],
            "火": [
                "传统文化中，火象征热情与活力",
                "传统方位文化中，南方与火元素相关",
                "传统文化认为餐饮、娱乐等行业与火相关",
                "传统色彩文化中，红色、紫色属火"
            ],
            "土": [
                "传统文化中，土象征稳定与包容",
                "传统方位文化中，中心与土元素相关",
                "传统文化认为建筑、农业等行业与土相关",
                "传统色彩文化中，黄色、棕色属土"
            ]
        }
        
        advice = advice_map.get(weakest, [])
        
        if xi_yong["喜神"]:
            advice.append(f"传统五行理论中，{xi_yong['喜神']}与{weakest}存在相生关系")
        
        return advice[:4]


# 测试
if __name__ == "__main__":
    calculator = BaziCalculator()
    result = calculator.calculate(1990, 3, 15, 12, 0, "male")
    
    import json
    print(json.dumps(result, ensure_ascii=False, indent=2))
