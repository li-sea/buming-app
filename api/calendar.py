"""
万年历 API 路由
"""
from fastapi import APIRouter, HTTPException, Query
from models.schemas import BaziResponse, APIResponse
from core.lunar_calendar import solar_to_lunar, lunar_to_solar, get_today_info, get_zodiac
from datetime import datetime

router = APIRouter()


@router.post("/solar-to-lunar", response_model=APIResponse, summary="阳历转农历")
async def solar_to_lunar_api(
    year: int = Query(..., description="阳历年"),
    month: int = Query(..., description="阳历月"),
    day: int = Query(..., description="阳历日"),
    hour: int = Query(0, description="时辰")
):
    """
    阳历转农历
    
    **使用示例:**
    ```
    GET /api/calendar/solar-to-lunar?year=2026&month=4&day=14&hour=10
    ```
    """
    try:
        result = solar_to_lunar(year, month, day, hour)
        
        return APIResponse(
            success=True,
            message="转换成功",
            data=result
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"转换失败：{str(e)}")


@router.get("/lunar-to-solar", response_model=APIResponse, summary="农历转阳历")
async def lunar_to_solar_api(
    year: int = Query(..., description="农历年"),
    month: int = Query(..., description="农历月"),
    day: int = Query(..., description="农历日"),
    is_leap_month: bool = Query(False, description="是否闰月")
):
    """
    农历转阳历
    
    **使用示例:**
    ```
    GET /api/calendar/lunar-to-solar?year=2026&month=3&day=17
    ```
    """
    try:
        result = lunar_to_solar(year, month, day, is_leap_month)
        
        return APIResponse(
            success=True,
            message="转换成功",
            data=result
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"转换失败：{str(e)}")


@router.get("/today", response_model=APIResponse, summary="获取今日信息")
async def get_today_api():
    """
    获取今日阴阳历信息
    
    **使用示例:**
    ```
    GET /api/calendar/today
    ```
    """
    try:
        result = get_today_info()
        
        return APIResponse(
            success=True,
            message="查询成功",
            data=result
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询失败：{str(e)}")


@router.get("/zodiac/{year}", response_model=APIResponse, summary="获取生肖")
async def get_zodiac_api(year: int):
    """
    根据年份获取生肖
    
    **使用示例:**
    ```
    GET /api/calendar/zodiac/1990
    ```
    """
    try:
        zodiac = get_zodiac(year)
        
        return APIResponse(
            success=True,
            message="查询成功",
            data={
                "year": year,
                "zodiac": zodiac,
                "zodiac_str": f"{year}年属{zodiac}"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询失败：{str(e)}")
