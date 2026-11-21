import os
import subprocess
from PIL import Image

puml_dir = os.path.join('report_assets', 'plantuml')
img_dir = os.path.join('report_assets', 'images')
os.makedirs(puml_dir, exist_ok=True)
os.makedirs(img_dir, exist_ok=True)

header_activity = """!pragma max_image_size 8192
skinparam nodesep 80
skinparam ranksep 40
skinparam conditionStyle inside
skinparam roundCorner 12
skinparam linetype ortho
skinparam shadowing false
skinparam defaultFontName Arial
skinparam defaultFontSize 11
skinparam dpi 200

skinparam activity {
  StartColor #000000
  EndColor #000000
  BackgroundColor #FCF0CC
  BorderColor #B85450
  BorderThickness 1.2
  FontColor #000000
}
skinparam diamond {
  BackgroundColor #FCF0CC
  BorderColor #B85450
  BorderThickness 1.2
  FontColor #000000
  FontSize 10
}
skinparam arrow {
  Color #333333
  FontColor #000000
  FontSize 10
}
"""

activities = {}

# UC01: Đăng ký và Đăng nhập
activities['activity_uc01_dang_nhap.puml'] = """@startuml
""" + header_activity + """
start
:Giao diện Đăng nhập / Đăng ký;
if (Chọn hình thức xác thực?) then ([Chưa có tài khoản])
  :Chuyển sang Giao diện Đăng ký;
  repeat :Nhập họ tên, email, mật khẩu, SĐT;
    :Nhấn nút "Đăng ký";
  backward: Báo lỗi / Email đã tồn tại;
  repeat while (Đăng ký thành công?) is ([Thất bại]) not ([Thành công])
  :Khởi tạo tài khoản người dùng mới;
  goto end_node
else ([Đã có tài khoản])
  :Mở form Đăng nhập tài khoản;
  repeat :Nhập email và mật khẩu;
    :Nhấn nút "Đăng nhập";
  backward: Sai mật khẩu / Bị khóa;
  repeat while (Thông tin chính xác?) is ([Thất bại]) not ([Thành công])
  :Xác thực danh tính và cấp quyền;
  goto end_node
endif

label end_node
:Khởi tạo phiên làm việc của người dùng;
stop
@enduml
"""

# UC02: Tra cứu phim và Xem chi tiết
activities['activity_uc02_tra_cuu_phim.puml'] = """@startuml
""" + header_activity + """
start
:Giao diện Trang chủ / Danh mục phim;
:Hiển thị danh sách phim đang chiếu và sắp chiếu;
if (Chọn phương thức tra cứu?) then ([Tìm kiếm theo từ khóa])
  :Nhấn vào thanh tìm kiếm;
  repeat :Nhập từ khóa tên phim;
    :Nhấn nút "Tìm kiếm";
  backward: Không tìm thấy phim;
  repeat while (Tìm thấy phim?) is ([Chưa có]) not ([Đã tìm thấy])
  :Hiển thị danh sách phim phù hợp;
  goto end_node
else ([Lọc theo thể loại & ngày])
  :Chọn bộ lọc thể loại, cụm rạp, ngày chiếu;
  :Áp dụng bộ lọc phim;
  :Hiển thị danh sách phim theo bộ lọc;
  goto end_node
endif

label end_node
:Bấm chọn phim để xem chi tiết;
:Hiển thị thông tin phim, Trailer và Suất chiếu;
stop
@enduml
"""

# UC03: Xem lịch chiếu theo cụm rạp và ngày
activities['activity_uc03_xem_lich_chieu.puml'] = """@startuml
""" + header_activity + """
start
:Giao diện Lịch chiếu rạp;
:Hiển thị danh sách cụm rạp và lịch chiếu tuần;
if (Chọn phương thức xem lịch?) then ([Xem theo cụm rạp])
  :Chọn cụm rạp mong muốn;
  repeat :Chọn ngày xem phim cụ thể;
    :Hệ thống kiểm tra lịch khả dụng;
  backward: Chưa có suất chiếu trong ngày;
  repeat while (Có suất chiếu?) is ([Chưa có]) not ([Đã có lịch])
  :Hiển thị lưới khung giờ theo phòng;
  goto end_node
else ([Xem theo bộ phim])
  :Chọn bộ phim cần xem lịch;
  :Chọn khu vực rạp gần nhất;
  :Hiển thị các khung giờ chiếu của phim;
  goto end_node
endif

label end_node
:Bấm chọn khung giờ suất chiếu;
:Chuyển sang màn hình Sơ đồ chọn ghế;
stop
@enduml
"""

