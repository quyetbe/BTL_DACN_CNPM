import win32com.client
import os
import re

word = win32com.client.Dispatch('Word.Application')
word.DisplayAlerts = 0
word.Visible = False

doc_path = os.path.abspath('BTL_DACN_CNPM_3.docx')
doc = word.Documents.Open(doc_path, ReadOnly=True)

fig_re = re.compile(r'^(Hình\s+\d+\.\d+)\.')
tbl_re = re.compile(r'^(Bảng\s+\d+\.\d+)\.')

fig_pages = {}
tbl_pages = {}

for p in doc.Paragraphs:
    text = p.Range.Text.strip()
    m_fig = fig_re.match(text)
    if m_fig:
        key = m_fig.group(1)
        # get page number
        page = p.Range.Information(1)
        if page > 10 and key not in fig_pages:
            fig_pages[key] = (page, text)
            print(f"{key} -> Page {page}")
    
    m_tbl = tbl_re.match(text)
    if m_tbl:
        key = m_tbl.group(1)
        page = p.Range.Information(1)
        if page > 10 and key not in tbl_pages:
            tbl_pages[key] = (page, text)
            print(f"{key} -> Page {page}")

doc.Close(False)
word.Quit()

with open("all_caption_pages.txt", "w", encoding="utf-8") as f:
    f.write("=== FIGURES ===\n")
    for k in sorted(fig_pages.keys(), key=lambda x: [int(n) for n in re.findall(r'\d+', x)]):
        f.write(f"{k} | Page {fig_pages[k][0]} | {fig_pages[k][1]}\n")
    f.write("\n=== TABLES ===\n")
    for k in sorted(tbl_pages.keys(), key=lambda x: [int(n) for n in re.findall(r'\d+', x)]):
        f.write(f"{k} | Page {tbl_pages[k][0]} | {tbl_pages[k][1]}\n")

print("Done extracting all pages!")
