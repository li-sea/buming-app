"""
不认命 App - 快速测试版 API
功能：八字计算、寺庙匹配、法器推荐
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import json
import random
from datetime import datetime
import os
from bazi_lunar import BaziCalculator

# 初始化八字计算器
bazi_calc = BaziCalculator()

app = FastAPI(
    title="不认命 - 传统文化学习工具",
    description="八字知识与寺庙文化介绍 - 测试版",
    version="1.0.0"
)

# 允许 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 加载寺庙数据
TEMPLES = []
DATA_DIR = os.path.join(os.path.dirname(__file__), "../data")

def load_temples():
    """加载所有寺庙数据"""
    global TEMPLES
    TEMPLES = []
    loaded_files = []
    
    # 加载所有 JSON 文件
    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".json"):
            filepath = os.path.join(DATA_DIR, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        count = len(data)
                        TEMPLES.extend(data)
                        loaded_files.append(f"{filename}: {count}座")
                    elif isinstance(data, dict):
                        # 处理 {"meta": ..., "temples": [...]} 格式
                        temples_list = data.get('temples', [])
                        if temples_list:
                            count = len(temples_list)
                            TEMPLES.extend(temples_list)
                            loaded_files.append(f"{filename}: {count}座")
            except Exception as e:
                print(f"Error loading {filename}: {e}")
    
    # 去重（根据 name+province）
    seen = set()
    unique_temples = []
    for temple in TEMPLES:
        key = f"{temple.get('name', '')}_{temple.get('province', '')}"
        if key not in seen:
            seen.add(key)
            unique_temples.append(temple)
    
    TEMPLES = unique_temples
    
    print(f"Loaded files: {', '.join(loaded_files)}")
    print(f"Total temples (after dedup): {len(TEMPLES)}座")

load_temples()

# 请求模型
class BaziInput(BaseModel):
    year: int
    month: int
    day: int
    hour: int
    gender: str = "male"  # male or female

class MatchRequest(BaseModel):
    bazi: Optional[str] = None
    year: Optional[int] = None
    month: Optional[int] = None
    day: Optional[int] = None
    hour: Optional[int] = None
    gender: str = "male"
    prayer_focus: Optional[str] = None  # 祈福方向：事业、财运、姻缘、健康等
    location: Optional[str] = None  # 省份或城市

# 专业八字计算（使用 lunar-python）
def calculate_bazi(year: int, month: int, day: int, hour: int, minute: int = 0, gender: str = "male") -> Dict[str, Any]:
    """
    专业版八字计算（使用 lunar-python）
    """
    result = bazi_calc.calculate(year, month, day, hour, minute, gender)
    return result

# 五行属性（从 lunar-python 结果获取）
def get_wuxing(bazi_result: Dict) -> Dict[str, int]:
    """获取五行属性（从 lunar-python 结果）"""
    if "五行" in bazi_result and "分布" in bazi_result["五行"]:
        return bazi_result["五行"]["分布"]
    # 兼容旧版
    return {"木": 0, "火": 0, "土": 0, "金": 0, "水": 0}

# 寺庙匹配算法
def match_temples(bazi_result: Dict, prayer_focus: Optional[str] = None, location: Optional[str] = None, limit: int = 5) -> List[Dict]:
    """
    寺庙匹配算法
    根据八字、祈福方向、地理位置推荐寺庙
    """
    wuxing = bazi_result["五行"]["分布"]
    weakest_wuxing = bazi_result["五行"]["最弱"]
    
    # 五行对应的寺庙类型
    wuxing_temple_types = {
        "木": ["道教", "佛教"],
        "火": ["道教", "文庙"],
        "土": ["佛教", "城隍庙"],
        "金": ["道教", "清真寺"],
        "水": ["佛教", "妈祖庙"]
    }
    
    # 祈福方向对应的寺庙
    prayer_temple_map = {
        "事业": ["道教", "关帝庙", "文庙"],
        "财运": ["财神庙", "道教", "关帝庙"],
        "姻缘": ["月老庙", "妈祖庙"],
        "健康": ["佛教", "道教", "药王庙"],
        "平安": ["佛教", "道教", "城隍庙", "妈祖庙"],
        "学业": ["文庙", "文昌阁"],
        "修行": ["佛教", "道教"]
    }
    
    # 筛选寺庙
    scored_temples = []
    for temple in TEMPLES:
        score = 0
        
        # 类型匹配
        temple_type = temple.get("type", "")
        temple_subtype = temple.get("subtype", "")
        
        preferred_types = wuxing_temple_types.get(weakest_wuxing, [])
        if temple_type in preferred_types or temple_subtype in preferred_types:
            score += 20
        
        # 祈福方向匹配
        if prayer_focus:
            preferred_for_prayer = prayer_temple_map.get(prayer_focus, [])
            if temple_type in preferred_for_prayer or temple_subtype in preferred_for_prayer:
                score += 30
        
        # 地理位置匹配
        if location:
            temple_province = temple.get("province", "")
            temple_city = temple.get("city", "")
            if location in temple_province or location in temple_city:
                score += 40
        
        # 评级加分
        rating = temple.get("rating", 0)
        score += rating * 10
        
        # 5 星寺庙额外加分
        if rating == 5:
            score += 20
        
        scored_temples.append((score, temple))
    
    # 按分数排序
    scored_temples.sort(key=lambda x: x[0], reverse=True)
    
    # 返回前 N 个
    result = []
    for score, temple in scored_temples[:limit]:
        temple_copy = temple.copy()
        temple_copy["match_score"] = score
        temple_copy["match_reason"] = f"传统五行文化中，{weakest_wuxing}代表"
        reason_map = {"木": "生长与发展", "火": "热情与活力", "土": "稳定与包容", "金": "坚定与清晰", "水": "智慧与流动"}
        temple_copy["match_reason"] += reason_map.get(weakest_wuxing, "")
        if prayer_focus:
            temple_copy["match_reason"] += f"，与{prayer_focus}主题相关"
        temple_copy["match_reason"] += f"，文化评级{temple.get('rating', 0)}⭐"
        result.append(temple_copy)
    
    return result

# 法器推荐算法
def recommend_faqi(bazi_result: Dict, temples: List[Dict]) -> List[Dict[str, str]]:
    """
    根据八字和推荐寺庙推荐法器
    """
    wuxing = bazi_result["五行"]["分布"]
    weakest_wuxing = bazi_result["五行"]["最弱"]
    
    # 五行对应的传统文化元素（仅供文化参考）
    wuxing_faqi = {
        "木": [
            {"name": "绿幽灵水晶", "description": "传统文化中，木象征生长与发展", "cultural_meaning": "木元素代表生机与活力"},
            {"name": "翡翠", "description": "传统文化中的珍贵玉石", "cultural_meaning": "玉在中华文化中象征品德"},
            {"name": "木质饰品", "description": "天然木材，传统文化中用于装饰", "cultural_meaning": "木制品体现自然之美"}
        ],
        "火": [
            {"name": "红玛瑙", "description": "传统文化中的红色宝石", "cultural_meaning": "红色在中国文化中象征喜庆"},
            {"name": "石榴石", "description": "传统饰品材料", "cultural_meaning": "石榴多籽，象征多子多福"},
            {"name": "红色饰品", "description": "传统文化中红色代表吉祥", "cultural_meaning": "红色辟邪是民间传统观念"}
        ],
        "土": [
            {"name": "黄水晶", "description": "传统文化中的黄色宝石", "cultural_meaning": "黄色在传统文化中象征尊贵"},
            {"name": "玉石", "description": "中华文化核心元素之一", "cultural_meaning": "君子比德于玉"},
            {"name": "陶瓷", "description": "中国传统工艺代表", "cultural_meaning": "陶瓷是中华文化的重要载体"}
        ],
        "金": [
            {"name": "白水晶", "description": "传统文化中的透明宝石", "cultural_meaning": "水晶在文化中象征纯洁"},
            {"name": "银饰", "description": "传统饰品材料", "cultural_meaning": "银在民间传统中有特殊地位"},
            {"name": "金属饰品", "description": "传统工艺制品", "cultural_meaning": "金属工艺体现传统技艺"}
        ],
        "水": [
            {"name": "黑曜石", "description": "传统文化中的黑色宝石", "cultural_meaning": "黑色在五行中代表水"},
            {"name": "海蓝宝", "description": "蓝色宝石，传统文化中少见", "cultural_meaning": "蓝色象征智慧与深邃"},
            {"name": "水晶", "description": "传统文化中的珍贵材料", "cultural_meaning": "水晶在文化中象征清澈透明"}
        ]
    }
    
    # 返回对应五行的法器
    return wuxing_faqi.get(weakest_wuxing, wuxing_faqi["土"])

# API 路由
@app.get("/")
async def root():
    return {
        "message": "不认命 - 传统文化学习工具",
        "version": "1.0.0",
        "temples_loaded": len(TEMPLES),
        "docs": "/docs",
        "disclaimer": "本 API 仅供传统文化学习与研究使用"
    }

@app.get("/api/temples")
async def get_temples(
    province: Optional[str] = None,
    type: Optional[str] = None,
    limit: int = 10
):
    """获取寺庙列表"""
    result = TEMPLES
    
    if province:
        result = [t for t in result if province in t.get("province", "")]
    
    if type:
        result = [t for t in result if type in t.get("type", "") or type in t.get("subtype", "")]
    
    return result[:limit]

@app.post("/api/bazi")
async def calculate_bazi_endpoint(year: int, month: int, day: int, hour: int, minute: int = 0, gender: str = "male"):
    """计算八字（专业版）"""
    if not (1900 <= year <= 2100):
        raise HTTPException(status_code=400, detail="年份必须在 1900-2100 之间")
    if not (1 <= month <= 12):
        raise HTTPException(status_code=400, detail="月份必须在 1-12 之间")
    if not (1 <= day <= 31):
        raise HTTPException(status_code=400, detail="日期必须在 1-31 之间")
    if not (0 <= hour <= 23):
        raise HTTPException(status_code=400, detail="时辰必须在 0-23 之间")
    
    bazi_result = calculate_bazi(year, month, day, hour, minute, gender)
    
    return bazi_result

@app.post("/api/match")
async def match_temples_endpoint(request: MatchRequest):
    """寺庙匹配（专业版）"""
    # 计算八字
    year = request.year or 1990
    month = request.month or 1
    day = request.day or 1
    hour = request.hour or 12
    
    bazi_result = calculate_bazi(year, month, day, hour, 0, request.gender)
    
    # 匹配寺庙
    temples = match_temples(
        bazi_result,
        prayer_focus=request.prayer_focus,
        location=request.location,
        limit=5
    )
    
    # 推荐法器
    faqi = recommend_faqi(bazi_result, temples)
    
    return {
        "bazi": bazi_result["八字"],
        "wuxing": bazi_result["五行"]["分布"],
        "weakest": bazi_result["五行"]["最弱"],
        "xiyong": bazi_result["喜用神"],
        "minggua": bazi_result["命卦"],
        "temples": temples,
        "faqi": faqi,
        "advice": bazi_result["建议"]
    }

@app.get("/api/stats")
async def get_stats():
    """获取统计数据"""
    stats = {
        "total_temples": len(TEMPLES),
        "by_type": {},
        "by_province": {},
        "by_rating": {"5": 0, "4": 0, "3": 0}
    }
    
    for temple in TEMPLES:
        # 按类型统计
        t_type = temple.get("type", "其他")
        stats["by_type"][t_type] = stats["by_type"].get(t_type, 0) + 1
        
        # 按省份统计
        province = temple.get("province", "未知")
        stats["by_province"][province] = stats["by_province"].get(province, 0) + 1
        
        # 按评级统计
        rating = temple.get("rating", 0)
        if rating >= 5:
            stats["by_rating"]["5"] += 1
        elif rating >= 4:
            stats["by_rating"]["4"] += 1
        else:
            stats["by_rating"]["3"] += 1
    
    return stats

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
