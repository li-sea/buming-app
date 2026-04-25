#!/usr/bin/env python3
"""
不认命 App - 自动化测试脚本
模拟真人操作，8 小时不间断测试
"""

import requests
import random
import time
import json
from datetime import datetime

API_BASE = "http://localhost:8001"

# 测试数据池
TEST_DATA = [
    {"year": 1990, "month": 3, "day": 15, "hour": 11, "gender": "male", "prayer_focus": "事业"},
    {"year": 1985, "month": 7, "day": 22, "hour": 9, "gender": "female", "prayer_focus": "财运"},
    {"year": 1992, "month": 1, "day": 8, "hour": 23, "gender": "male", "prayer_focus": "姻缘"},
    {"year": 1988, "month": 11, "day": 30, "hour": 5, "gender": "female", "prayer_focus": "健康"},
    {"year": 1995, "month": 6, "day": 18, "hour": 13, "gender": "male", "prayer_focus": "学业"},
    {"year": 1983, "month": 9, "day": 25, "hour": 15, "gender": "female", "prayer_focus": "平安"},
    {"year": 1991, "month": 4, "day": 12, "hour": 7, "gender": "male", "prayer_focus": "修行"},
    {"year": 1987, "month": 12, "day": 3, "hour": 19, "gender": "female", "prayer_focus": ""},
    {"year": 1994, "month": 2, "day": 28, "hour": 21, "gender": "male", "prayer_focus": "事业"},
    {"year": 1989, "month": 8, "day": 16, "hour": 1, "gender": "female", "prayer_focus": "财运"},
]

