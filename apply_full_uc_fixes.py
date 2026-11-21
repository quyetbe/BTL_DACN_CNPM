import os
import shutil
import zipfile
import docx
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

def apply_fixes():
    print("=================================================================")
    print("🚀 BẮT ĐẦU CẬP NHẬT BIỂU ĐỒ UC PHÂN RÃ VÀ ĐẶC TẢ TRONG BTL_DACN_CNPM_3.DOCX")
    print("=================================================================")

    # 1. SAO CHÉP CÁC BIỂU ĐỒ MỚI VÀO REPORT_ASSETS/IMAGES
    img_map = {
        'image48.png': 'report_assets/uc_diagrams_new/uc_tong_quat.png',
        'image49.png': 'report_assets/uc_diagrams_new/uc01_dang_nhap.png',
        'image50.png': 'report_assets/uc_diagrams_new/uc02_dang_ky.png',
        'image51.png': 'report_assets/uc_diagrams_new/uc03_quan_ly_tai_khoan.png',
        'image52.png': 'report_assets/uc_diagrams_new/uc04_tra_cuu_phim.png',
        'image53.png': 'report_assets/uc_diagrams_new/uc05_dat_ve_chon_ghe.png',
        'image54.png': 'report_assets/uc_diagrams_new/uc06_gio_ve_combo.png',
        'image55.png': 'report_assets/uc_diagrams_new/uc07_ban_ve_pos.png',
        'image56.png': 'report_assets/uc_diagrams_new/uc08_soat_ve_qr.png',
        'image57.png': 'report_assets/uc_diagrams_new/uc09_quan_ly_phim.png',
        'image58.png': 'report_assets/uc_diagrams_new/uc10_quan_ly_phong_chieu.png',
        'image59.png': 'report_assets/uc_diagrams_new/uc11_lap_suat_chieu.png',
        'image60.png': 'report_assets/uc_diagrams_new/uc12_gia_ve_combo.png',
        'image61.png': 'report_assets/uc_diagrams_new/uc13_bao_cao_doanh_thu.png',
        'image62.png': 'report_assets/uc_diagrams_new/uc14_quan_ly_nguoi_dung.png',
        'image63.png': 'report_assets/uc_diagrams_new/uc15_cau_hinh_audit.png',
    }

    # Backup docx
    backup_path = 'BTL_DACN_CNPM_3_backup.docx'
    if not os.path.exists(backup_path):
        shutil.copy2('BTL_DACN_CNPM_3.docx', backup_path)
        print("Đã sao lưu file gốc tại:", backup_path)

    # 2. THAY THẾ TRỰC TIẾP HÌNH ẢNH TRONG FILE ZIP DOCX
    temp_zip = 'temp_update_doc.docx'
    with zipfile.ZipFile('BTL_DACN_CNPM_3.docx', 'r') as zin:
        with zipfile.ZipFile(temp_zip, 'w', compression=zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                fname = item.filename
                # Check if fname is one of the replaced images
                matched = False
                for target_img, src_path in img_map.items():
                    if fname == f'word/media/{target_img}':
                        with open(src_path, 'rb') as f_new:
                            zout.writestr(item, f_new.read())
                        matched = True
                        # print(f"  -> Đã thay thế ảnh {fname} bằng {src_path}")
                        break
                if not matched:
                    zout.writestr(item, zin.read(fname))

    # Ghi đè file docx với hình ảnh mới
    shutil.move(temp_zip, 'BTL_DACN_CNPM_3.docx')
    print("✅ Đã thay thế thành công toàn bộ 16 hình ảnh Use Case chất lượng cao trong file DOCX!")

    # 3. MỞ VÀ CẬP NHẬT NỘI DUNG VĂN BẢN VÀ BẢNG ĐẶC TẢ QUA PYTHON-DOCX
    doc = docx.Document('BTL_DACN_CNPM_3.docx')

    # Danh sách các caption cần sửa lại số hiệu
    caption_fixes = {
        "Hình 4.21. Biểu đồ Use Case phân rã: Soát vé qua mã QR & Cảnh báo gian lận":
            "Hình 4.10. Biểu đồ Use Case phân rã: Soát vé qua mã QR & Cảnh báo gian lận",
        "Hình 4.22. Biểu đồ Use Case phân rã: Quản lý danh mục phim chiếu rạp":
            "Hình 4.11. Biểu đồ Use Case phân rã: Quản lý danh mục phim chiếu rạp",
        "Hình 4.23. Biểu đồ Use Case phân rã: Quản lý phòng chiếu & Cấu hình sơ đồ ghế":
            "Hình 4.12. Biểu đồ Use Case phân rã: Quản lý phòng chiếu & Cấu hình sơ đồ ghế",
        "Hình 4.24. Biểu đồ Use Case phân rã: Lập lịch suất chiếu & Chống xung đột":
            "Hình 4.13. Biểu đồ Use Case phân rã: Lập lịch suất chiếu & Chống xung đột",
        "Hình 4.25. Biểu đồ Use Case phân rã: Quản lý bảng giá vé và combo F&B":
            "Hình 4.14. Biểu đồ Use Case phân rã: Quản lý bảng giá vé và combo F&B",
        "Hình 4.26. Biểu đồ Use Case phân rã: Báo cáo & Thống kê doanh thu rạp":
            "Hình 4.15. Biểu đồ Use Case phân rã: Báo cáo & Thống kê doanh thu rạp",
        "Hình 4.27. Biểu đồ Use Case phân rã: Quản lý người dùng & Phân quyền vai trò (RBAC)":
            "Hình 4.16. Biểu đồ Use Case phân rã: Quản lý người dùng & Phân quyền vai trò (RBAC)",
        "Hình 4.28. Biểu đồ Use Case phân rã: Cấu hình tham số rạp & Giám sát Audit Log":
            "Hình 4.17. Biểu đồ Use Case phân rã: Cấu hình tham số rạp & Giám sát Audit Log",
        "Hình 4.29. Biểu đồ hoạt động: Quy trình Đặt vé và chọn ghế của Khách hàng":
            "Hình 4.18. Biểu đồ hoạt động: Quy trình Đặt vé và chọn ghế của Khách hàng",
        "Hình 4.30. Biểu đồ hoạt động: Quy trình Lập lịch suất chiếu của Manager":
            "Hình 4.19. Biểu đồ hoạt động: Quy trình Lập lịch suất chiếu của Manager",
        "Hình 4.31. Biểu đồ hoạt động: Quy trình Soát vé QR & Cảnh báo gian lận của Staff":
            "Hình 4.20. Biểu đồ hoạt động: Quy trình Soát vé QR & Cảnh báo gian lận của Staff",
    }

    # Cập nhật các đoạn văn giới thiệu ca sử dụng nếu cần
    intro_fixes = {
        "Ca sử dụng UC02: Đăng ký tài khoản: Tạo tài khoản thành viên mới trong hệ thống để đặt vé, tích lũy điểm và nhận ưu đãi.":
            "Ca sử dụng UC02: Đăng ký tài khoản: Cho phép khách hàng đăng ký tài khoản thành viên mới trong hệ thống với các thông tin hợp lệ (Họ tên, Email, Số điện thoại, Mật khẩu băm an toàn qua BCrypt) để thực hiện đặt vé trực tuyến.",
        "Ca sử dụng UC03: Quản lý thông tin tài khoản: Xem và chỉnh sửa thông tin cá nhân (Họ tên, Số điện thoại) và thực hiện đổi mật khẩu tài khoản.":
            "Ca sử dụng UC03: Quản lý thông tin tài khoản: Xem thông tin cá nhân, cập nhật họ tên, số điện thoại và thực hiện đổi mật khẩu tài khoản với cơ chế đối soát mật khẩu cũ an toàn.",
        "Ca sử dụng UC05: Đặt vé & Chọn ghế ngồi (kèm khóa giữ 5p): Lựa chọn vị trí ghế trên sơ đồ trực quan, khóa giữ chỗ 5 phút và thanh toán trực tuyến an toàn.":
            "Ca sử dụng UC05: Đặt vé & Chọn ghế ngồi (kèm khóa giữ 5p): Lựa chọn vị trí ghế ngồi trên sơ đồ ma trận trực quan (Ghế thường, VIP, Sweetbox) và kích hoạt cơ chế khóa giữ ghế tạm thời trong 5 phút qua SeatLock.",
        "Ca sử dụng UC06: Quản lý giỏ vé & Chọn combo bắp nước: Thêm các gói combo bắp rang, nước ngọt vào đơn vé và quản lý lịch sử các vé đã mua kèm mã QR.":
            "Ca sử dụng UC06: Quản lý giỏ vé & Chọn combo bắp nước: Lựa chọn các gói combo bắp nước F&B, kiểm tra tóm tắt đơn vé, thực hiện thanh toán trực tuyến và sinh vé điện tử kèm mã QR Code an toàn.",
    }

    # Duyệt paragraphs trong văn bản để sửa
    for p in doc.paragraphs:
        txt = p.text.strip()
        for old_cap, new_cap in caption_fixes.items():
            if txt == old_cap:
                p.text = new_cap
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p.runs[0].font.name = 'Times New Roman'
                p.runs[0].font.size = Pt(11)
                p.runs[0].font.italic = True
                p.runs[0].font.bold = True
                print(f"  -> Đã sửa caption: {old_cap} => {new_cap}")
                break
        for old_intro, new_intro in intro_fixes.items():
            if txt == old_intro:
                p.text = new_intro
                p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                p.runs[0].font.name = 'Times New Roman'
                p.runs[0].font.size = Pt(13)
                print(f"  -> Đã cập nhật mô tả dẫn dắt: {old_intro[:40]}...")
                break

    # 4. CẬP NHẬT 15 BẢNG ĐẶC TẢ CHI TIẾT (TABLES 8 - 22)
    # Helper set text for table row
    def set_row_content(table, row_idx, value_text):
        cell = table.rows[row_idx].cells[1]
        cell.text = ""
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.space_before = Pt(0)
        run = p.add_run(value_text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(11.5)

    specs = {
        8: { # UC01
            "Tên Use Case": "UC01: Đăng nhập hệ thống",
            "Tác nhân chính": "Khách hàng (Client), Nhân viên quầy (Staff), Quản lý rạp (Manager), Quản trị viên (Admin)",
            "Mục đích": "Xác thực danh tính người dùng qua Email và Mật khẩu, cấp phiên làm việc (Session) an toàn và phân quyền điều hướng đúng phân hệ quản lý.",
            "Tiền điều kiện": "Người dùng truy cập trang /login và tài khoản đã tồn tại trong CSDL bảng users.",
            "Hậu điều kiện": "Người dùng được cấp phiên làm việc (req.session.user) lưu thông tin định danh và điều hướng về đúng trang chức năng.",
            "Luồng sự kiện chính (Basic Flow)":
                "1. Người dùng bấm nút 'Đăng nhập' trên thanh điều hướng hoặc truy cập đường dẫn /login.\n"
                "2. Hệ thống hiển thị biểu mẫu đăng nhập yêu cầu nhập Email và Mật khẩu.\n"
                "3. Người dùng nhập thông tin email, mật khẩu và bấm nút 'Đăng nhập'.\n"
                "4. Hệ thống gọi User.findByEmail(email) tra cứu tài khoản trong bảng users.\n"
                "5. Hệ thống kiểm tra cột status: tài khoản phải ở trạng thái 'active'.\n"
                "6. Hệ thống đối soát mật khẩu băm bằng hàm bcrypt.compareSync(password, user.password_hash).\n"
                "7. Xác thực thành công: Hệ thống khởi tạo session lưu user_id, role_id, role_name, full_name, email, phone.\n"
                "8. Hệ thống điều hướng an toàn (chống Open Redirect Attack):\n"
                "   • Admin -> /admin/users\n"
                "   • Manager -> /manager/dashboard\n"
                "   • Staff -> /staff/pos\n"
                "   • Client -> / (hoặc URL trang đặt vé trước đó nếu có tham số returnTo).",
            "Luồng sự kiện phụ (Alternative Flow)":
                "4a. Nếu email không tồn tại trong hệ thống: Báo lỗi 'Email hoặc mật khẩu không chính xác!'.\n"
                "6a. Nếu mật khẩu không khớp: Báo lỗi 'Email hoặc mật khẩu không chính xác!'.",
            "Luồng ngoại lệ (Exception Flow)":
                "5a. Nếu tài khoản có status = 'locked': Hệ thống từ chối đăng nhập và hiển thị cảnh báo đỏ: 'Tài khoản của bạn đã bị khóa! Vui lòng liên hệ quản trị viên.'",
            "Quy tắc nghiệp vụ (Business Rules)":
                "Mật khẩu người dùng được băm bảo mật bằng BCrypt (salt rounds = 10); phiên đăng nhập quản lý qua Express-Session lưu trên máy chủ; điều hướng an toàn qua hàm isSafeRedirect()."
        },
        9: { # UC02
            "Tên Use Case": "UC02: Đăng ký tài khoản",
            "Tác nhân chính": "Khách hàng vãng lai (Chưa có tài khoản)",
            "Mục đích": "Cho phép khách hàng tạo tài khoản thành viên mới trong hệ thống để thực hiện đặt vé xem phim trực tuyến.",
            "Tiền điều kiện": "Khách hàng truy cập website và chưa đăng nhập tài khoản.",
            "Hậu điều kiện": "Tài khoản mới được lưu vào bảng users với role_id = 4 (client), status = 'active'; hệ thống tự động cấp session đăng nhập thành viên.",
            "Luồng sự kiện chính (Basic Flow)":
                "1. Người dùng nhấn nút 'Đăng ký' trên thanh menu hoặc từ trang đăng nhập (/register).\n"
                "2. Hệ thống hiển thị biểu mẫu đăng ký gồm: Họ và tên, Email, Số điện thoại, Mật khẩu và Xác nhận mật khẩu.\n"
                "3. Khách hàng điền thông tin và bấm nút 'Tạo tài khoản'.\n"
                "4. Hệ thống kiểm tra tính hợp lệ của dữ liệu đầu vào:\n"
                "   • Các trường bắt buộc không được để trống.\n"
                "   • Email đúng định dạng regex chuẩn.\n"
                "   • Số điện thoại là chuỗi chữ số từ 8-20 ký tự.\n"
                "   • Mật khẩu có độ dài tối thiểu 6 ký tự.\n"
                "   • Mật khẩu xác nhận phải trùng khớp tuyệt đối.\n"
                "5. Hệ thống gọi User.findByEmail() kiểm tra trùng lặp email trong CSDL.\n"
                "6. Dữ liệu hợp lệ: Hệ thống băm mật khẩu qua bcrypt.hashSync(password, 10).\n"
                "7. Hệ thống thêm bản ghi vào bảng users với role_id = 4 (Client), status = 'active'.\n"
                "8. Hệ thống tự động cấp session đăng nhập và chuyển hướng về trang chủ (/?welcome=1) hoặc tiếp tục quy trình đặt vé dang dở.",
            "Luồng sự kiện phụ (Alternative Flow)":
                "5a. Nếu email đã được đăng ký: Hệ thống báo lỗi 'Email này đã được sử dụng trên hệ thống, vui lòng chọn email khác!'.",
            "Luồng ngoại lệ (Exception Flow)":
                "4a. Nếu mật khẩu xác nhận không khớp: Báo lỗi 'Mật khẩu xác nhận không khớp!'.\n"
                "4b. Nếu mật khẩu dưới 6 ký tự: Báo lỗi 'Mật khẩu phải chứa ít nhất 6 ký tự!'.",
            "Quy tắc nghiệp vụ (Business Rules)":
                "Email là định danh duy nhất (UNIQUE) trên toàn hệ thống; mọi tài khoản đăng ký công khai đều tự động gán quyền Khách hàng (role_id = 4)."
        },
        10: { # UC03
            "Tên Use Case": "UC03: Quản lý thông tin tài khoản",
            "Tác nhân chính": "Khách hàng, Nhân viên, Quản lý, Admin (Người dùng đã đăng nhập)",
            "Mục đích": "Cho phép người dùng xem thông tin cá nhân, cập nhật họ tên, số điện thoại và thực hiện đổi mật khẩu tài khoản.",
            "Tiền điều kiện": "Người dùng đã đăng nhập thành công vào hệ thống (req.session.user tồn tại).",
            "Hậu điều kiện": "Thông tin cá nhân hoặc mật khẩu mới được cập nhật vào bảng users và đồng bộ trong session hiện hành.",
            "Luồng sự kiện chính (Basic Flow)":
                "1. Người dùng bấm vào menu tài khoản và chọn 'Hồ sơ cá nhân' (/profile).\n"
                "2. Hệ thống truy vấn CSDL bảng users và hiển thị: Họ tên, Email, Số điện thoại, Vai trò tài khoản.\n"
                "3. Để cập nhật hồ sơ: Người dùng chỉnh sửa Họ tên, Số điện thoại và nhấn 'Lưu thay đổi'.\n"
                "4. Hệ thống thực thi câu lệnh UPDATE users SET full_name=?, phone=? WHERE id=?.\n"
                "5. Hệ thống cập nhật lại các trường tương ứng trong req.session.user và thông báo thành công.\n"
                "6. Để đổi mật khẩu: Người dùng chuyển sang form đổi mật khẩu, nhập Mật khẩu hiện tại, Mật khẩu mới và Xác nhận mật khẩu mới.\n"
                "7. Hệ thống kiểm tra mật khẩu hiện tại bằng bcrypt.compareSync() với password_hash trong CSDL.\n"
                "8. Mật khẩu cũ chính xác và mật khẩu mới hợp lệ (>= 6 ký tự): Hệ thống băm mật khẩu mới và cập nhật vào CSDL, hiển thị thông báo đổi mật khẩu thành công.",
            "Luồng sự kiện phụ (Alternative Flow)":
                "7a. Nếu nhập sai mật khẩu cũ: Hệ thống báo lỗi 'Mật khẩu hiện tại không chính xác!'.\n"
                "6a. Nếu mật khẩu xác nhận không khớp: Báo lỗi 'Mật khẩu xác nhận không khớp!'.",
            "Luồng ngoại lệ (Exception Flow)":
                "6b. Nếu mật khẩu mới dưới 6 ký tự: Báo lỗi 'Mật khẩu mới phải có tối thiểu 6 ký tự!'.",
            "Quy tắc nghiệp vụ (Business Rules)":
                "Địa chỉ Email là định danh đăng nhập nên cố định và không được phép tự ý thay đổi trong hồ sơ cá nhân; mật khẩu mới bắt buộc phải băm BCrypt trước khi ghi vào CSDL."
        },
        11: { # UC04
            "Tên Use Case": "UC04: Tra cứu phim và lịch chiếu rạp",
            "Tác nhân chính": "Khách hàng (Client), Khách vãng lai (Guest)",
            "Mục đích": "Xem danh mục phim đang chiếu, phim sắp chiếu, tìm kiếm phim theo từ khóa, xem trailer YouTube và xem lịch chiếu theo cụm rạp CineStar.",
            "Tiền điều kiện": "Người dùng đã truy cập vào hệ thống website.",
            "Hậu điều kiện": "Danh sách phim và khung giờ các suất chiếu tương ứng được kết xuất trực quan.",
            "Luồng sự kiện chính (Basic Flow)":
                "1. Người dùng truy cập trang chủ (/) hoặc mục 'Phim' (/movies).\n"
                "2. Hệ thống tải danh mục phim từ bảng movies, phân loại rõ ràng thành 2 tab: 'Phim đang chiếu' (status='now_showing') và 'Phim sắp chiếu' (status='coming_soon').\n"
                "3. Người dùng có thể tìm kiếm phim theo từ khóa tiêu đề hoặc lọc theo thể loại phim.\n"
                "4. Người dùng bấm vào một bộ phim để xem chi tiết (/movies/:id).\n"
                "5. Hệ thống hiển thị: Poster, Tiêu đề, Thời lượng, Ngày phát hành, Phân loại độ tuổi (P/K/T13/T16/T18), Đạo diễn, Diễn viên, Tóm tắt nội dung và Trailer YouTube nhúng.\n"
                "6. Hệ thống truy vấn bảng showtimes và rooms để hiển thị danh sách các suất chiếu khả dụng theo ngày và theo từng cụm rạp CineStar.\n"
                "7. Người dùng bấm chọn khung giờ chiếu mong muốn để chuyển sang bước chọn ghế đặt vé.",
            "Luồng sự kiện phụ (Alternative Flow)":
                "3a. Nếu không tìm thấy phim phù hợp với từ khóa: Hệ thống hiển thị thông báo 'Không tìm thấy bộ phim phù hợp!'.",
            "Luồng ngoại lệ (Exception Flow)":
                "4a. Nếu ID phim không tồn tại hoặc phim đã ngừng chiếu: Hệ thống điều hướng về trang 404.",
            "Quy tắc nghiệp vụ (Business Rules)":
                "Chỉ các bộ phim có trạng thái 'now_showing' và có suất chiếu hợp lệ mới cho phép khách hàng đặt vé; phim 'coming_soon' chỉ xem thông tin và trailer giới thiệu."
        },
        12: { # UC05
            "Tên Use Case": "UC05: Đặt vé trực tuyến & Chọn ghế ngồi (kèm khóa giữ 5p)",
            "Tác nhân chính": "Khách hàng có tài khoản thành viên (Client)",
            "Mục đích": "Lựa chọn vị trí ghế trên sơ đồ ma trận trực quan của phòng chiếu và khóa giữ chỗ tạm thời trong 5 phút qua SeatLock.",
            "Tiền điều kiện": "Khách hàng đã chọn một suất chiếu cụ thể và đăng nhập tài khoản thành viên.",
            "Hậu điều kiện": "Vị trí ghế được ghi nhận tạm khóa trong bảng seat_locks với thời gian hết hạn expires_at = NOW() + 5 phút.",
            "Luồng sự kiện chính (Basic Flow)":
                "1. Khách hàng bấm chọn suất chiếu mong muốn (/booking/seats/:showtimeId).\n"
                "2. Hệ thống kiểm tra session qua requireLogin (nếu chưa đăng nhập sẽ chuyển hướng sang /login kèm returnTo).\n"
                "3. Hệ thống tải sơ đồ ghế phòng chiếu từ bảng seats và trạng thái ghế thời gian thực:\n"
                "   • Ghế đã bán (tickets) -> hiển thị màu xám, bị khóa không thể bấm.\n"
                "   • Ghế đang bảo trì (seats.status='maintenance') -> hiển thị biểu tượng cấm.\n"
                "   • Ghế đang bị giữ bởi người khác (seat_locks) -> hiển thị màu vàng, bị khóa.\n"
                "   • Ghế còn trống -> hiển thị theo loại: Thường (xanh), VIP (cam), Sweetbox (hồng).\n"
                "4. Khách hàng click chọn các vị trí ghế ngồi mong muốn (ví dụ: D07, D08). Hệ thống tính tiền vé tự động: Giá = base_price * price_multiplier.\n"
                "5. Khách hàng bấm nút 'TIẾP TỤC BƯỚC TIẾP THEO >>'.\n"
                "6. Hệ thống gửi yêu cầu khóa ghế tới API /booking/api/lock-seats.\n"
                "7. Controller kiểm tra xung đột: nếu ghế hợp lệ, hệ thống tạo bản ghi trong bảng seat_locks lưu session_id, showtime_id, seat_id và expires_at = NOW() + 5 phút.\n"
                "8. Hệ thống kích hoạt đồng hồ đếm ngược 5:00 phút trên giao diện và chuyển hướng sang bước chọn combo bắp nước (/booking/combos/:showtimeId).",
            "Luồng sự kiện phụ (Alternative Flow)":
                "6a. Nếu có ít nhất một ghế vừa bị người khác giữ trước: Hệ thống từ chối khóa, thông báo 'Ghế vừa có người chọn, vui lòng chọn vị trí khác!'.",
            "Luồng ngoại lệ (Exception Flow)":
                "8a. Nếu đồng hồ đếm ngược hết 5 phút mà khách chưa hoàn tất thanh toán: Hệ thống tự động xóa bản ghi trong seat_locks và nhả ghế cho người khác.",
            "Quy tắc nghiệp vụ (Business Rules)":
                "Thời gian giữ ghế tạm thời tối đa là 5 phút (300 giây) để ngăn chặn đầu cơ giữ ghế ảo; mỗi khách hàng được đặt tối đa 8 ghế trong một đơn."
        },
        13: { # UC06
            "Tên Use Case": "UC06: Quản lý giỏ vé & Chọn combo bắp nước",
            "Tác nhân chính": "Khách hàng có tài khoản thành viên (Client)",
            "Mục đích": "Thêm các gói combo bắp nước F&B vào đơn vé, kiểm tra tóm tắt đơn hàng, thanh toán trực tuyến và nhận vé điện tử kèm mã QR Code.",
            "Tiền điều kiện": "Khách hàng đang giữ ghế hợp lệ trong thời gian 5 phút của suất chiếu.",
            "Hậu điều kiện": "Đơn hàng được lưu vào bảng bookings (payment_status='paid'), chi tiết vé được tạo trong tickets kèm chuỗi qr_data, combo lưu trong booking_combos.",
            "Luồng sự kiện chính (Basic Flow)":
                "1. Tại bước chọn combo (/booking/combos/:showtimeId), hệ thống hiển thị danh mục combo F&B từ bảng combos: Tên, Mô tả thành phần, Đơn giá và Ảnh.\n"
                "2. Khách hàng tăng/giảm số lượng combo theo nhu cầu (hoặc bỏ qua) và nhấn 'TIẾP TỤC THANH TOÁN >>'.\n"
                "3. Hệ thống lưu danh sách combo vào session và chuyển sang trang thanh toán (/booking/checkout/:showtimeId).\n"
                "4. Hệ thống hiển thị tóm tắt toàn bộ đơn hàng: Tên phim, Cụm rạp, Phòng chiếu, Suất chiếu, Vị trí ghế, Tiền vé, Danh mục combo, Tiền combo và Tổng thanh toán (VND).\n"
                "5. Khách hàng lựa chọn cổng thanh toán trực tuyến: VNPAY, MoMo hoặc Thẻ tín dụng/ATM.\n"
                "6. Khách hàng bấm 'XÁC NHẬN THANH TOÁN'. Hệ thống gọi BookingController.processPayment().\n"
                "7. Hệ thống thực hiện Transaction CSDL:\n"
                "   • Tạo mã đơn hàng duy nhất booking_code (VD: BKG-20261029-XXXXXX).\n"
                "   • Chèn bản ghi vào bảng bookings với payment_status = 'paid', booking_type = 'online'.\n"
                "   • Chèn các bản ghi vào bảng tickets, sinh mã ticket_code và chuỗi qr_data.\n"
                "   • Chèn chi tiết các combo vào bảng booking_combos.\n"
                "   • Xóa các bản ghi khóa tạm trong bảng seat_locks.\n"
                "8. Hệ thống điều hướng sang trang thành công (/booking/success/:bookingCode), hiển thị vé điện tử kèm mã QR Code từng ghế để khách tải về máy hoặc xem trong 'Vé của tôi'.",
            "Luồng sự kiện phụ (Alternative Flow)":
                "8a. Khách hàng có thể truy cập mục 'Vé của tôi' (/my-tickets) bất kỳ lúc nào để xem lại lịch sử các vé đã mua kèm mã QR Code soát vé.",
            "Luồng ngoại lệ (Exception Flow)":
                "6a. Nếu thời gian 5 phút giữ chỗ đã hết hạn trước khi bấm thanh toán: Hệ thống hủy giao dịch và thông báo 'Thời gian giữ ghế đã hết hạn, vui lòng đặt lại vé!'.",
            "Quy tắc nghiệp vụ (Business Rules)":
                "Ràng buộc toàn vẹn UNIQUE(showtime_id, seat_id) trong bảng tickets đảm bảo một vị trí ghế không bao giờ bị bán trùng 2 lần trong cùng một suất chiếu; chuỗi qr_data chứa mã vé kèm chữ ký bảo mật."
        },
        14: { # UC07
            "Tên Use Case": "UC07: Bán vé trực tiếp tại quầy POS",
            "Tác nhân chính": "Nhân viên quầy (Staff)",
            "Mục đích": "Hỗ trợ nhân viên bán vé cho khách hàng vãng lai trực tiếp tại rạp nhanh chóng dưới 30 giây, thu tiền mặt/thẻ và in vé xem phim kèm mã QR.",
            "Tiền điều kiện": "Nhân viên đã đăng nhập tài khoản có vai trò staff, manager hoặc admin và truy cập giao diện /staff/pos.",
            "Hậu điều kiện": "Đơn hàng được lưu vào bookings với booking_type = 'pos', created_by = staff_id; in vé xem phim và hóa đơn thành công.",
            "Luồng sự kiện chính (Basic Flow)":
                "1. Nhân viên mở giao diện Bán vé POS (/staff/pos). Hệ thống tự động tải các suất chiếu hôm nay của rạp.\n"
                "2. Nhân viên click chọn suất chiếu phim theo yêu cầu của khách hàng.\n"
                "3. Hệ thống hiển thị sơ đồ ghế thời gian thực qua API /staff/api/pos-seats/:showtimeId.\n"
                "4. Nhân viên click chọn vị trí ghế và chọn thêm combo bắp nước F&B (nếu có).\n"
                "5. Nhân viên nhập Họ tên và Số điện thoại khách hàng (không bắt buộc với khách vãng lai).\n"
                "6. Nhân viên chọn hình thức thanh toán: 'Tiền mặt' hoặc 'Quẹt thẻ/Mã QR'.\n"
                "7. Nhân viên nhấn nút 'XÁC NHẬN BÁN VÉ & XUẤT HÓA ĐƠN'.\n"
                "8. Hệ thống gọi StaffController.posCheckout() tạo đơn hàng bookings (user_id = NULL, booking_type = 'pos', created_by = staff_id).\n"
                "9. Hệ thống sinh các bản ghi trong tickets, cập nhật trạng thái ghế và mở lệnh in vé nhiệt chứa mã QR Code, thông tin suất chiếu và hóa đơn quầy giao cho khách.",
            "Luồng sự kiện phụ (Alternative Flow)":
                "4a. Nhân viên có thể nhấn nút 'Làm mới đơn' để hủy các ghế vừa chọn và thao tác lại từ đầu.",
            "Luồng ngoại lệ (Exception Flow)":
                "8a. Nếu ghế đã bị khách hàng online đặt trong tích tắc: Hệ thống báo lỗi 'Ghế đã được đặt, vui lòng chọn ghế khác!'.",
            "Quy tắc nghiệp vụ (Business Rules)":
                "Bán vé tại quầy không bắt buộc khách hàng phải đăng ký tài khoản thành viên; mọi đơn vé quầy đều gắn với mã định danh nhân viên (created_by) phục vụ đối soát doanh thu theo ca."
        },
        15: { # UC08
            "Tên Use Case": "UC08: Soát vé qua mã QR & Cảnh báo gian lận",
            "Tác nhân chính": "Nhân viên soát vé (Staff)",
            "Mục đích": "Kiểm soát ra vào phòng chiếu bằng Camera quét mã QR trên vé, tự động xác thực CSDL và phát cảnh báo chống vé giả mạo, vé quay vòng.",
            "Tiền điều kiện": "Nhân viên đăng nhập vào phân hệ Soát vé (/staff/scan) và cấp quyền truy cập Camera/Webcam.",
            "Hậu điều kiện": "Vé hợp lệ được cập nhật status = 'checked_in', lưu mốc thời gian checked_in_at = NOW() và mã nhân viên checked_in_by = staff_id.",
            "Luồng sự kiện chính (Basic Flow)":
                "1. Khách hàng đưa mã QR vé xem phim trước Camera hoặc súng quét mã vạch.\n"
                "2. Thư viện HTML5-QRCode tự động nhận diện và trích xuất chuỗi mã vé (hoặc nhân viên nhập mã TKT thủ công).\n"
                "3. Hệ thống gửi mã vé tới API /staff/api/check-ticket đối soát với bảng tickets trong CSDL.\n"
                "4. Hệ thống kiểm tra trạng thái vé: Nếu vé tồn tại và có status = 'unused':\n"
                "   • Gọi Ticket.checkIn(code, staffId).\n"
                "   • Cập nhật status = 'checked_in', checked_in_at = NOW(), checked_in_by = staff_id.\n"
                "   • Hiển thị thông báo XANH LÁ: 'SOÁT VÉ THÀNH CÔNG! HỢP LỆ VÀO PHÒNG'.\n"
                "   • Hiển thị chi tiết: Tên phim, Phòng chiếu, Suất chiếu, Ghế ngồi và Họ tên khách.\n"
                "5. Hệ thống tự động ghi nhận vé vào danh sách lịch sử soát vé trong ngày (/staff/history).",
            "Luồng sự kiện phụ (Alternative Flow)":
                "5a. Nhân viên có thể mở tab 'Lịch sử soát vé' (/staff/history) để theo dõi số lượng khách đã vào phòng chiếu theo từng ca trực.",
            "Luồng ngoại lệ (Exception Flow)":
                "4a. Nếu vé có status = 'checked_in' (đã soát trước đó): Hệ thống lập tức phát còi báo động và hiển thị banner ĐỎ chớp nháy: 'CẢNH BÁO GIAN LẬN: VÉ ĐÃ ĐƯỢC SỬ DỤNG TRƯỚC ĐÓ!' kèm thời gian đã check-in lần đầu để ngăn chặn vé quay vòng.\n"
                "4b. Nếu mã vé không tồn tại trong CSDL: Hiển thị cảnh báo VÀNG: 'VÉ KHÔNG HỢP LỆ HOẶC VÉ GIẢ MẠO!'.",
            "Quy tắc nghiệp vụ (Business Rules)":
                "Mỗi mã vé chỉ được phép check-in duy nhất một lần; hệ thống bắt buộc lưu mã định danh nhân viên (checked_in_by) để kiểm soát trách nhiệm nội bộ."
        },
        16: { # UC09
            "Tên Use Case": "UC09: Quản lý danh mục phim chiếu rạp",
            "Tác nhân chính": "Quản lý rạp (Manager), Quản trị viên (Admin)",
            "Mục đích": "Quản lý toàn diện danh mục phim chiếu tại rạp (thêm mới, chỉnh sửa thông tin, tải lên poster, nhúng trailer YouTube và cập nhật trạng thái phát hành).",
            "Tiền điều kiện": "Người dùng đăng nhập với quyền Manager hoặc Admin và truy cập /manager/movies.",
            "Hậu điều kiện": "Bản ghi phim được thêm mới, cập nhật hoặc xóa trong bảng movies; file poster được lưu trữ trên server.",
            "Luồng sự kiện chính (Basic Flow)":
                "1. Quản lý truy cập mục 'Quản lý phim' (/manager/movies). Hệ thống hiển thị bảng danh sách các phim kèm trạng thái phát hành.\n"
                "2. Thêm phim mới: Quản lý nhấn 'Thêm phim mới' (/manager/movies/create).\n"
                "3. Hệ thống hiển thị form nhập: Tiêu đề, Tên gốc, Thể loại, Thời lượng (phút), Ngày phát hành, Ngày kết thúc, Giới hạn độ tuổi (P/K/T13/T16/T18), Đạo diễn, Diễn viên, Mô tả tóm tắt, Link trailer YouTube và trường chọn file ảnh Poster.\n"
                "4. Quản lý điền thông tin, chọn file ảnh poster và nhấn 'Lưu thông tin phim'.\n"
                "5. Hệ thống kiểm tra dữ liệu, upload ảnh vào thư mục /public/uploads/posters/ qua Multer và thực thi chèn bản ghi vào bảng movies.\n"
                "6. Hệ thống chuyển hướng về danh sách phim và hiển thị thông báo thành công.\n"
                "7. Chỉnh sửa phim: Quản lý bấm 'Sửa' (/manager/movies/edit/:id), cập nhật thông tin hoặc chuyển đổi trạng thái (now_showing, coming_soon, ended) và nhấn 'Cập nhật'.",
            "Luồng sự kiện phụ (Alternative Flow)":
                "1a. Quản lý có thể tìm kiếm phim theo tên hoặc lọc theo thể loại và trạng thái phát hành.",
            "Luồng ngoại lệ (Exception Flow)":
                "4a. Nếu thiếu các trường bắt buộc (Tiêu đề, Thời lượng, Ngày phát hành): Hệ thống báo lỗi và giữ lại dữ liệu form.\n"
                "7a. Xóa phim: Nếu bộ phim đã có suất chiếu trong bảng showtimes, hệ thống chặn xóa cứng để bảo vệ toàn vẹn dữ liệu, chỉ cho phép chuyển trạng thái sang 'ended'.",
            "Quy tắc nghiệp vụ (Business Rules)":
                "Thời lượng phim (duration) phải là số nguyên dương tính theo phút; phân loại độ tuổi tuân thủ chuẩn Cục Điện ảnh: P, K, T13, T16, T18."
        },
        17: { # UC10
            "Tên Use Case": "UC10: Quản lý phòng chiếu & Cấu hình sơ đồ ghế",
            "Tác nhân chính": "Quản lý rạp (Manager), Quản trị viên (Admin)",
            "Mục đích": "Quản lý cơ sở vật chất phòng chiếu của rạp, cấu hình thông số kỹ thuật màn hình và điều chỉnh trạng thái bảo trì của từng vị trí ghế ngồi.",
            "Tiền điều kiện": "Người dùng đăng nhập với quyền Manager hoặc Admin và truy cập /manager/rooms.",
            "Hậu điều kiện": "Bản ghi phòng mới được thêm vào bảng rooms; ma trận ghế ngồi trong bảng seats được tự động sinh hoặc cập nhật trạng thái.",
            "Luồng sự kiện chính (Basic Flow)":
                "1. Quản lý truy cập mục 'Phòng chiếu & Sơ đồ ghế' (/manager/rooms).\n"
                "2. Hệ thống hiển thị danh sách các phòng: Tên phòng, Loại màn hình (2D, 3D, IMAX, 4DX), Số hàng ghế, Số ghế mỗi hàng, Tổng số ghế và Trạng thái.\n"
                "3. Thêm phòng mới: Quản lý nhấn 'Tạo phòng chiếu mới', nhập Tên phòng, chọn Loại màn hình, nhập Số hàng ghế (A-G) và Số ghế mỗi hàng (1-12).\n"
                "4. Quản lý nhấn 'Lưu phòng chiếu'. Hệ thống thực hiện Transaction chèn bản ghi vào bảng rooms, sau đó tự động chạy vòng lặp sinh đầy đủ các bản ghi ghế vào bảng seats (A01 đến G12).\n"
                "5. Cấu hình chi tiết ghế: Quản lý bấm 'Xem sơ đồ ghế' của phòng (/manager/rooms/:id).\n"
                "6. Giao diện kết xuất sơ đồ ma trận ghế trực quan. Quản lý click vào ghế bất kỳ để:\n"
                "   • Bật/Tắt bảo trì ghế hỏng (chuyển đổi status giữa 'active' và 'maintenance').\n"
                "   • Đổi loại ghế (Ghế thường regular, VIP vip, Sweetbox sweetbox) và hệ số giá tương ứng.\n"
                "7. Quản lý nhấn 'Cập nhật cấu hình ghế'. Hệ thống lưu CSDL và thông báo thành công.",
            "Luồng sự kiện phụ (Alternative Flow)":
                "Không có.",
            "Luồng ngoại lệ (Exception Flow)":
                "3a. Tên phòng chiếu không được trùng lặp trong cùng một cụm rạp.",
            "Quy tắc nghiệp vụ (Business Rules)":
                "Ghế có trạng thái 'maintenance' sẽ tự động bị khóa trên toàn bộ hệ thống đặt vé trực tuyến và quầy POS để tránh bán vé vị trí ghế hỏng cho khách."
        },
        18: { # UC11
            "Tên Use Case": "UC11: Lập lịch suất chiếu & Chống xung đột",
            "Tác nhân chính": "Quản lý rạp (Manager), Quản trị viên (Admin)",
            "Mục đích": "Lập thời khóa biểu các suất chiếu phim, áp dụng thuật toán ConflictDetector tự động phát hiện và ngăn chặn trùng lịch phòng chiếu.",
            "Tiền điều kiện": "Quản lý đăng nhập vào phân hệ /manager/showtimes và dữ liệu Phim, Phòng chiếu đã có sẵn trong CSDL.",
            "Hậu điều kiện": "Bản ghi suất chiếu mới được ghi nhận an toàn vào bảng showtimes với trạng thái scheduled và thời gian không bị xung đột.",
            "Luồng sự kiện chính (Basic Flow)":
                "1. Quản lý truy cập phân hệ 'Lập lịch suất chiếu' (/manager/showtimes).\n"
                "2. Hệ thống hiển thị thời khóa biểu lịch chiếu hiện có theo từng phòng và từng ngày.\n"
                "3. Quản lý nhấn 'Tạo suất chiếu mới' (/manager/showtimes/create).\n"
                "4. Quản lý chọn: Bộ phim chiếu, Phòng chiếu, Ngày chiếu, Giờ bắt đầu (start_time) và Giá vé cơ bản (base_price, mặc định 80.000 VNĐ).\n"
                "5. Hệ thống tự động tính thời gian kết thúc dự kiến: end_time = start_time + duration + buffer_minutes (15 phút dọn phòng).\n"
                "6. Khi quản lý thay đổi thời gian hoặc phòng, hệ thống tự động kích hoạt AJAX gọi module ConflictDetector.checkShowtimeConflict().\n"
                "7. Module thực hiện truy vấn kiểm tra giao thoa khoảng thời gian:\n"
                "   WHERE room_id = ? AND status = 'scheduled' AND (start_time < new_end_time AND end_time > new_start_time).\n"
                "8. Không có xung đột: Hệ thống hiển thị thông báo XANH 'Phòng chiếu trống, khung giờ an toàn!' và mở nút 'Lưu suất chiếu'.\n"
                "9. Quản lý nhấn 'Lưu suất chiếu'. Hệ thống chèn bản ghi vào bảng showtimes và đồng bộ lên lịch bán vé toàn rạp.",
            "Luồng sự kiện phụ (Alternative Flow)":
                "8a. Nếu phát hiện giao thoa thời gian: Hệ thống khóa nút Lưu, hiển thị banner cảnh báo ĐỎ: 'XUNG ĐỘT PHÒNG CHIẾU: Đã có suất chiếu phim khác từ [HH:mm] đến [HH:mm]!' và gợi ý khung giờ an toàn tiếp theo.",
            "Luồng ngoại lệ (Exception Flow)":
                "4a. Nếu thời gian bắt đầu được chọn trong quá khứ: Hệ thống báo lỗi và từ chối tạo suất chiếu.\n"
                "9a. Không thể hủy hoặc xóa suất chiếu nếu đã có khách hàng mua vé trong bảng tickets.",
            "Quy tắc nghiệp vụ (Business Rules)":
                "Thời gian đệm dọn dẹp vệ sinh phòng chiếu (buffer_minutes = 15 phút) bắt buộc phải được cộng thêm vào thời gian chiếm dụng phòng để chuẩn bị cho suất chiếu kế tiếp."
        },
        19: { # UC12
            "Tên Use Case": "UC12: Quản lý bảng giá vé và danh mục combo F&B",
            "Tác nhân chính": "Quản lý rạp (Manager), Quản trị viên (Admin)",
            "Mục đích": "Cấu hình bảng giá vé cơ bản theo loại màn hình, quản lý hệ số phụ thu theo loại ghế và thiết lập danh mục gói combo bắp nước kinh doanh tại rạp.",
            "Tiền điều kiện": "Người dùng đăng nhập với quyền Manager hoặc Admin.",
            "Hậu điều kiện": "Dữ liệu giá vé và danh mục combo bắp nước được cập nhật vào bảng showtimes, seats và combos trong CSDL.",
            "Luồng sự kiện chính (Basic Flow)":
                "1. Quản lý truy cập mục 'Quản lý Combo Bắp Nước' (/manager/combos).\n"
                "2. Hệ thống hiển thị bảng danh sách combo: Tên gói, Mô tả thành phần, Giá bán (VNĐ), Ảnh minh họa và Trạng thái (active/inactive).\n"
                "3. Thêm combo mới: Quản lý nhấn 'Thêm Combo Mới', nhập Tên gói (VD: Combo Solo, Combo Couple), Đơn giá, Mô tả chi tiết và nhập link ảnh.\n"
                "4. Quản lý nhấn 'Lưu Combo'. Hệ thống kiểm tra dữ liệu và thêm bản ghi vào bảng combos.\n"
                "5. Chỉnh sửa combo: Quản lý bấm nút 'Sửa' trên từng dòng combo, điều chỉnh giá bán hoặc mô tả thành phần và nhấn 'Cập nhật'.\n"
                "6. Xóa / Tạm dừng bán combo: Quản lý chuyển trạng thái sang 'inactive' để ngừng kinh doanh gói combo trên luồng đặt vé.\n"
                "7. Đối với giá vé: Quản lý thiết lập giá vé cơ sở (base_price) khi tạo từng suất chiếu (suất 2D là 80.000 VNĐ, suất IMAX là 120.000 VNĐ) và hệ số giá ghế: Thường x1.0, VIP x1.25, Sweetbox x2.2.",
            "Luồng sự kiện phụ (Alternative Flow)":
                "Không có.",
            "Luồng ngoại lệ (Exception Flow)":
                "3a. Giá bán combo và giá vé cơ sở phải là số nguyên dương lớn hơn 0.",
            "Quy tắc nghiệp vụ (Business Rules)":
                "Giá bán combo và giá vé hiển thị trên website là giá cuối cùng bằng đơn vị Việt Nam Đồng (VNĐ)."
        },
        20: { # UC13
            "Tên Use Case": "UC13: Báo cáo & Thống kê doanh thu rạp",
            "Tác nhân chính": "Quản lý rạp (Manager), Quản trị viên (Admin)",
            "Mục đích": "Theo dõi các chỉ số tài chính, tổng doanh thu bán vé và combo F&B, số lượng vé tiêu thụ và Tỷ lệ lấp đầy phòng chiếu (Occupancy Rate %) theo thời gian thực.",
            "Tiền điều kiện": "Người dùng đăng nhập với vai trò Manager hoặc Admin và truy cập /manager/dashboard hoặc /manager/reports.",
            "Hậu điều kiện": "Báo cáo tổng hợp, biểu đồ trực quan và dữ liệu thống kê được kết xuất trên màn hình quản lý.",
            "Luồng sự kiện chính (Basic Flow)":
                "1. Quản lý truy cập màn hình Dashboard tổng quan (/manager/dashboard).\n"
                "2. Hệ thống tính toán và hiển thị 4 chỉ số KPI vận hành:\n"
                "   • Doanh thu hôm nay (VNĐ).\n"
                "   • Tổng số vé đã bán trong ngày.\n"
                "   • Số suất chiếu đang hoạt động.\n"
                "   • Tổng số lượng phim đang chiếu tại rạp.\n"
                "3. Hệ thống kết xuất biểu đồ cột Chart.js hiển thị doanh thu 7 ngày gần nhất, cho phép so sánh xu hướng doanh thu giữa các ngày trong tuần.\n"
                "4. Quản lý chuyển sang trang 'Báo cáo chi tiết' (/manager/reports).\n"
                "5. Hệ thống thống kê doanh thu theo từng bộ phim chiếu rạp: Tổng số vé bán ra, Doanh thu tiền vé, Doanh thu combo bắp nước và Tổng thu.\n"
                "6. Hệ thống tính toán Tỷ lệ lấp đầy phòng chiếu (Occupancy Rate %):\n"
                "   Tỷ lệ lấp đầy = (Tổng số vé đã bán / Tổng số ghế khả dụng của các suất chiếu) * 100%.\n"
                "7. Quản lý có thể chọn bộ lọc thời gian: 'Hôm nay', '7 ngày qua', 'Tháng này' để cập nhật lại số liệu thống kê.",
            "Luồng sự kiện phụ (Alternative Flow)":
                "Không có.",
            "Luồng ngoại lệ (Exception Flow)":
                "Không có.",
            "Quy tắc nghiệp vụ (Business Rules)":
                "Doanh thu chỉ được tính trên các đơn hàng đã thanh toán thành công (payment_status = 'paid'). Các đơn hàng bị hủy hoặc quá hạn không được tính vào doanh thu."
        },
        21: { # UC14
            "Tên Use Case": "UC14: Quản lý người dùng & Phân quyền vai trò (RBAC)",
            "Tác nhân chính": "Quản trị viên (Admin)",
            "Mục đích": "Giám sát tài khoản người dùng toàn hệ thống, tạo mới tài khoản nhân viên/quản lý, phân quyền vai trò theo mô hình RBAC và khóa/mở khóa tài khoản.",
            "Tiền điều kiện": "Người dùng đăng nhập với vai trò Quản trị viên cao nhất (admin) và truy cập phân hệ /admin/users.",
            "Hậu điều kiện": "Dữ liệu người dùng trong bảng users được cập nhật vai trò role_id hoặc trạng thái status.",
            "Luồng sự kiện chính (Basic Flow)":
                "1. Admin truy cập mục 'Quản lý người dùng' (/admin/users).\n"
                "2. Hệ thống hiển thị bảng danh sách toàn bộ người dùng: ID, Họ tên, Email, Số điện thoại, Vai trò (Admin, Manager, Staff, Client), Trạng thái (Active/Locked) và Ngày tạo.\n"
                "3. Admin có thể lọc người dùng theo vai trò hoặc tìm kiếm theo Tên / Email.\n"
                "4. Thêm tài khoản mới: Admin nhấn 'Tạo người dùng mới' (/admin/users/create), nhập Họ tên, Email, SĐT, Mật khẩu khởi tạo và chọn Vai trò (role_id: 1-Admin, 2-Manager, 3-Staff, 4-Client).\n"
                "5. Hệ thống kiểm tra trùng lặp email, băm mật khẩu bằng BCrypt và lưu bản ghi vào CSDL.\n"
                "6. Khóa / Mở khóa tài khoản: Admin nhấn nút chuyển đổi trạng thái (Toggle Status). Hệ thống đổi status giữa 'active' và 'locked'. Khi tài khoản bị khóa, người dùng lập tức bị từ chối đăng nhập tại UC01.\n"
                "7. Phân quyền vai trò: Admin nhấn 'Sửa' (/admin/users/edit/:id), thay đổi vai trò của người dùng và lưu lại.",
            "Luồng sự kiện phụ (Alternative Flow)":
                "1a. Admin có thể thực hiện xóa tài khoản người dùng không còn hoạt động.",
            "Luồng ngoại lệ (Exception Flow)":
                "6a. Admin không thể tự khóa hoặc xóa tài khoản của chính mình (hệ thống có cơ chế bảo vệ tài khoản quản trị tối cao).",
            "Quy tắc nghiệp vụ (Business Rules)":
                "Phân quyền tuân thủ nghiêm ngặt mô hình RBAC (Role-Based Access Control): Admin có toàn quyền hệ thống; Manager quản lý rạp; Staff bán vé & soát vé; Client đặt vé trực tuyến."
        },
        22: { # UC15
            "Tên Use Case": "UC15: Cấu hình tham số rạp & Giám sát Audit Log",
            "Tác nhân chính": "Quản trị viên (Admin)",
            "Mục đích": "Cài đặt các tham số vận hành cốt lõi của rạp trong CSDL system_settings và theo dõi nhật ký kiểm toán (Audit Logs) để giám sát an ninh toàn hệ thống.",
            "Tiền điều kiện": "Người dùng đăng nhập với quyền Admin cao nhất.",
            "Hậu điều kiện": "Các tham số trong bảng system_settings được cập nhật; danh sách nhật ký kiểm toán được hiển thị phục vụ công tác thanh tra.",
            "Luồng sự kiện chính (Basic Flow)":
                "1. Admin truy cập mục 'Cài đặt hệ thống' (/admin/settings).\n"
                "2. Hệ thống hiển thị các tham số cấu hình vận hành hiện hành:\n"
                "   • buffer_minutes: Thời gian đệm dọn phòng chiếu giữa hai suất chiếu liên tiếp (mặc định 15 phút).\n"
                "   • hold_time: Thời gian khóa giữ ghế tạm thời khi đặt vé trực tuyến (mặc định 5 phút).\n"
                "   • cinema_name: Tên thương hiệu rạp chiếu phim (CineStar Cinema).\n"
                "   • hotline: Đường dây nóng hỗ trợ khách hàng.\n"
                "   • address: Địa chỉ trụ sở rạp chiếu phim.\n"
                "3. Admin điều chỉnh các giá trị tham số và nhấn 'Lưu cài đặt'.\n"
                "4. Hệ thống cập nhật các khóa giá trị tương ứng vào bảng system_settings. Mọi module đặt vé và lập lịch suất chiếu sẽ ngay lập tức áp dụng tham số mới.\n"
                "5. Giám sát Audit Log: Admin truy cập mục 'Nhật ký hệ thống' (/admin/audit-logs).\n"
                "6. Hệ thống hiển thị bảng danh sách nhật ký kiểm toán: Mốc thời gian (Timestamp), Tài khoản thực hiện (User ID / Tên), Loại hành động (Đăng nhập, Tạo suất chiếu, Khóa tài khoản, Bán vé quầy, Cập nhật giá) và Địa chỉ IP truy cập.\n"
                "7. Admin có thể tra cứu, lọc nhật ký theo thời gian để kiểm tra an ninh hệ thống.",
            "Luồng sự kiện phụ (Alternative Flow)":
                "Không có.",
            "Luồng ngoại lệ (Exception Flow)":
                "3a. Các tham số thời gian (buffer_minutes, hold_time) bắt buộc phải là số nguyên dương lớn hơn 0.",
            "Quy tắc nghiệp vụ (Business Rules)":
                "Mọi thay đổi tham số hệ thống đều có hiệu lực tức thời mà không cần phải khởi động lại máy chủ ứng dụng; nhật ký kiểm toán là dữ liệu bất biến (chỉ đọc) để đảm bảo tính minh bạch khi đối soát."
        }
    }

    key_row_map = {
        "Tên Use Case": 1,
        "Tác nhân chính": 2,
        "Mục đích": 3,
        "Tiền điều kiện": 4,
        "Hậu điều kiện": 5,
        "Luồng sự kiện chính (Basic Flow)": 6,
        "Luồng sự kiện phụ (Alternative Flow)": 7,
        "Luồng ngoại lệ (Exception Flow)": 8,
        "Quy tắc nghiệp vụ (Business Rules)": 9
    }

    for tbl_idx, spec_data in specs.items():
        table = doc.tables[tbl_idx]
        print(f"Đang cập nhật Table {tbl_idx}: {spec_data['Tên Use Case']}...")
        for key, text_val in spec_data.items():
            r_idx = key_row_map.get(key)
            if r_idx and r_idx < len(table.rows):
                set_row_content(table, r_idx, text_val)

    # 5. LƯU LẠI TÀI LIỆU
    output_docx = "BTL_DACN_CNPM_3.docx"
    doc.save(output_docx)
    print("=================================================================")
    print(f"🎉 ĐÃ HOÀN TẤT CẬP NHẬT FILE BÁO CÁO: {output_docx}")
    print("=================================================================")

if __name__ == '__main__':
    apply_fixes()
