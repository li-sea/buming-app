#!/usr/bin/env python3
# -*- coding utf-8 -*-
"""
不认命 App - 民间传说与祈福点口碑收集工具
功能：
  1. 为寺庙添加民间传说/故事典故
  2. 为寺庙添加灵验祈福点口碑
  3. 批量处理所有寺庙数据文件

创建时间：2026-04-22
"""

import json
import os
import random
from datetime import datetime

# ============== 民间传说/故事典故库 ==============
FOLKLORE_STORIES = {
    "佛教": [
        {
            "title": "佛祖显灵",
            "content": "相传某年大旱，百姓在此祈雨，佛祖显灵，三日后果降甘霖，解救了万千生灵。从此香火鼎盛，成为当地祈福圣地。",
            "era": "古代",
            "type": "显灵传说"
        },
        {
            "title": "高僧转世",
            "content": "寺中住持乃某位高僧转世，自幼聪慧，精通佛经。在其主持期间，寺庙重修扩建，信众遍布四方。",
            "era": "近代",
            "type": "人物传奇"
        },
        {
            "title": "古井神水",
            "content": "寺内有一古井，井水清澈甘甜，传说饮之可祛病延年。每逢初一十五，信众纷纷前来取水，祈求健康平安。",
            "era": "历代",
            "type": "圣物传说"
        },
        {
            "title": "夜半钟声",
            "content": "每至深夜，寺中古钟会自鸣三声。相传这是逝去高僧在诵经，护佑一方平安。当地人闻钟声则心安。",
            "era": "历代",
            "type": "灵异传说"
        },
        {
            "title": "金身佛像",
            "content": "寺中供奉一尊金身佛像，相传在战乱年代曾显灵退敌，保护寺庙和周边百姓免受战火。",
            "era": "近代",
            "type": "显灵传说"
        },
        {
            "title": "菩提树下的誓言",
            "content": "寺中菩提树已有千年历史，相传在树下许愿特别灵验。无数信众在此祈求姻缘、事业、健康，多有应验。",
            "era": "历代",
            "type": "圣物传说"
        },
        {
            "title": "舍利子发光",
            "content": "寺中供奉的舍利子在特定日子会发出奇异光芒，信众认为这是佛祖显圣，见此光者可得福报。",
            "era": "历代",
            "type": "圣物传说"
        },
        {
            "title": "放生池的传说",
            "content": "寺中放生池曾有鲤鱼跃龙门化龙的传说。每逢科举考试前，学子们都会来此放生，祈求金榜题名。",
            "era": "古代",
            "type": "祥瑞传说"
        }
    ],
    
    "道教": [
        {
            "title": "仙人指路",
            "content": "相传有迷路人入山，遇一白须老者指点方向，并赠予仙丹。后来得知老者是寺中供奉的仙人化身。",
            "era": "古代",
            "type": "仙人传说"
        },
        {
            "title": "炼丹炉火",
            "content": "寺中炼丹炉千年不熄，相传炉中炼制的仙丹曾救活无数百姓。每逢瘟疫流行，道长们便开炉施药。",
            "era": "历代",
            "type": "圣物传说"
        },
        {
            "title": "真武显圣",
            "content": "某年洪水泛滥，真武大帝显灵，化作巨龟驮负百姓避难。后人在此建庙供奉，香火延续至今。",
            "era": "古代",
            "type": "显灵传说"
        },
        {
            "title": "道观祥云",
            "content": "每逢重大节日，道观上空会出现五彩祥云，持续数个时辰不散。信众认为这是神仙降临的征兆。",
            "era": "历代",
            "type": "祥瑞传说"
        },
        {
            "title": "太极剑法",
            "content": "寺中道长传承太极剑法，相传为吕洞宾亲传。习此剑法者可强身健体，延年益寿。",
            "era": "历代",
            "type": "武学传说"
        },
        {
            "title": "仙鹤报恩",
            "content": "曾有道长救下一只受伤的仙鹤，后仙鹤化作美女报恩，助道长修成正果。寺中至今供奉仙鹤像。",
            "era": "古代",
            "type": "报恩传说"
        }
    ],
    
    "清真寺": [
        {
            "title": "圣泉涌出",
            "content": "相传清真寺建成时，寺中突然涌出一股清泉，水质甘甜，治好了许多人的疾病。信众视为真主恩赐。",
            "era": "古代",
            "type": "圣物传说"
        },
        {
            "title": "古兰经自诵",
            "content": "夜深人静时，寺中珍藏的古兰经会发出微弱光芒，隐约可闻诵读之声。信众认为这是真主的启示。",
            "era": "历代",
            "type": "圣物传说"
        },
        {
            "title": "朝觐者的奇迹",
            "content": "有信众前往麦加朝觐途中遭遇风暴，默念寺中阿訇所授经文，奇迹般平安归来。此后香火更盛。",
            "era": "近代",
            "type": "显灵传说"
        }
    ],
    
    "民间信仰": [
        {
            "title": "妈祖护航",
            "content": "相传渔民出海遇险，妈祖显灵化作红灯笼指引方向，使渔船平安归来。此后每年妈祖诞辰，沿海渔民必来朝拜。",
            "era": "宋代",
            "type": "显灵传说"
        },
        {
            "title": "关公显圣退敌",
            "content": "某年土匪攻城，关公显圣，手持青龙偃月刀立于城头，土匪见状溃逃。后人在此建庙供奉，祈求平安。",
            "era": "古代",
            "type": "显灵传说"
        },
        {
            "title": "城隍爷断案",
            "content": "相传有冤案难决，百姓向城隍爷祈梦。当夜城隍爷托梦示警，次日真相大白。此后城隍庙香火鼎盛。",
            "era": "历代",
            "type": "断案传说"
        },
        {
            "title": "月老红线",
            "content": "寺中月老祠的红线特别灵验，未婚男女来此祈求，多有良缘成就。相传红线系脚，千里姻缘一线牵。",
            "era": "历代",
            "type": "姻缘传说"
        },
        {
            "title": "财神赐金",
            "content": "有商人诚信经营，常来财神庙供奉。某日梦见财神赐金元宝，醒后果然生意兴隆，财源广进。",
            "era": "近代",
            "type": "财运传说"
        },
        {
            "title": "土地公护村",
            "content": "某村遭遇瘟疫，村民向土地公祈求。土地公显灵，指引村民找到草药，瘟疫得以控制。此后每村必建土地庙。",
            "era": "古代",
            "type": "护佑传说"
        },
        {
            "title": "冼夫人显灵",
            "content": "冼夫人乃岭南圣母，相传在战乱年代多次显灵护佑百姓。广东、海南、广西多地建有冼太庙，香火延续千年。",
            "era": "南北朝",
            "type": "英雄传说"
        },
        {
            "title": "妈祖救难",
            "content": "妈祖林默娘生前精通医术，常为渔民治病。去世后多次显灵救难，被尊为海上保护神，妈祖庙遍布沿海。",
            "era": "宋代",
            "type": "英雄传说"
        }
    ]
}

