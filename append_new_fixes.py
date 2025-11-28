#!/usr/bin/env python3
"""
Append new fixes found during Stage 3A review to EnglishFixTable.csv
"""

import csv

# New fixes to add (from comprehensive review)
new_fixes = [
    # Pack 16 - Question Words
    ("english", 16, "Question Words", 44, "chinese", "现在是几奌", "现在是几点", "Wrong character: 奌 should be 点 (o'clock)"),
    ("english", 16, "Question Words", 44, "pinyin", "xiàn zài shì jǐ diǎn", "xiàn zài shì jǐ diǎn", "Fix pinyin to match corrected Chinese (point not dian)"),

    # Pack 49 - Kitchen Items
    ("english", 49, "Kitchen Items", 7, "portuguese", "afundar", "pia", "Wrong word: afundar=verb sink/submerge, should be pia=noun kitchen sink"),
    ("english", 49, "Kitchen Items", 17, "chinese", "平移", "平底锅", "Wrong meaning: 平移=translate/pan(camera), should be 平底锅=cooking pan"),
    ("english", 49, "Kitchen Items", 17, "pinyin", "píng yí", "píng dǐ guō", "Fix pinyin to match corrected Chinese"),

    # Pack 51 - Household Chores
    ("english", 51, "Household Chores", 10, "chinese", "波兰", "擦亮", "Wrong meaning: 波兰=Poland(country), should be 擦亮=polish(verb)"),
    ("english", 51, "Household Chores", 10, "pinyin", "bō lán", "cā liàng", "Fix pinyin to match corrected Chinese"),

    # Pack 52 - More Food
    ("english", 52, "More Food", 12, "chinese", "石灰", "青柠", "Wrong meaning: 石灰=limestone, should be 青柠=lime(fruit)"),
    ("english", 52, "More Food", 12, "pinyin", "shí huī", "qīng níng", "Fix pinyin to match corrected Chinese"),
    ("english", 52, "More Food", 20, "chinese", "土耳其", "火鸡", "Wrong meaning: 土耳其=Turkey(country), should be 火鸡=turkey(bird)"),
    ("english", 52, "More Food", 20, "pinyin", "tǔ ěr qí", "huǒ jī", "Fix pinyin to match corrected Chinese"),

    # Pack 53 - Fruits
    ("english", 53, "Fruits", 12, "chinese", "石灰", "青柠", "Wrong meaning: 石灰=limestone, should be 青柠=lime(fruit)"),
    ("english", 53, "Fruits", 12, "pinyin", "shí huī", "qīng níng", "Fix pinyin to match corrected Chinese"),

    # Pack 54 - Vegetables
    ("english", 54, "Vegetables", 18, "chinese", "壁球", "南瓜", "Wrong meaning: 壁球=squash(sport), should be 南瓜=squash(vegetable)"),
    ("english", 54, "Vegetables", 18, "pinyin", "bì qiú", "nán guā", "Fix pinyin to match corrected Chinese"),

    # Pack 56 - Jobs 1
    ("english", 56, "Jobs 1", 56, "chinese", "银行银行家", "银行家", "Redundant: 银行 appears twice"),
    ("english", 56, "Jobs 1", 56, "pinyin", "yín háng yín háng jiā", "yín háng jiā", "Fix pinyin to match corrected Chinese"),

    # Pack 59 - Nature
    ("english", 59, "Nature", 15, "chinese", "摇滚", "石头", "Wrong meaning: 摇滚=rock music, should be 石头=rock/stone"),
    ("english", 59, "Nature", 15, "pinyin", "yáo gǔn", "shí tóu", "Fix pinyin to match corrected Chinese"),
    ("english", 59, "Nature", 18, "chinese", "明星", "星星", "Wrong meaning: 明星=celebrity, should be 星星=star in sky"),
    ("english", 59, "Nature", 18, "pinyin", "míng xīng", "xīng xīng", "Fix pinyin to match corrected Chinese"),

    # Pack 62 - Sports
    ("english", 62, "Sports", 7, "chinese", "运行", "跑步", "Wrong context: 运行=running(computer), should be 跑步=running(physical)"),
    ("english", 62, "Sports", 7, "pinyin", "yùn xíng", "pǎo bù", "Fix pinyin to match corrected Chinese"),
    ("english", 62, "Sports", 12, "chinese", "玩家", "球员", "Wrong context: 玩家=player(games), should be 球员=player(sports)"),
    ("english", 62, "Sports", 12, "pinyin", "wán jiā", "qiú yuán", "Fix pinyin to match corrected Chinese"),
    ("english", 62, "Sports", 13, "chinese", "匹配", "比赛", "Wrong meaning: 匹配=match/pair, should be 比赛=sports match"),
    ("english", 62, "Sports", 13, "pinyin", "pǐ pèi", "bǐ sài", "Fix pinyin to match corrected Chinese"),
    ("english", 62, "Sports", 16, "chinese", "种族", "赛跑", "Wrong meaning: 种族=race(ethnicity), should be 赛跑=race(running)"),
    ("english", 62, "Sports", 16, "pinyin", "zhǒng zú", "sài pǎo", "Fix pinyin to match corrected Chinese"),

    # Pack 63 - More Sports
    ("english", 63, "More Sports", 18, "chinese", "解决", "擒抱", "Wrong meaning: 解决=solve, should be 擒抱=tackle(sports)"),
    ("english", 63, "More Sports", 18, "pinyin", "jiě jué", "qín bào", "Fix pinyin to match corrected Chinese"),
    ("english", 63, "More Sports", 19, "chinese", "加班", "加时赛", "Wrong context: 加班=work overtime, should be 加时赛=sports overtime"),
    ("english", 63, "More Sports", 19, "pinyin", "jiā bān", "jiā shí sài", "Fix pinyin to match corrected Chinese"),
    ("english", 63, "More Sports", 21, "chinese", "继电器", "接力", "Wrong meaning: 继电器=relay(electrical), should be 接力=relay(race)"),
    ("english", 63, "More Sports", 21, "pinyin", "jì diàn qì", "jiē lì", "Fix pinyin to match corrected Chinese"),

    # Pack 64 - Entertainment
    ("english", 64, "Entertainment", 13, "chinese", "性能", "表演", "Wrong context: 性能=performance(machine), should be 表演=performance(artistic)"),
    ("english", 64, "Entertainment", 13, "pinyin", "xìng néng", "biǎo yǎn", "Fix pinyin to match corrected Chinese"),
    ("english", 64, "Entertainment", 15, "chinese", "风扇", "粉丝", "Wrong meaning: 风扇=electric fan, should be 粉丝=fan(enthusiast)"),
    ("english", 64, "Entertainment", 15, "pinyin", "fēng shàn", "fěn sī", "Fix pinyin to match corrected Chinese"),

    # Pack 65 - More Emotions
    ("english", 65, "More Emotions", 6, "chinese", "强调", "有压力", "Wrong part of speech: 强调=stress(verb), should be 有压力=stressed(adjective)"),
    ("english", 65, "More Emotions", 6, "pinyin", "qiáng diào", "yǒu yā lì", "Fix pinyin to match corrected Chinese"),

    # Pack 66 - Personality
    ("english", 66, "Personality", 10, "chinese", "病人", "有耐心的", "Wrong meaning: 病人=patient(noun hospital), should be 有耐心的=patient(adjective)"),
    ("english", 66, "Personality", 10, "pinyin", "bìng rén", "yǒu nài xīn de", "Fix pinyin to match corrected Chinese"),

    # Pack 67 - Physical Appearance
    ("english", 67, "Physical Appearance", 3, "chinese", "脂肪", "胖", "Wrong part of speech: 脂肪=fat(noun), should be 胖=fat(adjective)"),
    ("english", 67, "Physical Appearance", 3, "pinyin", "zhī fáng", "pàng", "Fix pinyin to match corrected Chinese"),
    ("english", 67, "Physical Appearance", 6, "chinese", "适合", "健康", "Wrong context: 适合=suitable, should be 健康=physically fit"),
    ("english", 67, "Physical Appearance", 6, "pinyin", "shì hé", "jiàn kāng", "Fix pinyin to match corrected Chinese"),
    ("english", 67, "Physical Appearance", 19, "chinese", "图", "身材", "Wrong meaning: 图=figure/diagram, should be 身材=body figure"),
    ("english", 67, "Physical Appearance", 19, "pinyin", "tú", "shēn cái", "Fix pinyin to match corrected Chinese"),

    # Pack 69 - Money & Banking (already has fixes but missing row 14)
    ("english", 69, "Money & Banking", 14, "chinese", "平衡", "余额", "Wrong context: 平衡=balance(equilibrium), should be 余额=account balance"),
    ("english", 69, "Money & Banking", 14, "pinyin", "píng héng", "yú é", "Fix pinyin to match corrected Chinese"),

    # Pack 72 - Verbs of Motion
    ("english", 72, "Verbs of Motion", 4, "chinese", "电梯", "举起", "Wrong part of speech: 电梯=elevator(noun), should be 举起=lift(verb)"),
    ("english", 72, "Verbs of Motion", 4, "pinyin", "diàn tī", "jǔ qǐ", "Fix pinyin to match corrected Chinese"),
    ("english", 72, "Verbs of Motion", 12, "chinese", "破折号", "冲刺", "Wrong meaning: 破折号=dash(punctuation), should be 冲刺=dash(run)"),
    ("english", 72, "Verbs of Motion", 12, "pinyin", "pò zhé hào", "chōng cì", "Fix pinyin to match corrected Chinese"),

    # Pack 78 - Conjunctions
    ("english", 78, "Conjunctions", 9, "chinese", "之后而", "当...时", "Contradictory: 之后=after but while=simultaneous, should be 当...时=while/when"),
    ("english", 78, "Conjunctions", 9, "pinyin", "zhī hòu ér", "dāng... shí", "Fix pinyin to match corrected Chinese"),

    # Pack 86 - Workplace Actions (already has some fixes but missing row 3 spanish/portuguese)
    ("english", 86, "Workplace Actions", 3, "spanish", "fuego", "despedir", "Wrong meaning: fuego=fire(flames), should be despedir=fire(employee)"),
    ("english", 86, "Workplace Actions", 3, "portuguese", "fogo", "demitir", "Wrong meaning: fogo=fire(flames), should be demitir=fire(employee)"),

    # Pack 89 - Relationships (already has fixes but missing row 21)
    ("english", 89, "Relationships", 21, "chinese", "债券", "纽带", "Wrong meaning: 债券=bond(financial), should be 纽带=bond(emotional)"),
    ("english", 89, "Relationships", 21, "pinyin", "zhài quàn", "niǔ dài", "Fix pinyin to match corrected Chinese"),

    # Pack 92 - Housing (row 3 already in fix table, but missing row 36)
    ("english", 92, "Housing", 36, "chinese", "不错的邻居", "不错的社区", "Wrong meaning: nice neighbor vs nice neighborhood for Housing theme"),
    ("english", 92, "Housing", 36, "pinyin", "bù cuò de lín jū", "bù cuò de shè qū", "Fix pinyin to match corrected Chinese"),

    # Pack 93 - News & Media (already has some fixes but missing row 9 portuguese)
    ("english", 93, "News & Media", 9, "portuguese", "pressione", "imprensa", "Wrong meaning: pressione=press button, should be imprensa=the press(journalism)"),

    # Pack 96 - Food Preparation (already has many fixes but missing row 6)
    ("english", 96, "Food Preparation", 6, "chinese", "刨丝器", "磨碎", "Wrong part of speech: 刨丝器=grater(noun tool), should be 磨碎=grate(verb)"),
    ("english", 96, "Food Preparation", 6, "pinyin", "páo sī qì", "mó suì", "Fix pinyin to match corrected Chinese"),

    # Pack 127 - Social Issues
    ("english", 127, "Social Issues", 14, "chinese", "包含", "包容", "Wrong word: 包含=contain/include, should be 包容=inclusion/inclusivity"),
    ("english", 127, "Social Issues", 14, "pinyin", "bāo hán", "bāo róng", "Fix pinyin to match corrected Chinese"),

    # Pack 132 - Formal Vocabulary 2
    ("english", 132, "Formal Vocabulary 2", 12, "chinese", "校长", "主要", "Wrong meaning: 校长=principal(person), should be 主要=principal(main/primary)"),
    ("english", 132, "Formal Vocabulary 2", 12, "pinyin", "xiào zhǎng", "zhǔ yào", "Fix pinyin to match corrected Chinese"),

    # Pack 136 - Academic Adjectives
    ("english", 136, "Academic Adjectives", 31, "chinese", "一致一致的性能", "一致的性能", "Duplication: 一致 appears twice"),
    ("english", 136, "Academic Adjectives", 31, "pinyin", "yī zhì yī zhì de xìng néng", "yī zhì de xìng néng", "Fix pinyin to match corrected Chinese"),
    ("english", 136, "Academic Adjectives", 33, "chinese", "相反反对意见", "相反的意见", "Redundant: both 相反 and 反对 mean opposition"),
    ("english", 136, "Academic Adjectives", 33, "pinyin", "xiāng fǎn fǎn duì yì jiàn", "xiāng fǎn de yì jiàn", "Fix pinyin to match corrected Chinese"),

    # Pack 137 - Academic Adjectives 2
    ("english", 137, "Academic Adjectives 2", 24, "chinese", "视", "取决于", "Incomplete: just 视 doesn't make sense, should be 取决于=depend on"),
    ("english", 137, "Academic Adjectives 2", 24, "pinyin", "shì", "qǔ jué yú", "Fix pinyin to match corrected Chinese"),
    ("english", 137, "Academic Adjectives 2", 25, "chinese", "而定取决于", "取决于", "Redundant: both 而定 and 取决于 mean depend on"),
    ("english", 137, "Academic Adjectives 2", 25, "pinyin", "ér dìng qǔ jué yú", "qǔ jué yú", "Fix pinyin to match corrected Chinese"),
    ("english", 137, "Academic Adjectives 2", 34, "chinese", "的积分中级", "中级水平", "Wrong word: 积分=integral/points not intermediate, should be 中级水平=intermediate level"),
    ("english", 137, "Academic Adjectives 2", 34, "pinyin", "de jī fēn zhōng jí", "zhōng jí shuǐ píng", "Fix pinyin to match corrected Chinese"),

    # Pack 141 - Research & Statistics
    ("english", 141, "Research & Statistics", 42, "chinese", "的有效性测试可靠性", "测试可靠性", "Confused mix: remove extra prefix, focus on reliability"),
    ("english", 141, "Research & Statistics", 42, "pinyin", "de yǒu xiào xìng cè shì kě kào xìng", "cè shì kě kào xìng", "Fix pinyin to match corrected Chinese"),
    ("english", 141, "Research & Statistics", 54, "chinese", "的分布统计异常值", "统计异常值", "Extra prefix that doesn't belong"),
    ("english", 141, "Research & Statistics", 54, "pinyin", "de fēn bù tǒng jì yì cháng zhí", "tǒng jì yì cháng zhí", "Fix pinyin to match corrected Chinese"),
    ("english", 141, "Research & Statistics", 60, "chinese", "之间的相关性计算中位数", "计算中位数", "Leftover text from previous row"),
    ("english", 141, "Research & Statistics", 60, "pinyin", "zhī jiān de xiāng guān xìng jì suàn zhōng wèi shù", "jì suàn zhōng wèi shù", "Fix pinyin to match corrected Chinese"),

    # Pack 142 - Psychology Basics
    ("english", 142, "Psychology Basics", 5, "chinese", "内存", "记忆", "Wrong context: 内存=RAM/computer memory, should be 记忆=human memory"),
    ("english", 142, "Psychology Basics", 5, "pinyin", "nèi cún", "jì yì", "Fix pinyin to match corrected Chinese"),
    ("english", 142, "Psychology Basics", 26, "chinese", "的看法关注中心", "关注中心", "Extra prefix that doesn't belong"),
    ("english", 142, "Psychology Basics", 26, "pinyin", "de kàn fǎ guān zhù zhōng xīn", "guān zhù zhōng xīn", "Fix pinyin to match corrected Chinese"),
    ("english", 142, "Psychology Basics", 32, "chinese", "的动机人类行为", "人类行为", "Leftover text from previous row"),
    ("english", 142, "Psychology Basics", 32, "pinyin", "de dòng jī rén lèi xíng wéi", "rén lèi xíng wéi", "Fix pinyin to match corrected Chinese"),

    # Pack 147 - Project Management
    ("english", 147, "Project Management", 26, "chinese", "的时间表关键交付成果", "关键交付成果", "Leftover text from previous row"),
    ("english", 147, "Project Management", 26, "pinyin", "de shí jiān biǎo guān jiàn jiāo fù chéng guǒ", "guān jiàn jiāo fù chéng guǒ", "Fix pinyin to match corrected Chinese"),
    ("english", 147, "Project Management", 32, "chinese", "的分配任务依赖", "任务依赖", "Extra prefix that doesn't belong"),
    ("english", 147, "Project Management", 32, "pinyin", "de fēn pèi rèn wù yī lài", "rèn wù yī lài", "Fix pinyin to match corrected Chinese"),

    # Pack 148 - Business Advanced
    ("english", 148, "Business Advanced", 28, "chinese", "联合创始人财务支持者", "财务支持者", "Leftover prefix from previous row"),
    ("english", 148, "Business Advanced", 28, "pinyin", "lián hé chuàng shǐ rén cái wù zhī chí zhě", "cái wù zhī chí zhě", "Fix pinyin to match corrected Chinese"),
    ("english", 148, "Business Advanced", 30, "chinese", "的支持者安全资金", "获得资金", "Wrong translation: 安全资金=safe funds, should be 获得资金=secure funding"),
    ("english", 148, "Business Advanced", 30, "pinyin", "de zhī chí zhě ān quán zī jīn", "huò dé zī jīn", "Fix pinyin to match corrected Chinese"),
    ("english", 148, "Business Advanced", 34, "chinese", "的估值公司收购", "公司收购", "Leftover prefix from previous row"),
    ("english", 148, "Business Advanced", 34, "pinyin", "de gū zhí gōng sī shōu gòu", "gōng sī shōu gòu", "Fix pinyin to match corrected Chinese"),
    ("english", 148, "Business Advanced", 38, "chinese", "之间的合并引导公司", "自筹资金的公司", "Leftover prefix + literal translation, should be business idiom"),
    ("english", 148, "Business Advanced", 38, "pinyin", "zhī jiān de hé bìng yǐn dǎo gōng sī", "zì chóu zī jīn de gōng sī", "Fix pinyin to match corrected Chinese"),
    ("english", 148, "Business Advanced", 46, "chinese", "的模型获得牵引力", "获得发展势头", "Leftover prefix + too literal translation"),
    ("english", 148, "Business Advanced", 46, "pinyin", "de mó xíng huò dé qiān yǐn lì", "huò dé fā zhǎn shì tóu", "Fix pinyin to match corrected Chinese"),
    ("english", 148, "Business Advanced", 58, "chinese", "的可扩展性创造协同效应", "创造协同效应", "Leftover prefix from previous row"),
    ("english", 148, "Business Advanced", 58, "pinyin", "de kě kuò zhǎn xìng chuàng zào xié tóng xiào yìng", "chuàng zào xié tóng xiào yìng", "Fix pinyin to match corrected Chinese"),
    ("english", 148, "Business Advanced", 60, "chinese", "之间的协同作用投资组合多元化", "投资组合多元化", "Leftover prefix from previous row"),
    ("english", 148, "Business Advanced", 60, "pinyin", "zhī jiān de xié tóng zuò yòng tóu zī zǔ hé duō yuán huà", "tóu zī zǔ hé duō yuán huà", "Fix pinyin to match corrected Chinese"),

    # Pack 149 - Environmental Science
    ("english", 149, "Environmental Science", 32, "chinese", "的污染环境恶化", "环境恶化", "Leftover prefix from previous row"),
    ("english", 149, "Environmental Science", 32, "pinyin", "de wū rǎn huán jìng è huà", "huán jìng è huà", "Fix pinyin to match corrected Chinese"),
    ("english", 149, "Environmental Science", 34, "chinese", "的退化栖息地恢复", "栖息地恢复", "Leftover prefix from previous row"),
    ("english", 149, "Environmental Science", 34, "pinyin", "de tuì huà qī xī dì huī fù", "qī xī dì huī fù", "Fix pinyin to match corrected Chinese"),
    ("english", 149, "Environmental Science", 42, "chinese", "的管理应对气候变化", "应对气候变化", "Leftover prefix from previous row"),
    ("english", 149, "Environmental Science", 42, "pinyin", "de guǎn lǐ yìng duì qì hòu biàn huà", "yìng duì qì hòu biàn huà", "Fix pinyin to match corrected Chinese"),

    # Pack 153 - Formal Connectors
    ("english", 153, "Formal Connectors", 61, "chinese", "这就是谎言", "问题在此", "MAJOR ERROR: 谎言=lie/falsehood, herein lies=here exists/problem is here"),
    ("english", 153, "Formal Connectors", 61, "pinyin", "zhè jiù shì huǎng yán", "wèn tí zài cǐ", "Fix pinyin to match corrected Chinese"),

    # Pack 154 - Advanced Verbs
    ("english", 154, "Advanced Verbs", 40, "chinese", "证实证实故事", "证实故事", "Duplication: 证实 appears twice"),
    ("english", 154, "Advanced Verbs", 40, "pinyin", "zhèng shí zhèng shí gù shì", "zhèng shí gù shì", "Fix pinyin to match corrected Chinese"),
    ("english", 154, "Advanced Verbs", 45, "chinese", "之间勾画清楚", "清楚勾画", "Extra prefix that doesn't fit"),
    ("english", 154, "Advanced Verbs", 45, "pinyin", "zhī jiān gōu huà qīng chǔ", "qīng chǔ gōu huà", "Fix pinyin to match corrected Chinese"),
    ("english", 154, "Advanced Verbs", 47, "chinese", "推断推断数据", "推断数据", "Duplication: 推断 appears twice"),
    ("english", 154, "Advanced Verbs", 47, "pinyin", "tuī duàn tuī duàn shù jù", "tuī duàn shù jù", "Fix pinyin to match corrected Chinese"),

    # Pack 157 - Response Patterns
    ("english", 157, "Response Patterns", 61, "chinese", "内部询问", "请进询问", "Wrong context: inquire within is idiomatic sign phrase, should be 请进询问"),
    ("english", 157, "Response Patterns", 61, "pinyin", "nèi bù xún wèn", "qǐng jìn xún wèn", "Fix pinyin to match corrected Chinese"),

    # Pack 160 - Apology & Excuse Patterns (already has some fixes but missing these)
    ("english", 160, "Apology & Excuse Patterns", 24, "chinese", "兼容默许", "默许", "Leftover prefix from previous row"),
    ("english", 160, "Apology & Excuse Patterns", 24, "pinyin", "jiān róng mò xǔ", "mò xǔ", "Fix pinyin to match corrected Chinese"),
    ("english", 160, "Apology & Excuse Patterns", 42, "chinese", "和谐相处一致", "一致", "Redundant/awkward phrasing"),
    ("english", 160, "Apology & Excuse Patterns", 42, "pinyin", "hé xié xiāng chǔ yī zhì", "yī zhì", "Fix pinyin to match corrected Chinese"),
    ("english", 160, "Apology & Excuse Patterns", 46, "chinese", "之间的不和谐共同点", "共同点", "Leftover prefix from previous row"),
    ("english", 160, "Apology & Excuse Patterns", 46, "pinyin", "zhī jiān de bù hé xié gòng tóng diǎn", "gòng tóng diǎn", "Fix pinyin to match corrected Chinese"),
    ("english", 160, "Apology & Excuse Patterns", 52, "chinese", "对齐协调利益", "协调利益", "Redundant: both mean align/coordinate"),
    ("english", 160, "Apology & Excuse Patterns", 52, "pinyin", "duì qí xié tiáo lì yì", "xié tiáo lì yì", "Fix pinyin to match corrected Chinese"),
    ("english", 160, "Apology & Excuse Patterns", 54, "chinese", "发生冲突性格冲突", "性格冲突", "Duplication: 冲突 appears twice"),
    ("english", 160, "Apology & Excuse Patterns", 54, "pinyin", "fā shēng chōng tū xìng gé chōng tū", "xìng gé chōng tū", "Fix pinyin to match corrected Chinese"),
]

# Append to existing fix table
input_file = "/home/user/LPH/EnglishWords/EnglishFixTable.csv"
output_file = "/home/user/LPH/EnglishWords/EnglishFixTable.csv"

# Read existing fixes
with open(input_file, 'r', encoding='utf-8') as f:
    existing_lines = f.readlines()

# Append new fixes
with open(output_file, 'w', encoding='utf-8', newline='') as f:
    # Write existing content
    for line in existing_lines:
        f.write(line)

    # Write new fixes
    writer = csv.writer(f)
    for fix in new_fixes:
        writer.writerow(fix)

print(f"✓ Added {len(new_fixes)} new fixes to EnglishFixTable.csv")
print(f"  Total fixes now: {len(existing_lines) - 1 + len(new_fixes)}")
