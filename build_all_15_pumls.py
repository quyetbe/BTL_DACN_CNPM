# Script tạo 15 Biểu đồ hoạt động và 15 Biểu đồ tuần tự cho 15 Use Case chính
# - Biểu đồ hoạt động: Chuẩn phong cách ảnh mẫu (nền kem #FCF0CC, viền nâu đỏ #B85450, bo góc, nét thẳng, kim cương điều kiện).
#   QUY TẮC MỚI: Bỏ hình thoi trống, chỉ thẳng vào nút kết thúc, điều kiện sai/lỗi thì quay lại từ đầu (vòng lặp lặp lại).
# - Biểu đồ tuần tự: CHỈ DÙNG CHỮ TIẾNG VIỆT, HOÀN TOÀN KHÔNG DÙNG CODE, THUẬT TOÁN, CÔNG THỨC.

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
skinparam conditionEndStyle hline
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
else ([Đã có tài khoản])
  :Mở form Đăng nhập tài khoản;
  repeat :Nhập email và mật khẩu;
    :Nhấn nút "Đăng nhập";
  backward: Sai mật khẩu / Bị khóa;
  repeat while (Thông tin chính xác?) is ([Thất bại]) not ([Thành công])
  :Xác thực danh tính và cấp quyền;
endif
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
else ([Lọc theo thể loại & ngày])
  :Chọn bộ lọc thể loại, cụm rạp, ngày chiếu;
  :Áp dụng bộ lọc phim;
  :Hiển thị danh sách phim theo bộ lọc;
endif
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
else ([Xem theo bộ phim])
  :Chọn bộ phim cần xem lịch;
  :Chọn khu vực rạp gần nhất;
  :Hiển thị các khung giờ chiếu của phim;
endif
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
else ([Đổi suất chiếu khác])
  :Nhấn nút quay lại chọn suất chiếu;
  :Hủy phiên chọn ghế hiện tại;
endif
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
else ([Không chọn combo])
  :Nhấn nút "Bỏ qua bắp nước";
  :Giữ nguyên tổng giá trị tiền vé;
endif
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
else ([Không dùng mã])
  :Giữ nguyên số tiền thanh toán;
endif
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
else ([Yêu cầu hủy vé])
  :Kiểm tra điều kiện trước suất chiếu;
  :Nhập lý do hủy vé xem phim;
  :Xác nhận hủy và nhả ghế về trạng thái trống;
endif
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
else ([Không mua])
  :Giữ nguyên giá tiền vé xem phim;
endif
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
else ([Nhập mã vé thủ công])
  :Nhấn vào ô nhập mã vé dự phòng;
  :Nhập mã ký tự vé bằng bàn phím;
  :Bấm nút "Kiểm tra vé";
endif
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
else ([Vé gian lận (Đã soát)])
  :Phát âm thanh cảnh báo còi báo động;
  :Hiển thị chi tiết thời gian đã soát lần đầu;
  :Từ chối cho vào rạp và lập biên bản;
endif
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
else ([Sửa hoặc Xóa phim])
  :Chọn một bộ phim trong danh sách;
  if (Thao tác quản lý?) then ([Sửa phim])
    :Chỉnh sửa thông tin phim;
    :Nhấn nút "Lưu cập nhật";
  else ([Xóa phim])
    :Nhấn nút "Xóa phim";
    :Xác nhận xóa khỏi hệ thống;
  endif
endif
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
else ([Quản lý trạng thái ghế])
  :Mở sơ đồ ghế của phòng chiếu;
  if (Tác vụ bảo trì?) then ([Báo ghế hỏng])
    :Click chọn vị trí ghế bị hỏng;
    :Nhấn nút "Chuyển sang bảo trì";
    :Tạm khóa vị trí ghế không cho bán;
  else ([Mở lại ghế])
    :Click chọn ghế đã sửa xong;
    :Nhấn nút "Kích hoạt lại ghế";
    :Chuyển trạng thái sang khả dụng;
  endif
endif
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
else ([Sửa hoặc Hủy suất chiếu])
  :Chọn một suất chiếu trên lịch tuần;
  if (Thao tác quản lý?) then ([Đổi giờ chiếu])
    :Nhập khung giờ chiếu mới;
    :Kiểm tra xung đột và cập nhật lịch;
  else ([Hủy suất chiếu])
    :Nhấn nút "Hủy suất chiếu";
    :Xác nhận hủy và giải phóng phòng chiếu;
  endif
endif
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
else ([Xuất báo cáo tổng hợp])
  :Nhấn nút "Xuất báo cáo PDF / Excel";
  :Hệ thống kết xuất và tải file báo cáo về máy;
endif
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
else ([Cấu hình tham số rạp])
  :Chọn mục "Cài đặt tham số vận hành";
  :Thiết lập thời gian giữ ghế 5p và đệm 15p;
  :Nhấn nút "Lưu cấu hình hệ thống";