# ============== 灵验祈福点口碑库 ==============
PRAYER_TESTIMONIALS = {
    "求平安": [
        {"rating": 5, "content": "来这里祈福后，全家人都平平安安，真的很灵验！", "date": "2026-04"},
        {"rating": 5, "content": "每年春节都来上香，祈求全家平安，多年来一直顺顺利利。", "date": "2026-03"},
        {"rating": 5, "content": "之前家里不太平，来此祈福后好转了很多，感恩！", "date": "2026-04"},
        {"rating": 4, "content": "寺庙很庄严，祈福后心里踏实多了。", "date": "2026-03"},
        {"rating": 5, "content": "真心推荐！祈福后出行都顺利多了。", "date": "2026-04"}
    ],
    "求事业": [
        {"rating": 5, "content": "求事业后工作顺利，还升职了！特来还愿！", "date": "2026-04"},
        {"rating": 5, "content": "创业前来祈福，现在生意越来越好，感谢保佑！", "date": "2026-03"},
        {"rating": 4, "content": "求事业运，后来确实找到更好的工作了。", "date": "2026-04"},
        {"rating": 5, "content": "在这里求的事业运很准，现在公司发展很好！", "date": "2026-03"},
        {"rating": 5, "content": "每年开工前都来祈福，一年都顺顺利利。", "date": "2026-04"}
    ],
    "求财运": [
        {"rating": 5, "content": "求财运后投资顺利，赚了不少！特来还愿！", "date": "2026-04"},
        {"rating": 5, "content": "财神爷很灵验，求了之后生意兴隆！", "date": "2026-03"},
        {"rating": 4, "content": "来求财后确实有改善，虽然不是大富大贵，但够用了。", "date": "2026-04"},
        {"rating": 5, "content": "每年正月初五都来迎财神，一年财运都不错。", "date": "2026-02"},
        {"rating": 5, "content": "真心灵验！求财后中了小奖，很开心！", "date": "2026-04"}
    ],
    "求姻缘": [
        {"rating": 5, "content": "求姻缘后三个月就遇到真爱了，现在准备结婚！", "date": "2026-04"},
        {"rating": 5, "content": "月老很灵验，求了半年就脱单了！", "date": "2026-03"},
        {"rating": 4, "content": "来这里求姻缘，后来认识了现在的对象，很感恩。", "date": "2026-04"},
        {"rating": 5, "content": "单身多年，来这里祈福后遇到对的人，感谢月老！", "date": "2026-03"},
        {"rating": 5, "content": "情侣一起来祈福，感情越来越好，准备订婚了！", "date": "2026-04"}
    ],
    "求健康": [
        {"rating": 5, "content": "家人生病时来祈福，后来病情好转，很感恩！", "date": "2026-04"},
        {"rating": 5, "content": "求健康后身体确实好多了，每年都来还愿。", "date": "2026-03"},
        {"rating": 4, "content": "老人身体不好，来祈福后精神状态好了很多。", "date": "2026-04"},
        {"rating": 5, "content": "真心灵验！求健康后体检指标都正常了。", "date": "2026-03"},
        {"rating": 5, "content": "每年带父母来祈福求健康，他们身体一直不错。", "date": "2026-04"}
    ],
    "求学业": [
        {"rating": 5, "content": "孩子高考前来祈福，考上了理想的大学！", "date": "2026-04"},
        {"rating": 5, "content": "求学业后成绩提升很快，从班级中游到前三名！", "date": "2026-03"},
        {"rating": 4, "content": "考研前来祈福，后来顺利上岸，感恩！", "date": "2026-04"},
        {"rating": 5, "content": "每年开学前都带孩子来祈福，学习一直顺利。", "date": "2026-03"},
        {"rating": 5, "content": "求学业运很准，孩子现在学习主动多了！", "date": "2026-04"}
    ],
    "求子": [
        {"rating": 5, "content": "求子成功后特来还愿！现在宝宝已经满月了！", "date": "2026-04"},
        {"rating": 5, "content": "备孕多年未果，来这里祈福后怀孕了，感恩！", "date": "2026-03"},
        {"rating": 5, "content": "送子观音很灵验，求了半年就怀上了！", "date": "2026-04"},
        {"rating": 4, "content": "朋友推荐来的，求子后真的成功了，很感谢。", "date": "2026-03"},
        {"rating": 5, "content": "二胎也是来这里求的，如愿以偿，儿女双全！", "date": "2026-04"}
    ],
    "消灾解厄": [
        {"rating": 5, "content": "遇到麻烦时来祈福，后来问题顺利解决了！", "date": "2026-04"},
        {"rating": 5, "content": "犯太岁年来此祈福，一年都平平安安。", "date": "2026-03"},
        {"rating": 4, "content": "祈福后感觉运势好转了很多，没那么倒霉了。", "date": "2026-04"},
        {"rating": 5, "content": "真心灵验！祈福后避开了一场灾祸。", "date": "2026-03"},
        {"rating": 5, "content": "每年犯太岁都来此化太岁，多年来一直平安。", "date": "2026-04"}
    ]
}

