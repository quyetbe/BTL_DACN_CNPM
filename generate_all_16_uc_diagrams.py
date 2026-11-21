import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['figure.autolayout'] = True

out_dir = os.path.join('report_assets', 'uc_diagrams_new')
os.makedirs(out_dir, exist_ok=True)

def draw_actor(ax, x, y, name, scale=1.0):
    # Head
    head = patches.Circle((x, y + 4*scale), 1.5*scale, facecolor='#FFE4C4', edgecolor='#4A2810', linewidth=1.7, zorder=5)
    ax.add_patch(head)
    # Body
    ax.plot([x, x], [y + 2.5*scale, y - 2.0*scale], color='#4A2810', linewidth=2.0, zorder=4)
    # Arms
    ax.plot([x - 2.6*scale, x + 2.6*scale], [y + 0.9*scale, y + 0.9*scale], color='#4A2810', linewidth=2.0, zorder=4)
    # Legs
    ax.plot([x, x - 2.0*scale], [y - 2.0*scale, y - 5.8*scale], color='#4A2810', linewidth=2.0, zorder=4)
    ax.plot([x, x + 2.0*scale], [y - 2.0*scale, y - 5.8*scale], color='#4A2810', linewidth=2.0, zorder=4)
    # Label
    ax.text(x, y - 7.6*scale, name, ha='center', va='top', fontsize=9.2, fontweight='bold', color='#1A1A1A', zorder=6)

def draw_uc(ax, x, y, text, w=29, h=6.6, fontsize=8.6, bgcolor='#FFF8EE', edgecolor='#8B5A2B', zorder=3):
    ellipse = patches.Ellipse((x, y), w, h, facecolor=bgcolor, edgecolor=edgecolor, linewidth=1.4, zorder=zorder)
    ax.add_patch(ellipse)
    ax.text(x, y, text, ha='center', va='center', fontsize=fontsize, color='#1A1A1A', zorder=zorder+1, multialignment='center')

def draw_sys_box(ax, x, y, w, h, title):
    rect = patches.Rectangle((x, y), w, h, facecolor='#FAFAFA', edgecolor='#2B2D42', linewidth=1.8, zorder=1)
    ax.add_patch(rect)
    header = patches.Rectangle((x, y + h - 7.2), w, 7.2, facecolor='#ECEAE4', edgecolor='#2B2D42', linewidth=1.8, zorder=2)
    ax.add_patch(header)
    ax.text(x + w/2, y + h - 3.6, title, ha='center', va='center', fontsize=11, fontweight='bold', color='#1D2D44', zorder=3)

def draw_line(ax, x1, y1, x2, y2, color='#2B2D42', lw=1.2, zorder=2):
    ax.plot([x1, x2], [y1, y2], color=color, linewidth=lw, zorder=zorder)

def draw_rel(ax, x1, y1, x2, y2, rel_type="<<include>>", label_pos=0.5, offset=(0, 1.4), color='#7B2D26'):
    ax.annotate(
        "", xy=(x2, y2), xytext=(x1, y1),
        arrowprops=dict(arrowstyle="->", color=color, linestyle="--", linewidth=1.25, shrinkA=3, shrinkB=3),
        zorder=3
    )
    mx = x1 + (x2 - x1) * label_pos + offset[0]
    my = y1 + (y2 - y1) * label_pos + offset[1]
    ax.text(mx, my, rel_type, ha='center', va='center', fontsize=8.0, fontweight='bold', color=color,
            bbox=dict(boxstyle="square,pad=0.12", facecolor='white', edgecolor='none', alpha=0.9), zorder=4)

# ==============================================================================
# 0. USE CASE TỔNG QUÁT (15 USE CASES ĐÚNG CHUẨN)
# ==============================================================================
def gen_uc_tong_quat():
    fig, ax = plt.subplots(figsize=(16, 12), dpi=300)
    ax.set_xlim(0, 160)
    ax.set_ylim(0, 125)
    ax.axis('off')

    draw_sys_box(ax, 34, 4, 92, 117, "HỆ THỐNG ĐẶT VÉ VÀ QUẢN LÝ RẠP CHIẾU PHIM (CINESTAR CINEMA)")

    # 4 Tác nhân chính
    draw_actor(ax, 16, 92, "Khách hàng\n(Client)", scale=1.1)
    draw_actor(ax, 16, 32, "Nhân viên quầy\n(Staff)", scale=1.1)
    draw_actor(ax, 144, 92, "Quản lý rạp\n(Manager)", scale=1.1)
    draw_actor(ax, 144, 32, "Quản trị viên\n(Admin)", scale=1.1)

    # Nhóm Use Case chung ở trên cùng
    draw_uc(ax, 80, 111, "UC01. Đăng nhập & Đăng xuất", w=30, h=5.8, bgcolor='#FEF3C7', edgecolor='#B45309')
    draw_uc(ax, 80, 103, "UC02. Đăng ký tài khoản", w=30, h=5.6, bgcolor='#FEF3C7', edgecolor='#B45309')
    draw_uc(ax, 80, 95, "UC03. Quản lý thông tin tài khoản", w=30, h=5.6, bgcolor='#FEF3C7', edgecolor='#B45309')

    # Cột trái (Client & Staff)
    client_staff_ucs = [
        (58, 83, "UC04. Tra cứu phim & Lịch chiếu", 'client'),
        (58, 73, "UC05. Đặt vé trực tuyến & Chọn ghế (5p)", 'client'),
        (58, 63, "UC06. Quản lý giỏ vé & Chọn combo F&B", 'client'),
        (58, 43, "UC07. Bán vé trực tiếp tại quầy POS", 'staff'),
        (58, 29, "UC08. Soát vé QR & Cảnh báo gian lận", 'staff'),
    ]

    # Cột phải (Manager & Admin)
    mgr_admin_ucs = [
        (102, 83, "UC09. Quản lý danh mục phim", 'mgr'),
        (102, 73, "UC10. Quản lý phòng & Cấu hình ghế", 'mgr'),
        (102, 63, "UC11. Lập suất chiếu (Chống trùng)", 'mgr'),
        (102, 53, "UC12. Quản lý bảng giá & Combo F&B", 'mgr'),
        (102, 43, "UC13. Báo cáo doanh thu & Lấp đầy", 'mgr'),
        (102, 29, "UC14. Quản lý người dùng & RBAC", 'admin'),
        (102, 17, "UC15. Cài đặt hệ thống & Audit Logs", 'admin'),
    ]

    for (x, y, text, role) in client_staff_ucs:
        draw_uc(ax, x, y, text, w=29, h=6.0)
        if role == 'client':
            draw_line(ax, 20, 92, x - 14.5, y)
        elif role == 'staff':
            draw_line(ax, 20, 32, x - 14.5, y)

    for (x, y, text, role) in mgr_admin_ucs:
        draw_uc(ax, x, y, text, w=29, h=6.0)
        if role == 'mgr':
            draw_line(ax, 140, 92, x + 14.5, y)
        elif role == 'admin':
            draw_line(ax, 140, 32, x + 14.5, y)

    # Nối tác nhân tới UC chung (UC01, UC02, UC03)
    draw_line(ax, 20, 92, 65, 111)   # Client -> UC01
    draw_line(ax, 20, 92, 65, 103)   # Client -> UC02
    draw_line(ax, 20, 92, 65, 95)    # Client -> UC03
    draw_line(ax, 20, 32, 65, 111)   # Staff -> UC01
    draw_line(ax, 20, 32, 65, 95)    # Staff -> UC03
    draw_line(ax, 140, 92, 95, 111)  # Manager -> UC01
    draw_line(ax, 140, 92, 95, 95)   # Manager -> UC03
    draw_line(ax, 140, 32, 95, 111)  # Admin -> UC01
    draw_line(ax, 140, 32, 95, 95)   # Admin -> UC03

    # Kế thừa vai trò Admin -> Manager/Staff (Admin có toàn quyền)
    ax.annotate("", xy=(144, 82), xytext=(144, 42),
                arrowprops=dict(arrowstyle="->", color="#2B2D42", linestyle="-", linewidth=1.2))
    ax.text(145.5, 62, "Kế thừa\nquyền", fontsize=8, color="#2B2D42")

    plt.tight_layout()
    fpath = os.path.join(out_dir, 'uc_tong_quat.png')
    plt.savefig(fpath, dpi=300, bbox_inches='tight')
    plt.close()
    print("OK:", fpath)