endif
stop
@enduml
"""

header_sequence = """!pragma max_image_size 8192
skinparam monochrome true
skinparam shadowing false
skinparam defaultFontName Arial
skinparam defaultFontSize 11
skinparam maxMessageSize 180
skinparam dpi 200
"""

sequences = {}

# ==============================================================================
# 15 BIỂU ĐỒ TUẦN TỰ (CHỈ DÙNG TIẾNG VIỆT, KHÔNG CODE, KHÔNG CÔNG THỨC, KHÔNG THUẬT TOÁN)
# ==============================================================================

# UC01
sequences['sequence_uc01_dang_nhap.puml'] = """@startuml
""" + header_sequence + """
title BIỂU ĐỒ TUẦN TỰ: UC01 - ĐĂNG KÝ VÀ ĐĂNG NHẬP TÀI KHOẢN

actor "Người dùng" as User
boundary "Giao diện Đăng nhập" as UI_Login
control "Bộ điều khiển Xác thực" as Ctrl
entity "Tài khoản người dùng" as ModelUser
database "Cơ sở dữ liệu" as DB

User -> UI_Login: 1. Nhập thông tin Email và Mật khẩu
activate UI_Login

UI_Login -> Ctrl: 2. Gửi thông tin đăng nhập lên máy chủ
activate Ctrl

Ctrl -> ModelUser: 3. Yêu cầu tìm kiếm tài khoản theo Email
activate ModelUser

ModelUser -> DB: 4. Truy vấn thông tin người dùng từ cơ sở dữ liệu
activate DB
DB --> ModelUser: Trả về bản ghi thông tin người dùng
deactivate DB

ModelUser --> Ctrl: Cung cấp đối tượng tài khoản người dùng
deactivate ModelUser

Ctrl -> Ctrl: 5. So khớp mật khẩu và kiểm tra trạng thái hoạt động
alt Mật khẩu chính xác và tài khoản đang hoạt động
  Ctrl -> Ctrl: 6. Khởi tạo phiên làm việc của người dùng
  Ctrl --> UI_Login: 7a. Điều hướng người dùng vào hệ thống
  UI_Login --> User: 8a. Hiển thị giao diện chính tương ứng vai trò
else Sai mật khẩu hoặc tài khoản đã bị khóa
  Ctrl --> UI_Login: 7b. Trả về thông báo lỗi đăng nhập thất bại
  UI_Login --> User: 8b. Hiển thị thông báo lỗi trên màn hình
end
deactivate Ctrl
deactivate UI_Login
@enduml
"""

# UC02
sequences['sequence_uc02_tra_cuu_phim.puml'] = """@startuml
""" + header_sequence + """
title BIỂU ĐỒ TUẦN TỰ: UC02 - TRA CỨU PHIM VÀ XEM CHI TIẾT

actor "Khách hàng" as Client
boundary "Giao diện Danh mục phim" as UI_Movie
control "Bộ điều khiển Phim" as Ctrl
entity "Phim chiếu" as ModelMovie
database "Cơ sở dữ liệu" as DB

Client -> UI_Movie: 1. Nhập từ khóa tìm kiếm hoặc chọn thể loại phim
activate UI_Movie

UI_Movie -> Ctrl: 2. Gửi yêu cầu tìm kiếm phim theo điều kiện
activate Ctrl

Ctrl -> ModelMovie: 3. Yêu cầu lọc danh sách phim phù hợp
activate ModelMovie

ModelMovie -> DB: 4. Truy vấn các bộ phim đang chiếu thỏa mãn điều kiện
activate DB
DB --> ModelMovie: Trả về danh sách các bộ phim tìm thấy
deactivate DB

ModelMovie --> Ctrl: Cung cấp danh sách các bộ phim
deactivate ModelMovie

Ctrl --> UI_Movie: 5. Hiển thị danh sách các thẻ phim trên giao diện
deactivate Ctrl

UI_Movie --> Client: 6. Hiển thị danh sách phim kèm hình ảnh Poster
deactivate UI_Movie

Client -> UI_Movie: 7. Bấm chọn một bộ phim cụ thể để xem chi tiết
activate UI_Movie

UI_Movie -> Ctrl: 8. Gửi yêu cầu lấy thông tin chi tiết của phim
activate Ctrl

Ctrl -> ModelMovie: 9. Yêu cầu chi tiết phim và lịch chiếu đi kèm
activate ModelMovie

ModelMovie -> DB: 10. Truy vấn thông tin chi tiết và danh sách suất chiếu
activate DB
DB --> ModelMovie: Trả về đầy đủ thông tin phim và suất chiếu
deactivate DB

ModelMovie --> Ctrl: Cung cấp dữ liệu chi tiết bộ phim
deactivate ModelMovie

Ctrl --> UI_Movie: 11. Trình bày nội dung chi tiết và danh sách suất chiếu
deactivate Ctrl

UI_Movie --> Client: 12. Hiển thị thông tin phim, trailer và các giờ chiếu
deactivate UI_Movie
@enduml
"""

# UC03
sequences['sequence_uc03_xem_lich_chieu.puml'] = """@startuml
""" + header_sequence + """
title BIỂU ĐỒ TUẦN TỰ: UC03 - XEM LỊCH CHIẾU THEO CỤM RẠP VÀ NGÀY

