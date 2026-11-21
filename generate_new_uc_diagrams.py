import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['figure.autolayout'] = True

img_dir = os.path.join('report_assets', 'images')
os.makedirs(img_dir, exist_ok=True)

def draw_actor(ax, x, y, name, scale=1.0):
    head = patches.Circle((x, y + 4*scale), 1.5*scale, facecolor='white', edgecolor='black', linewidth=1.5)
    ax.add_patch(head)
    # Body
    ax.plot([x, x], [y + 2.5*scale, y - 1.5*scale], color='black', linewidth=1.5)
    # Arms
    ax.plot([x - 2.5*scale, x + 2.5*scale], [y + 1*scale, y + 1*scale], color='black', linewidth=1.5)
    # Legs
    ax.plot([x, x - 2*scale], [y - 1.5*scale, y - 5*scale], color='black', linewidth=1.5)
    ax.plot([x, x + 2*scale], [y - 1.5*scale, y - 5*scale], color='black', linewidth=1.5)
    # Label
    ax.text(x, y - 7.5*scale, name, ha='center', va='top', fontsize=9.5, fontweight='bold')

def draw_usecase(ax, x, y, text, w=27, h=6.5, fontsize=9.0):
    ellipse = patches.Ellipse((x, y), w, h, facecolor='white', edgecolor='black', linewidth=1.3)
    ax.add_patch(ellipse)
    ax.text(x, y, text, ha='center', va='center', fontsize=fontsize)

# -----------------------------------------------------------------------------
# 1. BIỂU ĐỒ USE CASE TỔNG QUÁT (15 USE CASES CHÍNH)
# -----------------------------------------------------------------------------
def generate_uc_tong_quat():
    fig, ax = plt.subplots(figsize=(16, 12.5), dpi=300)
    ax.set_xlim(0, 160)
    ax.set_ylim(0, 130)
    ax.axis('off')

    sys_box = patches.Rectangle((35, 5), 90, 120, facecolor='white', edgecolor='black', linewidth=1.6)
    ax.add_patch(sys_box)
    ax.text(80, 121, "HỆ THỐNG ĐẶT VÉ VÀ QUẢN LÝ SUẤT CHIẾU CINESTAR CINEMA", ha='center', va='center', fontsize=11.5, fontweight='bold')

    # Actors
    draw_actor(ax, 16, 92, "Khách hàng\n(Client)", scale=1.1)
    draw_actor(ax, 16, 26, "Nhân viên quầy\n(Staff)", scale=1.1)
    draw_actor(ax, 144, 92, "Quản lý rạp\n(Manager)", scale=1.1)
    draw_actor(ax, 144, 26, "Quản trị viên\n(Admin)", scale=1.1)

    # Common UC
    draw_usecase(ax, 80, 112, "UC01. Đăng ký & Đăng nhập", w=28, h=6.5)

    # Client UCs (6 UCs)
    ucs_client = [
        (58, 100, "UC02. Tra cứu danh mục phim"),
        (58, 87, "UC03. Xem lịch chiếu rạp & ngày"),
        (58, 74, "UC04. Chọn ghế & Khóa tạm 5p"),
        (58, 61, "UC05. Chọn combo bắp nước"),
        (58, 48, "UC06. Đặt vé & Thanh toán online"),
        (58, 35, "UC07. Quản lý vé & Mã QR cá nhân")
    ]

    # Staff UCs (3 UCs)
    ucs_staff = [
        (58, 22, "UC08. Bán vé tại quầy (POS)"),
        (75, 12, "UC09. Quét mã QR camera"),
        (95, 12, "UC10. Đối soát & Báo gian lận")
    ]

    # Manager UCs (4 UCs)
    ucs_manager = [
        (102, 100, "UC11. Quản lý danh mục phim"),
        (102, 87, "UC12. Quản lý phòng & Ghế bảo trì"),
        (102, 74, "UC13. Lập lịch suất chiếu (Chống trùng)"),
        (102, 61, "UC14. Báo cáo doanh thu & Lấp đầy")
    ]

    # Admin UC (1 UC)
    ucs_admin = [
        (102, 35, "UC15. Quản lý User, RBAC & Cài đặt")
    ]

    for (x, y, text) in ucs_client:
        draw_usecase(ax, x, y, text, w=27, h=6.2, fontsize=8.5)
        ax.plot([20, 35, 44.5], [92, y, y], color='black', linewidth=1.1)

    for (x, y, text) in ucs_staff:
        w_box = 24 if "camera" in text or "gian lận" in text else 27
        draw_usecase(ax, x, y, text, w=w_box, h=6.2, fontsize=8.2)

    # Staff connections
    ax.plot([20, 35, 44.5], [26, 22, 22], color='black', linewidth=1.1)
    ax.plot([20, 35, 63], [26, 12, 12], color='black', linewidth=1.1)
    ax.plot([20, 30, 30, 83], [26, 8, 8, 8], color='black', linewidth=1.1)
    ax.plot([83, 83], [8, 12], color='black', linewidth=1.1)

    for (x, y, text) in ucs_manager:
        draw_usecase(ax, x, y, text, w=27, h=6.2, fontsize=8.5)
        ax.plot([140, 125, 115.5], [92, y, y], color='black', linewidth=1.1)

    # Manager also checks UC10 fraud
    ax.plot([140, 125, 107], [92, 12, 12], color='black', linewidth=1.1)

    for (x, y, text) in ucs_admin:
        draw_usecase(ax, x, y, text, w=27, h=6.2, fontsize=8.5)
        ax.plot([140, 125, 115.5], [26, y, y], color='black', linewidth=1.1)

    # Actor to Login lines
    ax.plot([20, 35, 66], [92, 112, 112], color='black', linewidth=1.1)
    ax.plot([20, 28, 28, 66], [26, 26, 112, 112], color='black', linewidth=1.1)
    ax.plot([140, 125, 94], [92, 112, 112], color='black', linewidth=1.1)
    ax.plot([140, 132, 132, 94], [26, 26, 112, 112], color='black', linewidth=1.1)

    plt.tight_layout()
    fpath = os.path.join(img_dir, 'drawio_usecase_tong_quat.png')
    plt.savefig(fpath, dpi=300, bbox_inches='tight')
    plt.close()
    print("Generated:", fpath)