# ==============================================================================
# UC01. ĐĂNG NHẬP HỆ THỐNG
# ==============================================================================
def gen_uc01():
    fig, ax = plt.subplots(figsize=(14, 8), dpi=300)
    ax.set_xlim(0, 140)
    ax.set_ylim(0, 80)
    ax.axis('off')

    draw_sys_box(ax, 34, 4, 102, 72, "PHÂN RÃ USE CASE: UC01 - ĐĂNG NHẬP HỆ THỐNG")
    draw_actor(ax, 16, 42, "Người dùng\n(User)", scale=1.1)

    # Cột 1: Use case chính
    draw_uc(ax, 58, 48, "Đăng nhập\nvào hệ thống", w=24, h=7.5, bgcolor='#FEF3C7', edgecolor='#B45309')
    draw_line(ax, 20, 42, 46, 48)

    draw_uc(ax, 58, 20, "Đăng xuất\nkhỏi hệ thống", w=24, h=7.0, bgcolor='#FEF3C7', edgecolor='#B45309')
    draw_line(ax, 20, 42, 46, 20)

    # Cột 2: Include & Extend
    draw_uc(ax, 105, 66, "Nhập Email & Mật khẩu\n(Kiểm tra cú pháp)", w=27, h=7.0)
    draw_uc(ax, 105, 52, "Xác thực BCrypt\nvới CSDL bảng users", w=27, h=7.0)
    draw_uc(ax, 105, 38, "Khởi tạo Session\n& Điều hướng theo Role", w=27, h=7.0)
    draw_uc(ax, 105, 24, "Báo lỗi sai Email\nhoặc Mật khẩu", w=27, h=7.0, bgcolor='#FFF1F2', edgecolor='#BE123C')
    draw_uc(ax, 105, 10, "Từ chối tài khoản bị khóa\n(status = 'locked')", w=27, h=7.0, bgcolor='#FFF1F2', edgecolor='#BE123C')

    draw_rel(ax, 70, 52, 91.5, 66, "<<include>>", label_pos=0.45, offset=(0, 2.0))
    draw_rel(ax, 70, 49, 91.5, 52, "<<include>>", label_pos=0.45, offset=(0, 2.0))
    draw_rel(ax, 70, 46, 91.5, 38, "<<include>>", label_pos=0.45, offset=(0, 2.0))
    draw_rel(ax, 70, 43, 91.5, 25, "<<extend>>", label_pos=0.45, offset=(0, -2.0), color='#BE123C')
    draw_rel(ax, 68, 41, 91.5, 12, "<<extend>>", label_pos=0.4, offset=(0, -2.0), color='#BE123C')

    plt.tight_layout()
    fpath = os.path.join(out_dir, 'uc01_dang_nhap.png')
    plt.savefig(fpath, dpi=300, bbox_inches='tight')
    plt.close()
    print("OK:", fpath)