def log(message):
    """打印带时间戳的日志"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def test_api_root():
    """测试根路径"""
    try:
        resp = requests.get(f"{API_BASE}/", timeout=5)
        return resp.status_code == 200
    except Exception as e:
        log(f"❌ 根路径测试失败：{e}")
        return False

def test_bazi_calculation(data):
    """测试八字计算"""
    try:
        resp = requests.post(
            f"{API_BASE}/api/bazi",
            params={
                "year": data["year"],
                "month": data["month"],
                "day": data["day"],
                "hour": data["hour"],
                "gender": data["gender"]
            },
            timeout=10
        )
        if resp.status_code != 200:
            log(f"❌ 八字计算失败：{resp.status_code}")
            return False
        
        result = resp.json()
        # 验证返回数据结构
        required_keys = ["基本信息", "八字", "五行"]
        for key in required_keys:
            if key not in result:
                log(f"❌ 缺少必要字段：{key}")
                return False
        
        return True
    except Exception as e:
        log(f"❌ 八字计算异常：{e}")
        return False

def test_temple_match(data):
    """测试寺庙匹配"""
    try:
        resp = requests.post(
            f"{API_BASE}/api/match",
            json={
                "year": data["year"],
                "month": data["month"],
                "day": data["day"],
                "hour": data["hour"],
                "gender": data["gender"],
                "prayer_focus": data.get("prayer_focus"),
                "seed": random.randint(0, 10000)  # 随机种子测试多样性
            },
            timeout=15
        )
        if resp.status_code != 200:
            log(f"❌ 寺庙匹配失败：{resp.status_code}")
            return False
        
        result = resp.json()
        # 验证返回数据结构
        required_keys = ["bazi", "wuxing", "temples", "faqi"]
        for key in required_keys:
            if key not in result:
                log(f"❌ 缺少必要字段：{key}")
                return False
        
        # 验证寺庙数量
        if not isinstance(result["temples"], list) or len(result["temples"]) == 0:
            log(f"❌ 寺庙列表为空")
            return False
        
        # 验证佩戴建议
        if not isinstance(result["faqi"], list) or len(result["faqi"]) == 0:
            log(f"❌ 佩戴建议为空")
            return False
        
        # 验证佩戴建议字段
        for faqi in result["faqi"]:
            required_faqi_keys = ["name", "description", "wear_method", "wear_position", "reason"]
            for key in required_faqi_keys:
                if key not in faqi:
                    log(f"❌ 佩戴建议缺少字段：{key}")
                    return False
        
        return True
    except Exception as e:
        log(f"❌ 寺庙匹配异常：{e}")
        return False

def test_stats():
    """测试统计接口"""
    try:
        resp = requests.get(f"{API_BASE}/api/stats", timeout=5)
        if resp.status_code != 200:
            log(f"❌ 统计接口失败：{resp.status_code}")
            return False
        
        result = resp.json()
        if result.get("total_temples", 0) == 0:
            log(f"❌ 寺庙总数为 0")
            return False
        
        return True
    except Exception as e:
        log(f"❌ 统计接口异常：{e}")
        return False

def run_single_test_round(round_num):
    """执行一轮完整测试"""
    log(f"📍 第 {round_num} 轮测试开始")
    
    results = {
        "root": False,
        "bazi": False,
        "match": False,
        "stats": False
    }
    
    # 测试根路径
    results["root"] = test_api_root()
    time.sleep(random.uniform(0.5, 1.5))  # 模拟真人间隔
    
    # 随机选择测试数据
    test_data = random.choice(TEST_DATA)
    
    # 测试八字计算
    results["bazi"] = test_bazi_calculation(test_data)
    time.sleep(random.uniform(1.0, 2.0))
    
    # 测试寺庙匹配
    results["match"] = test_temple_match(test_data)
    time.sleep(random.uniform(1.0, 2.0))
    
    # 测试统计接口
    results["stats"] = test_stats()
    
    # 汇总结果
    success_count = sum(results.values())
    total_count = len(results)
    
    if success_count == total_count:
        log(f"✅ 第 {round_num} 轮测试全部通过 ({success_count}/{total_count})")
        return True
    else:
        log(f"⚠️ 第 {round_num} 轮测试部分通过 ({success_count}/{total_count})")
        return False

def run_8hour_test():
    """执行 8 小时不间断测试"""
    log("🚀 开始 8 小时不间断测试")
    log(f"📊 测试数据池：{len(TEST_DATA)} 组")
    
    start_time = time.time()
    duration_seconds = 8 * 60 * 60  # 8 小时
    round_count = 0
    success_count = 0
    fail_count = 0
    
    # 统计信息
    avg_response_time = 0
    response_times = []
    
    try:
        while True:
            elapsed = time.time() - start_time
            
            # 检查是否达到 8 小时
            if elapsed >= duration_seconds:
                log("⏰ 8 小时测试完成！")
                break
            
            # 执行测试
            round_count += 1
            start = time.time()
            
            if run_single_test_round(round_count):
                success_count += 1
            else:
                fail_count += 1
            
            # 计算响应时间
            elapsed_round = time.time() - start
            response_times.append(elapsed_round)
            avg_response_time = sum(response_times) / len(response_times)
            
            # 进度报告
            progress = (elapsed / duration_seconds) * 100
            log(f"📈 进度：{progress:.1f}% | 成功：{success_count} | 失败：{fail_count} | 平均耗时：{avg_response_time:.2f}s")
            
            # 随机休息 5-15 秒（模拟真人）
            sleep_time = random.uniform(5, 15)
            time.sleep(sleep_time)
    
    except KeyboardInterrupt:
        log("⚠️ 用户中断测试")
    except Exception as e:
        log(f"❌ 测试异常：{e}")
    finally:
        # 最终报告
        total_time = time.time() - start_time
        log("=" * 50)
        log("📊 测试报告")
        log("=" * 50)
        log(f"总耗时：{total_time / 3600:.2f} 小时")
        log(f"总轮数：{round_count}")
        log(f"成功：{success_count} ({success_count/round_count*100:.1f}%)")
        log(f"失败：{fail_count} ({fail_count/round_count*100:.1f}%)")
        log(f"平均响应时间：{avg_response_time:.2f}秒")
        log("=" * 50)

if __name__ == "__main__":
    run_8hour_test()