# -----------------------------------------------------------------------------
# 2. BIỂU ĐỒ PHÂN RÃ USE CASE ĐĂNG KÝ VÀ ĐĂNG NHẬP
# -----------------------------------------------------------------------------
def generate_uc_dang_nhap():
    fig, ax = plt.subplots(figsize=(15, 9), dpi=300)
    ax.set_xlim(0, 150)
    ax.set_ylim(0, 95)
    ax.axis('off')

    sys_box = patches.Rectangle((36, 6), 106, 84, facecolor='white', edgecolor='black', linewidth=1.6)
    ax.add_patch(sys_box)
    ax.text(89, 86, "PHÂN RÃ USE CASE: ĐĂNG KÝ VÀ ĐĂNG NHẬP (XÁC THỰC TÀI KHOẢN)", ha='center', va='center', fontsize=11.5, fontweight='bold')

    draw_actor(ax, 16, 64, "Khách hàng\n(Client)", scale=1.1)
    draw_actor(ax, 16, 26, "Nhân viên / Quản lý / Admin\n(Staff, Manager, Admin)", scale=1.1)

    ucs = [
        (66, 74, "Đăng ký tài khoản"),
        (66, 56, "Đăng nhập hệ thống"),
        (66, 36, "Đổi mật khẩu tài khoản"),
        (66, 18, "Đăng xuất hệ thống")
    ]

    subs = [
        (116, 74, "<<include>>\nKiểm tra email & Băm BCrypt"),
        (116, 56, "<<include>>\nXác thực thông tin & Cấp Session"),
        (116, 42, "<<extend>>\nBáo lỗi sai pass / Khóa nick"),
        (116, 26, "<<extend>>\nQuên mật khẩu & Khôi phục")
    ]

    for (x, y, text) in ucs:
        draw_usecase(ax, x, y, text, w=28, h=6.5)

    for (x, y, text) in subs:
        draw_usecase(ax, x, y, text, w=29, h=6.5, fontsize=8.5)

    # Actor lines
    # Client connects to Đăng ký, Đăng nhập, Đổi pass, Đăng xuất
    ax.plot([22, 35, 52], [64, 74, 74], color='black', linewidth=1.2)
    ax.plot([22, 35, 52], [64, 56, 56], color='black', linewidth=1.2)
    ax.plot([22, 35, 52], [64, 36, 36], color='black', linewidth=1.2)
    ax.plot([22, 35, 52], [64, 18, 18], color='black', linewidth=1.2)

    # Internal actors connect to Đăng nhập, Đổi pass, Đăng xuất
    ax.plot([22, 32, 52], [26, 56, 56], color='black', linewidth=1.2)
    ax.plot([22, 35, 52], [26, 36, 36], color='black', linewidth=1.2)
    ax.plot([22, 35, 52], [26, 18, 18], color='black', linewidth=1.2)

    # Relationships
    # Đăng ký -> include Kiểm tra email
    ax.plot([80, 101.5], [74, 74], color='black', linewidth=1.2, linestyle='--')
    ax.text(91, 76, "<<include>>", ha='center', va='bottom', fontsize=8.5)

    # Đăng nhập -> include Xác thực
    ax.plot([80, 101.5], [56, 56], color='black', linewidth=1.2, linestyle='--')
    ax.text(91, 58, "<<include>>", ha='center', va='bottom', fontsize=8.5)

    # Đăng nhập -> extend Báo lỗi
    ax.plot([80, 95, 101.5], [56, 42, 42], color='black', linewidth=1.2, linestyle='--')
    ax.text(91, 45, "<<extend>>", ha='center', va='bottom', fontsize=8.5)

    # Đăng nhập -> extend Quên pass
    ax.plot([80, 95, 101.5], [56, 26, 26], color='black', linewidth=1.2, linestyle='--')
    ax.text(91, 29, "<<extend>>", ha='center', va='bottom', fontsize=8.5)

    plt.tight_layout()
    fpath = os.path.join(img_dir, 'drawio_usecase_dang_nhap.png')
    plt.savefig(fpath, dpi=300, bbox_inches='tight')
    plt.close()
    print("Generated:", fpath)