# ==============================================================================
# UC02. ĐĂNG KÝ TÀI KHOẢN
# ==============================================================================
def gen_uc02():
    fig, ax = plt.subplots(figsize=(14, 8), dpi=300)
    ax.set_xlim(0, 140)
    ax.set_ylim(0, 80)
    ax.axis('off')

    draw_sys_box(ax, 34, 4, 102, 72, "PHÂN RÃ USE CASE: UC02 - ĐĂNG KÝ TÀI KHOẢN")
    draw_actor(ax, 16, 42, "Khách hàng\nvãng lai", scale=1.1)

    draw_uc(ax, 58, 42, "Đăng ký\ntài khoản mới", w=24, h=8.0, bgcolor='#FEF3C7', edgecolor='#B45309')
    draw_line(ax, 20, 42, 46, 42)

    draw_uc(ax, 105, 66, "Nhập thông tin cá nhân\n(Tên, Email, SĐT, Pass)", w=27, h=7.0)
    draw_uc(ax, 105, 52, "Kiểm tra hợp lệ dữ liệu\n(Regex Email, SĐT, Pass>=6)", w=27, h=7.0)
    draw_uc(ax, 105, 38, "Kiểm tra trùng Email\ntrong CSDL users", w=27, h=7.0)
    draw_uc(ax, 105, 24, "Băm BCrypt & Lưu User\n(role_id=4: Client)", w=27, h=7.0)
    draw_uc(ax, 105, 10, "Báo lỗi trùng Email\nhoặc Pass không khớp", w=27, h=7.0, bgcolor='#FFF1F2', edgecolor='#BE123C')

    draw_rel(ax, 70, 46, 91.5, 66, "<<include>>", label_pos=0.45, offset=(0, 2.0))
    draw_rel(ax, 70, 44, 91.5, 52, "<<include>>", label_pos=0.45, offset=(0, 2.0))
    draw_rel(ax, 70, 42, 91.5, 38, "<<include>>", label_pos=0.45, offset=(0, 2.0))
    draw_rel(ax, 70, 40, 91.5, 25, "<<include>>", label_pos=0.45, offset=(0, -2.0))
    draw_rel(ax, 68, 38, 91.5, 12, "<<extend>>", label_pos=0.4, offset=(0, -2.0), color='#BE123C')

    plt.tight_layout()
    fpath = os.path.join(out_dir, 'uc02_dang_ky.png')
    plt.savefig(fpath, dpi=300, bbox_inches='tight')
    plt.close()
    print("OK:", fpath)

# ==============================================================================
# UC03. QUẢN LÝ THÔNG TIN TÀI KHOẢN
# ==============================================================================
def gen_uc03():
    fig, ax = plt.subplots(figsize=(14, 8), dpi=300)
    ax.set_xlim(0, 140)
    ax.set_ylim(0, 80)
    ax.axis('off')

    draw_sys_box(ax, 34, 4, 102, 72, "PHÂN RÃ USE CASE: UC03 - QUẢN LÝ THÔNG TIN TÀI KHOẢN")
    draw_actor(ax, 16, 42, "Người dùng\nđã đăng nhập", scale=1.1)

    draw_uc(ax, 58, 54, "Xem hồ sơ\ncá nhân", w=24, h=7.5, bgcolor='#FEF3C7', edgecolor='#B45309')
    draw_uc(ax, 58, 26, "Đổi mật khẩu\ntài khoản", w=24, h=7.5, bgcolor='#FEF3C7', edgecolor='#B45309')
    draw_line(ax, 20, 42, 46, 54)
    draw_line(ax, 20, 42, 46, 26)

    draw_uc(ax, 105, 66, "Hiển thị thông tin\n(Họ tên, Email, SĐT, Role)", w=27, h=7.0)
    draw_uc(ax, 105, 52, "Cập nhật thông tin\n(Họ tên & Số điện thoại)", w=27, h=7.0)
    draw_uc(ax, 105, 34, "Xác thực mật khẩu cũ\nqua BCrypt.compare()", w=27, h=7.0)
    draw_uc(ax, 105, 20, "Cập nhật mật khẩu mới\n(Băm BCrypt & Lưu CSDL)", w=27, h=7.0)
    draw_uc(ax, 105, 8, "Báo lỗi khi mật khẩu cũ\nkhông chính xác", w=27, h=6.6, bgcolor='#FFF1F2', edgecolor='#BE123C')

    draw_rel(ax, 70, 56, 91.5, 66, "<<include>>", label_pos=0.5, offset=(0, 2.0))
    draw_rel(ax, 70, 53, 91.5, 52, "<<extend>>", label_pos=0.5, offset=(0, 2.0))
    draw_rel(ax, 70, 28, 91.5, 34, "<<include>>", label_pos=0.5, offset=(0, 2.0))
    draw_rel(ax, 70, 25, 91.5, 20, "<<include>>", label_pos=0.5, offset=(0, -2.0))
    draw_rel(ax, 70, 22, 91.5, 9, "<<extend>>", label_pos=0.5, offset=(0, -2.0), color='#BE123C')

    plt.tight_layout()
    fpath = os.path.join(out_dir, 'uc03_quan_ly_tai_khoan.png')
    plt.savefig(fpath, dpi=300, bbox_inches='tight')
    plt.close()
    print("OK:", fpath)

# ==============================================================================
# UC04. TRA CỨU PHIM VÀ LỊCH CHIẾU RẠP
# ==============================================================================
def gen_uc04():
    fig, ax = plt.subplots(figsize=(14, 8), dpi=300)
    ax.set_xlim(0, 140)
    ax.set_ylim(0, 80)
    ax.axis('off')

    draw_sys_box(ax, 34, 4, 102, 72, "PHÂN RÃ USE CASE: UC04 - TRA CỨU PHIM VÀ LỊCH CHIẾU RẠP")
    draw_actor(ax, 16, 42, "Khách hàng\n(Client/Guest)", scale=1.1)

    draw_uc(ax, 58, 54, "Xem danh sách phim\n(Đang & Sắp chiếu)", w=24, h=7.5, bgcolor='#FEF3C7', edgecolor='#B45309')
    draw_uc(ax, 58, 26, "Xem chi tiết phim\n& Lịch chiếu rạp", w=24, h=7.5, bgcolor='#FEF3C7', edgecolor='#B45309')
    draw_line(ax, 20, 42, 46, 54)
    draw_line(ax, 20, 42, 46, 26)

    draw_uc(ax, 105, 66, "Tìm kiếm phim theo từ khóa\n(Tên phim, thể loại)", w=27, h=7.0)
    draw_uc(ax, 105, 52, "Lọc phim theo ngày chiếu\n& cụm rạp CineStar", w=27, h=7.0)
    draw_uc(ax, 105, 36, "Xem thông tin chi tiết\n(Đạo diễn, diễn viên, độ tuổi)", w=27, h=7.0)
    draw_uc(ax, 105, 22, "Xem Trailer phim\n(Nhúng video YouTube)", w=27, h=7.0)
    draw_uc(ax, 105, 8, "Tra cứu khung giờ chiếu\n& Phòng chiếu khả dụng", w=27, h=6.6)

    draw_rel(ax, 70, 57, 91.5, 66, "<<extend>>", label_pos=0.5, offset=(0, 2.0))
    draw_rel(ax, 70, 53, 91.5, 52, "<<extend>>", label_pos=0.5, offset=(0, 2.0))
    draw_rel(ax, 70, 28, 91.5, 36, "<<include>>", label_pos=0.5, offset=(0, 2.0))
    draw_rel(ax, 70, 25, 91.5, 22, "<<extend>>", label_pos=0.5, offset=(0, -2.0))
    draw_rel(ax, 70, 22, 91.5, 9, "<<include>>", label_pos=0.5, offset=(0, -2.0))

    plt.tight_layout()
    fpath = os.path.join(out_dir, 'uc04_tra_cuu_phim.png')
    plt.savefig(fpath, dpi=300, bbox_inches='tight')
    plt.close()
    print("OK:", fpath)

