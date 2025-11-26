#!/usr/bin/env python3
"""
Fix Chinese base words to ensure they are single words, not phrases.
"""

import csv
import re

# Define the fixes for each pack
# Format: pack_number: new_base_words_array
PACK_FIXES = {
    # Pack 2: Personal Pronouns - remove phrase pronouns
    2: "[我,你,他,她,它,我们,你们,他们,她们,咱们,自己,别人,人家,大家,谁]",

    # Pack 14: Emergency - fix phrases
    14: "[救命,帮忙,紧急,危险,警察,注意,医院,厕所,出口,丢失,迷路,安全,疼痛,难受,求助]",

    # Pack 16: Days of Week - proper structure with full day names
    16: "[星期一,星期二,星期三,星期四,星期五,星期六,星期日,周,周末,工作日,礼拜,每周]",

    # Pack 23: Daily Actions - fix "起" to "起床"
    23: "[起床,睡觉,洗脸,刷牙,洗澡,洗手,穿衣,脱衣,吃饭,喝水,上班,下班,上学,放学,回家,出门,休息]",

    # Pack 34: Weather - remove 很 from adjectives
    34: "[天气,晴天,阴天,下雨,下雪,刮风,打雷,闪电,大雾,结冰,温度,热,冷,暖和,凉快,预报]",

    # Pack 40: Health - fix phrase issues
    40: "[健康,生病,感冒,发烧,咳嗽,头疼,胃疼,受伤,流血,吃药,打针,休息,就医,康复,严重]",

    # Pack 47: Hobbies - convert to single words/activities
    47: "[阅读,电影,音乐,运动,旅游,摄影,绘画,唱歌,跳舞,游泳,爬山,钓鱼,购物,游戏,网络]",

    # Pack 54: Opinions & Views - remove pronouns and fix phrases
    54: "[觉得,认为,同意,反对,主意,道理,观点,角度,总结,看法,意见]",

    # Pack 55: Making Plans - fix phrases
    55: "[打算,计划,决定,安排,日期,时间,空闲,改天,见面,约定]",

    # Pack 56: Expressing Needs - remove negation forms
    56: "[需要,想要,必须,应该,不必,急需,渴望,期待]",

    # Pack 57: Asking for Help - replace fragments with proper words
    57: "[帮助,请求,感谢,乐意,问题,能力,办法,自己]",

    # Pack 58: Giving Directions - fix phrases
    58: "[直走,左转,右转,路口,前方,右侧,距离,远近,方向]",

    # Pack 59: Describing Situations - remove phrases
    59: "[情况,正常,复杂,简单,进行,结束,开始,完成,顺利]",

    # Pack 60: Talking About Problems - fix phrase issues
    60: "[问题,麻烦,严重,解决,办法,困难,方案,处理]",

    # Pack 61: Money & Payments - fix phrases
    61: "[价格,贵,便宜,打折,现金,刷卡,支付,钱,发票]",

    # Pack 62: At Restaurant - fix fragments
    62: "[点菜,推荐,菜单,辣,咸,买单,打包,味道,服务员]",

    # Pack 63: At Hotel - fix phrases
    63: "[订房,入住,退房,房间,早餐,热水,打扫,服务,钥匙]",

    # Pack 64: At Airport - fix phrases
    64: "[登机,登机口,托运,行李,延误,取消,安检,大厅,提取]",

    # Pack 65: At Doctor - fix phrases
    65: "[不舒服,疼痛,头疼,胃疼,发烧,吃药,打针,休息,复查]",

    # Pack 66: Making Appointments - fix fragments
    66: "[预约,时间,明天,下周,取消,确认,准时,更改]",

    # Pack 67: Weather Conversations - fix phrases
    67: "[天气,下雨,太阳,风,冷,热,穿衣,雨伞]",

    # Pack 68: Phone Conversations - fix phrases
    68: "[喂,请问,在,不在,稍等,方便,信号,回电,挂断]",

    # Pack 69: Social Situations - keep as common expressions (idioms)
    69: "[认识,见面,好久不见,最近,老样子,聚会,联系,顺利]",

    # Pack 70: Invitations & Offers - fix phrases
    70: "[邀请,请客,一起,感谢,接受,改天,客气,拒绝]",

    # Pack 71: Agreeing & Disagreeing - fix phrases
    71: "[同意,反对,赞成,有理,支持,情况,部分,完全]",

    # Pack 72: Expressing Certainty - fix phrases
    72: "[确定,不确定,可能,应该,肯定,绝对,也许,大概]",

    # Pack 73: Time Expressions - fix phrases
    73: "[刚才,马上,稍等,以前,以后,进行,一直,完成]",

    # Pack 74: Frequency Expressions - fix phrases
    74: "[每天,经常,有时,很少,从不,总是,首次,最后]",

    # Pack 75: Describing Amounts - fix degree words
    75: "[很多,很少,足够,不够,刚好,太多,太少,差不多]",

    # Pack 76: Quality Descriptions - fix phrases
    76: "[质量,正品,假货,性价比,值得,优质,合格,品质]",

    # Pack 77: Making Comparisons - fix phrases
    77: "[比较,不如,差不多,不同,以前,预期,相同,更好]",

    # Pack 78: Expressing Preferences - keep simple forms
    78: "[喜欢,讨厌,最爱,无所谓,偏好,一般,选择,倾向]",

    # Pack 79: Giving Reasons - fix phrases
    79: "[因为,所以,原因,理由,解释,说明,由于,缘故]",

    # Pack 83: Time Expressions Advanced - fix phrases
    83: "[刚才,马上,稍等,以前,以后,之前,之后,完成,进行]",

    # Pack 84: Frequency & Duration - fix phrases
    84: "[每天,每次,经常,有时,很少,从不,一直,永远]",

    # Pack 85: Comparison & Degree - fix phrases
    85: "[比较,相同,不同,更加,最好,越来越,非常,相当]",

    # Pack 86: Cause & Effect - fix phrases
    86: "[因为,所以,由于,导致,造成,产生,关系,根据]",

    # Pack 87: Conditions & Assumptions - fix "只有这样"
    87: "[如果,假设,万一,除非,只要,否则,不然,虽然]",

    # Pack 89: Modal Particles - keep particles but remove phrases
    89: "[吗,吧,呢,啊,嘛,好,行,可以,原来,算了]",

    # Pack 92: Describing Things - fix "什么东西"
    92: "[东西,事情,类型,样子,形状,大小,材料,质量]",

    # Pack 94: Extent & Degree - fix "太好了"
    94: "[非常,很,太,有点,差不多,足够,不够,特别]",

    # Pack 96: Describing Problems - fix phrases
    96: "[问题,困难,麻烦,差错,故障,不足,严重,棘手]",

    # Pack 97: Solutions & Methods - fix phrases
    97: "[解决,办法,措施,改善,方法,计划,建议,方案]",

    # Pack 102: Describing Processes - fix phrases
    102: "[过程,步骤,阶段,环节,首先,然后,最后,完成]",

    # Pack 104: Quality & Standards - fix "质量一般"
    104: "[品质,质量,标准,要求,检验,合格,优质,次品]",

    # Pack 105: Evaluation & Assessment - fix "个人认为"
    105: "[评价,评估,认为,显然,好像,估计,预计,判断]",

    # Pack 106: Abstract Concepts - fix "这个想法"
    106: "[想法,概念,原则,道理,意义,理想,梦想,观念]",
}

def fix_base_words():
    input_file = 'ChineseWords/ChineseWordsOverview.csv'
    output_file = 'ChineseWords/ChineseWordsOverview.csv'

    # Read the CSV
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)

    header = rows[0]
    base_words_col = header.index('Chinese_Base_Words')

    changes_made = []

    for i, row in enumerate(rows[1:], start=1):
        pack_num = int(row[0])
        if pack_num in PACK_FIXES:
            old_value = row[base_words_col]
            new_value = PACK_FIXES[pack_num]
            row[base_words_col] = new_value
            changes_made.append({
                'pack': pack_num,
                'title': row[1],
                'old': old_value,
                'new': new_value
            })

    # Write back
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    # Print summary
    print(f"Fixed {len(changes_made)} packs:")
    for change in changes_made:
        print(f"\nPack {change['pack']}: {change['title']}")
        print(f"  Before: {change['old'][:60]}...")
        print(f"  After:  {change['new'][:60]}...")

    return changes_made

if __name__ == '__main__':
    fix_base_words()