# -----------------------------------------------------------------------------
# 3. BIỂU ĐỒ PHÂN RÃ USE CASE TRA CỨU PHIM VÀ XEM LỊCH CHIẾU
# -----------------------------------------------------------------------------
def generate_uc_tra_cuu_phim():
    fig, ax = plt.subplots(figsize=(15, 9), dpi=300)
    ax.set_xlim(0, 150)
    ax.set_ylim(0, 95)
    ax.axis('off')

    sys_box = patches.Rectangle((36, 6), 106, 84, facecolor='white', edgecolor='black', linewidth=1.6)
    ax.add_patch(sys_box)
    ax.text(89, 86, "PHÂN RÃ USE CASE: TRA CỨU PHIM VÀ XEM LỊCH CHIẾU", ha='center', va='center', fontsize=11.5, fontweight='bold')

    draw_actor(ax, 16, 60, "Khách vãng lai\n(Guest)", scale=1.1)
    draw_actor(ax, 16, 24, "Khách hàng\n(Client)", scale=1.1)

    ucs = [
        (66, 74, "Xem danh mục phim đang chiếu"),
        (66, 62, "Xem danh mục phim sắp chiếu"),
        (66, 50, "Tìm kiếm phim theo từ khóa"),
        (66, 38, "Lọc phim (thể loại, rạp, ngày)"),
        (66, 26, "Xem chi tiết phim & Trailer"),
        (66, 14, "Xem lịch chiếu theo cụm rạp")
    ]

    subs = [
        (116, 26, "<<extend>>\nXem phân loại độ tuổi (P/T18)"),
        (116, 14, "<<include>>\nTra cứu phòng chiếu & Giờ")
    ]

    for (x, y, text) in ucs:
        draw_usecase(ax, x, y, text, w=28, h=6.5)
        # Connect both Guest & Client
        ax.plot([22, 35, 52], [60, y, y], color='black', linewidth=1.1)
        ax.plot([22, 35, 52], [24, y, y], color='black', linewidth=1.1)

    for (x, y, text) in subs:
        draw_usecase(ax, x, y, text, w=29, h=6.5, fontsize=8.5)

    ax.plot([80, 101.5], [26, 26], color='black', linewidth=1.2, linestyle='--')
    ax.text(91, 28, "<<extend>>", ha='center', va='bottom', fontsize=8.5)

    ax.plot([80, 101.5], [14, 14], color='black', linewidth=1.2, linestyle='--')
    ax.text(91, 16, "<<include>>", ha='center', va='bottom', fontsize=8.5)

    plt.tight_layout()
    fpath = os.path.join(img_dir, 'drawio_usecase_tra_cuu_phim.png')
    plt.savefig(fpath, dpi=300, bbox_inches='tight')
    plt.close()
    print("Generated:", fpath)