actor "Khách hàng" as Client
boundary "Giao diện Lịch chiếu" as UI_Showtime
boundary "Giao diện Chọn ghế" as UI_Seat
control "Bộ điều khiển Lịch chiếu" as Ctrl
entity "Suất chiếu" as ModelShowtime
database "Cơ sở dữ liệu" as DB

Client -> UI_Showtime: 1. Chọn cụm rạp và ngày chiếu mong muốn
activate UI_Showtime

UI_Showtime -> Ctrl: 2. Gửi yêu cầu lấy lịch chiếu theo rạp và ngày
activate Ctrl

Ctrl -> ModelShowtime: 3. Yêu cầu danh sách suất chiếu của rạp
activate ModelShowtime

ModelShowtime -> DB: 4. Truy vấn các suất chiếu khả dụng trong ngày
activate DB
DB --> ModelShowtime: Trả về danh sách suất chiếu theo phòng
deactivate DB

ModelShowtime --> Ctrl: Cung cấp dữ liệu các suất chiếu
deactivate ModelShowtime

Ctrl -> Ctrl: 5. Phân nhóm suất chiếu theo định dạng phòng chiếu
Ctrl --> UI_Showtime: 6. Hiển thị lưới các khung giờ suất chiếu
deactivate Ctrl

UI_Showtime --> Client: 7. Hiển thị các nút giờ chiếu (18:45, 20:30, ...)
deactivate UI_Showtime

Client -> UI_Showtime: 8. Nhấp chọn một khung giờ suất chiếu cụ thể
activate UI_Showtime

UI_Showtime -> UI_Seat: 9. Chuyển hướng sang màn hình chọn ghế ngồi
deactivate UI_Showtime
activate UI_Seat

UI_Seat --> Client: 10. Hiển thị sơ đồ ghế của suất chiếu đã chọn
deactivate UI_Seat
@enduml
"""

# UC04
sequences['sequence_uc04_chon_ghe_khoa_ghe.puml'] = """@startuml
""" + header_sequence + """
title BIỂU ĐỒ TUẦN TỰ: UC04 - CHỌN GHẾ NGỒI VÀ KHÓA TẠM THỜI 5 PHÚT

actor "Khách hàng" as Client
boundary "Giao diện Chọn ghế" as UI_Seat
control "Bộ điều khiển Đặt vé" as Ctrl
entity "Khóa giữ ghế" as ModelLock
database "Cơ sở dữ liệu" as DB

Client -> UI_Seat: 1. Nhấp chọn các vị trí ghế ngồi trên sơ đồ
activate UI_Seat

UI_Seat -> UI_Seat: 2. Tự động tính tổng tiền tạm tính theo loại ghế

Client -> UI_Seat: 3. Nhấn nút "Tiếp tục" để giữ chỗ
UI_Seat -> Ctrl: 4. Gửi yêu cầu khóa giữ các ghế đã chọn
activate Ctrl

Ctrl -> ModelLock: 5. Yêu cầu kiểm tra và giữ ghế tạm thời cho khách
activate ModelLock

ModelLock -> DB: 6. Kiểm tra trạng thái hiện tại của các ghế được chọn
activate DB
DB --> ModelLock: Trả về danh sách ghế đang bị giữ hoặc đã bán
deactivate DB

alt Các ghế đã chọn đều còn trống hợp lệ
  ModelLock -> DB: 7a. Lưu bản ghi khóa giữ ghế tạm thời trong 5 phút
  activate DB
  DB --> ModelLock: Xác nhận khóa giữ ghế thành công
  deactivate DB
  ModelLock --> Ctrl: Thông báo các vị trí ghế đã được khóa giữ
  Ctrl --> UI_Seat: 8a. Phản hồi thành công và kích hoạt đếm ngược 5 phút
  UI_Seat --> Client: 9a. Chuyển tiếp sang bước chọn bắp nước đi kèm
else Có ghế đã bị người khác chọn trước đó
  ModelLock --> Ctrl: Thông báo ghế đã bị giữ bởi khách hàng khác
  deactivate ModelLock
  Ctrl --> UI_Seat: 8b. Báo lỗi xung đột ghế vừa có người chọn
  UI_Seat --> Client: 9b. Cập nhật màu ghế bị giữ và yêu cầu chọn lại
end
deactivate Ctrl
deactivate UI_Seat
@enduml
"""

# UC05
sequences['sequence_uc05_chon_combo_fb.puml'] = """@startuml
""" + header_sequence + """
title BIỂU ĐỒ TUẦN TỰ: UC05 - CHỌN COMBO BẮP NƯỚC (F&B)

actor "Khách hàng" as Client
boundary "Giao diện Bắp nước" as UI_Combo
control "Bộ điều khiển Bắp nước" as Ctrl
entity "Gói Bắp nước" as ModelCombo
database "Cơ sở dữ liệu" as DB

Client -> UI_Combo: 1. Truy cập vào trang lựa chọn bắp nước
activate UI_Combo

UI_Combo -> Ctrl: 2. Gửi yêu cầu lấy danh mục các gói bắp nước
activate Ctrl

