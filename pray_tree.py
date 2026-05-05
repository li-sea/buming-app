"""
不认命 App - 祈福树模块
功能：种树、点赞、分享
"""

import json
import os
import time
import random
from typing import Dict, List, Optional
from datetime import datetime, timedelta

# 数据存储
DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "pray_trees.json")

class PrayTreeManager:
    """祈福树管理器"""
    
    def __init__(self):
        self.trees = self._load_trees()
    
    def _load_trees(self) -> Dict:
        """加载所有祈福树数据"""
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"trees": {}, "likes": {}}
    
    def _save_trees(self):
        """保存数据"""
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.trees, f, ensure_ascii=False, indent=2)
    
    def create_tree(self, user_id: str, prayer_focus: str, wish: str, birth_date: str = None) -> Dict:
        """
        种一棵祈福树
        
        Args:
            user_id: 用户 ID
            prayer_focus: 祈福方向（事业/财运/姻缘/健康/平安/学业）
            wish: 心愿内容
            birth_date: 生日（可选，用于星空图）
        
        Returns:
            树的信息
        """
        tree_id = f"tree_{int(time.time())}_{random.randint(1000, 9999)}"
        
        tree = {
            "tree_id": tree_id,
            "user_id": user_id,
            "prayer_focus": prayer_focus,
            "wish": wish,
            "birth_date": birth_date,
            "created_at": datetime.now().isoformat(),
            "level": 1,  # 1-10
            "likes": 0,
            "likers": [],  # 点赞用户列表
            "status": "growing",  # growing, blooming, fruiting
            "share_count": 0
        }
        
        self.trees["trees"][tree_id] = tree
        self.trees["likes"][tree_id] = []
        self._save_trees()
        
        return self._get_tree_info(tree_id)
    
    def like_tree(self, tree_id: str, liker_id: str) -> Dict:
        """
        给祈福树点赞
        
        Args:
            tree_id: 树 ID
            liker_id: 点赞用户 ID
        
        Returns:
            树的信息
        """
        if tree_id not in self.trees["trees"]:
            raise ValueError("树不存在")
        
        tree = self.trees["trees"][tree_id]
        
        # 检查是否已点赞
        if liker_id in tree["likers"]:
            return self._get_tree_info(tree_id)
        
        # 添加点赞
        tree["likers"].append(liker_id)
        tree["likes"] = len(tree["likers"])
        
        # 更新等级
        tree["level"] = min(10, tree["likes"] + 1)
        
        # 更新状态
        if tree["level"] >= 10:
            tree["status"] = "fruiting"
        elif tree["level"] >= 5:
            tree["status"] = "blooming"
        else:
            tree["status"] = "growing"
        
        self._save_trees()
        return self._get_tree_info(tree_id)
    
    def get_tree(self, tree_id: str) -> Dict:
        """获取树信息"""
        if tree_id not in self.trees["trees"]:
            raise ValueError("树不存在")
        return self._get_tree_info(tree_id)
    
    def get_user_trees(self, user_id: str) -> List[Dict]:
        """获取用户所有树"""
        user_trees = []
        for tree_id, tree in self.trees["trees"].items():
            if tree["user_id"] == user_id:
                user_trees.append(self._get_tree_info(tree_id))
        return sorted(user_trees, key=lambda x: x["created_at"], reverse=True)
    
    def get_hot_trees(self, limit: int = 20) -> List[Dict]:
        """获取热门树（点赞最多的）"""
        all_trees = list(self.trees["trees"].values())
        all_trees.sort(key=lambda x: x["likes"], reverse=True)
        
        result = []
        for tree in all_trees[:limit]:
            result.append(self._get_tree_info(tree["tree_id"]))
        return result
    
    def get_random_trees(self, limit: int = 20) -> List[Dict]:
        """获取随机树（用于祈福广场）"""
        all_trees = list(self.trees["trees"].values())
        random.shuffle(all_trees)
        
        result = []
        for tree in all_trees[:limit]:
            result.append(self._get_tree_info(tree["tree_id"]))
        return result
    
    def share_tree(self, tree_id: str) -> Dict:
        """
        分享树（增加分享计数）
        
        Returns:
            分享信息
        """
        if tree_id not in self.trees["trees"]:
            raise ValueError("树不存在")
        
        tree = self.trees["trees"][tree_id]
        tree["share_count"] = tree.get("share_count", 0) + 1
        self._save_trees()
        
        return {
            "tree_id": tree_id,
            "share_count": tree["share_count"],
            "share_url": f"https://buming.app/pray/{tree_id}"
        }
    
    def _get_tree_info(self, tree_id: str) -> Dict:
        """获取树详细信息"""
        tree = self.trees["trees"][tree_id]
        
        # 树的状态描述
        status_map = {
            "growing": "成长中",
            "blooming": "开花中",
            "fruiting": "已结果"
        }
        
        # 树 emoji
        tree_emoji_map = {
            1: "🌱", 2: "🌱", 3: "🌿", 4: "🌿",
            5: "🌳", 6: "🌳", 7: "🌳", 8: "🌸",
            9: "🌸", 10: "🌳🌸🌳"
        }
        
        # 祈福方向 emoji
        prayer_emoji_map = {
            "事业": "💼",
            "财运": "💰",
            "姻缘": "💕",
            "健康": "💪",
            "平安": "🙏",
            "学业": "📚"
        }
        
        return {
            "tree_id": tree_id,
            "user_id": tree["user_id"],
            "prayer_focus": tree["prayer_focus"],
            "prayer_emoji": prayer_emoji_map.get(tree["prayer_focus"], "🙏"),
            "wish": tree["wish"],
            "birth_date": tree.get("birth_date"),
            "created_at": tree["created_at"],
            "level": tree["level"],
            "likes": tree["likes"],
            "likers_count": len(tree["likers"]),
            "status": tree["status"],
            "status_text": status_map.get(tree["status"], "成长中"),
            "tree_emoji": tree_emoji_map.get(tree["level"], "🌱"),
            "share_count": tree.get("share_count", 0),
            "need_likes": max(0, 10 - tree["likes"]),
            "is_fruiting": tree["level"] >= 10
        }

# 全局实例
pray_tree_manager = PrayTreeManager()