# -----------------------------------------------------------------------------
# 4. BIỂU ĐỒ PHÂN RÃ USE CASE ĐẶT VÉ TRỰC TUYẾN VÀ CHỌN GHẾ
# -----------------------------------------------------------------------------
def generate_uc_dat_ve():
    fig, ax = plt.subplots(figsize=(15, 9), dpi=300)
    ax.set_xlim(0, 150)
    ax.set_ylim(0, 95)
    ax.axis('off')

    sys_box = patches.Rectangle((36, 6), 106, 84, facecolor='white', edgecolor='black', linewidth=1.6)
    ax.add_patch(sys_box)
    ax.text(89, 86, "PHÂN RÃ USE CASE: ĐẶT VÉ TRỰC TUYẾN VÀ CHỌN GHẾ", ha='center', va='center', fontsize=11.5, fontweight='bold')

    draw_actor(ax, 16, 48, "Khách hàng\n(Client)", scale=1.2)

    ucs = [
        (66, 74, "Chọn suất chiếu phim"),
        (66, 58, "Chọn vị trí ghế ngồi sơ đồ"),
        (66, 42, "Chọn combo bắp nước F&B"),
        (66, 26, "Thanh toán trực tuyến"),
        (66, 12, "Quản lý vé cá nhân ('Vé của tôi')")
    ]

    subs = [
        (116, 64, "<<include>>\nKhóa giữ ghế tạm 5 phút"),
        (116, 50, "<<extend>>\nTự động nhả ghế khi quá 5p"),
        (116, 26, "<<include>>\nSinh vé điện tử & Mã QR Code")
    ]

    for (x, y, text) in ucs:
        draw_usecase(ax, x, y, text, w=28, h=6.5)
        ax.plot([22, 35, 52], [48, y, y], color='black', linewidth=1.2)

    for (x, y, text) in subs:
        draw_usecase(ax, x, y, text, w=29, h=6.5, fontsize=8.5)

    ax.plot([80, 96, 101.5], [58, 64, 64], color='black', linewidth=1.2, linestyle='--')
    ax.text(91, 65, "<<include>>", ha='center', va='bottom', fontsize=8.5)

    ax.plot([80, 96, 101.5], [58, 50, 50], color='black', linewidth=1.2, linestyle='--')
    ax.text(91, 51, "<<extend>>", ha='center', va='bottom', fontsize=8.5)

    ax.plot([80, 101.5], [26, 26], color='black', linewidth=1.2, linestyle='--')
    ax.text(91, 28, "<<include>>", ha='center', va='bottom', fontsize=8.5)

    plt.tight_layout()
    fpath = os.path.join(img_dir, 'drawio_usecase_dat_ve.png')
    plt.savefig(fpath, dpi=300, bbox_inches='tight')
    plt.close()
    print("Generated:", fpath)