# ==============================================================================
# UC05. ĐẶT VÉ TRỰC TUYẾN & CHỌN GHẾ NGỒI
# ==============================================================================
def gen_uc05():
    fig, ax = plt.subplots(figsize=(14, 8), dpi=300)
    ax.set_xlim(0, 140)
    ax.set_ylim(0, 80)
    ax.axis('off')

    draw_sys_box(ax, 34, 4, 102, 72, "PHÂN RÃ USE CASE: UC05 - ĐẶT VÉ TRỰC TUYẾN & CHỌN GHẾ NGỒI")
    draw_actor(ax, 16, 42, "Khách hàng\n(Client)", scale=1.1)

    draw_uc(ax, 58, 42, "Đặt vé & Chọn ghế\ntrực tuyến", w=24, h=8.0, bgcolor='#FEF3C7', edgecolor='#B45309')
    draw_line(ax, 20, 42, 46, 42)

    draw_uc(ax, 105, 66, "Hiển thị sơ đồ ghế ma trận\n(Thường, VIP, Sweetbox)", w=27, h=7.0)
    draw_uc(ax, 105, 52, "Chọn vị trí ghế ngồi\n(Tính tiền theo hệ số giá)", w=27, h=7.0)
    draw_uc(ax, 105, 38, "Khóa giữ ghế tạm 5 phút\n(Gọi API SeatLock)", w=27, h=7.0)
    draw_uc(ax, 105, 24, "Cảnh báo ghế đã bị đặt\nhoặc đang được giữ", w=27, h=7.0, bgcolor='#FFF1F2', edgecolor='#BE123C')
    draw_uc(ax, 105, 10, "Tự động nhả ghế khi hết\nthời gian 5:00 đếm ngược", w=27, h=7.0, bgcolor='#FFF1F2', edgecolor='#BE123C')

    draw_rel(ax, 70, 46, 91.5, 66, "<<include>>", label_pos=0.45, offset=(0, 2.0))
    draw_rel(ax, 70, 44, 91.5, 52, "<<include>>", label_pos=0.45, offset=(0, 2.0))
    draw_rel(ax, 70, 42, 91.5, 38, "<<include>>", label_pos=0.45, offset=(0, 2.0))
    draw_rel(ax, 70, 40, 91.5, 25, "<<extend>>", label_pos=0.45, offset=(0, -2.0), color='#BE123C')
    draw_rel(ax, 68, 38, 91.5, 12, "<<extend>>", label_pos=0.4, offset=(0, -2.0), color='#BE123C')

    plt.tight_layout()
    fpath = os.path.join(out_dir, 'uc05_dat_ve_chon_ghe.png')
    plt.savefig(fpath, dpi=300, bbox_inches='tight')
    plt.close()
    print("OK:", fpath)

# ==============================================================================
# UC06. QUẢN LÝ GIỎ VÉ & CHỌN COMBO BẮP NƯỚC
# ==============================================================================
def gen_uc06():
    fig, ax = plt.subplots(figsize=(14, 8), dpi=300)
    ax.set_xlim(0, 140)
    ax.set_ylim(0, 80)
    ax.axis('off')

    draw_sys_box(ax, 34, 4, 102, 72, "PHÂN RÃ USE CASE: UC06 - QUẢN LÝ GIỎ VÉ & CHỌN COMBO BẮP NƯỚC")
    draw_actor(ax, 16, 42, "Khách hàng\n(Client)", scale=1.1)

    draw_uc(ax, 58, 54, "Chọn combo F&B\n& Kiểm tra đơn", w=24, h=7.5, bgcolor='#FEF3C7', edgecolor='#B45309')
    draw_uc(ax, 58, 26, "Thanh toán & Nhận vé\n('Vé của tôi')", w=24, h=7.5, bgcolor='#FEF3C7', edgecolor='#B45309')
    draw_line(ax, 20, 42, 46, 54)
    draw_line(ax, 20, 42, 46, 26)

    draw_uc(ax, 105, 66, "Thêm combo bắp nước F&B\n(Tăng / giảm số lượng)", w=27, h=7.0)
    draw_uc(ax, 105, 52, "Tính tổng tiền đơn hàng\n(Tiền vé + Tiền combo)", w=27, h=7.0)
    draw_uc(ax, 105, 36, "Chọn phương thức TT\n(VNPAY, MoMo, Thẻ ATM)", w=27, h=7.0)
    draw_uc(ax, 105, 22, "Xác nhận TT & Tạo Booking\n(payment_status = 'paid')", w=27, h=7.0)
    draw_uc(ax, 105, 8, "Sinh vé điện tử chi tiết\nkèm mã QR Code soát vé", w=27, h=6.6)

    draw_rel(ax, 70, 56, 91.5, 66, "<<extend>>", label_pos=0.5, offset=(0, 2.0))
    draw_rel(ax, 70, 53, 91.5, 52, "<<include>>", label_pos=0.5, offset=(0, 2.0))
    draw_rel(ax, 70, 28, 91.5, 36, "<<include>>", label_pos=0.5, offset=(0, 2.0))
    draw_rel(ax, 70, 25, 91.5, 22, "<<include>>", label_pos=0.5, offset=(0, -2.0))
    draw_rel(ax, 70, 22, 91.5, 9, "<<include>>", label_pos=0.5, offset=(0, -2.0))

    plt.tight_layout()
    fpath = os.path.join(out_dir, 'uc06_gio_ve_combo.png')
    plt.savefig(fpath, dpi=300, bbox_inches='tight')
    plt.close()
    print("OK:", fpath)

