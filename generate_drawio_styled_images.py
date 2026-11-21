# ==============================================================================
# SCRIPT XUẤT 16 ẢNH BIỂU ĐỒ VỚI PHONG CÁCH DRAW.IO CHUẨN 300 DPI
# ==============================================================================
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Thiết lập Font Times New Roman chuẩn học thuật
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif']
plt.rcParams['figure.autolayout'] = True

out_dir = os.path.join('report_assets', 'drawio_exported_images')
os.makedirs(out_dir, exist_ok=True)

def draw_actor(ax, x, y, name, scale=1.0):
    # Head
    head = patches.Circle((x, y + 4.0*scale), 1.5*scale, facecolor='#FFFFFF', edgecolor='#1E293B', linewidth=1.6, zorder=5)
    ax.add_patch(head)
    # Body
    ax.plot([x, x], [y + 2.5*scale, y - 1.8*scale], color='#1E293B', linewidth=1.8, zorder=4)
    # Arms
    ax.plot([x - 2.5*scale, x + 2.5*scale], [y + 0.8*scale, y + 0.8*scale], color='#1E293B', linewidth=1.8, zorder=4)
    # Legs
    ax.plot([x, x - 2.0*scale], [y - 1.8*scale, y - 5.5*scale], color='#1E293B', linewidth=1.8, zorder=4)
    ax.plot([x, x + 2.0*scale], [y - 1.8*scale, y - 5.5*scale], color='#1E293B', linewidth=1.8, zorder=4)
    # Label
    ax.text(x, y - 7.5*scale, name, ha='center', va='top', fontsize=9.2, fontweight='bold', color='#0F172A', zorder=6)

def draw_device(ax, x, y, name, w=14, h=8):
    rect = patches.FancyBboxPatch((x - w/2, y - h/2), w, h, boxstyle="round,pad=0.5", 
                                  facecolor='#F1F5F9', edgecolor='#475569', linewidth=1.5, zorder=4)
    ax.add_patch(rect)
    ax.text(x, y, name, ha='center', va='center', fontsize=8.5, fontweight='bold', color='#0F172A', zorder=5)

def draw_uc(ax, x, y, text, w=28, h=6.5, kind='normal'):
    if kind == 'main':
        bgcolor, edgecolor, textcolor, weight, size = '#FEF3C7', '#D97706', '#78350F', 'bold', 8.8
    elif kind == 'error':
        bgcolor, edgecolor, textcolor, weight, size = '#FFF1F2', '#F43F5E', '#9F1239', 'normal', 8.5
    elif kind == 'header':
        bgcolor, edgecolor, textcolor, weight, size = '#FEF3C7', '#D97706', '#78350F', 'bold', 8.8
    else:
        bgcolor, edgecolor, textcolor, weight, size = '#FFFFFF', '#475569', '#1E293B', 'normal', 8.5

    ellipse = patches.Ellipse((x, y), w, h, facecolor=bgcolor, edgecolor=edgecolor, linewidth=1.4, zorder=3)
    ax.add_patch(ellipse)
    ax.text(x, y, text, ha='center', va='center', fontsize=size, fontweight=weight, color=textcolor, zorder=4, multialignment='center')

def draw_sys_box(ax, x, y, w, h, title):
    rect = patches.Rectangle((x, y), w, h, facecolor='#F8FAFC', edgecolor='#475569', 
                             linewidth=1.5, linestyle=(0, (6, 4)), zorder=1)
    ax.add_patch(rect)
    ax.text(x + w/2, y + h - 2.8, title, ha='center', va='center', fontsize=11.0, 
            fontweight='bold', color='#0F172A', zorder=2)

def draw_line(ax, x1, y1, x2, y2):
    ax.plot([x1, x2], [y1, y2], color='#334155', linewidth=1.4, zorder=2)

def draw_rel(ax, x1, y1, x2, y2, rel_type="<<include>>", label_pos=0.5, offset=(0, 1.8), color=None):
    if color is None:
        color = '#0284C7' if rel_type == "<<include>>" else '#BE123C'
    
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->,head_width=0.35,head_length=0.6", 
                                color=color, linestyle=(0, (4, 3)), linewidth=1.3),
                zorder=2)
    
    lx = x1 + (x2 - x1) * label_pos + offset[0]
    ly = y1 + (y2 - y1) * label_pos + offset[1]
    ax.text(lx, ly, rel_type, fontsize=8.0, fontstyle='italic', color=color,
            ha='center', va='center',
            bbox=dict(boxstyle="round,pad=0.25", fc="white", ec=color, lw=0.6),
            zorder=6)