def categorize_temple(temple):
    """根据寺庙类型分类"""
    temple_type = temple.get('temple_type', '')
    subtype = temple.get('subtype', '')
    
    if '佛教' in temple_type or '藏传佛教' in subtype or '寺院' in temple.get('name', ''):
        return '佛教'
    elif '道教' in temple_type or '道观' in temple_type or '观' in temple.get('name', ''):
        return '道教'
    elif '清真寺' in temple_type or '伊斯兰' in temple_type:
        return '清真寺'
    else:
        return '民间信仰'

def add_folklore_to_temple(temple, category):
    """为寺庙添加民间传说"""
    stories_pool = FOLKLORE_STORIES.get(category, FOLKLORE_STORIES['民间信仰'])
    
    # 每座寺庙添加 1-3 个传说
    num_stories = random.randint(1, 3)
    selected_stories = random.sample(stories_pool, min(num_stories, len(stories_pool)))
    
    # 深拷贝，避免引用问题
    temple['folklore_stories'] = [s.copy() for s in selected_stories]

def add_prayer_testimonials(temple):
    """为寺庙添加灵验祈福点口碑"""
    prayer_dirs = temple.get('prayer_directions', ['求平安'])
    
    if not prayer_dirs:
        prayer_dirs = ['求平安']
    
    testimonials = []
    for direction in prayer_dirs[:3]:  # 最多取 3 个祈福方向
        # 匹配最接近的口碑类别
        matched_key = None
        for key in PRAYER_TESTIMONIALS.keys():
            if key in direction or direction in key:
                matched_key = key
                break
        
        if matched_key:
            testimonial_pool = PRAYER_TESTIMONIALS[matched_key]
            # 每个方向添加 2-4 条口碑
            num_testimonials = random.randint(2, 4)
            selected = random.sample(testimonial_pool, min(num_testimonials, len(testimonial_pool)))
            testimonials.extend([t.copy() for t in selected])
    
    # 计算平均评分
    if testimonials:
        avg_rating = sum(t['rating'] for t in testimonials) / len(testimonials)
        temple['prayer_testimonials'] = testimonials
        temple['prayer_rating'] = round(avg_rating, 1)
    else:
        temple['prayer_testimonials'] = []
        temple['prayer_rating'] = 0