# ==============================================================================
# UC07. BÁN VÉ TRỰC TIẾP TẠI QUẦY POS
# ==============================================================================
def gen_uc07():
    fig, ax = plt.subplots(figsize=(14, 8), dpi=300)
    ax.set_xlim(0, 140)
    ax.set_ylim(0, 80)
    ax.axis('off')

    draw_sys_box(ax, 34, 4, 102, 72, "PHÂN RÃ USE CASE: UC07 - BÁN VÉ TRỰC TIẾP TẠI QUẦY POS")
    draw_actor(ax, 16, 42, "Nhân viên quầy\n(Staff)", scale=1.1)

    draw_uc(ax, 58, 42, "Bán vé xem phim\ntại quầy POS", w=24, h=8.0, bgcolor='#FEF3C7', edgecolor='#B45309')
    draw_line(ax, 20, 42, 46, 42)

    draw_uc(ax, 105, 66, "Tra cứu suất chiếu hôm nay\n& Sơ đồ ghế quầy POS", w=27, h=7.0)
    draw_uc(ax, 105, 52, "Chọn vị trí ghế ngồi\n& Thêm combo bắp nước", w=27, h=7.0)
    draw_uc(ax, 105, 38, "Nhập thông tin khách mua\n(Khách vãng lai, Tên, SĐT)", w=27, h=7.0)
    draw_uc(ax, 105, 24, "Thu tiền tại quầy\n(Tiền mặt / Thẻ ngân hàng)", w=27, h=7.0)
    draw_uc(ax, 105, 10, "Xuất đơn POS & In vé xem phim\nkèm mã QR Code quầy", w=27, h=7.0)

    draw_rel(ax, 70, 46, 91.5, 66, "<<include>>", label_pos=0.45, offset=(0, 2.0))
    draw_rel(ax, 70, 44, 91.5, 52, "<<include>>", label_pos=0.45, offset=(0, 2.0))
    draw_rel(ax, 70, 42, 91.5, 38, "<<include>>", label_pos=0.45, offset=(0, 2.0))
    draw_rel(ax, 70, 40, 91.5, 25, "<<include>>", label_pos=0.45, offset=(0, -2.0))
    draw_rel(ax, 68, 38, 91.5, 12, "<<include>>", label_pos=0.4, offset=(0, -2.0))

    plt.tight_layout()
    fpath = os.path.join(out_dir, 'uc07_ban_ve_pos.png')
    plt.savefig(fpath, dpi=300, bbox_inches='tight')
    plt.close()
    print("OK:", fpath)

# ==============================================================================
# UC08. SOÁT VÉ QUA MÃ QR & CẢNH BÁO GIAN LẬN
# ==============================================================================
def gen_uc08():
    fig, ax = plt.subplots(figsize=(14, 8), dpi=300)
    ax.set_xlim(0, 140)
    ax.set_ylim(0, 80)
    ax.axis('off')

    draw_sys_box(ax, 34, 4, 102, 72, "PHÂN RÃ USE CASE: UC08 - SOÁT VÉ QR & CẢNH BÁO GIAN LẬN")
    draw_actor(ax, 16, 42, "Nhân viên\nsoát vé", scale=1.1)

    draw_uc(ax, 58, 48, "Quét mã QR\nsoát vé vào cửa", w=24, h=7.5, bgcolor='#FEF3C7', edgecolor='#B45309')
    draw_uc(ax, 58, 18, "Xem lịch sử\nsoát vé trong ca", w=24, h=7.0, bgcolor='#FEF3C7', edgecolor='#B45309')
    draw_line(ax, 20, 42, 46, 48)
    draw_line(ax, 20, 42, 46, 18)

    draw_uc(ax, 105, 66, "Quét QR qua Camera\nhoặc nhập mã TKT thủ công", w=27, h=7.0)
    draw_uc(ax, 105, 52, "Đối soát mã vé trong CSDL\n(Kiểm tra bảng tickets)", w=27, h=7.0)
    draw_uc(ax, 105, 38, "Xác nhận check-in (Đổi\nstatus='checked_in', lưu giờ)", w=27, h=7.0)
    draw_uc(ax, 105, 24, "Cảnh báo ĐỎ vé đã dùng\n(Gian lận vé quay vòng)", w=27, h=7.0, bgcolor='#FFF1F2', edgecolor='#BE123C')
    draw_uc(ax, 105, 10, "Cảnh báo vé không tồn tại\nhoặc vé giả mạo", w=27, h=7.0, bgcolor='#FFF1F2', edgecolor='#BE123C')

    draw_rel(ax, 70, 52, 91.5, 66, "<<include>>", label_pos=0.45, offset=(0, 2.0))
    draw_rel(ax, 70, 49, 91.5, 52, "<<include>>", label_pos=0.45, offset=(0, 2.0))
    draw_rel(ax, 70, 46, 91.5, 38, "<<include>>", label_pos=0.45, offset=(0, 2.0))
    draw_rel(ax, 70, 43, 91.5, 25, "<<extend>>", label_pos=0.45, offset=(0, -2.0), color='#BE123C')
    draw_rel(ax, 68, 41, 91.5, 12, "<<extend>>", label_pos=0.4, offset=(0, -2.0), color='#BE123C')

    plt.tight_layout()
    fpath = os.path.join(out_dir, 'uc08_soat_ve_qr.png')
    plt.savefig(fpath, dpi=300, bbox_inches='tight')
    plt.close()
    print("OK:", fpath)

