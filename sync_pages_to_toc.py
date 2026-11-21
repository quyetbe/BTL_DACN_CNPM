import re

# Đọc output thực tế từ log của task 1990
with open(r'C:\Users\Nguyễn Mạnh Quyết\.gemini\antigravity\brain\92e0a31e-d56a-4057-9e0f-49857079c428\.system_generated\steps\1990\output.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Tạo dict lưu trữ {tên_mục: số_trang}
page_map = {}
for line in text.splitlines():
    if '===> Page' in line:
        parts = line.split('===> Page')
        title = parts[0].strip()
        pg = parts[1].strip()
        page_map[title] = pg

print(f"Tổng số mục đo được: {len(page_map)}")

# Đọc cover_and_intro.py
with open('report_sections/cover_and_intro.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Cập nhật Mục lục (toc_entries)
def update_toc(m):
    prefix = m.group(1)
    title = m.group(2)
    old_pg = m.group(3)
    
    # Tìm trong page_map
    clean_title = title.strip()
    new_pg = old_pg
    for k, v in page_map.items():
        if k == clean_title or k.startswith(clean_title) or clean_title.startswith(k):
            new_pg = v
            break
    return f'("{prefix}{clean_title}", "{new_pg}")'

# Cập nhật Danh mục hình vẽ (figures_list)
def update_lof(m):
    title = m.group(1)
    old_pg = m.group(2)
    new_pg = old_pg
    for k, v in page_map.items():
        if k == title or k.startswith(title) or title.startswith(k):
            new_pg = v
            break
    return f'("{title}", "{new_pg}")'

# Cập nhật Danh mục bảng biểu (tables_list)
def update_lot(m):
    title = m.group(1)
    old_pg = m.group(2)
    new_pg = old_pg
    for k, v in page_map.items():
        if k == title or k.startswith(title) or title.startswith(k):
            new_pg = v
            break
    return f'("{title}", "{new_pg}")'

# Thay thế trong content
# Format: ("  1.1. Lý do chọn đề tài", "12")
content = re.sub(r'\("(\s*)([^"]+)",\s*"(\d+)"\)', update_toc, content)

with open('report_sections/cover_and_intro.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Đã cập nhật cover_and_intro.py với số trang thực tế!")
