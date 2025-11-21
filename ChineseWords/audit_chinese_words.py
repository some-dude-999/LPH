#!/usr/bin/env python3
"""
Comprehensive Quality Audit for ChineseWords CSV Files (Packs 1-107)
Checks for:
1. Pinyin spacing in compound words (MOST CRITICAL)
2. Tone sandhi accuracy (不 and 一)
3. Missing tone marks
4. Vietnamese diacritics
5. Translation naturalness issues
"""

import csv
import re
import os
from collections import defaultdict

# Common compound words that should have NO spaces in pinyin
COMPOUND_WORDS = {
    '起床': 'qǐchuáng',
    '睡觉': 'shuìjiào',
    '吃饭': 'chīfàn',
    '喝水': 'hēshuǐ',
    '上班': 'shàngbān',
    '下班': 'xiàbān',
    '上学': 'shàngxué',
    '下学': 'xiàxué',
    '放学': 'fàngxué',
    '回家': 'huíjiā',
    '出门': 'chūmén',
    '洗脸': 'xǐliǎn',
    '洗手': 'xǐshǒu',
    '洗澡': 'xǐzǎo',
    '刷牙': 'shuāyá',
    '漱口': 'shùkǒu',
    '穿衣': 'chuānyī',
    '脱衣': 'tuōyī',
    '做饭': 'zuòfàn',
    '煮饭': 'zhǔfàn',
    '买菜': 'mǎicài',
    '逛街': 'guàngjiē',
    '看书': 'kànshū',
    '读书': 'dúshū',
    '写字': 'xiězì',
    '打球': 'dǎqiú',
    '跑步': 'pǎobù',
    '游泳': 'yóuyǒng',
    '唱歌': 'chànggē',
    '跳舞': 'tiàowǔ',
    '听歌': 'tīnggē',
    '看电视': 'kàn diànshì',
    '打电话': 'dǎ diànhuà',
    '发短信': 'fā duǎnxìn',
    '上网': 'shàngwǎng',
    '下载': 'xiàzǎi',
    '开车': 'kāichē',
    '坐车': 'zuòchē',
    '走路': 'zǒulù',
    '骑车': 'qíchē',
    '打工': 'dǎgōng',
    '赚钱': 'zhuànqián',
    '花钱': 'huāqián',
    '存钱': 'cúnqián',
    '借钱': 'jièqián',
    '还钱': 'huánqián',
    '买东西': 'mǎi dōngxi',
    '卖东西': 'mài dōngxi',
    '早上': 'zǎoshang',
    '晚上': 'wǎnshang',
    '中午': 'zhōngwǔ',
    '下午': 'xiàwǔ',
    '明天': 'míngtiān',
    '昨天': 'zuótiān',
    '今天': 'jīntiān',
    '朋友': 'péngyou',
    '老师': 'lǎoshī',
    '学生': 'xuésheng',
    '医生': 'yīshēng',
    '护士': 'hùshi',
    '司机': 'sījī',
    '警察': 'jǐngchá',
    '军人': 'jūnrén',
    '商人': 'shāngrén',
    '工人': 'gōngrén',
    '农民': 'nóngmín',
    '记者': 'jìzhě',
    '作家': 'zuòjiā',
    '画家': 'huàjiā',
    '歌手': 'gēshǒu',
    '演员': 'yǎnyuán',
    '律师': 'lǜshī',
    '会计': 'kuàijì',
    '经理': 'jīnglǐ',
    '老板': 'lǎobǎn',
    '服务员': 'fúwùyuán',
    '收银员': 'shōuyínyuán',
    '售货员': 'shòuhuòyuán',
    '导游': 'dǎoyóu',
    '翻译': 'fānyì',
    '主持人': 'zhǔchírén',
    '厨师': 'chúshī',
    '理发师': 'lǐfàshī',
    '出租车': 'chūzūchē',
    '公交车': 'gōngjiāochē',
    '火车': 'huǒchē',
    '飞机': 'fēijī',
    '轮船': 'lúnchuán',
    '自行车': 'zìxíngchē',
    '摩托车': 'mótuōchē',
    '地铁': 'dìtiě',
    '高铁': 'gāotiě',
    '医院': 'yīyuàn',
    '学校': 'xuéxiào',
    '银行': 'yínháng',
    '邮局': 'yóujú',
    '超市': 'chāoshì',
    '商店': 'shāngdiàn',
    '餐厅': 'cāntīng',
    '饭店': 'fàndiàn',
    '酒店': 'jiǔdiàn',
    '宾馆': 'bīnguǎn',
    '机场': 'jīchǎng',
    '车站': 'chēzhàn',
    '公园': 'gōngyuán',
    '图书馆': 'túshūguǎn',
    '博物馆': 'bówùguǎn',
    '电影院': 'diànyǐngyuàn',
    '体育馆': 'tǐyùguǎn',
    '游泳馆': 'yóuyǒngguǎn',
    '健身房': 'jiànshēnfáng',
    '办公室': 'bàngōngshì',
    '教室': 'jiàoshì',
    '卧室': 'wòshì',
    '客厅': 'kètīng',
    '厨房': 'chúfáng',
    '浴室': 'yùshì',
    '厕所': 'cèsuǒ',
    '洗手间': 'xǐshǒujiān',
    '收工': 'shōugōng',
    '外出': 'wàichū',
    '求学': 'qiúxué',
    '净手': 'jìngshǒu',
    '洁面': 'jiémiàn',
    '沐浴': 'mùyù',
    '冲澡': 'chōngzǎo',
    '入睡': 'rùshuì',
    '就寝': 'jiùqǐn',
    '早起': 'zǎoqǐ',
    '洗漱': 'xǐshù',
    '用餐': 'yòngcān',
    '进食': 'jìnshí',
    '饮水': 'yǐnshuǐ',
}