# ==============================================================================
# UC09. QUẢN LÝ DANH MỤC PHIM CHIẾU RẠP
# ==============================================================================
def gen_uc09():
    fig, ax = plt.subplots(figsize=(14, 8), dpi=300)
    ax.set_xlim(0, 140)
    ax.set_ylim(0, 80)
    ax.axis('off')

    draw_sys_box(ax, 34, 4, 102, 72, "PHÂN RÃ USE CASE: UC09 - QUẢN LÝ DANH MỤC PHIM CHIẾU RẠP")
    draw_actor(ax, 16, 42, "Quản lý rạp\n(Manager)", scale=1.1)

    draw_uc(ax, 58, 42, "Quản lý\ndanh mục phim", w=24, h=8.0, bgcolor='#FEF3C7', edgecolor='#B45309')
    draw_line(ax, 20, 42, 46, 42)

    draw_uc(ax, 105, 66, "Xem danh sách & Lọc phim\ntheo trạng thái phát hành", w=27, h=7.0)
    draw_uc(ax, 105, 52, "Thêm mới phim chiếu rạp\n(Tải lên Poster & Link Trailer)", w=27, h=7.0)
    draw_uc(ax, 105, 38, "Chỉnh sửa thông tin phim\n(Tiêu đề, thời lượng, độ tuổi)", w=27, h=7.0)
    draw_uc(ax, 105, 24, "Cập nhật trạng thái phim\n(now_showing / coming_soon / ended)", w=27, h=7.0)
    draw_uc(ax, 105, 10, "Xóa phim khỏi hệ thống\n(Ràng buộc toàn vẹn suất chiếu)", w=27, h=7.0, bgcolor='#FFF1F2', edgecolor='#BE123C')

    draw_rel(ax, 70, 46, 91.5, 66, "<<include>>", label_pos=0.45, offset=(0, 2.0))
    draw_rel(ax, 70, 44, 91.5, 52, "<<extend>>", label_pos=0.45, offset=(0, 2.0))
    draw_rel(ax, 70, 42, 91.5, 38, "<<extend>>", label_pos=0.45, offset=(0, 2.0))
    draw_rel(ax, 70, 40, 91.5, 25, "<<extend>>", label_pos=0.45, offset=(0, -2.0))
    draw_rel(ax, 68, 38, 91.5, 12, "<<extend>>", label_pos=0.4, offset=(0, -2.0), color='#BE123C')

    plt.tight_layout()
    fpath = os.path.join(out_dir, 'uc09_quan_ly_phim.png')
    plt.savefig(fpath, dpi=300, bbox_inches='tight')
    plt.close()
    print("OK:", fpath)

# ==============================================================================
# UC10. QUẢN LÝ PHÒNG CHIẾU & CẤU HÌNH SƠ ĐỒ GHẾ
# ==============================================================================
def gen_uc10():
    fig, ax = plt.subplots(figsize=(14, 8), dpi=300)
    ax.set_xlim(0, 140)
    ax.set_ylim(0, 80)
    ax.axis('off')

    draw_sys_box(ax, 34, 4, 102, 72, "PHÂN RÃ USE CASE: UC10 - QUẢN LÝ PHÒNG CHIẾU & SƠ ĐỒ GHẾ")
    draw_actor(ax, 16, 42, "Quản lý rạp\n(Manager)", scale=1.1)

    draw_uc(ax, 58, 42, "Quản lý phòng chiếu\n& Cấu hình ghế", w=24, h=8.0, bgcolor='#FEF3C7', edgecolor='#B45309')
    draw_line(ax, 20, 42, 46, 42)

    draw_uc(ax, 105, 66, "Xem danh sách phòng chiếu\n(Loại màn hình: 2D, 3D, IMAX)", w=27, h=7.0)
    draw_uc(ax, 105, 52, "Tạo phòng chiếu mới\n& Tự sinh sơ đồ ma trận ghế", w=27, h=7.0)
    draw_uc(ax, 105, 38, "Xem chi tiết sơ đồ ghế\ntheo từng hàng (A -> G)", w=27, h=7.0)
    draw_uc(ax, 105, 24, "Bật / Tắt bảo trì ghế hỏng\n(active <-> maintenance)", w=27, h=7.0)
    draw_uc(ax, 105, 10, "Cập nhật phân loại ghế\n(Thường, VIP, Sweetbox)", w=27, h=7.0)

    draw_rel(ax, 70, 46, 91.5, 66, "<<include>>", label_pos=0.45, offset=(0, 2.0))
    draw_rel(ax, 70, 44, 91.5, 52, "<<extend>>", label_pos=0.45, offset=(0, 2.0))
    draw_rel(ax, 70, 42, 91.5, 38, "<<include>>", label_pos=0.45, offset=(0, 2.0))
    draw_rel(ax, 70, 40, 91.5, 25, "<<extend>>", label_pos=0.45, offset=(0, -2.0))
    draw_rel(ax, 68, 38, 91.5, 12, "<<extend>>", label_pos=0.4, offset=(0, -2.0))

    plt.tight_layout()
    fpath = os.path.join(out_dir, 'uc10_quan_ly_phong_chieu.png')
    plt.savefig(fpath, dpi=300, bbox_inches='tight')
    plt.close()
    print("OK:", fpath)

# ==============================================================================
# UC11. LẬP LỊCH SUẤT CHIẾU & CHỐNG XUNG ĐỘT
# ==============================================================================
def gen_uc11():
    fig, ax = plt.subplots(figsize=(14, 8), dpi=300)
    ax.set_xlim(0, 140)
    ax.set_ylim(0, 80)
    ax.axis('off')

    draw_sys_box(ax, 34, 4, 102, 72, "PHÂN RÃ USE CASE: UC11 - LẬP LỊCH SUẤT CHIẾU & CHỐNG XUNG ĐỘT")
    draw_actor(ax, 16, 42, "Quản lý rạp\n(Manager)", scale=1.1)

    draw_uc(ax, 58, 48, "Lập lịch suất chiếu\nmới cho phòng", w=24, h=7.5, bgcolor='#FEF3C7', edgecolor='#B45309')
    draw_uc(ax, 58, 18, "Quản lý & Hủy\nsuất chiếu hiện có", w=24, h=7.0, bgcolor='#FEF3C7', edgecolor='#B45309')
    draw_line(ax, 20, 42, 46, 48)
    draw_line(ax, 20, 42, 46, 18)

    draw_uc(ax, 105, 66, "Chọn Phim, Phòng chiếu,\nNgày & Giờ bắt đầu", w=27, h=7.0)
    draw_uc(ax, 105, 52, "Tự động tính giờ kết thúc\n(start + duration + buffer 15p)", w=27, h=7.0)
    draw_uc(ax, 105, 38, "Kiểm tra xung đột phòng\n(ConflictDetector kiểm tra giao thoa)", w=27, h=7.0)
    draw_uc(ax, 105, 24, "Cảnh báo trùng lịch phòng\n& Khóa nút Lưu suất chiếu", w=27, h=7.0, bgcolor='#FFF1F2', edgecolor='#BE123C')
    draw_uc(ax, 105, 10, "Lưu suất chiếu vào CSDL\n& Cập nhật trạng thái scheduled", w=27, h=7.0)

    draw_rel(ax, 70, 52, 91.5, 66, "<<include>>", label_pos=0.45, offset=(0, 2.0))
    draw_rel(ax, 70, 49, 91.5, 52, "<<include>>", label_pos=0.45, offset=(0, 2.0))
    draw_rel(ax, 70, 46, 91.5, 38, "<<include>>", label_pos=0.45, offset=(0, 2.0))
    draw_rel(ax, 70, 43, 91.5, 25, "<<extend>>", label_pos=0.45, offset=(0, -2.0), color='#BE123C')
    draw_rel(ax, 68, 41, 91.5, 12, "<<include>>", label_pos=0.4, offset=(0, -2.0))

    plt.tight_layout()
    fpath = os.path.join(out_dir, 'uc11_lap_suat_chieu.png')
    plt.savefig(fpath, dpi=300, bbox_inches='tight')
    plt.close()
    print("OK:", fpath)

