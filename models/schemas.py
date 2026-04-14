"""
不认命 App - 数据模型定义
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime


# ========== 八字计算相关模型 ==========

class BaziRequest(BaseModel):
    """八字计算请求"""
    year: int = Field(..., description="出生年份（公历）", example=1990)
    month: int = Field(..., description="出生月份（1-12）", example=5)
    day: int = Field(..., description="出生日期（1-31）", example=15)
    hour: int = Field(..., description="出生时辰（0-23）", example=10)
    name: Optional[str] = Field(None, description="姓名", example="海哥")


class BaziResponse(BaseModel):
    """八字计算响应"""
    success: bool = True
    message: str = "计算成功"
    data: Optional[Dict] = None
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())


# ========== 寺庙相关模型 ==========

class TempleSearchRequest(BaseModel):
    """寺庙搜索请求"""
    keyword: Optional[str] = Field(None, description="关键词", example="雍和宫")
    city: Optional[str] = Field(None, description="城市", example="北京")
    province: Optional[str] = Field(None, description="省份", example="北京市")
    temple_type: Optional[str] = Field(None, description="类型", example="佛教")
    page: int = Field(1, description="页码", example=1)
    page_size: int = Field(20, description="每页数量", example=20)


class TempleSimple(BaseModel):
    """寺庙简单信息"""
    id: int
    name: str
    city: str
    province: str
    temple_type: str
    rating: float
    match_score: Optional[float] = None


class TempleDetail(BaseModel):
    """寺庙详细信息"""
    id: int
    name: str
    location: str
    latitude: float
    longitude: float
    city: str
    province: str
    district: str
    temple_type: str
    telephone: str
    history: str
    main_deity: str
    prayer_directions: List[str]
    specialties: List[str]
    rating: float
    is_famous: bool
    data_level: str
    source: str
    match_score: Optional[float] = None


class TempleListResponse(BaseModel):
    """寺庙列表响应"""
    success: bool = True
    message: str = "查询成功"
    data: Optional[List[Dict]] = None
    total: int = 0
    page: int = 1
    page_size: int = 20
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())


class TempleMatchRequest(BaseModel):
    """寺庙匹配请求"""
    year: int
    month: int
    day: int
    hour: int
    limit: int = Field(10, description="返回数量", example=10)
    city: Optional[str] = Field(None, description="限制城市", example="北京")


# ========== 用户相关模型 ==========

class UserSaveRequest(BaseModel):
    """保存用户请求"""
    name: str = Field(..., description="姓名", example="海哥")
    birth_year: int
    birth_month: int
    birth_day: int
    birth_hour: int
    phone: Optional[str] = None
    email: Optional[str] = None


class UserSaveResponse(BaseModel):
    """保存用户响应"""
    success: bool = True
    message: str = "保存成功"
    user_id: str
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())


# ========== 通用响应模型 ==========

class APIResponse(BaseModel):
    """通用 API 响应"""
    success: bool = True
    message: str = "操作成功"
    data: Optional[Dict] = None
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())


class ErrorResponse(BaseModel):
    """错误响应"""
    success: bool = False
    message: str
    error_code: str = "UNKNOWN_ERROR"
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