Ctrl -> ModelCombo: 3. Yêu cầu danh sách các combo đang phục vụ
activate ModelCombo

ModelCombo -> DB: 4. Truy vấn các gói combo đang hoạt động trong CSDL
activate DB
DB --> ModelCombo: Trả về danh mục combo bắp nước kèm giá bán
deactivate DB

ModelCombo --> Ctrl: Cung cấp danh sách các gói combo
deactivate ModelCombo

Ctrl --> UI_Combo: 5. Hiển thị danh sách các gói bắp nước trên giao diện
deactivate Ctrl

Client -> UI_Combo: 6. Tăng số lượng gói combo mong muốn
UI_Combo -> UI_Combo: 7. Cập nhật tổng tiền đơn hàng gồm vé và combo
Client -> UI_Combo: 8. Nhấn nút "Tiếp tục thanh toán"
UI_Combo --> Client: 9. Chuyển sang màn hình xác nhận thông tin thanh toán
deactivate UI_Combo
@enduml
"""

# UC06
sequences['sequence_uc06_dat_ve_thanh_toan.puml'] = """@startuml
""" + header_sequence + """
title BIỂU ĐỒ TUẦN TỰ: UC06 - ĐẶT VÉ TRỰC TUYẾN VÀ THANH TOÁN

actor "Khách hàng" as Client
boundary "Giao diện Thanh toán" as UI_Pay
control "Bộ điều khiển Thanh toán" as Ctrl
entity "Đơn đặt vé" as ModelBooking
database "Cơ sở dữ liệu" as DB
boundary "Cổng thanh toán trực tuyến" as Gateway

Client -> UI_Pay: 1. Chọn phương thức thanh toán và bấm "Thanh toán"
activate UI_Pay

UI_Pay -> Ctrl: 2. Gửi yêu cầu khởi tạo giao dịch thanh toán
activate Ctrl

Ctrl -> Gateway: 3. Yêu cầu cổng thanh toán tạo phiên giao dịch mới
activate Gateway
Gateway --> Ctrl: Cung cấp đường dẫn trang thanh toán an toàn
Ctrl --> UI_Pay: 4. Chuyển hướng sang giao diện cổng thanh toán
deactivate Ctrl

UI_Pay --> Client: 5. Hiển thị màn hình quét mã thanh toán ngân hàng
Client -> Gateway: 6. Khách hàng thực hiện quét mã thanh toán trên ứng dụng
Gateway -> Gateway: 7. Xác thực và trừ tiền trong tài khoản khách hàng
Gateway -> Ctrl: 8. Gửi tín hiệu thông báo thanh toán thành công
activate Ctrl
deactivate Gateway

Ctrl -> ModelBooking: 9. Yêu cầu xác nhận đơn vé và cấp vé điện tử
activate ModelBooking

ModelBooking -> DB: 10. Cập nhật đơn vé thành đã thanh toán, lưu vé và giải phóng khóa ghế
activate DB
DB --> ModelBooking: Xác nhận lưu trữ giao dịch thành công
deactivate DB

ModelBooking --> Ctrl: Cung cấp thông tin đơn vé hoàn tất
deactivate ModelBooking

Ctrl --> UI_Pay: 11. Chuyển hướng sang trang hoàn thành đặt vé
deactivate Ctrl

UI_Pay --> Client: 12. Hiển thị vé xem phim điện tử kèm mã QR Code
deactivate UI_Pay
@enduml
"""

# UC07
sequences['sequence_uc07_quan_ly_ve_qr.puml'] = """@startuml
""" + header_sequence + """
title BIỂU ĐỒ TUẦN TỰ: UC07 - QUẢN LÝ VÉ CÁ NHÂN VÀ XUẤT TRÌNH QR

actor "Khách hàng" as Client
boundary "Giao diện Vé cá nhân" as UI_MyTickets
control "Bộ điều khiển Vé" as Ctrl
entity "Vé xem phim" as ModelTicket
database "Cơ sở dữ liệu" as DB

Client -> UI_MyTickets: 1. Truy cập vào trang quản lý vé cá nhân
activate UI_MyTickets

UI_MyTickets -> Ctrl: 2. Gửi yêu cầu lấy danh sách vé của người dùng
activate Ctrl

Ctrl -> ModelTicket: 3. Yêu cầu danh sách vé theo định danh người dùng
activate ModelTicket

ModelTicket -> DB: 4. Truy vấn các đơn đặt vé trong lịch sử cá nhân
activate DB
DB --> ModelTicket: Trả về danh sách vé đã đặt và trạng thái vé
deactivate DB

ModelTicket --> Ctrl: Cung cấp danh sách các vé xem phim
deactivate ModelTicket

Ctrl --> UI_MyTickets: 5. Hiển thị danh sách vé đã mua trên giao diện
deactivate Ctrl

Client -> UI_MyTickets: 6. Bấm chọn một vé cụ thể để xem chi tiết
UI_MyTickets -> Ctrl: 7. Yêu cầu mã QR Code của vé xem phim đã chọn
activate Ctrl