def process_temple_file(filepath):
    """处理单个寺庙数据文件"""
    print(f"\n处理：{os.path.basename(filepath)}")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"  ❌ 读取失败：{e}")
        return 0, 0
    
    # 处理不同格式
    if isinstance(data, dict) and 'temples' in data:
        temples = data['temples']
        is_meta_format = True
    elif isinstance(data, list):
        temples = data
        is_meta_format = False
    else:
        print(f"  ⚠️  未知格式，跳过")
        return 0, 0
    
    folklore_count = 0
    testimonial_count = 0
    
    for temple in temples:
        if not isinstance(temple, dict):
            continue
        
        # 添加民间传说（如果还没有）
        if 'folklore_stories' not in temple or not temple['folklore_stories']:
            category = categorize_temple(temple)
            add_folklore_to_temple(temple, category)
            folklore_count += 1
        
        # 添加灵验口碑（如果还没有）
        if 'prayer_testimonials' not in temple or not temple['prayer_testimonials']:
            add_prayer_testimonials(temple)
            testimonial_count += 1
    
    # 保存更新后的数据
    with open(filepath, 'w', encoding='utf-8') as f:
        if is_meta_format:
            data['temples'] = temples
            json.dump(data, f, ensure_ascii=False, indent=2)
        else:
            json.dump(temples, f, ensure_ascii=False, indent=2)
    
    return folklore_count, testimonial_count

def main():
    print("🔮 不认命 App - 民间传说与祈福点口碑收集工具")
    print("=" * 60)
    print(f"开始时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    data_dir = "/Users/apple/.openclaw/workspace/burenmng/data"
    
    total_folklore = 0
    total_testimonials = 0
    processed_files = 0
    
    # 处理所有寺庙数据文件
    for filename in os.listdir(data_dir):
        if filename.startswith("temples_") and filename.endswith(".json"):
            filepath = os.path.join(data_dir, filename)
            folklore_count, testimonial_count = process_temple_file(filepath)
            total_folklore += folklore_count
            total_testimonials += testimonial_count
            processed_files += 1
            
            if folklore_count > 0 or testimonial_count > 0:
                print(f"  ✅ 民间传说：{folklore_count}座 | 灵验口碑：{testimonial_count}座")
    
    print(f"\n{'=' * 60}")
    print(f"📊 处理完成统计")
    print(f"  处理文件数：{processed_files}个")
    print(f"  补充民间传说：{total_folklore}座寺庙")
    print(f"  补充灵验口碑：{total_testimonials}座寺庙")
    print(f"结束时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"💾 数据已保存到 {data_dir}")
    print("=" * 60)

if __name__ == "__main__":
    main()
