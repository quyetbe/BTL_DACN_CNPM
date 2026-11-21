import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['figure.autolayout'] = True

output_dir = 'temp_uc_diagrams'
os.makedirs(output_dir, exist_ok=True)

def draw_actor(ax, x, y, name, scale=1.0):
    # Head
    head = patches.Circle((x, y + 4*scale), 1.6*scale, facecolor='#FFE4C4', edgecolor='#5C3A21', linewidth=1.6, zorder=5)
    ax.add_patch(head)
    # Body
    ax.plot([x, x], [y + 2.4*scale, y - 2.2*scale], color='#5C3A21', linewidth=2.0, zorder=4)
    # Arms
    ax.plot([x - 2.8*scale, x + 2.8*scale], [y + 0.8*scale, y + 0.8*scale], color='#5C3A21', linewidth=2.0, zorder=4)
    # Legs
    ax.plot([x, x - 2.2*scale], [y - 2.2*scale, y - 6.2*scale], color='#5C3A21', linewidth=2.0, zorder=4)
    ax.plot([x, x + 2.2*scale], [y - 2.2*scale, y - 6.2*scale], color='#5C3A21', linewidth=2.0, zorder=4)
    # Label
    ax.text(x, y - 8.2*scale, name, ha='center', va='top', fontsize=9.5, fontweight='bold', color='#1A1A1A', zorder=6)

def draw_uc_oval(ax, x, y, text, w=30, h=6.5, fontsize=8.8, bgcolor='#FFF8EE', edgecolor='#99582A'):
    ellipse = patches.Ellipse((x, y), w, h, facecolor=bgcolor, edgecolor=edgecolor, linewidth=1.5, zorder=3)
    ax.add_patch(ellipse)
    ax.text(x, y, text, ha='center', va='center', fontsize=fontsize, color='#1A1A1A', zorder=4, multialignment='center')

def draw_system_box(ax, x, y, w, h, title):
    rect = patches.Rectangle((x, y), w, h, facecolor='#FAF9F6', edgecolor='#2B2D42', linewidth=1.8, linestyle='-', zorder=1)
    ax.add_patch(rect)
    header = patches.Rectangle((x, y + h - 7.5), w, 7.5, facecolor='#EAE8E1', edgecolor='#2B2D42', linewidth=1.8, zorder=2)
    ax.add_patch(header)
    ax.text(x + w/2, y + h - 3.8, title, ha='center', va='center', fontsize=11, fontweight='bold', color='#1F2421', zorder=3)

def draw_connector(ax, x1, y1, x2, y2, color='#2B2D42', lw=1.2, zorder=2):
    ax.plot([x1, x2], [y1, y2], color=color, linewidth=lw, zorder=zorder)

def draw_relationship(ax, x1, y1, x2, y2, rel_type="<<include>>", label_offset=(0, 1.5)):
    ax.annotate(
        "", xy=(x2, y2), xytext=(x1, y1),
        arrowprops=dict(arrowstyle="->", color="#6B2D18", linestyle="--", linewidth=1.3, shrinkA=2, shrinkB=2),
        zorder=3
    )
    mx = (x1 + x2) / 2 + label_offset[0]
    my = (y1 + y2) / 2 + label_offset[1]
    ax.text(mx, my, rel_type, ha='center', va='center', fontsize=8.2, fontweight='bold', color='#8B2635',
            bbox=dict(boxstyle="square,pad=0.15", facecolor='white', edgecolor='none', alpha=0.9), zorder=4)

# Test UC01
def test_uc01():
    fig, ax = plt.subplots(figsize=(13.5, 7.5), dpi=300)
    ax.set_xlim(0, 135)
    ax.set_ylim(0, 75)
    ax.axis('off')

    draw_system_box(ax, 32, 4, 99, 68, "PHÂN RÃ USE CASE: UC01 - ĐĂNG NHẬP HỆ THỐNG")
    draw_actor(ax, 14, 40, "Người dùng\n(User)", scale=1.1)

    # Actor connects to main use case
    draw_uc_oval(ax, 58, 48, "Nhập Email\n& Mật khẩu", w=24, h=7.5)
    draw_connector(ax, 18, 40, 46, 48)

    # Secondary main UC
    draw_uc_oval(ax, 58, 26, "Đăng xuất\nkhỏi hệ thống", w=24, h=7.0)
    draw_connector(ax, 18, 40, 46, 26)

    # Included use cases (column 2)
    draw_uc_oval(ax, 104, 62, "Xác thực BCrypt\n& Kiểm tra CSDL", w=26, h=7.5)
    draw_uc_oval(ax, 104, 48, "Kiểm tra trạng thái\ntài khoản (active/locked)", w=26, h=7.5)
    draw_uc_oval(ax, 104, 34, "Khởi tạo Session\n& Điều hướng theo Role", w=26, h=7.5)

    # Extended use cases
    draw_uc_oval(ax, 104, 20, "Báo lỗi sai thông tin\nEmail hoặc Mật khẩu", w=26, h=7.5, bgcolor='#FFF0F0', edgecolor='#C94A4A')
    draw_uc_oval(ax, 104, 8, "Từ chối & Cảnh báo\ntài khoản bị khóa", w=26, h=7.0, bgcolor='#FFF0F0', edgecolor='#C94A4A')

    # Relationships from 'Nhập Email & Mật khẩu'
    draw_relationship(ax, 70, 50, 91, 62, "<<include>>", label_offset=(0, 1.8))
    draw_relationship(ax, 70, 48, 91, 48, "<<include>>", label_offset=(0, 1.8))
    draw_relationship(ax, 70, 46, 91, 35, "<<include>>", label_offset=(0, 1.8))
    draw_relationship(ax, 68, 44, 91, 21, "<<extend>>", label_offset=(-2, -1.8))
    draw_relationship(ax, 64, 44, 91, 9, "<<extend>>", label_offset=(-4, -1.8))

    plt.tight_layout()
    fpath = os.path.join(output_dir, 'test_uc01.png')
    plt.savefig(fpath, dpi=300, bbox_inches='tight')
    plt.close()
    print("Generated test_uc01:", fpath)

if __name__ == '__main__':
    test_uc01()