# ==============================================================================
# UC12. QUẢN LÝ BẢNG GIÁ VÉ VÀ COMBO F&B
# ==============================================================================
def gen_uc12():
    fig, ax = plt.subplots(figsize=(14, 8), dpi=300)
    ax.set_xlim(0, 140)
    ax.set_ylim(0, 80)
    ax.axis('off')

    draw_sys_box(ax, 34, 4, 102, 72, "PHÂN RÃ USE CASE: UC12 - QUẢN LÝ BẢNG GIÁ VÉ VÀ COMBO F&B")
    draw_actor(ax, 16, 42, "Quản lý rạp\n(Manager)", scale=1.1)

    draw_uc(ax, 58, 54, "Cấu hình bảng\ngiá vé rạp", w=24, h=7.5, bgcolor='#FEF3C7', edgecolor='#B45309')
    draw_uc(ax, 58, 26, "Quản lý danh mục\ncombo bắp nước F&B", w=24, h=7.5, bgcolor='#FEF3C7', edgecolor='#B45309')
    draw_line(ax, 20, 42, 46, 54)
    draw_line(ax, 20, 42, 46, 26)

    draw_uc(ax, 105, 66, "Cấu hình giá vé cơ bản\ntheo loại phòng (2D, 3D, IMAX)", w=27, h=7.0)
    draw_uc(ax, 105, 52, "Thiết lập hệ số giá ghế\n(Thường: 1.0, VIP: 1.25, Đôi: 2.2)", w=27, h=7.0)
    draw_uc(ax, 105, 36, "Xem danh sách combo F&B\n(Tên, mô tả, giá bán, ảnh)", w=27, h=7.0)
    draw_uc(ax, 105, 22, "Thêm mới gói combo F&B\nvào thực đơn bán hàng", w=27, h=7.0)
    draw_uc(ax, 105, 8, "Chỉnh sửa hoặc xóa combo\n(status = 'inactive')", w=27, h=6.6)

    draw_rel(ax, 70, 56, 91.5, 66, "<<include>>", label_pos=0.5, offset=(0, 2.0))
    draw_rel(ax, 70, 53, 91.5, 52, "<<include>>", label_pos=0.5, offset=(0, 2.0))
    draw_rel(ax, 70, 28, 91.5, 36, "<<include>>", label_pos=0.5, offset=(0, 2.0))
    draw_rel(ax, 70, 25, 91.5, 22, "<<extend>>", label_pos=0.5, offset=(0, -2.0))
    draw_rel(ax, 70, 22, 91.5, 9, "<<extend>>", label_pos=0.5, offset=(0, -2.0))

    plt.tight_layout()
    fpath = os.path.join(out_dir, 'uc12_gia_ve_combo.png')
    plt.savefig(fpath, dpi=300, bbox_inches='tight')
    plt.close()
    print("OK:", fpath)

# ==============================================================================
# UC13. BÁO CÁO THỐNG KÊ DOANH THU & TỶ LỆ LẤP ĐẦY
# ==============================================================================
def gen_uc13():
    fig, ax = plt.subplots(figsize=(14, 8), dpi=300)
    ax.set_xlim(0, 140)
    ax.set_ylim(0, 80)
    ax.axis('off')

    draw_sys_box(ax, 34, 4, 102, 72, "PHÂN RÃ USE CASE: UC13 - BÁO CÁO THỐNG KÊ DOANH THU & LẤP ĐẦY")
    draw_actor(ax, 16, 42, "Quản lý rạp\n(Manager)", scale=1.1)

    draw_uc(ax, 58, 42, "Xem báo cáo thống kê\n& Dashboard quản lý", w=24, h=8.0, bgcolor='#FEF3C7', edgecolor='#B45309')
    draw_line(ax, 20, 42, 46, 42)

    draw_uc(ax, 105, 66, "Xem Dashboard KPI hôm nay\n(Doanh thu, vé bán, suất chiếu)", w=27, h=7.0)
    draw_uc(ax, 105, 52, "Theo dõi biểu đồ cột 7 ngày\n(Chart.js trực quan doanh thu)", w=27, h=7.0)
    draw_uc(ax, 105, 38, "Thống kê doanh thu theo phim\n(Doanh thu vé + F&B combo)", w=27, h=7.0)
    draw_uc(ax, 105, 24, "Tính Tỷ lệ lấp đầy phòng chiếu\n(Occupancy Rate % theo suất)", w=27, h=7.0)
    draw_uc(ax, 105, 10, "Lọc báo cáo theo khoảng thời gian\n(Hôm nay, 7 ngày, tháng này)", w=27, h=7.0)

    draw_rel(ax, 70, 46, 91.5, 66, "<<include>>", label_pos=0.45, offset=(0, 2.0))
    draw_rel(ax, 70, 44, 91.5, 52, "<<include>>", label_pos=0.45, offset=(0, 2.0))
    draw_rel(ax, 70, 42, 91.5, 38, "<<include>>", label_pos=0.45, offset=(0, 2.0))
    draw_rel(ax, 70, 40, 91.5, 25, "<<include>>", label_pos=0.45, offset=(0, -2.0))
    draw_rel(ax, 68, 38, 91.5, 12, "<<extend>>", label_pos=0.4, offset=(0, -2.0))

    plt.tight_layout()
    fpath = os.path.join(out_dir, 'uc13_bao_cao_doanh_thu.png')
    plt.savefig(fpath, dpi=300, bbox_inches='tight')
    plt.close()
    print("OK:", fpath)