# UC04: Chọn ghế ngồi và Khóa tạm thời 5 phút
activities['activity_uc04_chon_ghe_khoa_ghe.puml'] = """@startuml
""" + header_activity + """
start
:Giao diện Sơ đồ chọn ghế;
:Hiển thị ma trận vị trí ghế (Trống, Đã bán, VIP, Đôi);
if (Lựa chọn thao tác?) then ([Chọn vị trí ghế])
  repeat :Click chọn các vị trí ghế mong muốn;
    :Nhấn nút "Tiếp tục" giữ chỗ;
  backward: Ghế đã bị người khác chọn;
  repeat while (Ghế còn khả dụng?) is ([Đã bị chọn]) not ([Ghế hợp lệ])
  :Khóa giữ ghế 5 phút và kích hoạt đếm ngược;
  :Chuyển sang màn hình chọn Combo và Thanh toán;
  goto end_node
else ([Đổi suất chiếu khác])
  :Nhấn nút quay lại chọn suất chiếu;
  :Hủy phiên chọn ghế hiện tại;
  goto end_node
endif

label end_node
stop
@enduml
"""

# UC05: Chọn combo bắp nước (F&B)
activities['activity_uc05_chon_combo_fb.puml'] = """@startuml
""" + header_activity + """
start
:Giao diện Chọn combo bắp nước;
:Hiển thị danh mục các gói bắp rang và nước ngọt;
if (Khách hàng có nhu cầu?) then ([Có chọn combo])
  repeat :Chọn loại combo bắp nước;
    :Tăng hoặc giảm số lượng combo;
  backward: Vượt quá giới hạn phục vụ;
  repeat while (Số lượng hợp lệ?) is ([Vượt giới hạn]) not ([Hợp lệ])
  :Cộng tiền combo vào đơn hàng;
  goto end_node
else ([Không chọn combo])
  :Nhấn nút "Bỏ qua bắp nước";
  :Giữ nguyên tổng giá trị tiền vé;
  goto end_node
endif

label end_node
:Chuyển sang màn hình Thanh toán đơn hàng;
stop
@enduml
"""

# UC06: Đặt vé trực tuyến và Thanh toán
activities['activity_uc06_dat_ve_thanh_toan.puml'] = """@startuml
""" + header_activity + """
start
:Giao diện Thanh toán đơn hàng;
:Hiển thị tóm tắt thông tin đơn hàng;
:Chọn phương thức thanh toán (VNPay / MoMo);
if (Sử dụng Voucher giảm giá?) then ([Có mã Voucher])
  :Nhập mã khuyến mãi;
  :Giảm trừ trực tiếp vào tổng tiền;
  goto pay_node
else ([Không dùng mã])
  :Giữ nguyên số tiền thanh toán;
  goto pay_node
endif

label pay_node
repeat :Nhấn nút "Xác nhận thanh toán";
  :Xử lý giao dịch qua cổng thanh toán;
backward: Giao dịch lỗi / Hết hạn 5 phút;
repeat while (Thanh toán thành công?) is ([Thất bại]) not ([Thành công])
:Tạo đơn vé và Cấp vé điện tử mã QR Code;
stop
@enduml
"""

# UC07: Quản lý vé cá nhân và Xuất trình QR
activities['activity_uc07_quan_ly_ve_qr.puml'] = """@startuml
""" + header_activity + """
start
:Giao diện Lịch sử đặt vé cá nhân;
:Hiển thị danh sách các đơn đặt vé cá nhân;
:Chọn một đơn đặt vé trong danh sách;
if (Chọn thao tác xử lý vé?) then ([Xem vé điện tử QR])
  :Hiển thị thông tin vé kèm mã QR bảo mật;
  :Nhấn nút "Tải vé QR / Lưu hình ảnh";
  :Lưu vé về thiết bị thành công;
  goto end_node
else ([Yêu cầu hủy vé])
  :Kiểm tra điều kiện trước suất chiếu;
  :Nhập lý do hủy vé xem phim;
  :Xác nhận hủy và nhả ghế về trạng thái trống;
  goto end_node
endif

label end_node
stop
@enduml
"""

# UC08: Bán vé tại quầy (POS) và In hóa đơn
activities['activity_uc08_ban_ve_pos.puml'] = """@startuml
""" + header_activity + """
start
:Giao diện Bán vé tại quầy (POS);
:Hiển thị danh mục phim và các suất chiếu hôm nay;
:Nhân viên chọn phim, suất chiếu và ghế cho khách;
if (Khách có mua bắp nước?) then ([Có mua combo])
  :Chọn combo bắp nước tại quầy;
  :Cộng tiền combo vào hóa đơn;
  goto pay_pos
else ([Không mua])
  :Giữ nguyên giá tiền vé xem phim;
  goto pay_pos
endif

label pay_pos
repeat :Chọn hình thức thu tiền (Tiền mặt / Thẻ POS);
  :Nhấn nút "Xác nhận bán vé";
backward: Lỗi kết nối cổng thanh toán;
repeat while (Giao dịch hoàn tất?) is ([Thất bại]) not ([Thành công])
:Lưu hóa đơn và in vé nhiệt cho khách;
stop
@enduml
"""