# ==============================================================================
# 0. USE CASE TỔNG QUÁT (15 USE CASES)
# ==============================================================================
def gen_uc_tong_quat():
    fig, ax = plt.subplots(figsize=(16, 12), dpi=300)
    ax.set_xlim(0, 160)
    ax.set_ylim(0, 120)
    ax.axis('off')

    draw_sys_box(ax, 35, 6, 90, 108, "HỆ THỐNG ĐẶT VÉ VÀ QUẢN LÝ SUẤT CHIẾU CINESTAR CINEMA")

    # 4 Actors
    draw_actor(ax, 18, 92, "Khách hàng\n(Client)", scale=1.1)
    draw_actor(ax, 18, 32, "Nhân viên quầy\n(Staff)", scale=1.1)
    draw_actor(ax, 142, 92, "Quản lý rạp\n(Manager)", scale=1.1)
    draw_actor(ax, 142, 32, "Quản trị viên\n(Admin)", scale=1.1)

    # Use cases dùng chung (Ở trên cùng trung tâm)
    draw_uc(ax, 80, 107, "UC01. Đăng nhập hệ thống", w=28, h=5.6, kind='header')
    draw_uc(ax, 80, 99, "UC02. Đăng ký tài khoản", w=28, h=5.6, kind='header')
    draw_uc(ax, 80, 91, "UC03. Quản lý thông tin tài khoản", w=28, h=5.6, kind='header')

    # Cột trái (Client & Staff)
    client_staff = [
        (58, 80, "UC04. Tra cứu phim & Lịch chiếu", 'client'),
        (58, 70, "UC05. Đặt vé trực tuyến & Chọn ghế (5p)", 'client'),
        (58, 60, "UC06. Quản lý giỏ vé & Chọn combo F&B", 'client'),
        (58, 42, "UC07. Bán vé trực tiếp tại quầy POS", 'staff'),
        (58, 28, "UC08. Soát vé QR & Cảnh báo gian lận", 'staff'),
    ]

    # Cột phải (Manager & Admin)
    mgr_admin = [
        (102, 80, "UC09. Quản lý danh mục phim", 'mgr'),
        (102, 70, "UC10. Quản lý phòng & Cấu hình ghế", 'mgr'),
        (102, 60, "UC11. Lập suất chiếu (Chống trùng)", 'mgr'),
        (102, 50, "UC12. Quản lý bảng giá & Combo F&B", 'mgr'),
        (102, 40, "UC13. Báo cáo doanh thu & Lấp đầy", 'mgr'),
        (102, 26, "UC14. Quản lý người dùng & RBAC", 'admin'),
        (102, 14, "UC15. Cài đặt hệ thống & Audit Logs", 'admin'),
    ]

    for (x, y, text, role) in client_staff:
        draw_uc(ax, x, y, text, w=28, h=5.8)
        if role == 'client':
            draw_line(ax, 20, 92, x - 14, y)
        elif role == 'staff':
            draw_line(ax, 20, 32, x - 14, y)

    for (x, y, text, role) in mgr_admin:
        draw_uc(ax, x, y, text, w=28, h=5.8)
        if role == 'mgr':
            draw_line(ax, 140, 92, x + 14, y)
        elif role == 'admin':
            draw_line(ax, 140, 32, x + 14, y)

    # Nối tác nhân tới UC chung
    draw_line(ax, 20, 92, 66, 107)
    draw_line(ax, 20, 92, 66, 99)
    draw_line(ax, 20, 92, 66, 91)
    draw_line(ax, 20, 32, 66, 107)
    draw_line(ax, 20, 32, 66, 91)
    draw_line(ax, 140, 92, 94, 107)
    draw_line(ax, 140, 92, 94, 91)
    draw_line(ax, 140, 32, 94, 107)
    draw_line(ax, 140, 32, 94, 91)

    # Kế thừa vai trò Admin -> Manager
    ax.annotate("", xy=(142, 82), xytext=(142, 42),
                arrowprops=dict(arrowstyle="-|>,head_width=0.6,head_length=0.9", 
                                facecolor="white", edgecolor="#1E293B", linewidth=1.4))
    ax.text(143.5, 62, "Kế thừa\nquyền", fontsize=8.0, color="#1E293B", fontweight='bold')

    plt.tight_layout()
    fpath = os.path.join(out_dir, 'drawio_uc_tong_quat.png')
    plt.savefig(fpath, dpi=300, bbox_inches='tight')
    plt.close()
    print("Exported:", fpath)