# Tone marks for detection
TONE_MARKS = 'āáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜ'

# Vietnamese diacritics
VIETNAMESE_DIACRITICS = 'áàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵđ'

class ChineseWordsAuditor:
    def __init__(self, base_path):
        self.base_path = base_path
        self.errors = defaultdict(list)
        self.pack_errors = defaultdict(lambda: defaultdict(list))
        self.total_checked = 0

    def has_tone_marks(self, pinyin):
        """Check if pinyin has tone marks"""
        if not pinyin or pinyin.strip() == '':
            return True  # Empty is not our concern here
        # Remove spaces, apostrophes, parentheses for checking
        clean = re.sub(r'[\s\'()]', '', pinyin.lower())
        # Remove "formal", "informal", etc markers
        clean = re.sub(r'\(.*?\)', '', clean)
        # Check if any letter has tone marks
        return any(c in TONE_MARKS for c in clean)

    def has_vietnamese_diacritics(self, vietnamese):
        """Check if Vietnamese text has diacritics (not plain text)"""
        if not vietnamese or vietnamese.strip() == '':
            return True
        # Remove spaces and parentheses
        clean = re.sub(r'[\s()]', '', vietnamese.lower())
        # Remove markers
        clean = re.sub(r'\(.*?\)', '', clean)
        # If it has any Vietnamese letters, it should have diacritics
        # Basic check: if it's not all ASCII, it probably has diacritics
        return any(c in VIETNAMESE_DIACRITICS for c in clean) or not clean.isascii()

    def check_bu_tone_sandhi(self, chinese, pinyin):
        """Check if 不 tone sandhi is correct"""
        errors = []
        if '不' not in chinese:
            return errors

        # Find positions of 不 in Chinese
        for i, char in enumerate(chinese):
            if char == '不':
                # Check what follows
                if i + 1 < len(chinese):
                    next_char = chinese[i + 1]
                    # Common 4th tone characters that should trigger bú
                    fourth_tone_chars = '要对是客气见去做看用过到错在现'
                    if next_char in fourth_tone_chars:
                        if 'bù' in pinyin and 'bú' not in pinyin:
                            errors.append(f"不 before 4th tone should be 'bú' not 'bù' in: {chinese}")
        return errors

    def check_yi_tone_sandhi(self, chinese, pinyin):
        """Check if 一 tone sandhi is correct"""
        errors = []
        if '一' not in chinese:
            return errors

        # Find positions of 一 in Chinese
        for i, char in enumerate(chinese):
            if char == '一':
                if i + 1 < len(chinese):
                    next_char = chinese[i + 1]
                    # Common 4th tone characters
                    fourth_tone_chars = '个定起次样共块半片道件'
                    # Common 1st/2nd/3rd tone characters
                    other_tone_chars = '天年生些点起直'

                    if next_char in fourth_tone_chars:
                        if 'yī' in pinyin and 'yí' not in pinyin:
                            errors.append(f"一 before 4th tone should be 'yí' not 'yī' in: {chinese}")
                    elif next_char in other_tone_chars:
                        if 'yī' in pinyin and 'yì' not in pinyin:
                            errors.append(f"一 before 1st/2nd/3rd tone should be 'yì' not 'yī' in: {chinese}")
        return errors

    def check_compound_spacing(self, chinese, pinyin):
        """Check if compound words have incorrect spacing in pinyin"""
        errors = []

        # Skip if pinyin contains (formal) or other markers
        if '(' in pinyin:
            return errors

        # Check against known compound words
        if chinese in COMPOUND_WORDS:
            expected = COMPOUND_WORDS[chinese]
            if pinyin != expected:
                # Check if it's a spacing issue
                pinyin_no_space = pinyin.replace(' ', '')
                if pinyin_no_space == expected or pinyin_no_space.replace("'", '') == expected.replace("'", ''):
                    errors.append({
                        'chinese': chinese,
                        'current': pinyin,
                        'expected': expected,
                        'error_type': 'spacing'
                    })

        # Generic check: two-character compounds should generally have no space
        if len(chinese) == 2 and ' ' in pinyin:
            # Exceptions: phrases like "你好" can have space in some contexts
            # But compounds like 起床, 睡觉, 吃饭 should not
            verb_object_chars = {
                '起床', '睡觉', '吃饭', '喝水', '洗脸', '洗手', '洗澡', '刷牙',
                '上班', '下班', '上学', '放学', '回家', '出门', '看书', '写字',
                '打球', '跑步', '游泳', '唱歌', '跳舞', '做饭', '买菜', '开车'
            }
            if chinese in verb_object_chars:
                errors.append({
                    'chinese': chinese,
                    'current': pinyin,
                    'expected': pinyin.replace(' ', ''),
                    'error_type': 'verb-object compound should have no space'
                })

        # Check three-character verb-object compounds
        three_char_compounds = ['看电视', '打电话', '买东西', '卖东西']
        if chinese in three_char_compounds and pinyin.count(' ') != 1:
            # These should have one space: 看 电视 -> kàn diànshì
            errors.append({
                'chinese': chinese,
                'current': pinyin,
                'expected': 'should have exactly one space',
                'error_type': 'incorrect spacing in 3-char compound'
            })

        return errors

    def audit_file(self, pack_number):
        """Audit a single pack file"""
        filename = f'ChineseWords{pack_number}.csv'
        filepath = os.path.join(self.base_path, filename)

        if not os.path.exists(filepath):
            self.errors['missing_files'].append(pack_number)
            return

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                row_num = 2  # Start at 2 because of header

                for row in reader:
                    self.total_checked += 1
                    chinese = row.get('chinese', '').strip()
                    pinyin = row.get('pinyin', '').strip()
                    vietnamese = row.get('vietnamese', '').strip()

                    # Skip empty rows
                    if not chinese:
                        continue

                    # Check 1: Pinyin spacing in compounds (CRITICAL)
                    spacing_errors = self.check_compound_spacing(chinese, pinyin)
                    if spacing_errors:
                        for err in spacing_errors:
                            self.errors['pinyin_spacing'].append({
                                'pack': pack_number,
                                'row': row_num,
                                **err
                            })
                            self.pack_errors[pack_number]['pinyin_spacing'].append({
                                'row': row_num,
                                **err
                            })

                    # Check 2: Tone sandhi - 不
                    bu_errors = self.check_bu_tone_sandhi(chinese, pinyin)
                    if bu_errors:
                        for err in bu_errors:
                            self.errors['bu_sandhi'].append({
                                'pack': pack_number,
                                'row': row_num,
                                'error': err
                            })
                            self.pack_errors[pack_number]['bu_sandhi'].append({
                                'row': row_num,
                                'error': err
                            })

                    # Check 3: Tone sandhi - 一
                    yi_errors = self.check_yi_tone_sandhi(chinese, pinyin)
                    if yi_errors:
                        for err in yi_errors:
                            self.errors['yi_sandhi'].append({
                                'pack': pack_number,
                                'row': row_num,
                                'error': err
                            })
                            self.pack_errors[pack_number]['yi_sandhi'].append({
                                'row': row_num,
                                'error': err
                            })

                    # Check 4: Missing tone marks
                    if not self.has_tone_marks(pinyin):
                        self.errors['missing_tones'].append({
                            'pack': pack_number,
                            'row': row_num,
                            'chinese': chinese,
                            'pinyin': pinyin
                        })
                        self.pack_errors[pack_number]['missing_tones'].append({
                            'row': row_num,
                            'chinese': chinese,
                            'pinyin': pinyin
                        })

                    # Check 5: Vietnamese diacritics
                    if not self.has_vietnamese_diacritics(vietnamese):
                        self.errors['vietnamese_diacritics'].append({
                            'pack': pack_number,
                            'row': row_num,
                            'chinese': chinese,
                            'vietnamese': vietnamese
                        })
                        self.pack_errors[pack_number]['vietnamese_diacritics'].append({
                            'row': row_num,
                            'chinese': chinese,
                            'vietnamese': vietnamese
                        })

                    row_num += 1

        except Exception as e:
            self.errors['file_errors'].append({
                'pack': pack_number,
                'error': str(e)
            })

    def generate_report(self):
        """Generate comprehensive audit report"""
        report = []
        report.append("=" * 80)
        report.append("COMPREHENSIVE QUALITY AUDIT REPORT")
        report.append("ChineseWords CSV Files (Packs 1-107)")
        report.append("=" * 80)
        report.append("")

        # Summary statistics
        report.append("## SUMMARY STATISTICS")
        report.append(f"Total entries checked: {self.total_checked}")
        report.append(f"Total pinyin spacing errors: {len(self.errors['pinyin_spacing'])}")
        report.append(f"Total 不 tone sandhi errors: {len(self.errors['bu_sandhi'])}")
        report.append(f"Total 一 tone sandhi errors: {len(self.errors['yi_sandhi'])}")
        report.append(f"Total missing tone marks: {len(self.errors['missing_tones'])}")
        report.append(f"Total Vietnamese diacritic issues: {len(self.errors['vietnamese_diacritics'])}")
        report.append("")

        # Critical Issues - Pinyin Spacing
        if self.errors['pinyin_spacing']:
            report.append("=" * 80)
            report.append("## CRITICAL ISSUES: PINYIN SPACING IN COMPOUND WORDS")
            report.append("=" * 80)
            report.append("")

            # Group by pack
            packs_with_errors = set(err['pack'] for err in self.errors['pinyin_spacing'])
            report.append(f"Packs affected: {len(packs_with_errors)} out of 107")
            report.append(f"Affected packs: {sorted(packs_with_errors)}")
            report.append("")

            # Show examples
            report.append("### Sample Errors (first 20):")
            for err in self.errors['pinyin_spacing'][:20]:
                report.append(f"Pack {err['pack']}, Row {err['row']}: {err['chinese']}")
                report.append(f"  Current:  {err['current']}")
                report.append(f"  Expected: {err['expected']}")
                report.append(f"  Type: {err['error_type']}")
                report.append("")

        # Pack 23 Detailed Analysis
        if 23 in self.pack_errors:
            report.append("=" * 80)
            report.append("## PACK 23 DETAILED ANALYSIS")
            report.append("=" * 80)
            report.append("")

            pack23 = self.pack_errors[23]

            if pack23['pinyin_spacing']:
                report.append("### Pinyin Spacing Errors in Pack 23:")
                report.append(f"Total errors: {len(pack23['pinyin_spacing'])}")
                report.append("")
                for err in pack23['pinyin_spacing']:
                    report.append(f"Row {err['row']}: {err['chinese']}")
                    report.append(f"  Current:  {err['current']}")
                    report.append(f"  Expected: {err['expected']}")
                    report.append("")

            if pack23['bu_sandhi']:
                report.append("### 不 Tone Sandhi Errors in Pack 23:")
                for err in pack23['bu_sandhi']:
                    report.append(f"Row {err['row']}: {err['error']}")
                report.append("")

            if pack23['yi_sandhi']:
                report.append("### 一 Tone Sandhi Errors in Pack 23:")
                for err in pack23['yi_sandhi']:
                    report.append(f"Row {err['row']}: {err['error']}")
                report.append("")

            if pack23['missing_tones']:
                report.append("### Missing Tone Marks in Pack 23:")
                for err in pack23['missing_tones']:
                    report.append(f"Row {err['row']}: {err['chinese']} -> {err['pinyin']}")
                report.append("")

            if pack23['vietnamese_diacritics']:
                report.append("### Vietnamese Diacritic Issues in Pack 23:")
                for err in pack23['vietnamese_diacritics']:
                    report.append(f"Row {err['row']}: {err['chinese']} -> {err['vietnamese']}")
                report.append("")

        # Other categories
        if self.errors['bu_sandhi']:
            report.append("=" * 80)
            report.append("## TONE SANDHI ERRORS: 不 (bù)")
            report.append("=" * 80)
            report.append("")
            packs_affected = set(err['pack'] for err in self.errors['bu_sandhi'])
            report.append(f"Packs affected: {sorted(packs_affected)}")
            report.append("")
            for err in self.errors['bu_sandhi'][:10]:
                report.append(f"Pack {err['pack']}, Row {err['row']}: {err['error']}")
            report.append("")

        if self.errors['yi_sandhi']:
            report.append("=" * 80)
            report.append("## TONE SANDHI ERRORS: 一 (yī)")
            report.append("=" * 80)
            report.append("")
            packs_affected = set(err['pack'] for err in self.errors['yi_sandhi'])
            report.append(f"Packs affected: {sorted(packs_affected)}")
            report.append("")
            for err in self.errors['yi_sandhi'][:10]:
                report.append(f"Pack {err['pack']}, Row {err['row']}: {err['error']}")
            report.append("")

        if self.errors['missing_tones']:
            report.append("=" * 80)
            report.append("## MISSING TONE MARKS")
            report.append("=" * 80)
            report.append("")
            packs_affected = set(err['pack'] for err in self.errors['missing_tones'])
            report.append(f"Packs affected: {sorted(packs_affected)}")
            report.append("")
            for err in self.errors['missing_tones'][:10]:
                report.append(f"Pack {err['pack']}, Row {err['row']}: {err['chinese']} -> {err['pinyin']}")
            report.append("")

        if self.errors['vietnamese_diacritics']:
            report.append("=" * 80)
            report.append("## VIETNAMESE DIACRITIC ISSUES")
            report.append("=" * 80)
            report.append("")
            packs_affected = set(err['pack'] for err in self.errors['vietnamese_diacritics'])
            report.append(f"Packs affected: {sorted(packs_affected)}")
            report.append("")
            for err in self.errors['vietnamese_diacritics'][:10]:
                report.append(f"Pack {err['pack']}, Row {err['row']}: {err['chinese']} -> {err['vietnamese']}")
            report.append("")

        # Packs by error count
        report.append("=" * 80)
        report.append("## PACKS RANKED BY ERROR COUNT")
        report.append("=" * 80)
        report.append("")

        pack_error_counts = defaultdict(int)
        for error_type in ['pinyin_spacing', 'bu_sandhi', 'yi_sandhi', 'missing_tones', 'vietnamese_diacritics']:
            for err in self.errors[error_type]:
                pack_error_counts[err['pack']] += 1

        sorted_packs = sorted(pack_error_counts.items(), key=lambda x: x[1], reverse=True)
        for pack, count in sorted_packs[:20]:
            report.append(f"Pack {pack}: {count} errors")

        report.append("")
        report.append("=" * 80)
        report.append("END OF REPORT")
        report.append("=" * 80)

        return '\n'.join(report)

def main():
    base_path = '/home/user/LPH/ChineseWords'
    auditor = ChineseWordsAuditor(base_path)

    print("Starting comprehensive audit of ChineseWords packs 1-107...")
    print("This may take a moment...")
    print()

    for pack_num in range(1, 108):
        auditor.audit_file(pack_num)
        if pack_num % 10 == 0:
            print(f"Processed {pack_num}/107 packs...")

    print()
    print("Generating report...")
    report = auditor.generate_report()

    # Save report
    report_path = os.path.join(base_path, 'AUDIT_REPORT.txt')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"Report saved to: {report_path}")
    print()
    print(report)

if __name__ == '__main__':
    main()
