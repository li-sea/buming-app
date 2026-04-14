#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
不认命 App - 寺庙文化信息补充脚本
功能：批量补充寺庙的历史、祈福方向、主祀等信息
创建时间：2026-04-14
"""

import json
from datetime import datetime

# 输入输出文件
INPUT_FILE = "/Users/apple/.openclaw/workspace/program-shrimp/temples_cleaned.json"
OUTPUT_FILE = "/Users/apple/.openclaw/workspace/program-shrimp/temples_with_culture.json"

# 著名寺庙文化数据库（用于匹配知名寺庙）
FAMOUS_TEMPLES = {
    # 北京
    "雍和宫": {
        "history": "始建于清康熙三十三年（1694 年），原为雍正帝即位前的府邸，乾隆九年改为藏传佛教寺院。是北京地区规模最大的藏传佛教寺院。",
        "main_deity": "释迦牟尼佛",
        "prayer_directions": ["求平安", "求事业", "求健康", "求子"],
        "specialties": ["北京最大藏传佛教寺院", "皇家寺院", "清代建筑", "国家级文保"],
        "rating": 4.8
    },
    "潭柘寺": {
        "history": "始建于西晋永嘉元年（307 年），距今已有 1700 多年历史，是北京地区最古老的寺院。民间有'先有潭柘寺，后有北京城'的说法。",
        "main_deity": "释迦牟尼佛",
        "prayer_directions": ["求平安", "求健康", "求事业"],
        "specialties": ["北京最古老寺院", "皇家寺院", "国家级文保", "银杏王"],
        "rating": 4.7
    },
    "白云观": {
        "history": "始建于唐开元二十七年（739 年），是全真道三大祖庭之一，被誉为'全真第一丛林'。丘处机道长曾在此主持。",
        "main_deity": "三清",
        "prayer_directions": ["求平安", "求健康", "求财运"],
        "specialties": ["全真道祖庭", "唐代古刹", "国家级文保", "燕京八景"],
        "rating": 4.6
    },
    "大觉寺": {
        "history": "始建于辽咸雍四年（1068 年），是京西著名古刹。以玉兰、银杏、泉水闻名，乾隆皇帝曾多次到此游览。",
        "main_deity": "无量寿佛",
        "prayer_directions": ["求平安", "求智慧", "求健康"],
        "specialties": ["辽代古刹", "皇家寺院", "千年银杏", "玉兰花"],
        "rating": 4.7
    },
    
    # 上海
    "龙华寺": {
        "history": "始建于三国吴赤乌五年（242 年），是上海地区历史最悠久的古刹。相传为孙权为母亲所建，距今已有 1700 多年历史。",
        "main_deity": "弥勒佛",
        "prayer_directions": ["求平安", "求健康", "求事业"],
        "specialties": ["上海最古老寺院", "三国古刹", "龙华塔", "国家级文保"],
        "rating": 4.7
    },
    "静安寺": {
        "history": "始建于三国吴赤乌十年（247 年），是上海著名古刹。位于繁华的南京西路，是闹市中的清净之地。",
        "main_deity": "释迦牟尼佛",
        "prayer_directions": ["求平安", "求财运", "求事业"],
        "specialties": ["三国古刹", "都市名刹", "金顶", "国家级文保"],
        "rating": 4.6
    },
    "豫园": {
        "history": "始建于明嘉靖三十八年（1559 年），是江南古典园林的代表作。园内的城隍庙是上海重要的道教场所。",
        "main_deity": "城隍神",
        "prayer_directions": ["求平安", "求财运", "求事业"],
        "specialties": ["明代园林", "城隍庙", "国家级文保", "上海地标"],
        "rating": 4.7
    },
    
    # 广州
    "光孝寺": {
        "history": "始建于三国吴黄武元年（222 年），是岭南地区最古老的寺院。六祖惠能曾在此剃度，有'岭南第一古刹'之称。",
        "main_deity": "释迦牟尼佛",
        "prayer_directions": ["求平安", "求智慧", "求事业"],
        "specialties": ["岭南第一古刹", "六祖剃度处", "国家级文保", "三国古刹"],
        "rating": 4.7
    },
    "六榕寺": {
        "history": "始建于南朝刘宋元嘉年间（420-479 年），因苏东坡题字'六榕'而得名。花塔是广州的地标建筑。",
        "main_deity": "释迦牟尼佛",
        "prayer_directions": ["求平安", "求智慧", "求健康"],
        "specialties": ["六祖惠能", "花塔", "苏东坡题字", "国家级文保"],
        "rating": 4.6
    },
    "陈家祠": {
        "history": "始建于清光绪十六年（1890 年），是广东陈氏宗族的合族祠。集岭南民间建筑装饰艺术之大成，被誉为'岭南建筑艺术明珠'。",
        "main_deity": "陈氏祖先",
        "prayer_directions": ["求祖先保佑", "求家族兴旺", "求事业", "求学业"],
        "specialties": ["岭南建筑艺术明珠", "广东民间工艺博物馆", "国家级文保", "羊城八景"],
        "rating": 4.8
    },
    
    # 杭州
    "灵隐寺": {
        "history": "始建于东晋咸和元年（326 年），是江南著名古刹。济公和尚曾在此修行，香火极盛。",
        "main_deity": "释迦牟尼佛",
        "prayer_directions": ["求平安", "求健康", "求事业", "求姻缘"],
        "specialties": ["江南名刹", "济公道场", "飞来峰", "国家级文保"],
        "rating": 4.8
    },
    "法喜寺": {
        "history": "始建于五代吴越国时期（907-978 年），是天台宗名刹。以求姻缘灵验闻名，是杭州著名的网红寺庙。",
        "main_deity": "观音菩萨",
        "prayer_directions": ["求姻缘", "求子", "求平安", "求健康"],
        "specialties": ["求姻缘灵验", "网红寺庙", "吴越古刹", "素斋"],
        "rating": 4.7
    },
    
    # 成都
    "文殊院": {
        "history": "始建于隋大业年间（605-618 年），是川西著名佛教寺院。供奉文殊菩萨，是智慧的象征。",
        "main_deity": "文殊菩萨",
        "prayer_directions": ["求智慧", "求学业", "求平安"],
        "specialties": ["川西名刹", "隋代古刹", "国家级文保", "免费开放"],
        "rating": 4.7
    },
    "武侯祠": {
        "history": "始建于蜀汉建兴六年（228 年），是纪念诸葛亮、刘备等蜀汉英雄的祠庙。是中国唯一的君臣合祀祠庙。",
        "main_deity": "诸葛亮、刘备",
        "prayer_directions": ["求智慧", "求事业", "求学业", "求平安"],
        "specialties": ["三国文化圣地", "君臣合祀", "国家级文保", "4A 景区"],
        "rating": 4.8
    },
    
    # 西安
    "大雁塔": {
        "history": "始建于唐永徽三年（652 年），是玄奘法师为保存从印度带回的佛经而建。是西安的标志性建筑。",
        "main_deity": "释迦牟尼佛",
        "prayer_directions": ["求平安", "求智慧", "求学业"],
        "specialties": ["玄奘法师", "唐代古塔", "世界遗产", "西安地标"],
        "rating": 4.8
    },
    "大兴善寺": {
        "history": "始建于西晋泰始二年（266 年），是中国佛教密宗祖庭。隋唐时期成为全国翻译佛经的中心。",
        "main_deity": "释迦牟尼佛",
        "prayer_directions": ["求平安", "求智慧", "求健康"],
        "specialties": ["密宗祖庭", "西晋古刹", "国家级文保", "佛经翻译中心"],
        "rating": 4.6
    },
    
    # 南京
    "鸡鸣寺": {
        "history": "始建于西晋永康元年（300 年），是南京最古老的梵刹之一。相传梁武帝曾四次到此舍身为僧。",
        "main_deity": "观音菩萨",
        "prayer_directions": ["求姻缘", "求平安", "求健康"],
        "specialties": ["南京最古梵刹", "求姻缘灵验", "樱花大道", "南朝古刹"],
        "rating": 4.7
    },
    "夫子庙": {
        "history": "始建于宋景祐元年（1034 年），是供奉孔子的文庙。位于秦淮风光带核心，是江南文化中心。",
        "main_deity": "孔子",
        "prayer_directions": ["求学业", "求智慧", "求考试", "求事业"],
        "specialties": ["江南文化圣地", "秦淮风光", "四大文庙", "国家级文保"],
        "rating": 4.7
    },
    
    # 武汉
    "归元寺": {
        "history": "始建于清顺治十五年（1658 年），是武汉四大丛林之首。以五百罗汉堂闻名，数罗汉是特色活动。",
        "main_deity": "释迦牟尼佛",
        "prayer_directions": ["求平安", "求健康", "求事业"],
        "specialties": ["五百罗汉", "武汉四大丛林", "清代古刹", "国家级文保"],
        "rating": 4.7
    },
    
    # 苏州
    "寒山寺": {
        "history": "始建于南朝梁天监年间（502-519 年），因唐代诗人张继的《枫桥夜泊》而闻名天下。",
        "main_deity": "释迦牟尼佛",
        "prayer_directions": ["求平安", "求健康", "求智慧"],
        "specialties": ["枫桥夜泊", "唐代古刹", "新年钟声", "国家级文保"],
        "rating": 4.7
    },
    "虎丘": {
        "history": "始建于春秋时期，是吴王阖闾的陵墓。苏东坡说'到苏州不游虎丘，乃憾事也'。",
        "main_deity": "观音菩萨",
        "prayer_directions": ["求平安", "求健康", "求事业"],
        "specialties": ["吴王陵墓", "云岩寺塔", "苏东坡推荐", "5A 景区"],
        "rating": 4.7
    },
    
    # 福州
    "涌泉寺": {
        "history": "始建于唐建中四年（783 年），是鼓山的主寺。以'寺藏三宝'闻名，是福建著名古刹。",
        "main_deity": "释迦牟尼佛",
        "prayer_directions": ["求平安", "求健康", "求智慧"],
        "specialties": ["鼓山主寺", "唐代古刹", "寺藏三宝", "国家级文保"],
        "rating": 4.7
    },
    
    # 厦门
    "南普陀寺": {
        "history": "始建于唐代末年（约 900 年），是闽南著名佛寺。因供奉观音菩萨，又称'观音道场'。",
        "main_deity": "观音菩萨",
        "prayer_directions": ["求平安", "求子", "求姻缘", "求健康"],
        "specialties": ["观音道场", "闽南名刹", "厦门大学旁", "免费开放"],
        "rating": 4.8
    },
    
    # 天津
    "天后宫": {
        "history": "始建于元泰定三年（1326 年），是中国三大妈祖庙之一。是天津市区最古老的建筑群。",
        "main_deity": "妈祖（林默娘）",
        "prayer_directions": ["求平安", "求出海平安", "求子", "求姻缘"],
        "specialties": ["三大妈祖庙", "元代古建", "天津最古", "国家级文保"],
        "rating": 4.6
    },
    
    # 重庆
    "罗汉寺": {
        "history": "始建于北宋治平年间（1064-1067 年），因电影《疯狂的石头》而闻名。以五百罗汉堂著称。",
        "main_deity": "释迦牟尼佛",
        "prayer_directions": ["求平安", "求健康", "求事业"],
        "specialties": ["五百罗汉", "疯狂的石头", "宋代古刹", "市中心"],
        "rating": 4.5
    },
    
    # 长沙
    "岳麓书院": {
        "history": "始建于北宋开宝九年（976 年），是中国四大书院之一。朱熹、张栻曾在此讲学。",
        "main_deity": "孔子",
        "prayer_directions": ["求学业", "求智慧", "求考试"],
        "specialties": ["四大书院", "朱熹讲学", "千年学府", "国家级文保"],
        "rating": 4.7
    },
    "开福寺": {
        "history": "始建于五代后唐明宗天成二年（927 年），是长沙著名古刹。香火极盛，求姻缘灵验。",
        "main_deity": "释迦牟尼佛",
        "prayer_directions": ["求姻缘", "求平安", "求健康"],
        "specialties": ["求姻缘灵验", "五代古刹", "长沙名刹", "省级文保"],
        "rating": 4.6
    },
    
    # 昆明
    "圆通寺": {
        "history": "始建于唐代南诏年间（约 800 年），是云南最大佛教寺院。以圆通山樱花闻名。",
        "main_deity": "观音菩萨",
        "prayer_directions": ["求平安", "求健康", "求智慧"],
        "specialties": ["云南最大佛寺", "唐代古刹", "圆通樱花", "省级文保"],
        "rating": 4.6
    },
    
    # 青岛
    "崂山太清宫": {
        "history": "始建于西汉建元元年（前 140 年），是道教全真派重要道场。蒲松龄曾在此居住写作。",
        "main_deity": "三清",
        "prayer_directions": ["求平安", "求健康", "求长寿"],
        "specialties": ["道教名观", "西汉古观", "蒲松龄故居", "5A 景区"],
        "rating": 4.7
    },
    
    # 沈阳
    "实胜寺": {
        "history": "始建于清崇德三年（1638 年），是东北地区著名的藏传佛教寺院。皇太极敕建。",
        "main_deity": "释迦牟尼佛",
        "prayer_directions": ["求平安", "求健康", "求事业"],
        "specialties": ["皇家寺院", "清代古刹", "东北名刹", "国家级文保"],
        "rating": 4.5
    },
    
    # 太原
    "晋祠": {
        "history": "始建于北魏时期（约 500 年），是为纪念晋国开国诸侯唐叔虞而建。是中国现存最早的皇家祭祀园林。",
        "main_deity": "唐叔虞",
        "prayer_directions": ["求祖先保佑", "求事业", "求平安"],
        "specialties": ["皇家祭祀", "北魏古建", "晋水源头", "国家级文保"],
        "rating": 4.8
    },
    
    # 郑州
    "少林寺": {
        "history": "始建于北魏太和十九年（495 年），是佛教禅宗祖庭和少林武术发源地。被誉为'天下第一名刹'。",
        "main_deity": "达摩祖师",
        "prayer_directions": ["求平安", "求健康", "求事业", "求学业"],
        "specialties": ["禅宗祖庭", "少林武术", "北魏古刹", "世界遗产"],
        "rating": 4.8
    },
    
    # 济南
    "千佛山": {
        "history": "始建于唐代，因山上有千尊佛像而得名。是济南三大名胜之一。",
        "main_deity": "释迦牟尼佛",
        "prayer_directions": ["求平安", "求健康", "求事业"],
        "specialties": ["千尊佛像", "济南名胜", "唐代古刹", "4A 景区"],
        "rating": 4.6
    },
    
    # 哈尔滨
    "极乐寺": {
        "history": "始建于民国十二年（1923 年），是东北地区著名佛教寺院。建筑风格独特。",
        "main_deity": "释迦牟尼佛",
        "prayer_directions": ["求平安", "求健康", "求事业"],
        "specialties": ["东北名刹", "民国建筑", "风格独特", "省级文保"],
        "rating": 4.5
    },
    
    # 海口
    "五公祠": {
        "history": "始建于明代，是为纪念唐宋时期被贬到海南的五位名臣而建。",
        "main_deity": "五公",
        "prayer_directions": ["求学业", "求事业", "求平安"],
        "specialties": ["海南名胜", "明代古建", "五公文化", "国家级文保"],
        "rating": 4.5
    }
}

# 按类型补充默认文化信息
DEFAULT_CULTURE = {
    "佛教": {
        "prayer_directions": ["求平安", "求健康", "求智慧", "求事业"],
        "common_deities": ["释迦牟尼佛", "观音菩萨", "文殊菩萨", "普贤菩萨", "地藏菩萨"]
    },
    "道教": {
        "prayer_directions": ["求平安", "求健康", "求财运", "求长寿"],
        "common_deities": ["三清", "玉皇大帝", "太上老君", "吕洞宾", "关帝"]
    },
    "伊斯兰教": {
        "prayer_directions": ["求平安", "求健康", "求事业", "求家庭和睦"],
        "common_deities": ["真主安拉"]
    },
    "儒教": {
        "prayer_directions": ["求学业", "求智慧", "求考试", "求事业"],
        "common_deities": ["孔子", "孟子", "文昌帝君"]
    },
    "民间信仰": {
        "prayer_directions": ["求平安", "求财运", "求健康", "求事业"],
        "common_deities": ["土地公", "财神", "城隍爷", "妈祖", "关帝"]
    },
    "祠堂": {
        "prayer_directions": ["求祖先保佑", "求家族兴旺", "求事业", "求学业"],
        "common_deities": ["列祖列宗"]
    }
}


def enrich_temple(temple):
    """为单个寺庙补充文化信息"""
    name = temple.get("name", "")
    temple_type = temple.get("temple_type", "")
    
    # 1. 检查是否在著名寺庙数据库中
    culture = {}
    if name in FAMOUS_TEMPLES:
        culture = FAMOUS_TEMPLES[name].copy()
    else:
        # 2. 根据类型补充默认信息
        base_type = temple_type.split("/")[0]  # 处理复合类型
        if base_type in DEFAULT_CULTURE:
            culture["prayer_directions"] = DEFAULT_CULTURE[base_type]["prayer_directions"]
            culture["main_deity"] = DEFAULT_CULTURE[base_type]["common_deities"][0]
            culture["specialties"] = [f"{base_type}场所"]
            culture["rating"] = 4.3  # 默认评分
        
        # 3. 根据名称关键词补充
        if "观音" in name or "普陀" in name:
            culture["main_deity"] = "观音菩萨"
            culture["prayer_directions"] = ["求平安", "求子", "求姻缘", "求健康"]
        elif "文殊" in name:
            culture["main_deity"] = "文殊菩萨"
            culture["prayer_directions"] = ["求智慧", "求学业", "求考试"]
        elif "财神" in name or "关帝" in name:
            culture["main_deity"] = "财神"
            culture["prayer_directions"] = ["求财运", "求事业", "求平安"]
        elif "城隍" in name:
            culture["main_deity"] = "城隍爷"
            culture["prayer_directions"] = ["求平安", "求事业", "求财运"]
        elif "妈祖" in name or "天后" in name:
            culture["main_deity"] = "妈祖（林默娘）"
            culture["prayer_directions"] = ["求平安", "求出海平安", "求子"]
        elif "孔庙" in name or "文庙" in name:
            culture["main_deity"] = "孔子"
            culture["prayer_directions"] = ["求学业", "求智慧", "求考试"]
    
    # 4. 合并到寺庙数据
    temple["history"] = culture.get("history", "")
    temple["main_deity"] = culture.get("main_deity", "")
    temple["prayer_directions"] = culture.get("prayer_directions", [])
    temple["specialties"] = culture.get("specialties", [])
    temple["rating"] = culture.get("rating", temple.get("rating"))
    temple["data_level"] = "standard"  # 标准数据
    
    # 5. 标记是否为著名寺庙
    temple["is_famous"] = name in FAMOUS_TEMPLES
    
    return temple


def main():
    print("📚 开始补充文化信息...")
    print(f"📂 输入文件：{INPUT_FILE}")
    print(f"📂 输出文件：{OUTPUT_FILE}")
    print("-" * 50)
    
    # 读取数据
    print("📖 读取清洗后的数据...")
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    total_count = data.get("total", len(data.get("temples", [])))
    print(f"✅ 待处理：{total_count} 座寺庙")
    
    # 补充文化信息
    print("📚 开始补充文化信息...")
    enriched_temples = []
    famous_count = 0
    
    for i, temple in enumerate(data.get("temples", [])):
        enriched_temple = enrich_temple(temple)
        enriched_temples.append(enriched_temple)
        
        if enriched_temple.get("is_famous", False):
            famous_count += 1
        
        # 进度显示
        if (i + 1) % 1000 == 0:
            print(f"  进度：{i+1}/{total_count} ({(i+1)/total_count*100:.1f}%)")
    
    # 统计
    print(f"\n✅ 文化信息补充完成！")
    print(f"🌟 著名寺庙：{famous_count} 座")
    print(f"📝 普通寺庙：{total_count - famous_count} 座")
    
    # 保存结果
    print(f"\n💾 保存数据...")
    output_data = {
        "total": len(enriched_temples),
        "famous_count": famous_count,
        "crawl_time": datetime.now().isoformat(),
        "source": "高德地图 API + 文化数据库",
        "temples": enriched_temples
    }
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 数据已保存至：{OUTPUT_FILE}")
    print(f"📊 文件大小：{len(json.dumps(output_data, ensure_ascii=False))/1024/1024:.2f} MB")
    
    # 显示著名寺庙列表
    print(f"\n🌟 部分著名寺庙示例:")
    famous_list = list(FAMOUS_TEMPLES.keys())[:10]
    for name in famous_list:
        print(f"   - {name}")
    if len(FAMOUS_TEMPLES) > 10:
        print(f"   ... 共{len(FAMOUS_TEMPLES)}座")
    
    print("\n🎉 全部完成！")


if __name__ == "__main__":
    main()