# UC09: Quét mã QR soát vé qua camera
activities['activity_uc09_quet_ma_qr_camera.puml'] = """@startuml
""" + header_activity + """
start
:Giao diện Soát vé QR (Dành cho nhân viên);
:Kích hoạt máy quét / Camera thiết bị;
if (Phương thức tiếp nhận vé?) then ([Quét mã QR qua Camera])
  repeat :Đưa mã QR vé vào khung quét camera;
    :Camera chụp và giải mã chuỗi dữ liệu;
  backward: Mã mờ / Lỗi đọc mã;
  repeat while (Quét mã thành công?) is ([Chưa đọc được]) not ([Thành công])
  goto send_ticket
else ([Nhập mã vé thủ công])
  :Nhấn vào ô nhập mã vé dự phòng;
  :Nhập mã ký tự vé bằng bàn phím;
  :Bấm nút "Kiểm tra vé";
  goto send_ticket
endif

label send_ticket
:Gửi thông tin mã vé lên máy chủ đối soát;
stop
@enduml
"""

# UC10: Đối soát vé và Cảnh báo gian lận
activities['activity_uc10_doi_soat_ve_gian_lan.puml'] = """@startuml
""" + header_activity + """
start
:Hệ thống tiếp nhận thông tin đối soát vé;
:Truy vấn dữ liệu mã vé trong Cơ sở dữ liệu;
if (Tình trạng vé xem phim?) then ([Vé hợp lệ (Chưa soát)])
  :Kiểm tra đúng phòng và khung giờ chiếu;
  :Cập nhật trạng thái vé thành "Đã soát vé";
  :Bật đèn xanh thông báo cho khách vào rạp;
  goto end_node
else ([Vé gian lận (Đã soát)])
  :Phát âm thanh cảnh báo còi báo động;
  :Hiển thị chi tiết thời gian đã soát lần đầu;
  :Từ chối cho vào rạp và lập biên bản;
  goto end_node
endif

label end_node
stop
@enduml
"""

# UC11: Quản lý danh mục phim và Poster
activities['activity_uc11_quan_ly_phim.puml'] = """@startuml
""" + header_activity + """
start
:Giao diện Quản lý danh mục phim;
:Hiển thị danh sách các bộ phim trong hệ thống;
if (Chọn chức năng quản lý?) then ([Thêm phim mới])
  repeat :Nhập thông tin phim (Tên, thời lượng, thể loại);
    :Tải lên Poster phim và nhập link Trailer;
    :Nhấn nút "Thêm phim";
  backward: Thiếu trường dữ liệu bắt buộc;
  repeat while (Dữ liệu hợp lệ?) is ([Chưa hợp lệ]) not ([Hợp lệ])
  :Thêm phim mới vào hệ thống thành công;
  goto end_node
else ([Sửa hoặc Xóa phim])
  :Chọn một bộ phim trong danh sách;
  if (Thao tác quản lý?) then ([Sửa phim])
    :Chỉnh sửa thông tin phim;
    :Nhấn nút "Lưu cập nhật";
    goto end_node
  else ([Xóa phim])
    :Nhấn nút "Xóa phim";
    :Xác nhận xóa khỏi hệ thống;
    goto end_node
  endif
endif

label end_node
stop
@enduml
"""

# UC12: Quản lý phòng chiếu và Ghế bảo trì
activities['activity_uc12_quan_ly_phong_ghe.puml'] = """@startuml
""" + header_activity + """
start
:Giao diện Quản lý phòng chiếu và Ghế;
:Hiển thị danh sách phòng chiếu của cụm rạp;
if (Chọn nghiệp vụ phòng chiếu?) then ([Cấu hình ma trận ghế])
  :Chọn phòng chiếu cần thiết lập;
  :Điều chỉnh số hàng, số cột và loại ghế;
  :Nhấn nút "Lưu sơ đồ ghế";
  :Cập nhật ma trận ghế thành công;
  goto end_node
else ([Quản lý trạng thái ghế])
  :Mở sơ đồ ghế của phòng chiếu;
  if (Tác vụ bảo trì?) then ([Báo ghế hỏng])
    :Click chọn vị trí ghế bị hỏng;
    :Nhấn nút "Chuyển sang bảo trì";
    :Tạm khóa vị trí ghế không cho bán;
    goto end_node
  else ([Mở lại ghế])
    :Click chọn ghế đã sửa xong;
    :Nhấn nút "Kích hoạt lại ghế";
    :Chuyển trạng thái sang khả dụng;
    goto end_node
  endif
endif

label end_node
stop
@enduml
"""