# -----------------------------------------------------------------------------
# 5. BIỂU ĐỒ PHÂN RÃ USE CASE BÁN VÉ TẠI QUẦY VÀ SOÁT VÉ QR
# -----------------------------------------------------------------------------
def generate_uc_ban_ve_soat_ve():
    fig, ax = plt.subplots(figsize=(15, 9), dpi=300)
    ax.set_xlim(0, 150)
    ax.set_ylim(0, 95)
    ax.axis('off')

    sys_box = patches.Rectangle((36, 6), 106, 84, facecolor='white', edgecolor='black', linewidth=1.6)
    ax.add_patch(sys_box)
    ax.text(89, 86, "PHÂN RÃ USE CASE: BÁN VÉ TẠI QUẦY (POS) VÀ SOÁT VÉ QR", ha='center', va='center', fontsize=11.5, fontweight='bold')

    draw_actor(ax, 16, 48, "Nhân viên quầy\n(Staff)", scale=1.2)

    ucs = [
        (66, 72, "Bán vé trực tiếp tại quầy (POS)"),
        (66, 54, "Quét mã QR soát vé qua camera"),
        (66, 32, "Tra cứu danh sách vé đã bán"),
        (66, 14, "Xem lịch sử đối soát vé theo ca")
    ]

    subs = [
        (116, 72, "<<include>>\nIn vé xem phim & Hóa đơn quầy"),
        (116, 58, "<<include>>\nXác thực CSDL & Đổi 'checked_in'"),
        (116, 44, "<<extend>>\nCảnh báo còi đỏ vé đã sử dụng")
    ]

    for (x, y, text) in ucs:
        draw_usecase(ax, x, y, text, w=28, h=6.5)
        ax.plot([22, 35, 52], [48, y, y], color='black', linewidth=1.2)

    for (x, y, text) in subs:
        draw_usecase(ax, x, y, text, w=29, h=6.5, fontsize=8.5)

    ax.plot([80, 101.5], [72, 72], color='black', linewidth=1.2, linestyle='--')
    ax.text(91, 74, "<<include>>", ha='center', va='bottom', fontsize=8.5)

    ax.plot([80, 96, 101.5], [54, 58, 58], color='black', linewidth=1.2, linestyle='--')
    ax.text(91, 59, "<<include>>", ha='center', va='bottom', fontsize=8.5)

    ax.plot([80, 96, 101.5], [54, 44, 44], color='black', linewidth=1.2, linestyle='--')
    ax.text(91, 46, "<<extend>>", ha='center', va='bottom', fontsize=8.5)

    plt.tight_layout()
    fpath = os.path.join(img_dir, 'drawio_usecase_ban_ve_soat_ve.png')
    plt.savefig(fpath, dpi=300, bbox_inches='tight')
    plt.close()
    print("Generated:", fpath)

# -----------------------------------------------------------------------------
# 6. BIỂU ĐỒ PHÂN RÃ USE CASE QUẢN LÝ RẠP VÀ LẬP LỊCH SUẤT CHIẾU
# -----------------------------------------------------------------------------
def generate_uc_quan_ly_rap():
    fig, ax = plt.subplots(figsize=(15, 9), dpi=300)
    ax.set_xlim(0, 150)
    ax.set_ylim(0, 95)
    ax.axis('off')

    sys_box = patches.Rectangle((36, 6), 106, 84, facecolor='white', edgecolor='black', linewidth=1.6)
    ax.add_patch(sys_box)
    ax.text(89, 86, "PHÂN RÃ USE CASE: QUẢN LÝ RẠP VÀ LẬP LỊCH SUẤT CHIẾU", ha='center', va='center', fontsize=11.5, fontweight='bold')

    draw_actor(ax, 16, 48, "Quản lý rạp\n(Manager)", scale=1.2)

    ucs = [
        (66, 72, "Quản lý danh mục phim"),
        (66, 52, "Quản lý phòng chiếu & Ghế"),
        (66, 32, "Lập lịch suất chiếu mới"),
        (66, 14, "Quản lý bảng giá vé & Combo")
    ]

    subs = [
        (116, 72, "<<include>>\nTải lên poster & Trailer YouTube"),
        (116, 52, "<<include>>\nBật / Tắt bảo trì ghế hỏng"),
        (116, 32, "<<include>>\nKiểm tra xung đột (ConflictDetector)")
    ]

    for (x, y, text) in ucs:
        draw_usecase(ax, x, y, text, w=28, h=6.5)
        ax.plot([22, 35, 52], [48, y, y], color='black', linewidth=1.2)

    for (x, y, text) in subs:
        draw_usecase(ax, x, y, text, w=29, h=6.5, fontsize=8.5)

    ax.plot([80, 101.5], [72, 72], color='black', linewidth=1.2, linestyle='--')
    ax.text(91, 74, "<<include>>", ha='center', va='bottom', fontsize=8.5)

    ax.plot([80, 101.5], [52, 52], color='black', linewidth=1.2, linestyle='--')
    ax.text(91, 54, "<<include>>", ha='center', va='bottom', fontsize=8.5)

    ax.plot([80, 101.5], [32, 32], color='black', linewidth=1.2, linestyle='--')
    ax.text(91, 34, "<<include>>", ha='center', va='bottom', fontsize=8.5)

    plt.tight_layout()
    fpath = os.path.join(img_dir, 'drawio_usecase_quan_ly_rap.png')
    plt.savefig(fpath, dpi=300, bbox_inches='tight')
    plt.close()
    print("Generated:", fpath)

