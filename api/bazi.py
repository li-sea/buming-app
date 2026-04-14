"""
八字计算 API 路由
"""
from fastapi import APIRouter, HTTPException
from models.schemas import BaziRequest, BaziResponse, APIResponse
from core.bazi_calculator import calculate_bazi
from datetime import datetime

router = APIRouter()


@router.post("/calculate", response_model=BaziResponse, summary="计算八字")
async def calculate_bazi_api(request: BaziRequest):
    """
    根据出生年月日时计算八字
    
    **请求示例:**
    ```json
    {
        "year": 1990,
        "month": 5,
        "day": 15,
        "hour": 10,
        "name": "海哥"
    }
    ```
    """
    try:
        bazi_result = calculate_bazi(
            year=request.year,
            month=request.month,
            day=request.day,
            hour=request.hour
        )
        
        return BaziResponse(
            success=True,
            message="计算成功",
            data={
                "bazi": bazi_result["bazi"],
                "wuxing": bazi_result["wuxing"],
                "day_master": bazi_result["day_master"],
                "day_master_wuxing": bazi_result["day_master_wuxing"],
                "xishen": bazi_result["xishen"],
                "analysis": f"日主{bazi_result['day_master']}（{bazi_result['day_master_wuxing']}），五行中{bazi_result['xishen']}较弱，宜补{bazi_result['xishen']}"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"计算失败：{str(e)}")


@router.get("/{year}/{month}/{day}/{hour}", response_model=BaziResponse, summary="计算八字（GET）")
async def calculate_bazi_get(year: int, month: int, day: int, hour: int):
    """
    GET 方式计算八字（方便 URL 访问测试）
    
    **使用示例:**
    ```
    GET /api/bazi/1990/5/15/10
    ```
    """
    try:
        bazi_result = calculate_bazi(year=year, month=month, day=day, hour=hour)
        
        return BaziResponse(
            success=True,
            message="计算成功",
            data={
                "bazi": bazi_result["bazi"],
                "wuxing": bazi_result["wuxing"],
                "day_master": bazi_result["day_master"],
                "day_master_wuxing": bazi_result["day_master_wuxing"],
                "xishen": bazi_result["xishen"]
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"计算失败：{str(e)}")