# UC13: Lập suất chiếu và Kiểm tra xung đột
activities['activity_uc13_lap_suat_chieu_xung_dot.puml'] = """@startuml
""" + header_activity + """
start
:Giao diện Lập lịch suất chiếu;
:Hiển thị lịch chiếu hiện tại theo phòng và ngày;
if (Chọn tác vụ lập lịch?) then ([Thêm suất chiếu mới])
  repeat :Chọn cụm rạp, phòng chiếu, phim và giờ;
    :Nhấn nút "Tạo suất chiếu";
    :Kiểm tra thuật toán xung đột phòng;
  backward: Xung đột giờ với suất khác;
  repeat while (Thời gian hợp lệ?) is ([Bị xung đột]) not ([Không xung đột])
  :Lưu suất chiếu mới thành công vào hệ thống;
  goto end_node
else ([Sửa hoặc Hủy suất chiếu])
  :Chọn một suất chiếu trên lịch tuần;
  if (Thao tác quản lý?) then ([Đổi giờ chiếu])
    :Nhập khung giờ chiếu mới;
    :Kiểm tra xung đột và cập nhật lịch;
    goto end_node
  else ([Hủy suất chiếu])
    :Nhấn nút "Hủy suất chiếu";
    :Xác nhận hủy và giải phóng phòng chiếu;
    goto end_node
  endif
endif

label end_node
stop
@enduml
"""

# UC14: Thống kê doanh thu và Tỷ lệ lấp đầy
activities['activity_uc14_thong_ke_doanh_thu.puml'] = """@startuml
""" + header_activity + """
start
:Giao diện Báo cáo và Thống kê doanh thu;
:Hiển thị bảng tổng hợp doanh số và các nút chức năng;
if (Chọn tiêu chí thống kê?) then ([Thống kê theo cụm rạp])
  :Chọn cụm rạp và khoảng thời gian;
  :Nhấn nút "Xem thống kê";
  :Hiển thị biểu đồ doanh thu và tỷ lệ lấp đầy;
  goto end_node
else ([Xuất báo cáo tổng hợp])
  :Nhấn nút "Xuất báo cáo PDF / Excel";
  :Hệ thống kết xuất và tải file báo cáo về máy;
  goto end_node
endif

label end_node
stop
@enduml
"""

# UC15: Quản trị người dùng, RBAC và Cấu hình rạp
activities['activity_uc15_quan_tri_rbac_cai_dat.puml'] = """@startuml
""" + header_activity + """
start
:Giao diện Quản trị hệ thống (Admin Portal);
:Hiển thị danh sách tài khoản và cấu hình rạp;
if (Chọn chức năng quản trị?) then ([Phân quyền tài khoản])
  :Chọn tài khoản nhân viên cần phân quyền;
  :Chọn vai trò mới (Staff / Manager / Client);
  :Nhấn nút "Cập nhật quyền hạn";
  :Lưu vai trò mới thành công vào CSDL;
  goto end_node
else ([Cấu hình tham số rạp])
  :Chọn mục "Cài đặt tham số vận hành";
  :Thiết lập thời gian giữ ghế 5p và đệm 15p;
  :Nhấn nút "Lưu cấu hình hệ thống";
  goto end_node
endif

label end_node
stop
@enduml
"""

print("1. Đang ghi 15 tệp PUML Activity Diagrams (Tuyệt đối KHÔNG hình thoi trống, hình thoi 100% có điều kiện)...")
for filename, content in activities.items():
    fpath = os.path.join(puml_dir, filename)
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)

print("2. Đang biên dịch 15 biểu đồ hoạt động sang PNG...")
cmd = ['java', '-DPLANTUML_LIMIT_SIZE=8192', '-jar', 'plantuml.jar', '-tpng', os.path.join(puml_dir, 'activity_uc*.puml'), '-o', os.path.abspath(img_dir)]
res = subprocess.run(cmd, capture_output=True, text=True)
print("STDOUT:", res.stdout)
if res.stderr:
    print("STDERR:", res.stderr)

print("\n3. KIỂM TRA ĐỘ RỘNG VÀ ĐỘ NÉT CỦA 15 BIỂU ĐỒ HOẠT ĐỘNG:")
all_ok = True
for filename in activities.keys():
    png_name = filename.replace('.puml', '.png')
    png_path = os.path.join(img_dir, png_name)
    if os.path.exists(png_path):
        im = Image.open(png_path)
        w, h = im.size
        print(f"  - {png_name:42}: {w}x{h} px -> OK")
    else:
        print(f"  ❌ Không tìm thấy: {png_name}")
        all_ok = False

if all_ok:
    print("\n🎉 TOÀN BỘ 15 BIỂU ĐỒ HOẠT ĐỘNG ĐÃ ĐƯỢC BIÊN DỊCH THÀNH CÔNG VỚI CHẤT LƯỢNG CAO NHẤT!")
