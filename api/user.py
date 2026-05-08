"""
用户相关 API 路由
"""
from fastapi import APIRouter, HTTPException
from models.schemas import UserSaveRequest, UserSaveResponse, APIResponse
from datetime import datetime
import uuid

router = APIRouter()

# 临时用户存储（内存）
users_db = {}


@router.post("/save", response_model=UserSaveResponse, summary="保存用户信息")
async def save_user(request: UserSaveRequest):
    """
    保存用户信息
    
    **请求示例:**
    ```json
    {
        "name": "海哥",
        "birth_year": 1990,
        "birth_month": 5,
        "birth_day": 15,
        "birth_hour": 10,
        "phone": "13800138000"
    }
    ```
    """
    try:
        user_id = str(uuid.uuid4())
        
        users_db[user_id] = {
            "user_id": user_id,
            "name": request.name,
            "birth_year": request.birth_year,
            "birth_month": request.birth_month,
            "birth_day": request.birth_day,
            "birth_hour": request.birth_hour,
            "phone": request.phone,
            "email": request.email,
            "created_at": datetime.now().isoformat()
        }
        
        return UserSaveResponse(
            success=True,
            message="保存成功",
            user_id=user_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"保存失败：{str(e)}")


@router.get("/{user_id}", response_model=APIResponse, summary="获取用户信息")
async def get_user(user_id: str):
    """
    根据用户 ID 获取用户信息
    
    **使用示例:**
    ```
    GET /api/user/123e4567-e89b-12d3-a456-426614174000
    ```
    """
    try:
        if user_id in users_db:
            return APIResponse(
                success=True,
                message="查询成功",
                data=users_db[user_id]
            )
        else:
            raise HTTPException(status_code=404, detail="用户不存在")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询失败：{str(e)}")
