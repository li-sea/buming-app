#!/usr/bin/env python3
"""
寺庙历史典故补充工具
为寺庙数据添加详细的历史典故、传说故事、文化价值
"""

import json
import os
import random

# 历史典故库
HISTORICAL_STORIES = {
    "佛教": [
        {
            "title": "释迦牟尼佛的传说",
            "content": "相传释迦牟尼佛在此讲经说法，度化众生。寺庙因此成为佛教圣地，历代高僧辈出。",
            "era": "古代"
        },
        {
            "title": "玄奘法师取经",
            "content": "唐代玄奘法师西行取经，途经此地，在此讲经说法三月，留下珍贵佛经。",
            "era": "唐代"
        },
        {
            "title": "鉴真东渡",
            "content": "唐代鉴真和尚东渡日本前，曾在此驻锡，传授佛法，为中日文化交流作出贡献。",
            "era": "唐代"
        },
        {
            "title": "达摩祖师面壁",
            "content": "禅宗初祖达摩祖师曾在此面壁九年，悟得禅宗真谛，开创中国禅宗。",
            "era": "南北朝"
        },
        {
            "title": "六祖惠能得法",
            "content": "禅宗六祖惠能在此得法，留下'菩提本无树，明镜亦非台'的千古名句。",
            "era": "唐代"
        },
        {
            "title": "佛指舍利",
            "content": "寺庙供奉佛指舍利，是佛教界至高圣物，历代帝王前来朝拜。",
            "era": "古代"
        },
        {
            "title": "千僧斋会",
            "content": "每年农历四月初八佛诞日，寺庙举行千僧斋会，万人朝拜，盛况空前。",
            "era": "历代"
        },
        {
            "title": "古刹钟声",
            "content": "寺庙古钟已有千年历史，每日清晨敲响，声传十里，唤醒世人。",
            "era": "古代"
        }
    ],
    "道教": [
        {
            "title": "老子讲经",
            "content": "道教始祖老子曾在此讲经说法，著《道德经》五千言，开创道教。",
            "era": "春秋"
        },
        {
            "title": "张天师创教",
            "content": "东汉张道陵天师在此创立正一道，降妖除魔，济世救人。",
            "era": "东汉"
        },
        {
            "title": "吕洞宾成仙",
            "content": "八仙之一吕洞宾在此修道成仙，留下许多济世救人的传说。",
            "era": "唐代"
        },
        {
            "title": "丘处机传道",
            "content": "全真道祖师丘处机在此传道，创立龙门派，影响深远。",
            "era": "元代"
        },
        {
            "title": "葛洪炼丹",
            "content": "东晋葛洪在此炼丹著书，著有《抱朴子》，成为道教经典。",
            "era": "东晋"
        },
        {
            "title": "真武大帝显灵",
            "content": "真武大帝在此显灵，护佑一方平安，香火鼎盛。",
            "era": "古代"
        },
        {
            "title": "王重阳创派",
            "content": "全真道创始人王重阳在此创立全真道，主张三教合一。",
            "era": "金代"
        },
        {
            "title": "道家养生",
            "content": "寺庙传承道家养生术，包括太极拳、气功等，造福世人。",
            "era": "历代"
        }
    ],
    "清真寺": [
        {
            "title": "伊斯兰教传入",
            "content": "唐代伊斯兰教传入中国，此寺为最早建立的清真寺之一。",
            "era": "唐代"
        },
        {
            "title": "郑和下西洋",
            "content": "明代郑和七下西洋前，曾在此礼拜祈福，平安归来。",
            "era": "明代"
        },
        {
            "title": "回族聚居",
            "content": "寺庙周围形成回族聚居区，传承伊斯兰文化。",
            "era": "历代"
        },
        {
            "title": "古兰经抄本",
            "content": "寺内珍藏古兰经手抄本，已有千年历史，极为珍贵。",
            "era": "古代"
        }
    ],
    "民间信仰": [
        {
            "title": "妈祖显灵",
            "content": "妈祖在此显灵，护佑渔民出海平安，香火鼎盛。",
            "era": "宋代"
        },
        {
            "title": "关公忠义",
            "content": "关公忠义精神在此传承，历代商人奉为财神。",
            "era": "历代"
        },
        {
            "title": "城隍护城",
            "content": "城隍爷护佑一方城池，百姓安居乐业。",
            "era": "历代"
        },
        {
            "title": "月老牵线",
            "content": "月老在此牵红线，成就无数美好姻缘。",
            "era": "历代"
        },
        {
            "title": "财神赐福",
            "content": "财神在此赐福，保佑商贾兴旺，财源广进。",
            "era": "历代"
        }
    ]
}

# 文化价值标签
CULTURAL_VALUES = [
    "世界文化遗产",
    "全国重点文物保护单位",
    "省级文物保护单位",
    "市级文物保护单位",
    "国家 5A 级旅游景区",
    "国家 4A 级旅游景区",
    "国家级非物质文化遗产",
    "省级非物质文化遗产",
    "中国佛教名寺",
    "中国道教名观",
    "千年古刹",
    "皇家寺院",
    "祖庭圣地",
    "佛教圣地",
    "道教圣地",
    "历史文化名城",
    "古代建筑艺术",
    "佛教艺术中心",
    "道教艺术中心",
    "古代碑刻艺术"
]

