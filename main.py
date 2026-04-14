"""
不认命 App - FastAPI 主应用
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import json
import os
from datetime import datetime

# 导入路由
from api import bazi, temples, user, calendar

# 创建 FastAPI 应用
app = FastAPI(
    title="不认命 App API",
    description="八字计算与寺庙匹配 API 服务",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 配置 CORS（允许小程序访问）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应该指定具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 全局变量 - 寺庙数据
temples_data = []
temples_loaded_at = None


def load_temples_data():
    """加载寺庙数据"""
    global temples_data, temples_loaded_at
    
    data_file = "/Users/apple/.openclaw/workspace/program-shrimp/temples_with_history.json"
    
    if os.path.exists(data_file):
        with open(data_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            temples_data = data.get("temples", [])
            temples_loaded_at = datetime.now().isoformat()
            print(f"✅ 加载寺庙数据：{len(temples_data)} 座")
    else:
        print(f"⚠️ 数据文件不存在：{data_file}")


# 启动时加载数据
@app.on_event("startup")
async def startup_event():
    """应用启动时执行"""
    print("🦐 不认命 App API 启动中...")
    load_temples_data()
    print("✅ 启动完成！")


# 健康检查
@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "temples_loaded": len(temples_data),
        "loaded_at": temples_loaded_at,
        "timestamp": datetime.now().isoformat()
    }


# 根路径
@app.get("/")
async def root():
    """API 根路径"""
    return {
        "name": "不认命 App API",
        "version": "0.1.0",
        "description": "八字计算与寺庙匹配 API 服务",
        "docs": "/docs",
        "health": "/health",
        "api_prefix": "/api"
    }


# 注册路由
app.include_router(bazi.router, prefix="/api/bazi", tags=["八字计算"])
app.include_router(temples.router, prefix="/api/temples", tags=["寺庙相关"])
app.include_router(user.router, prefix="/api/user", tags=["用户相关"])
app.include_router(calendar.router, prefix="/api/calendar", tags=["万年历"])


# 全局异常处理
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """全局异常处理"""
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": f"服务器错误：{str(exc)}",
            "error_code": "INTERNAL_ERROR",
            "timestamp": datetime.now().isoformat()
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
