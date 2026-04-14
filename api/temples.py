"""
寺庙相关 API 路由
"""
from fastapi import APIRouter, HTTPException, Query
from models.schemas import TempleListResponse, TempleDetail, TempleMatchRequest
from core.matching import match_temples, generate_recommendation
from core.bazi_calculator import calculate_bazi
from datetime import datetime
import json
import os

router = APIRouter()

# 全局寺庙数据（从 main.py 导入）
temples_data = []


def get_temples_data():
    """获取寺庙数据"""
    global temples_data
    if not temples_data:
        data_file = "/Users/apple/.openclaw/workspace/program-shrimp/temples_with_history.json"
        if os.path.exists(data_file):
            with open(data_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                temples_data = data.get("temples", [])
    return temples_data


@router.get("/match", response_model=TempleListResponse, summary="根据八字匹配寺庙")
async def match_temples_api(
    year: int = Query(..., description="出生年份"),
    month: int = Query(..., description="出生月份"),
    day: int = Query(..., description="出生日期"),
    hour: int = Query(..., description="出生时辰"),
    limit: int = Query(10, description="返回数量"),
    city: str = Query(None, description="限制城市")
):
    """
    根据八字匹配最适合的寺庙
    
    **使用示例:**
    ```
    GET /api/temples/match?year=1990&month=5&day=15&hour=10&limit=10
    ```
    """
    try:
        temples = get_temples_data()
        
        # 计算八字
        bazi_result = calculate_bazi(year=year, month=month, day=day, hour=hour)
        
        # 匹配寺庙
        matched = match_temples(temples, bazi_result, limit=limit, city=city)
        
        # 生成推荐
        recommendation = generate_recommendation(bazi_result, matched)
        
        return TempleListResponse(
            success=True,
            message="匹配成功",
            data=matched,
            total=len(matched)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"匹配失败：{str(e)}")


@router.get("/search", response_model=TempleListResponse, summary="搜索寺庙")
async def search_temples_api(
    keyword: str = Query(None, description="关键词"),
    city: str = Query(None, description="城市"),
    province: str = Query(None, description="省份"),
    temple_type: str = Query(None, description="类型"),
    page: int = Query(1, description="页码"),
    page_size: int = Query(20, description="每页数量")
):
    """
    搜索寺庙
    
    **使用示例:**
    ```
    GET /api/temples/search?keyword=雍和宫&city=北京
    ```
    """
    try:
        temples = get_temples_data()
        
        # 过滤
        filtered = temples
        
        if keyword:
            filtered = [t for t in filtered if keyword.lower() in t.get("name", "").lower()]
        
        if city:
            filtered = [t for t in filtered if city in t.get("city", "")]
        
        if province:
            filtered = [t for t in filtered if province in t.get("province", "")]
        
        if temple_type:
            filtered = [t for t in filtered if temple_type in t.get("temple_type", "")]
        
        # 分页
        start = (page - 1) * page_size
        end = start + page_size
        paginated = filtered[start:end]
        
        return TempleListResponse(
            success=True,
            message="查询成功",
            data=paginated,
            total=len(filtered),
            page=page,
            page_size=page_size
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"搜索失败：{str(e)}")


@router.get("/{temple_id}", response_model=TempleDetail, summary="获取寺庙详情")
async def get_temple_detail_api(temple_id: int):
    """
    获取寺庙详细信息
    
    **使用示例:**
    ```
    GET /api/temples/123
    ```
    """
    try:
        temples = get_temples_data()
        
        # 查找寺庙（假设 temple_id 是索引）
        if 0 <= temple_id < len(temples):
            temple = temples[temple_id]
            return temple
        else:
            raise HTTPException(status_code=404, detail="寺庙不存在")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询失败：{str(e)}")


@router.get("/", response_model=TempleListResponse, summary="获取寺庙列表")
async def get_temples_list_api(
    page: int = Query(1, description="页码"),
    page_size: int = Query(20, description="每页数量")
):
    """
    获取寺庙列表（分页）
    
    **使用示例:**
    ```
    GET /api/temples?page=1&page_size=20
    ```
    """
    try:
        temples = get_temples_data()
        
        # 分页
        start = (page - 1) * page_size
        end = start + page_size
        paginated = temples[start:end]
        
        return TempleListResponse(
            success=True,
            message="查询成功",
            data=paginated,
            total=len(temples),
            page=page,
            page_size=page_size
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询失败：{str(e)}")