Ctrl -> Ctrl: 8. Tạo hình ảnh mã QR Code chứa thông tin bảo mật của vé
Ctrl --> UI_MyTickets: 9. Trả về chi tiết vé xem phim và hình ảnh mã QR
deactivate Ctrl

UI_MyTickets --> Client: 10. Hiển thị vé điện tử và mã QR để vào phòng chiếu
deactivate UI_MyTickets
@enduml
"""

# UC08
sequences['sequence_uc08_ban_ve_pos.puml'] = """@startuml
""" + header_sequence + """
title BIỂU ĐỒ TUẦN TỰ: UC08 - BÁN VÉ TẠI QUẦY (POS) VÀ IN HÓA ĐƠN

actor "Nhân viên quầy" as Staff
boundary "Giao diện Bán vé quầy" as UI_POS
control "Bộ điều khiển Bán vé quầy" as Ctrl
entity "Đơn đặt vé" as ModelBooking
database "Cơ sở dữ liệu" as DB

Staff -> UI_POS: 1. Chọn suất chiếu và ghế ngồi theo yêu cầu của khách
activate UI_POS

Staff -> UI_POS: 2. Chọn thêm combo bắp nước (nếu khách mua thêm)
Staff -> UI_POS: 3. Lựa chọn hình thức thanh toán của khách hàng
Staff -> UI_POS: 4. Bấm nút "Xuất vé bán tại quầy"
UI_POS -> Ctrl: 5. Gửi thông tin đơn vé quầy lên máy chủ
activate Ctrl

Ctrl -> ModelBooking: 6. Yêu cầu tạo đơn đặt vé trực tiếp tại quầy
activate ModelBooking

ModelBooking -> DB: 7. Lưu đơn vé, chi tiết các vé và combo vào CSDL
activate DB
DB --> ModelBooking: Xác nhận lưu trữ đơn vé thành công
deactivate DB

ModelBooking --> Ctrl: Cung cấp đối tượng đơn vé quầy hoàn tất
deactivate ModelBooking

Ctrl -> Ctrl: 8. Sinh mã QR vé và tạo lệnh in hóa đơn bán vé
Ctrl --> UI_POS: 9. Gửi dữ liệu vé và lệnh in xuống máy in quầy
deactivate Ctrl

UI_POS --> Staff: 10. Kích hoạt máy in vé và hiển thị thông báo thành công
deactivate UI_POS
@enduml
"""

# UC09
sequences['sequence_uc09_quet_ma_qr_camera.puml'] = """@startuml
""" + header_sequence + """
title BIỂU ĐỒ TUẦN TỰ: UC09 - QUÉT MÃ QR SOÁT VÉ QUA CAMERA

actor "Nhân viên soát vé" as Staff
boundary "Giao diện Soát vé" as UI_Scan
control "Bộ điều khiển Soát vé" as Ctrl
entity "Vé xem phim" as ModelTicket
database "Cơ sở dữ liệu" as DB

Staff -> UI_Scan: 1. Mở màn hình soát vé và kích hoạt camera thiết bị
activate UI_Scan

Staff -> UI_Scan: 2. Hướng camera về phía mã QR trên điện thoại của khách
UI_Scan -> UI_Scan: 3. Nhận diện hình ảnh và giải mã chuỗi mã vạch
UI_Scan -> Ctrl: 4. Gửi chuỗi mã vé thu được lên máy chủ kiểm tra
activate Ctrl

Ctrl -> Ctrl: 5. Kiểm tra chữ ký số bảo mật của mã vé điện tử
Ctrl -> ModelTicket: 6. Yêu cầu tìm kiếm thông tin vé theo mã vé
activate ModelTicket

ModelTicket -> DB: 7. Truy vấn thông tin chi tiết vé xem phim từ CSDL
activate DB
DB --> ModelTicket: Trả về bản ghi thông tin vé xem phim
deactivate DB

ModelTicket --> Ctrl: Cung cấp đối tượng vé xem phim
deactivate ModelTicket

Ctrl --> UI_Scan: 8. Trả về thông tin chi tiết: Phim, Phòng, Ghế, Trạng thái
deactivate Ctrl

UI_Scan --> Staff: 9. Hiển thị thông tin vé lên màn hình để nhân viên kiểm tra
deactivate UI_Scan
@enduml
"""

# UC10
sequences['sequence_uc10_doi_soat_ve_gian_lan.puml'] = """@startuml
""" + header_sequence + """
title BIỂU ĐỒ TUẦN TỰ: UC10 - ĐỐI SOÁT VÉ VÀ CẢNH BÁO GIAN LẬN

actor "Nhân viên soát vé" as Staff
boundary "Giao diện Soát vé" as UI_Scan
control "Bộ điều khiển Soát vé" as Ctrl
entity "Vé xem phim" as ModelTicket
database "Cơ sở dữ liệu" as DB

Staff -> UI_Scan: 1. Nhấn nút xác nhận cho khách vào phòng chiếu
activate UI_Scan

UI_Scan -> Ctrl: 2. Gửi yêu cầu đối soát và đánh dấu sử dụng vé
activate Ctrl