# ==============================================================================
# HÀM MẪU CHO CÁC USE CASE PHÂN RÃ (UC01 - UC15)
# ==============================================================================
def gen_decomposed_uc(uc_code, title, actor_name, main_ucs, sub_ucs, relations, secondary_actor=None, fname=None):
    fig, ax = plt.subplots(figsize=(14, 8), dpi=300)
    ax.set_xlim(0, 140)
    ax.set_ylim(0, 80)
    ax.axis('off')

    draw_sys_box(ax, 34, 4, 102, 72, f"PHÂN RÃ USE CASE: {uc_code} - {title.upper()}")
    draw_actor(ax, 16, 42, actor_name, scale=1.1)

    # Main UCs
    for muc in main_ucs:
        draw_uc(ax, muc['x'], muc['y'], muc['text'], w=muc.get('w', 24), h=muc.get('h', 7.5), kind='main')
        draw_line(ax, 20, 42, muc['x'] - muc.get('w', 24)/2, muc['y'])

    # Secondary actor if any
    if secondary_actor:
        if secondary_actor.get('type') == 'device':
            draw_device(ax, secondary_actor['x'], secondary_actor['y'], secondary_actor['name'])
        else:
            draw_actor(ax, secondary_actor['x'], secondary_actor['y'], secondary_actor['name'], scale=1.0)

    # Sub UCs
    for suc in sub_ucs:
        draw_uc(ax, suc['x'], suc['y'], suc['text'], w=suc.get('w', 27), h=suc.get('h', 6.8), kind=suc.get('kind', 'normal'))
        if suc.get('connect_secondary'):
            draw_line(ax, secondary_actor['x'] - 7, secondary_actor['y'], suc['x'] + suc.get('w', 27)/2, suc['y'])

    # Relations
    for rel in relations:
        draw_rel(ax, rel['x1'], rel['y1'], rel['x2'], rel['y2'], 
                 rel_type=rel['type'], label_pos=rel.get('label_pos', 0.45), 
                 offset=rel.get('offset', (0, 1.8)), color=rel.get('color'))

    plt.tight_layout()
    if fname is None:
        fname = f"drawio_{uc_code.lower()}.png"
    fpath = os.path.join(out_dir, fname)
    plt.savefig(fpath, dpi=300, bbox_inches='tight')
    plt.close()
    print("Exported:", fpath)