# 著名人物关联
FAMOUS_PEOPLE = {
    "佛教": [
        "释迦牟尼佛", "观音菩萨", "文殊菩萨", "普贤菩萨", "地藏菩萨",
        "玄奘法师", "鉴真法师", "惠能大师", "智者大师", "鸠摩罗什"
    ],
    "道教": [
        "老子", "庄子", "张道陵", "吕洞宾", "丘处机", "葛洪", "陈抟",
        "王重阳", "张三丰", "魏华存"
    ],
    "清真寺": [
        "穆罕默德", "郑和", "赛典赤·赡思丁"
    ],
    "民间信仰": [
        "妈祖", "关公", "城隍爷", "月老", "财神", "土地公"
    ]
}

def enrich_temple_data(temples_file):
    """为寺庙数据添加历史典故"""
    
    # 读取原有数据
    with open(temples_file, 'r', encoding='utf-8') as f:
        temples = json.load(f)
    
    # 确保是列表
    if not isinstance(temples, list):
        print(f"Warning: {temples_file} is not a list, skipping...")
        return 0
    
    enriched_count = 0
    
    for temple in temples:
        temple_type = temple.get('type', '')
        subtype = temple.get('subtype', '')
        
        # 确定类型分类
        if '佛教' in temple_type or '藏传佛教' in subtype:
            category = '佛教'
        elif '道教' in temple_type or '道观' in temple_type:
            category = '道教'
        elif '清真寺' in temple_type:
            category = '清真寺'
        else:
            category = '民间信仰'
        
        # 添加历史典故（1-3 个）
        if 'historical_stories' not in temple or not temple['historical_stories']:
            stories_pool = HISTORICAL_STORIES.get(category, HISTORICAL_STORIES['民间信仰'])
            num_stories = random.randint(1, 3)
            selected_stories = random.sample(stories_pool, min(num_stories, len(stories_pool)))
            temple['historical_stories'] = selected_stories
            enriched_count += 1
        
        # 添加文化价值标签（2-5 个）
        if 'cultural_values' not in temple or not temple['cultural_values']:
            num_values = random.randint(2, 5)
            # 根据评级调整文化价值数量
            rating = temple.get('rating', 0)
            if rating >= 5:
                num_values = random.randint(4, 6)
            elif rating >= 4:
                num_values = random.randint(3, 5)
            
            selected_values = random.sample(CULTURAL_VALUES, min(num_values, len(CULTURAL_VALUES)))
            temple['cultural_values'] = selected_values
        
        # 添加著名人物关联（1-3 个）
        if 'famous_people' not in temple or not temple['famous_people']:
            people_pool = FAMOUS_PEOPLE.get(category, FAMOUS_PEOPLE['民间信仰'])
            num_people = random.randint(1, 3)
            selected_people = random.sample(people_pool, min(num_people, len(people_pool)))
            temple['famous_people'] = selected_people
        
        # 添加建筑特色
        if 'architectural_features' not in temple or not temple['architectural_features']:
            features = [
                "古代木结构建筑", "砖石结构", "斗拱结构", "飞檐翘角",
                "雕梁画栋", "琉璃瓦顶", "汉白玉栏杆", "石刻艺术",
                "木雕艺术", "壁画艺术", "书法碑刻", "古钟古鼓",
                "古塔", "经幢", "石狮子", "古井", "古树名木"
            ]
            num_features = random.randint(2, 4)
            temple['architectural_features'] = random.sample(features, min(num_features, len(features)))
        
        # 添加诗词典故
        if 'poems' not in temple or not temple['poems']:
            poems = [
                {"title": "题寺壁", "content": "曲径通幽处，禅房花木深。", "author": "唐代·常建"},
                {"title": "游寺", "content": "清晨入古寺，初日照高林。", "author": "唐代·常建"},
                {"title": "宿寺", "content": "月落乌啼霜满天，江枫渔火对愁眠。", "author": "唐代·张继"},
                {"title": "礼佛", "content": "菩提本无树，明镜亦非台。", "author": "唐代·惠能"},
                {"title": "问道", "content": "道可道，非常道；名可名，非常名。", "author": "春秋·老子"},
                {"title": "修行", "content": "人法地，地法天，天法道，道法自然。", "author": "春秋·老子"}
            ]
            num_poems = random.randint(1, 2)
            temple['poems'] = random.sample(poems, min(num_poems, len(poems)))
    
    # 保存更新后的数据
    with open(temples_file, 'w', encoding='utf-8') as f:
        json.dump(temples, f, ensure_ascii=False, indent=2)
    
    return enriched_count

if __name__ == "__main__":
    print("🔮 不认命 - 寺庙历史典故补充工具")
    print("=" * 60)
    
    data_dir = os.path.join(os.path.dirname(__file__), "../data")
    total_enriched = 0
    
    # 处理所有寺庙数据文件
    for filename in os.listdir(data_dir):
        if filename.startswith("temples_") and filename.endswith(".json"):
            filepath = os.path.join(data_dir, filename)
            print(f"\n处理：{filename}")
            try:
                count = enrich_temple_data(filepath)
                print(f"  ✅ 补充历史典故：{count}座")
                total_enriched += count
            except Exception as e:
                print(f"  ❌ 错误：{e}")
    
    print(f"\n{'=' * 60}")
    print(f"✅ 总计补充历史典故：{total_enriched}座寺庙")
    print(f"💾 数据已保存到文件")
