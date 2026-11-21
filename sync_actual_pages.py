import re

# Đọc actual_pages_log.txt
with open('actual_pages_log.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

page_map = {}
for line in lines:
    line = line.strip()
    if '===> Page' in line:
        parts = line.split('===> Page')
        title = parts[0].strip()
        pg = parts[1].strip()
        page_map[title] = pg

print(f"Loaded {len(page_map)} entries from actual_pages_log.txt")

with open('report_sections/cover_and_intro.py', 'r', encoding='utf-8') as f:
    content = f.read()

def get_best_match(clean_title):
    # 1. Exact match
    if clean_title in page_map:
        return page_map[clean_title]
    
    # 2. Match by prefix ID like 'Hình 5.1.', 'Bảng 5.1.', '5.1.2.'
    m_id = re.match(r'^(Hình\s+\d+\.\d+|Bảng\s+\d+\.\d+|\d+\.\d+(\.\d+)?|CHƯƠNG\s+[IVX]+)', clean_title)
    if m_id:
        target_id = m_id.group(1)
        for k, v in page_map.items():
            if k.startswith(target_id + '.') or k.startswith(target_id + ' ') or k == target_id:
                return v

    # 3. Fuzzy match: starts with or contained
    for k, v in page_map.items():
        if k.startswith(clean_title) or clean_title.startswith(k):
            return v
    return None

updated_count = 0

def replace_entry(m):
    global updated_count
    indent = m.group(1)
    title = m.group(2)
    old_pg = m.group(3)
    clean_title = title.strip()
    
    new_pg = get_best_match(clean_title)
    if new_pg:
        if new_pg != old_pg:
            print(f"Updating: '{clean_title}': {old_pg} -> {new_pg}")
            updated_count += 1
        return f'("{indent}{clean_title}", "{new_pg}")'
    else:
        return m.group(0)

# Replace all ("title", "page") tuples
content_new = re.sub(r'\("(\s*)([^"]+)",\s*"(\d+)"\)', replace_entry, content)

with open('report_sections/cover_and_intro.py', 'w', encoding='utf-8', newline='\r\n') as f:
    f.write(content_new)

print(f"Updated {updated_count} page references in cover_and_intro.py")