# ==============================================================================
# TẠO 15 BIỂU ĐỒ PHÂN RÃ
# ==============================================================================
def gen_all():
    gen_uc_tong_quat()

    # UC01
    gen_decomposed_uc(
        "UC01", "Đăng nhập hệ thống", "Người dùng\n(User)",
        [
            {'x': 58, 'y': 48, 'text': "Đăng nhập\nvào hệ thống", 'w': 24, 'h': 7.5},
            {'x': 58, 'y': 20, 'text': "Đăng xuất\nkhỏi hệ thống", 'w': 24, 'h': 7.0}
        ],
        [
            {'x': 105, 'y': 66, 'text': "Nhập Email & Mật khẩu\n(Kiểm tra cú pháp)"},
            {'x': 105, 'y': 52, 'text': "Xác thực BCrypt\nvới CSDL bảng users"},
            {'x': 105, 'y': 38, 'text': "Khởi tạo Session\n& Điều hướng theo Role"},
            {'x': 105, 'y': 24, 'text': "Báo lỗi sai Email\nhoặc Mật khẩu", 'kind': 'error'},
            {'x': 105, 'y': 10, 'text': "Từ chối tài khoản bị khóa\n(status = 'locked')", 'kind': 'error'}
        ],
        [
            {'x1': 70, 'y1': 52, 'x2': 91.5, 'y2': 66, 'type': '<<include>>'},
            {'x1': 70, 'y1': 49, 'x2': 91.5, 'y2': 52, 'type': '<<include>>'},
            {'x1': 70, 'y1': 46, 'x2': 91.5, 'y2': 38, 'type': '<<include>>'},
            {'x1': 70, 'y1': 43, 'x2': 91.5, 'y2': 25, 'type': '<<extend>>', 'offset': (0, -1.8)},
            {'x1': 68, 'y1': 41, 'x2': 91.5, 'y2': 12, 'type': '<<extend>>', 'offset': (0, -1.8)}
        ],
        fname='drawio_uc01_dang_nhap.png'
    )

    # UC02
    gen_decomposed_uc(
        "UC02", "Đăng ký tài khoản", "Khách hàng\nvãng lai",
        [{'x': 58, 'y': 42, 'text': "Đăng ký\ntài khoản mới", 'w': 24, 'h': 8.0}],
        [
            {'x': 105, 'y': 66, 'text': "Nhập thông tin cá nhân\n(Tên, Email, SĐT, Pass)"},
            {'x': 105, 'y': 52, 'text': "Kiểm tra hợp lệ dữ liệu\n(Regex Email, SĐT, Pass>=6)"},
            {'x': 105, 'y': 38, 'text': "Kiểm tra trùng Email\ntrong CSDL users"},
            {'x': 105, 'y': 24, 'text': "Băm BCrypt & Lưu User\n(role_id=4: Client)"},
            {'x': 105, 'y': 10, 'text': "Báo lỗi trùng Email\nhoặc Pass không khớp", 'kind': 'error'}
        ],
        [
            {'x1': 70, 'y1': 46, 'x2': 91.5, 'y2': 66, 'type': '<<include>>'},
            {'x1': 70, 'y1': 44, 'x2': 91.5, 'y2': 52, 'type': '<<include>>'},
            {'x1': 70, 'y1': 42, 'x2': 91.5, 'y2': 38, 'type': '<<include>>'},
            {'x1': 70, 'y1': 40, 'x2': 91.5, 'y2': 25, 'type': '<<include>>', 'offset': (0, -1.8)},
            {'x1': 68, 'y1': 38, 'x2': 91.5, 'y2': 12, 'type': '<<extend>>', 'offset': (0, -1.8)}
        ],
        fname='drawio_uc02_dang_ky.png'
    )

    # UC03
    gen_decomposed_uc(
        "UC03", "Quản lý thông tin tài khoản", "Người dùng\nđã đăng nhập",
        [
            {'x': 58, 'y': 54, 'text': "Xem hồ sơ\ncá nhân", 'w': 24, 'h': 7.5},
            {'x': 58, 'y': 26, 'text': "Đổi mật khẩu\ntài khoản", 'w': 24, 'h': 7.5}
        ],
        [
            {'x': 105, 'y': 66, 'text': "Hiển thị thông tin\n(Họ tên, Email, SĐT, Role)"},
            {'x': 105, 'y': 52, 'text': "Cập nhật thông tin\n(Họ tên & Số điện thoại)"},
            {'x': 105, 'y': 34, 'text': "Xác thực mật khẩu cũ\nqua BCrypt.compare()"},
            {'x': 105, 'y': 20, 'text': "Cập nhật mật khẩu mới\n(Băm BCrypt & Lưu CSDL)"},
            {'x': 105, 'y': 8, 'text': "Báo lỗi khi mật khẩu cũ\nkhông chính xác", 'kind': 'error'}
        ],
        [
            {'x1': 70, 'y1': 56, 'x2': 91.5, 'y2': 66, 'type': '<<include>>'},
            {'x1': 70, 'y1': 53, 'x2': 91.5, 'y2': 52, 'type': '<<extend>>'},
            {'x1': 70, 'y1': 28, 'x2': 91.5, 'y2': 34, 'type': '<<include>>'},
            {'x1': 70, 'y1': 25, 'x2': 91.5, 'y2': 20, 'type': '<<include>>', 'offset': (0, -1.8)},
            {'x1': 68, 'y1': 23, 'x2': 91.5, 'y2': 10, 'type': '<<extend>>', 'offset': (0, -1.8)}
        ],
        fname='drawio_uc03_ho_so_doi_mk.png'
    )

    # UC04
    gen_decomposed_uc(
        "UC04", "Tra cứu phim và lịch chiếu", "Khách hàng",
        [
            {'x': 58, 'y': 54, 'text': "Tra cứu danh mục\nphim chiếu rạp", 'w': 24, 'h': 7.5},
            {'x': 58, 'y': 26, 'text': "Xem lịch chiếu\ntheo ngày & rạp", 'w': 24, 'h': 7.5}
        ],
        [
            {'x': 105, 'y': 66, 'text': "Lọc phim 'Đang chiếu'\nhoặc 'Sắp chiếu'"},
            {'x': 105, 'y': 52, 'text': "Xem chi tiết phim\n(Đạo diễn, trailer, thời lượng)"},
            {'x': 105, 'y': 34, 'text': "Chọn ngày xem phim\n(Lọc suất theo Date)"},
            {'x': 105, 'y': 20, 'text': "Xem danh sách phòng chiếu\nvà định dạng 2D/3D/IMAX"},
            {'x': 105, 'y': 8, 'text': "Chuyển sang màn hình\nchọn ghế ngồi (UC05)"}
        ],
        [
            {'x1': 70, 'y1': 56, 'x2': 91.5, 'y2': 66, 'type': '<<include>>'},
            {'x1': 70, 'y1': 53, 'x2': 91.5, 'y2': 52, 'type': '<<extend>>'},
            {'x1': 70, 'y1': 28, 'x2': 91.5, 'y2': 34, 'type': '<<include>>'},
            {'x1': 70, 'y1': 25, 'x2': 91.5, 'y2': 20, 'type': '<<include>>', 'offset': (0, -1.8)},
            {'x1': 68, 'y1': 23, 'x2': 91.5, 'y2': 10, 'type': '<<extend>>', 'offset': (0, -1.8)}
        ],
        fname='drawio_uc04_tra_cuu_phim.png'
    )

    # UC05
    gen_decomposed_uc(
        "UC05", "Đặt vé trực tuyến & Chọn ghế (Khóa 5p)", "Khách hàng",
        [{'x': 58, 'y': 42, 'text': "Chọn ghế ngồi\ntrực quan theo phòng", 'w': 24, 'h': 8.0}],
        [
            {'x': 105, 'y': 66, 'text': "Tải sơ đồ ma trận ghế\n(Trạng thái trống/đã đặt/VIP)"},
            {'x': 105, 'y': 52, 'text': "Khóa giữ ghế 5 phút\n(Ghi nhận bảng seat_locks)"},
            {'x': 105, 'y': 38, 'text': "Đếm ngược thời gian giữ ghế\n(Countdown Timer 5:00)"},
            {'x': 105, 'y': 24, 'text': "Hủy khóa giữ ghế\nkhi hết hạn 5 phút (Release)"},
            {'x': 105, 'y': 10, 'text': "Cảnh báo ghế vừa được\nkhách khác chọn giữ chỗ", 'kind': 'error'}
        ],
        [
            {'x1': 70, 'y1': 46, 'x2': 91.5, 'y2': 66, 'type': '<<include>>'},
            {'x1': 70, 'y1': 44, 'x2': 91.5, 'y2': 52, 'type': '<<include>>'},
            {'x1': 70, 'y1': 42, 'x2': 91.5, 'y2': 38, 'type': '<<include>>'},
            {'x1': 70, 'y1': 40, 'x2': 91.5, 'y2': 25, 'type': '<<extend>>', 'offset': (0, -1.8)},
            {'x1': 68, 'y1': 38, 'x2': 91.5, 'y2': 12, 'type': '<<extend>>', 'offset': (0, -1.8)}
        ],
        fname='drawio_uc05_dat_ve_chon_ghe.png'
    )

    # UC06
    gen_decomposed_uc(
        "UC06", "Quản lý giỏ vé, Chọn combo & Thanh toán", "Khách hàng",
        [
            {'x': 56, 'y': 52, 'text': "Quản lý giỏ vé\n& Chọn combo F&B", 'w': 23, 'h': 7.5},
            {'x': 56, 'y': 24, 'text': "Thanh toán đơn hàng\n& Nhận vé điện tử", 'w': 23, 'h': 7.5}
        ],
        [
            {'x': 98, 'y': 66, 'text': "Chọn số lượng combo\n(Bắp rang, nước ngọt)"},
            {'x': 98, 'y': 52, 'text': "Tính tổng tiền đơn hàng\n(Tiền vé + Tiền combo)"},
            {'x': 98, 'y': 36, 'text': "Chuyển hướng cổng VNPAY/MoMo\n& Nhận IPN Callback", 'connect_secondary': True},
            {'x': 98, 'y': 22, 'text': "Sinh mã QR Code bảo mật\ncho từng vé điện tử"},
            {'x': 98, 'y': 8, 'text': "Quản lý lịch sử vé\ntrong mục 'Vé của tôi'"}
        ],
        [
            {'x1': 67.5, 'y1': 55, 'x2': 84.5, 'y2': 66, 'type': '<<extend>>'},
            {'x1': 67.5, 'y1': 52, 'x2': 84.5, 'y2': 52, 'type': '<<include>>'},
            {'x1': 67.5, 'y1': 27, 'x2': 84.5, 'y2': 36, 'type': '<<include>>'},
            {'x1': 67.5, 'y1': 24, 'x2': 84.5, 'y2': 22, 'type': '<<include>>', 'offset': (0, -1.8)},
            {'x1': 66, 'y1': 21, 'x2': 84.5, 'y2': 10, 'type': '<<extend>>', 'offset': (0, -1.8)}
        ],
        secondary_actor={'x': 126, 'y': 36, 'name': "Cổng thanh toán\n(VNPAY / MoMo)", 'type': 'actor'},
        fname='drawio_uc06_gio_ve_thanh_toan.png'
    )

    # UC07
    gen_decomposed_uc(
        "UC07", "Bán vé trực tiếp tại quầy POS", "Nhân viên quầy\n(Staff)",
        [{'x': 58, 'y': 42, 'text': "Bán vé trực tiếp\ntại quầy POS", 'w': 24, 'h': 8.0}],
        [
            {'x': 105, 'y': 66, 'text': "Lọc suất chiếu hôm nay\ntheo phim và phòng"},
            {'x': 105, 'y': 52, 'text': "Chọn vị trí ghế trống\ntrên màn hình POS"},
            {'x': 105, 'y': 38, 'text': "Bán kèm combo bắp nước\n(Chọn bắp/nước tại quầy)"},
            {'x': 105, 'y': 24, 'text': "Thu tiền mặt / Quét mã QR\ntại quầy thu ngân"},
            {'x': 105, 'y': 10, 'text': "In vé nhiệt kèm mã QR\nvà hóa đơn cho khách"}
        ],
        [
            {'x1': 70, 'y1': 46, 'x2': 91.5, 'y2': 66, 'type': '<<include>>'},
            {'x1': 70, 'y1': 44, 'x2': 91.5, 'y2': 52, 'type': '<<include>>'},
            {'x1': 70, 'y1': 42, 'x2': 91.5, 'y2': 38, 'type': '<<extend>>'},
            {'x1': 70, 'y1': 40, 'x2': 91.5, 'y2': 25, 'type': '<<include>>', 'offset': (0, -1.8)},
            {'x1': 68, 'y1': 38, 'x2': 91.5, 'y2': 12, 'type': '<<include>>', 'offset': (0, -1.8)}
        ],
        fname='drawio_uc07_ban_ve_pos.png'
    )

    # UC08
    gen_decomposed_uc(
        "UC08", "Soát vé QR & Cảnh báo gian lận", "Nhân viên quầy\n(Staff)",
        [
            {'x': 56, 'y': 50, 'text': "Soát vé xem phim\nqua mã QR Code", 'w': 23, 'h': 7.5},
            {'x': 56, 'y': 22, 'text': "Xem lịch sử soát vé\ntheo ca trực", 'w': 23, 'h': 7.5}
        ],
        [
            {'x': 98, 'y': 66, 'text': "Quét mã QR từ vé giấy\nhoặc điện thoại khách", 'connect_secondary': True},
            {'x': 98, 'y': 52, 'text': "Xác thực mã vé & cập nhật\nstatus = 'checked_in'"},
            {'x': 98, 'y': 36, 'text': "Cảnh báo gian lận:\nVé đã dùng hoặc sai phòng", 'kind': 'error'},
            {'x': 98, 'y': 22, 'text': "Xem thống kê số vé\nđã soát trong ca trực"},
            {'x': 98, 'y': 8, 'text': "Đối soát danh sách khách\nđã vào phòng chiếu"}
        ],
        [
            {'x1': 67.5, 'y1': 53, 'x2': 84.5, 'y2': 66, 'type': '<<include>>'},
            {'x1': 67.5, 'y1': 50, 'x2': 84.5, 'y2': 52, 'type': '<<include>>'},
            {'x1': 67.5, 'y1': 47, 'x2': 84.5, 'y2': 36, 'type': '<<extend>>'},
            {'x1': 67.5, 'y1': 24, 'x2': 84.5, 'y2': 22, 'type': '<<include>>', 'offset': (0, -1.8)},
            {'x1': 66, 'y1': 21, 'x2': 84.5, 'y2': 10, 'type': '<<extend>>', 'offset': (0, -1.8)}
        ],
        secondary_actor={'x': 126, 'y': 66, 'name': "Thiết bị quét\nCamera/Scanner", 'type': 'device'},
        fname='drawio_uc08_soat_ve_qr.png'
    )

    # UC09
    gen_decomposed_uc(
        "UC09", "Quản lý danh mục phim", "Quản lý rạp\n(Manager)",
        [{'x': 58, 'y': 42, 'text': "Quản lý danh mục\nphim chiếu rạp", 'w': 24, 'h': 8.0}],
        [
            {'x': 105, 'y': 66, 'text': "Thêm phim mới vào hệ thống\n(Tiêu đề, thời lượng, thể loại)"},
            {'x': 105, 'y': 52, 'text': "Tải lên Poster phim\nqua thư viện Multer"},
            {'x': 105, 'y': 38, 'text': "Nhúng liên kết Video Trailer\nYouTube trực tuyến"},
            {'x': 105, 'y': 24, 'text': "Cập nhật thông tin & đổi\ntrạng thái (now/coming/ended)"},
            {'x': 105, 'y': 10, 'text': "Xóa phim khỏi danh mục\n(Ràng buộc toàn vẹn CSDL)", 'kind': 'error'}
        ],
        [
            {'x1': 70, 'y1': 46, 'x2': 91.5, 'y2': 66, 'type': '<<include>>'},
            {'x1': 70, 'y1': 44, 'x2': 91.5, 'y2': 52, 'type': '<<include>>'},
            {'x1': 70, 'y1': 42, 'x2': 91.5, 'y2': 38, 'type': '<<include>>'},
            {'x1': 70, 'y1': 40, 'x2': 91.5, 'y2': 25, 'type': '<<include>>', 'offset': (0, -1.8)},
            {'x1': 68, 'y1': 38, 'x2': 91.5, 'y2': 12, 'type': '<<extend>>', 'offset': (0, -1.8)}
        ],
        fname='drawio_uc09_quan_ly_phim.png'
    )

    # UC10
    gen_decomposed_uc(
        "UC10", "Quản lý phòng & Ma trận ghế", "Quản lý rạp\n(Manager)",
        [
            {'x': 58, 'y': 54, 'text': "Quản lý danh sách\nphòng chiếu phim", 'w': 24, 'h': 7.5},
            {'x': 58, 'y': 26, 'text': "Cấu hình ma trận ghế\ntheo phòng chiếu", 'w': 24, 'h': 7.5}
        ],
        [
            {'x': 105, 'y': 66, 'text': "Thêm/Sửa phòng chiếu\n(Định dạng 2D/3D/IMAX/4DX)"},
            {'x': 105, 'y': 52, 'text': "Khởi tạo ma trận ghế A-G\nvới 70-150 ghế/phòng"},
            {'x': 105, 'y': 36, 'text': "Phân loại ghế ngồi:\nThường, VIP, Sweetbox đôi"},
            {'x': 105, 'y': 22, 'text': "Chuyển trạng thái bảo trì\nghế hỏng (active/maintenance)"},
            {'x': 105, 'y': 8, 'text': "Kiểm tra ràng buộc phòng\nđang có suất chiếu hoạt động", 'kind': 'error'}
        ],
        [
            {'x1': 70, 'y1': 56, 'x2': 91.5, 'y2': 66, 'type': '<<include>>'},
            {'x1': 70, 'y1': 28, 'x2': 91.5, 'y2': 52, 'type': '<<include>>'},
            {'x1': 70, 'y1': 26, 'x2': 91.5, 'y2': 36, 'type': '<<include>>'},
            {'x1': 70, 'y1': 24, 'x2': 91.5, 'y2': 22, 'type': '<<extend>>', 'offset': (0, -1.8)},
            {'x1': 68, 'y1': 52, 'x2': 91.5, 'y2': 10, 'type': '<<extend>>', 'offset': (0, -1.8)}
        ],
        fname='drawio_uc10_phong_chieu_ghe.png'
    )

    # UC11
    gen_decomposed_uc(
        "UC11", "Lập suất chiếu chống trùng", "Quản lý rạp\n(Manager)",
        [{'x': 58, 'y': 42, 'text': "Lập lịch suất chiếu\ncho các phòng", 'w': 24, 'h': 8.0}],
        [
            {'x': 105, 'y': 66, 'text': "Chọn phim, phòng chiếu\nvà ngày/giờ bắt đầu"},
            {'x': 105, 'y': 52, 'text': "Tự động tính giờ kết thúc\n(start + duration + buffer 15p)"},
            {'x': 105, 'y': 38, 'text': "Kiểm tra trùng phòng/giờ chiếu\n(Thuật toán ConflictDetector)"},
            {'x': 105, 'y': 24, 'text': "Lưu suất chiếu mới hợp lệ\nvào bảng showtimes"},
            {'x': 105, 'y': 10, 'text': "Cảnh báo xung đột thời gian\nvà gợi ý khung giờ trống", 'kind': 'error'}
        ],
        [
            {'x1': 70, 'y1': 46, 'x2': 91.5, 'y2': 66, 'type': '<<include>>'},
            {'x1': 70, 'y1': 44, 'x2': 91.5, 'y2': 52, 'type': '<<include>>'},
            {'x1': 70, 'y1': 42, 'x2': 91.5, 'y2': 38, 'type': '<<include>>'},
            {'x1': 70, 'y1': 40, 'x2': 91.5, 'y2': 25, 'type': '<<include>>', 'offset': (0, -1.8)},
            {'x1': 68, 'y1': 38, 'x2': 91.5, 'y2': 12, 'type': '<<extend>>', 'offset': (0, -1.8)}
        ],
        fname='drawio_uc11_lap_suat_chieu.png'
    )

    # UC12
    gen_decomposed_uc(
        "UC12", "Bảng giá vé & Combo F&B", "Quản lý rạp\n(Manager)",
        [
            {'x': 58, 'y': 54, 'text': "Quản lý bảng giá vé\nxem phim", 'w': 24, 'h': 7.5},
            {'x': 58, 'y': 26, 'text': "Quản lý danh mục\ncombo bắp nước (F&B)", 'w': 24, 'h': 7.5}
        ],
        [
            {'x': 105, 'y': 66, 'text': "Cấu hình giá vé cơ sở\ntheo loại màn hình 2D/3D/IMAX"},
            {'x': 105, 'y': 52, 'text': "Thiết lập hệ số phụ thu\ncho ghế VIP và Sweetbox"},
            {'x': 105, 'y': 36, 'text': "Thêm combo bắp nước mới\n(Tên combo, giá bán, mô tả)"},
            {'x': 105, 'y': 22, 'text': "Cập nhật giá và tồn kho\ncombo bắp rang / nước ngọt"},
            {'x': 105, 'y': 8, 'text': "Bật/Tắt trạng thái mở bán\ncombo (is_active: 1 / 0)"}
        ],
        [
            {'x1': 70, 'y1': 56, 'x2': 91.5, 'y2': 66, 'type': '<<include>>'},
            {'x1': 70, 'y1': 53, 'x2': 91.5, 'y2': 52, 'type': '<<include>>'},
            {'x1': 70, 'y1': 28, 'x2': 91.5, 'y2': 36, 'type': '<<include>>'},
            {'x1': 70, 'y1': 25, 'x2': 91.5, 'y2': 22, 'type': '<<include>>', 'offset': (0, -1.8)},
            {'x1': 68, 'y1': 23, 'x2': 91.5, 'y2': 10, 'type': '<<extend>>', 'offset': (0, -1.8)}
        ],
        fname='drawio_uc12_gia_ve_combo.png'
    )

    # UC13
    gen_decomposed_uc(
        "UC13", "Báo cáo doanh thu & Lấp đầy", "Quản lý rạp\n(Manager)",
        [{'x': 58, 'y': 42, 'text': "Xem báo cáo thống kê\n& Dashboard quản lý", 'w': 24, 'h': 8.0}],
        [
            {'x': 105, 'y': 66, 'text': "Xem Dashboard KPI hôm nay\n(Doanh thu, vé bán, suất chiếu)"},
            {'x': 105, 'y': 52, 'text': "Theo dõi biểu đồ cột 7 ngày\n(Chart.js trực quan doanh thu)"},
            {'x': 105, 'y': 38, 'text': "Thống kê doanh thu theo phim\n(Doanh thu vé + F&B combo)"},
            {'x': 105, 'y': 24, 'text': "Tính Tỷ lệ lấp đầy phòng chiếu\n(Occupancy Rate % theo suất)"},
            {'x': 105, 'y': 10, 'text': "Lọc báo cáo theo khoảng thời gian\n(Hôm nay, 7 ngày, tháng này)"}
        ],
        [
            {'x1': 70, 'y1': 46, 'x2': 91.5, 'y2': 66, 'type': '<<include>>'},
            {'x1': 70, 'y1': 44, 'x2': 91.5, 'y2': 52, 'type': '<<include>>'},
            {'x1': 70, 'y1': 42, 'x2': 91.5, 'y2': 38, 'type': '<<include>>'},
            {'x1': 70, 'y1': 40, 'x2': 91.5, 'y2': 25, 'type': '<<include>>', 'offset': (0, -1.8)},
            {'x1': 68, 'y1': 38, 'x2': 91.5, 'y2': 12, 'type': '<<extend>>', 'offset': (0, -1.8)}
        ],
        fname='drawio_uc13_thong_ke_doanh_thu.png'
    )

    # UC14
    gen_decomposed_uc(
        "UC14", "Quản lý người dùng & RBAC", "Quản trị viên\n(Admin)",
        [{'x': 58, 'y': 42, 'text': "Quản lý người dùng\n& Phân quyền RBAC", 'w': 24, 'h': 8.0}],
        [
            {'x': 105, 'y': 66, 'text': "Xem danh sách & Lọc người dùng\ntheo vai trò (Admin, Mgr, Staff, Client)"},
            {'x': 105, 'y': 52, 'text': "Tạo mới tài khoản nhân viên\nhoặc quản lý rạp"},
            {'x': 105, 'y': 38, 'text': "Phân quyền vai trò RBAC\n(Cập nhật role_id trong users)"},
            {'x': 105, 'y': 24, 'text': "Khóa / Mở khóa tài khoản\n(Chuyển đổi status: active / locked)"},
            {'x': 105, 'y': 10, 'text': "Xóa tài khoản người dùng\n(Bảo vệ tài khoản quản trị chính)", 'kind': 'error'}
        ],
        [
            {'x1': 70, 'y1': 46, 'x2': 91.5, 'y2': 66, 'type': '<<include>>'},
            {'x1': 70, 'y1': 44, 'x2': 91.5, 'y2': 52, 'type': '<<extend>>'},
            {'x1': 70, 'y1': 42, 'x2': 91.5, 'y2': 38, 'type': '<<include>>'},
            {'x1': 70, 'y1': 40, 'x2': 91.5, 'y2': 25, 'type': '<<extend>>', 'offset': (0, -1.8)},
            {'x1': 68, 'y1': 38, 'x2': 91.5, 'y2': 12, 'type': '<<extend>>', 'offset': (0, -1.8)}
        ],
        fname='drawio_uc14_quan_ly_nguoi_dung.png'
    )

    # UC15
    gen_decomposed_uc(
        "UC15", "Cấu hình tham số & Audit Log", "Quản trị viên\n(Admin)",
        [
            {'x': 58, 'y': 54, 'text': "Cấu hình tham số\nvận hành rạp", 'w': 24, 'h': 7.5},
            {'x': 58, 'y': 26, 'text': "Giám sát nhật ký\nkiểm toán (Audit Log)", 'w': 24, 'h': 7.5}
        ],
        [
            {'x': 105, 'y': 66, 'text': "Cấu hình thời gian đệm dọn phòng\n(buffer_minutes = 15 phút)"},
            {'x': 105, 'y': 52, 'text': "Cấu hình thời gian giữ ghế tạm\n(hold_time = 5 phút)"},
            {'x': 105, 'y': 36, 'text': "Cập nhật thông tin rạp chiếu\n(Tên rạp, hotline, địa chỉ)"},
            {'x': 105, 'y': 22, 'text': "Xem lịch sử thao tác hệ thống\n(Timestamp, User, Hành động, IP)"},
            {'x': 105, 'y': 8, 'text': "Lọc và tra cứu nhật ký\nkiểm toán theo thời gian"}
        ],
        [
            {'x1': 70, 'y1': 56, 'x2': 91.5, 'y2': 66, 'type': '<<include>>'},
            {'x1': 70, 'y1': 53, 'x2': 91.5, 'y2': 52, 'type': '<<include>>'},
            {'x1': 70, 'y1': 50, 'x2': 91.5, 'y2': 36, 'type': '<<include>>', 'offset': (0, -1.8)},
            {'x1': 70, 'y1': 26, 'x2': 91.5, 'y2': 22, 'type': '<<include>>'},
            {'x1': 70, 'y1': 23, 'x2': 91.5, 'y2': 9, 'type': '<<extend>>', 'offset': (0, -1.8)}
        ],
        fname='drawio_uc15_cau_hinh_audit.png'
    )

if __name__ == '__main__':
    print("🚀 Bắt đầu xuất 16 ảnh biểu đồ chuẩn Draw.io...")
    gen_all()
    print("✅ Hoàn thành xuất 16 ảnh chất lượng cao 300 DPI!")