# -----------------------------------------------------------------------------
# 7. BIỂU ĐỒ PHÂN RÃ USE CASE THỐNG KÊ BÁO CÁO VÀ QUẢN TRỊ HỆ THỐNG
# -----------------------------------------------------------------------------
def generate_uc_thong_ke_quan_tri():
    fig, ax = plt.subplots(figsize=(15, 9), dpi=300)
    ax.set_xlim(0, 150)
    ax.set_ylim(0, 95)
    ax.axis('off')

    sys_box = patches.Rectangle((36, 6), 106, 84, facecolor='white', edgecolor='black', linewidth=1.6)
    ax.add_patch(sys_box)
    ax.text(89, 86, "PHÂN RÃ USE CASE: THỐNG KÊ BÁO CÁO VÀ QUẢN TRỊ HỆ THỐNG", ha='center', va='center', fontsize=11.5, fontweight='bold')

    draw_actor(ax, 16, 64, "Quản lý rạp\n(Manager)", scale=1.1)
    draw_actor(ax, 16, 24, "Quản trị viên\n(Admin)", scale=1.1)

    ucs = [
        (66, 74, "Theo dõi Dashboard doanh thu 7 ngày"),
        (66, 60, "Thống kê Tỷ lệ lấp đầy rạp (%)"),
        (66, 46, "Quản lý người dùng hệ thống"),
        (66, 32, "Phân quyền vai trò RBAC"),
        (66, 18, "Cài đặt tham số hệ thống rạp"),
        (66, 8, "Giám sát nhật ký (Audit Logs)")
    ]

    subs = [
        (116, 74, "<<include>>\nBiểu đồ cột Chart.js"),
        (116, 46, "<<include>>\nKhóa / Mở khóa tài khoản"),
        (116, 18, "<<include>>\nCấu hình thời gian đệm & Khóa ghế")
    ]

    for (x, y, text) in ucs:
        draw_usecase(ax, x, y, text, w=28, h=6.2)

    for (x, y, text) in subs:
        draw_usecase(ax, x, y, text, w=29, h=6.2, fontsize=8.5)

    # Manager connects to Dashboard & Tỷ lệ lấp đầy
    ax.plot([22, 35, 52], [64, 74, 74], color='black', linewidth=1.2)
    ax.plot([22, 35, 52], [64, 60, 60], color='black', linewidth=1.2)

    # Admin connects to all
    for y in [74, 60, 46, 32, 18, 8]:
        ax.plot([22, 35, 52], [24, y, y], color='black', linewidth=1.1)

    ax.plot([80, 101.5], [74, 74], color='black', linewidth=1.2, linestyle='--')
    ax.text(91, 76, "<<include>>", ha='center', va='bottom', fontsize=8.5)

    ax.plot([80, 101.5], [46, 46], color='black', linewidth=1.2, linestyle='--')
    ax.text(91, 48, "<<include>>", ha='center', va='bottom', fontsize=8.5)

    ax.plot([80, 101.5], [18, 18], color='black', linewidth=1.2, linestyle='--')
    ax.text(91, 20, "<<include>>", ha='center', va='bottom', fontsize=8.5)

    plt.tight_layout()
    fpath = os.path.join(img_dir, 'drawio_usecase_thong_ke_quan_tri.png')
    plt.savefig(fpath, dpi=300, bbox_inches='tight')
    plt.close()
    print("Generated:", fpath)

if __name__ == "__main__":
    generate_uc_tong_quat()
    generate_uc_dang_nhap()
    generate_uc_tra_cuu_phim()
    generate_uc_dat_ve()
    generate_uc_ban_ve_soat_ve()
    generate_uc_quan_ly_rap()
    generate_uc_thong_ke_quan_tri()
    print("All Use Case diagrams generated successfully.")