Ctrl -> ModelTicket: 3. Yêu cầu kiểm tra trạng thái vé với phòng và giờ hiện tại
activate ModelTicket

ModelTicket -> DB: 4. Truy vấn trạng thái sử dụng của vé trong CSDL
activate DB
DB --> ModelTicket: Trả về trạng thái vé đã dùng hay chưa
deactivate DB

alt Vé đã bị sử dụng trước đó (Gian lận vé)
  ModelTicket -> DB: 5a. Ghi nhận vi phạm gian lận vé vào nhật ký hệ thống
  activate DB
  DB --> ModelTicket: Xác nhận ghi nhật ký gian lận thành công
  deactivate DB
  ModelTicket --> Ctrl: Thông báo phát hiện gian lận vé
  Ctrl --> UI_Scan: 6a. Phát âm thanh cảnh báo đỏ: "Vé đã được sử dụng trước đó!"
  UI_Scan --> Staff: 7a. Hiển thị cảnh báo đỏ và hướng dẫn giữ khách để kiểm tra
else Vé hợp lệ và đúng phòng, đúng suất chiếu
  ModelTicket -> DB: 5b. Đánh dấu vé đã sử dụng và lưu thời điểm soát vé
  activate DB
  DB --> ModelTicket: Xác nhận cập nhật trạng thái thành công
  deactivate DB
  ModelTicket --> Ctrl: Thông báo vé hợp lệ vào phòng
  deactivate ModelTicket
  Ctrl --> UI_Scan: 6b. Bật tín hiệu xanh: "Soát vé thành công - Mời vào phòng"
  UI_Scan --> Staff: 7b. Đèn xanh hiển thị và xác nhận khách vào phòng xem phim
end
deactivate Ctrl
deactivate UI_Scan
@enduml
"""

# UC11
sequences['sequence_uc11_quan_ly_phim.puml'] = """@startuml
""" + header_sequence + """
title BIỂU ĐỒ TUẦN TỰ: UC11 - QUẢN LÝ DANH MỤC PHIM VÀ POSTER

actor "Quản lý rạp" as Manager
boundary "Giao diện Quản lý phim" as UI_MovieAdmin
control "Bộ điều khiển Quản lý phim" as Ctrl
entity "Phim chiếu" as ModelMovie
database "Cơ sở dữ liệu" as DB

Manager -> UI_MovieAdmin: 1. Nhập thông tin phim mới và chọn tệp ảnh Poster
activate UI_MovieAdmin

Manager -> UI_MovieAdmin: 2. Nhấn nút "Lưu phim mới"
UI_MovieAdmin -> Ctrl: 3. Gửi toàn bộ dữ liệu phim và tệp ảnh lên máy chủ
activate Ctrl

Ctrl -> Ctrl: 4. Tối ưu hóa kích thước và lưu ảnh Poster vào máy chủ
Ctrl -> ModelMovie: 5. Yêu cầu tạo mới bản ghi phim trong hệ thống
activate ModelMovie

ModelMovie -> DB: 6. Thêm bản ghi phim mới vào bảng danh mục phim
activate DB
DB --> ModelMovie: Xác nhận thêm mới phim thành công
deactivate DB

ModelMovie --> Ctrl: Cung cấp đối tượng phim mới tạo
deactivate ModelMovie

Ctrl --> UI_MovieAdmin: 7. Phản hồi thêm mới phim thành công
deactivate Ctrl

UI_MovieAdmin --> Manager: 8. Hiển thị bộ phim mới trên danh sách quản lý
deactivate UI_MovieAdmin
@enduml
"""

# UC12
sequences['sequence_uc12_quan_ly_phong_ghe.puml'] = """@startuml
""" + header_sequence + """
title BIỂU ĐỒ TUẦN TỰ: UC12 - QUẢN LÝ PHÒNG CHIẾU VÀ GHẾ BẢO TRÌ

actor "Quản lý rạp" as Manager
boundary "Giao diện Quản lý phòng" as UI_RoomAdmin
control "Bộ điều khiển Phòng chiếu" as Ctrl
entity "Ghế ngồi" as ModelSeat
database "Cơ sở dữ liệu" as DB

Manager -> UI_RoomAdmin: 1. Chọn phòng chiếu cần cấu hình lại ghế
activate UI_RoomAdmin

UI_RoomAdmin -> Ctrl: 2. Gửi yêu cầu lấy sơ đồ ghế hiện tại của phòng
activate Ctrl

Ctrl -> ModelSeat: 3. Yêu cầu danh sách các ghế của phòng chiếu
activate ModelSeat

ModelSeat -> DB: 4. Truy vấn thông tin các ghế ngồi trong phòng từ CSDL
activate DB
DB --> ModelSeat: Trả về danh sách ghế và trạng thái của từng ghế
deactivate DB

ModelSeat --> Ctrl: Cung cấp dữ liệu sơ đồ ghế của phòng
deactivate ModelSeat

Ctrl --> UI_RoomAdmin: 5. Hiển thị ma trận ghế của phòng chiếu
deactivate Ctrl

