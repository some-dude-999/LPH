#!/usr/bin/env python3
"""Fix delete_fix_tables.py placeholders with correct language/act values."""

import re

with open('/home/user/LPH/PromptCopier.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Strategy: Look backwards from each delete_fix_tables.py occurrence to find
# the most recent apply_fixes_by_act.py command, which has the language and act

lines = content.split('\n')
fixed_lines = []

for i, line in enumerate(lines):
    if 'delete_fix_tables.py {lang} {act}' in line:
        # Look backwards to find apply_fixes_by_act.py command
        lang = None
        act = None
        for j in range(i-1, max(0, i-100), -1):
            match = re.search(r'apply_fixes_by_act\.py (\w+) (\d+)', lines[j])
            if match:
                lang = match.group(1)
                act = match.group(2)
                break
        
        if lang and act:
            fixed_line = line.replace('{lang}', lang).replace('{act}', act)
            fixed_lines.append(fixed_line)
            print(f"Fixed: {lang} act {act}")
        else:
            print(f"Warning: Could not find language/act for line {i}")
            fixed_lines.append(line)
    else:
        fixed_lines.append(line)

content = '\n'.join(fixed_lines)

with open('/home/user/LPH/PromptCopier.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n✅ All placeholders fixed!")