# ==============================================================================
# UC14. QUẢN LÝ NGƯỜI DÙNG & PHÂN QUYỀN VAI TRÒ (RBAC)
# ==============================================================================
def gen_uc14():
    fig, ax = plt.subplots(figsize=(14, 8), dpi=300)
    ax.set_xlim(0, 140)
    ax.set_ylim(0, 80)
    ax.axis('off')

    draw_sys_box(ax, 34, 4, 102, 72, "PHÂN RÃ USE CASE: UC14 - QUẢN LÝ NGƯỜI DÙNG & PHÂN QUYỀN RBAC")
    draw_actor(ax, 16, 42, "Quản trị viên\n(Admin)", scale=1.1)

    draw_uc(ax, 58, 42, "Quản lý người dùng\n& Phân quyền RBAC", w=24, h=8.0, bgcolor='#FEF3C7', edgecolor='#B45309')
    draw_line(ax, 20, 42, 46, 42)

    draw_uc(ax, 105, 66, "Xem danh sách & Lọc người dùng\ntheo vai trò (Admin, Mgr, Staff, Client)", w=27, h=7.0)
    draw_uc(ax, 105, 52, "Tạo mới tài khoản nhân viên\nhoặc quản lý rạp", w=27, h=7.0)
    draw_uc(ax, 105, 38, "Phân quyền vai trò RBAC\n(Cập nhật role_id trong users)", w=27, h=7.0)
    draw_uc(ax, 105, 24, "Khóa / Mở khóa tài khoản\n(Chuyển đổi status: active / locked)", w=27, h=7.0)
    draw_uc(ax, 105, 10, "Xóa tài khoản người dùng\n(Bảo vệ tài khoản quản trị chính)", w=27, h=7.0, bgcolor='#FFF1F2', edgecolor='#BE123C')

    draw_rel(ax, 70, 46, 91.5, 66, "<<include>>", label_pos=0.45, offset=(0, 2.0))
    draw_rel(ax, 70, 44, 91.5, 52, "<<extend>>", label_pos=0.45, offset=(0, 2.0))
    draw_rel(ax, 70, 42, 91.5, 38, "<<include>>", label_pos=0.45, offset=(0, 2.0))
    draw_rel(ax, 70, 40, 91.5, 25, "<<extend>>", label_pos=0.45, offset=(0, -2.0))
    draw_rel(ax, 68, 38, 91.5, 12, "<<extend>>", label_pos=0.4, offset=(0, -2.0), color='#BE123C')

    plt.tight_layout()
    fpath = os.path.join(out_dir, 'uc14_quan_ly_nguoi_dung.png')
    plt.savefig(fpath, dpi=300, bbox_inches='tight')
    plt.close()
    print("OK:", fpath)

# ==============================================================================
# UC15. CẤU HÌNH THAM SỐ RẠP & GIÁM SÁT AUDIT LOG
# ==============================================================================
def gen_uc15():
    fig, ax = plt.subplots(figsize=(14, 8), dpi=300)
    ax.set_xlim(0, 140)
    ax.set_ylim(0, 80)
    ax.axis('off')

    draw_sys_box(ax, 34, 4, 102, 72, "PHÂN RÃ USE CASE: UC15 - CẤU HÌNH THAM SỐ RẠP & AUDIT LOGS")
    draw_actor(ax, 16, 42, "Quản trị viên\n(Admin)", scale=1.1)

    draw_uc(ax, 58, 54, "Cấu hình tham số\nvận hành rạp", w=24, h=7.5, bgcolor='#FEF3C7', edgecolor='#B45309')
    draw_uc(ax, 58, 26, "Giám sát nhật ký\nkiểm toán (Audit Log)", w=24, h=7.5, bgcolor='#FEF3C7', edgecolor='#B45309')
    draw_line(ax, 20, 42, 46, 54)
    draw_line(ax, 20, 42, 46, 26)

    draw_uc(ax, 105, 66, "Cấu hình thời gian đệm dọn phòng\n(buffer_minutes = 15 phút)", w=27, h=7.0)
    draw_uc(ax, 105, 52, "Cấu hình thời gian giữ ghế tạm\n(hold_time = 5 phút)", w=27, h=7.0)
    draw_uc(ax, 105, 36, "Cập nhật thông tin rạp chiếu\n(Tên rạp, hotline, địa chỉ)", w=27, h=7.0)
    draw_uc(ax, 105, 22, "Xem lịch sử thao tác hệ thống\n(Timestamp, User, Hành động, IP)", w=27, h=7.0)
    draw_uc(ax, 105, 8, "Lọc và tra cứu nhật ký\nkiểm toán theo thời gian", w=27, h=6.6)

    draw_rel(ax, 70, 56, 91.5, 66, "<<include>>", label_pos=0.5, offset=(0, 2.0))
    draw_rel(ax, 70, 53, 91.5, 52, "<<include>>", label_pos=0.5, offset=(0, 2.0))
    draw_rel(ax, 70, 50, 91.5, 36, "<<include>>", label_pos=0.5, offset=(0, -2.0))
    draw_rel(ax, 70, 26, 91.5, 22, "<<include>>", label_pos=0.5, offset=(0, 2.0))
    draw_rel(ax, 70, 23, 91.5, 9, "<<extend>>", label_pos=0.5, offset=(0, -2.0))

    plt.tight_layout()
    fpath = os.path.join(out_dir, 'uc15_cau_hinh_audit.png')
    plt.savefig(fpath, dpi=300, bbox_inches='tight')
    plt.close()
    print("OK:", fpath)

if __name__ == '__main__':
    print("🚀 Bắt đầu tạo 16 biểu đồ Use Case chất lượng cao...")
    gen_uc_tong_quat()
    gen_uc01()
    gen_uc02()
    gen_uc03()
    gen_uc04()
    gen_uc05()
    gen_uc06()
    gen_uc07()
    gen_uc08()
    gen_uc09()
    gen_uc10()
    gen_uc11()
    gen_uc12()
    gen_uc13()
    gen_uc14()
    gen_uc15()
    print("🎉 Hoàn tất tạo toàn bộ 16 biểu đồ!")