Manager -> UI_RoomAdmin: 6. Chọn ghế hỏng và bấm nút "Đánh dấu bảo trì"
UI_RoomAdmin -> Ctrl: 7. Gửi yêu cầu cập nhật trạng thái ghế sang bảo trì
activate Ctrl

Ctrl -> ModelSeat: 8. Yêu cầu đổi trạng thái ghế được chọn
activate ModelSeat

ModelSeat -> DB: 9. Cập nhật trạng thái bảo trì cho ghế trong CSDL
activate DB
DB --> ModelSeat: Xác nhận cập nhật thành công
deactivate DB

ModelSeat --> Ctrl: Thông báo hoàn tất cập nhật ghế
deactivate ModelSeat

Ctrl --> UI_RoomAdmin: 10. Phản hồi cập nhật thành công
deactivate Ctrl

UI_RoomAdmin --> Manager: 11. Đổi màu hiển thị của ghế sang trạng thái bảo trì
deactivate UI_RoomAdmin
@enduml
"""

# UC13
sequences['sequence_uc13_lap_suat_chieu_xung_dot.puml'] = """@startuml
""" + header_sequence + """
title BIỂU ĐỒ TUẦN TỰ: UC13 - LẬP SUẤT CHIẾU VÀ KIỂM TRA XUNG ĐỘT

actor "Quản lý rạp" as Manager
boundary "Giao diện Lập suất chiếu" as UI_ShowtimeAdmin
control "Bộ điều khiển Lập suất chiếu" as Ctrl
entity "Bộ kiểm tra xung đột" as ServiceConflict
entity "Suất chiếu" as ModelShowtime
database "Cơ sở dữ liệu" as DB

Manager -> UI_ShowtimeAdmin: 1. Nhập thông tin: Phim, Phòng chiếu, Ngày và Giờ bắt đầu
activate UI_ShowtimeAdmin

Manager -> UI_ShowtimeAdmin: 2. Nhấn nút "Lập suất chiếu mới"
UI_ShowtimeAdmin -> Ctrl: 3. Gửi thông tin suất chiếu mới lên máy chủ
activate Ctrl

Ctrl -> ServiceConflict: 4. Yêu cầu kiểm tra xung đột lịch chiếu trong phòng
activate ServiceConflict

ServiceConflict -> DB: 5. Truy vấn các suất chiếu hiện có trong phòng vào ngày đó
activate DB
DB --> ServiceConflict: Trả về danh sách suất chiếu hiện có trong phòng
deactivate DB

alt Phát hiện khung giờ bị trùng lặp với suất chiếu khác
  ServiceConflict --> Ctrl: Cảnh báo phát hiện xung đột lịch chiếu
  Ctrl --> UI_ShowtimeAdmin: 6a. Báo lỗi: "Phòng chiếu đã có lịch chiếu trong khung giờ này!"
  UI_ShowtimeAdmin --> Manager: 7a. Hiển thị cảnh báo đỏ và gợi ý các khung giờ còn trống
else Khung giờ hoàn toàn hợp lệ và không bị trùng
  ServiceConflict --> Ctrl: Xác nhận khung giờ hoàn toàn khả dụng
  deactivate ServiceConflict
  Ctrl -> ModelShowtime: 8. Yêu cầu tạo bản ghi suất chiếu mới
  activate ModelShowtime
  ModelShowtime -> DB: 9. Thêm mới suất chiếu vào bảng lịch chiếu trong CSDL
  activate DB
  DB --> ModelShowtime: Xác nhận thêm mới suất chiếu thành công
  deactivate DB
  ModelShowtime --> Ctrl: Cung cấp đối tượng suất chiếu mới tạo
  deactivate ModelShowtime
  Ctrl --> UI_ShowtimeAdmin: 10. Phản hồi thiết lập suất chiếu thành công
  deactivate Ctrl
  UI_ShowtimeAdmin --> Manager: 11. Cập nhật suất chiếu lên bảng thời khóa biểu của rạp
end
deactivate UI_ShowtimeAdmin
@enduml
"""

# UC14
sequences['sequence_uc14_thong_ke_doanh_thu.puml'] = """@startuml
""" + header_sequence + """
title BIỂU ĐỒ TUẦN TỰ: UC14 - THỐNG KÊ DOANH THU VÀ TỶ LỆ LẤP ĐẦY

actor "Quản lý rạp" as Manager
boundary "Bảng điều khiển Thống kê" as UI_Dash
control "Bộ điều khiển Thống kê" as Ctrl
entity "Dịch vụ Tổng hợp báo cáo" as ServiceReport
database "Cơ sở dữ liệu" as DB

Manager -> UI_Dash: 1. Chọn khoảng thời gian thống kê và chọn cụm rạp
activate UI_Dash

UI_Dash -> Ctrl: 2. Gửi yêu cầu lấy số liệu báo cáo theo bộ lọc
activate Ctrl

Ctrl -> ServiceReport: 3. Yêu cầu tổng hợp doanh thu và số lượng vé
activate ServiceReport

ServiceReport -> DB: 4. Truy vấn tổng tiền từ các đơn vé đã thanh toán
activate DB
DB --> ServiceReport: Trả về số liệu doanh thu và số vé bán ra
deactivate DB

ServiceReport -> DB: 5. Truy vấn sức chứa phòng và số ghế đã phục vụ
activate DB
DB --> ServiceReport: Trả về số liệu ghế ngồi theo từng suất chiếu
deactivate DB

ServiceReport -> ServiceReport: 6. Tính toán tổng doanh thu và tỷ lệ lấp đầy phòng chiếu
ServiceReport --> Ctrl: Cung cấp đầy đủ số liệu thống kê phân tích
deactivate ServiceReport

Ctrl --> UI_Dash: 7. Trả về tập dữ liệu thống kê hoàn chỉnh
deactivate Ctrl

UI_Dash -> UI_Dash: 8. Vẽ biểu đồ cột doanh thu và biểu đồ tròn tỷ lệ lấp đầy
UI_Dash --> Manager: 9. Hiển thị bảng điều khiển báo cáo trực quan cho quản lý
deactivate UI_Dash
@enduml
"""

# UC15
sequences['sequence_uc15_quan_tri_rbac_cai_dat.puml'] = """@startuml
""" + header_sequence + """
title BIỂU ĐỒ TUẦN TỰ: UC15 - QUẢN LÝ NGƯỜI DÙNG, RBAC VÀ CẤU HÌNH RẠP

actor "Quản trị viên" as Admin
boundary "Giao diện Quản trị" as UI_Admin
control "Bộ điều khiển Quản trị" as Ctrl
entity "Tài khoản người dùng" as ModelUser
database "Cơ sở dữ liệu" as DB

Admin -> UI_Admin: 1. Chọn tài khoản nhân viên và chọn vai trò mới cần cấp
activate UI_Admin

Admin -> UI_Admin: 2. Nhấn nút "Cập nhật phân quyền"
UI_Admin -> Ctrl: 3. Gửi yêu cầu thay đổi vai trò của người dùng
activate Ctrl

Ctrl -> ModelUser: 4. Yêu cầu cập nhật quyền hạn của tài khoản
activate ModelUser

ModelUser -> DB: 5. Cập nhật vai trò mới và ghi nhật ký giám sát vào CSDL
activate DB
DB --> ModelUser: Xác nhận cập nhật quyền hạn thành công
deactivate DB

ModelUser --> Ctrl: Thông báo hoàn tất phân quyền người dùng
deactivate ModelUser

Ctrl --> UI_Admin: 6. Phản hồi phân quyền tài khoản thành công
deactivate Ctrl

UI_Admin --> Admin: 7. Cập nhật nhãn vai trò mới của người dùng trên danh sách
deactivate UI_Admin
@enduml
"""

# ==============================================================================
# THỰC THI GHI FILE VÀ BIÊN DỊCH BẰNG PLANTUML
# ==============================================================================

print("1. Đang ghi các tệp PUML Activity Diagrams...")
for filename, content in activities.items():
    fpath = os.path.join(puml_dir, filename)
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)

print("2. Đang ghi các tệp PUML Sequence Diagrams...")
for filename, content in sequences.items():
    fpath = os.path.join(puml_dir, filename)
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)

print("3. Đang biên dịch tất cả tệp PUML sang PNG chất lượng cao (limit 8192)...")
cmd = ['java', '-DPLANTUML_LIMIT_SIZE=8192', '-jar', 'plantuml.jar', '-tpng', os.path.join(puml_dir, '*.puml'), '-o', os.path.abspath(img_dir)]
res = subprocess.run(cmd, capture_output=True, text=True)
print("STDOUT:", res.stdout)
if res.stderr:
    print("STDERR:", res.stderr)

# Kiểm tra kích thước và xác nhận không có ảnh nào bị chạm ngưỡng 4096
print("\n4. KIỂM TRA ĐỘ RỘNG VÀ ĐỘ NÉT CÁC BIỂU ĐỒ TUẦN TỰ:")
all_ok = True
for filename in sequences.keys():
    png_name = filename.replace('.puml', '.png')
    png_path = os.path.join(img_dir, png_name)
    if os.path.exists(png_path):
        im = Image.open(png_path)
        w, h = im.size
        status = "OK (Đầy đủ lifeline)" if w < 4096 else "⚠️ CẢNH BÁO: CHẠM NGƯỠNG 4096!"
        print(f"  - {png_name:42}: {w}x{h} px -> {status}")
        if w >= 4096:
            all_ok = False
    else:
        print(f"  ❌ Không tìm thấy: {png_name}")
        all_ok = False

if all_ok:
    print("\n🎉 TẤT CẢ 15 BIỂU ĐỒ TUẦN TỰ ĐÃ ĐƯỢC FIX LỖI THÀNH CÔNG VÀ KHÔNG BỊ TRUNCATE!")
else:
    print("\n⚠️ VẪN CÒN BIỂU ĐỒ BỊ CHẠM NGƯỠNG, CẦN ĐIỀU CHỈNH THÊM!")
