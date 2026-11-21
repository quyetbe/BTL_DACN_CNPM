import os
import subprocess
import xml.etree.ElementTree as ET
import re
from PIL import Image

puml_dir = os.path.join('report_assets', 'plantuml')
img_dir = os.path.join('report_assets', 'images')
os.makedirs(puml_dir, exist_ok=True)
os.makedirs(img_dir, exist_ok=True)

header_act = """!pragma max_image_size 8192
skinparam nodesep 80
skinparam ranksep 45
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

# UC01: Đăng ký & Đăng nhập
activities['activity_uc01_dang_nhap.puml'] = f"""@startuml
{header_act}
start
:Giao diện Đăng nhập / Đăng ký;
if (Chọn hình thức xác thực?) then ([Chưa có tài khoản])
  :Chuyển sang form Đăng ký thành viên;
  repeat :Nhập họ tên, email, mật khẩu, SĐT;
    :Nhấn nút "Đăng ký";
  backward: Báo lỗi / Email đã tồn tại;
  repeat while (Thông tin hợp lệ?) is ([Không hợp lệ]) not ([Hợp lệ])
  :Tạo tài khoản và kích hoạt phiên làm việc;
else ([Đã có tài khoản])
  :Mở form Đăng nhập tài khoản;
  repeat :Nhập email và mật khẩu;
    :Nhấn nút "Đăng nhập";
  backward: Sai mật khẩu / Bị khóa;
  repeat while (Xác thực tài khoản?) is ([Thất bại]) not ([Thành công])
  :Cấp mã JWT và khởi tạo phiên làm việc;
endif
stop
@enduml
"""

# UC02: Tra cứu phim (2 nhánh đều hoàn tất xem chi tiết và nối thẳng vào stop)
activities['activity_uc02_tra_cuu_phim.puml'] = f"""@startuml
{header_act}
start
:Giao diện Trang chủ / Danh mục phim;
:Hiển thị danh sách phim đang chiếu và sắp chiếu;
if (Chọn phương thức tra cứu?) then ([Tìm kiếm theo từ khóa])
  repeat :Nhập từ khóa tên phim / đạo diễn;
    :Nhấn nút "Tìm kiếm";
  backward: Không tìm thấy phim phù hợp;
  repeat while (Tìm thấy phim?) is ([Không tìm thấy]) not ([Đã tìm thấy])
  :Hiển thị danh sách phim tìm thấy;
  :Bấm chọn phim để xem chi tiết;
  :Hiển thị thông tin phim, Trailer và Suất chiếu;
else ([Lọc theo tiêu chí])
  :Chọn bộ lọc thể loại, cụm rạp, ngày chiếu;
  :Áp dụng bộ lọc phim;
  :Hiển thị danh sách phim theo bộ lọc;
  :Bấm chọn phim để xem chi tiết;
  :Hiển thị thông tin phim, Trailer và Suất chiếu;
endif
stop
@enduml
"""

# UC03: Xem lịch chiếu theo cụm rạp và ngày
activities['activity_uc03_xem_lich_chieu.puml'] = f"""@startuml
{header_act}
start
:Giao diện Lịch chiếu theo cụm rạp;
:Chọn cụm rạp và ngày chiếu mong muốn;
repeat :Tải danh sách suất chiếu từ hệ thống;
backward: Không có suất chiếu trong ngày / Chọn ngày khác;
repeat while (Có suất chiếu trong ngày?) is ([Không có]) not ([Có suất chiếu])
:Hiển thị lưới khung giờ suất chiếu theo phòng (2D, 3D, IMAX);
:Khách hàng click chọn khung giờ suất chiếu cụ thể;
:Chuyển hướng sang màn hình Chọn ghế và Đặt vé;
stop
@enduml
"""

# UC04: Chọn ghế & Khóa giữ tạm
activities['activity_uc04_chon_ghe_khoa_ghe.puml'] = f"""@startuml
{header_act}
start
:Mở sơ đồ ghế của phòng chiếu;
:Hiển thị trực quan trạng thái ghế (Trống, Đang giữ, Đã bán);
repeat :Khách hàng click chọn vị trí ghế mong muốn;
  :Gửi yêu cầu giữ ghế lên hệ thống;
backward: Ghế vừa có người chọn / Vui lòng chọn ghế khác;
repeat while (Ghế còn trống?) is ([Đã bị chiếm]) not ([Còn trống])
:Khóa giữ ghế tạm thời trong 5 phút trên Redis;
:Cập nhật trạng thái ghế sang "Đang giữ chỗ" trên toàn hệ thống;
:Hiển thị đồng hồ đếm ngược 5 phút thanh toán;
stop
@enduml
"""

# UC05: Chọn combo bắp nước F&B (2 nhánh nối thẳng vào stop)
activities['activity_uc05_chon_combo_fb.puml'] = f"""@startuml
{header_act}
start
:Giao diện Chọn dịch vụ bắp nước (F&B);
if (Khách có nhu cầu bắp nước?) then ([Có nhu cầu])
  :Hiển thị thực đơn Combo bắp nước và giá niêm yết;
  :Chọn loại combo và số lượng mong muốn;
  :Cộng dồn combo vào đơn đặt vé;
  :Chuyển sang màn hình Xác nhận và Thanh toán;
else ([Bỏ qua])
  :Bỏ qua bước chọn dịch vụ bắp nước;
  :Chuyển sang màn hình Xác nhận và Thanh toán;
endif
stop
@enduml
"""

# UC06: Đặt vé & Thanh toán
activities['activity_uc06_dat_ve_thanh_toan.puml'] = f"""@startuml
{header_act}
start
:Giao diện Xác nhận đơn đặt vé;
:Kiểm tra lại thông tin vé, ghế, combo và tổng tiền;
:Chọn cổng thanh toán điện tử (VNPay / MoMo / Thẻ ngân hàng);
repeat :Khách quét mã QR / Nhập thông tin thanh toán;
  :Cổng thanh toán xử lý giao dịch;
backward: Giao dịch thất bại / Quá hạn 5 phút (Nhả ghế về trống);
repeat while (Thanh toán thành công?) is ([Thất bại / Quá hạn]) not ([Thành công])
:Ghi nhận đơn đặt vé chính thức vào CSDL;
:Sinh mã vé điện tử QR Code bảo mật;
:Gửi email xác nhận kèm vé điện tử cho khách hàng;
stop
@enduml
"""

# UC07: Quản lý vé cá nhân & Tải QR
activities['activity_uc07_quan_ly_ve_qr.puml'] = f"""@startuml
{header_act}
start
:Mở giao diện Lịch sử đặt vé cá nhân;
:Hiển thị danh sách vé đã mua của tài khoản;
:Khách hàng chọn một đơn vé trong danh sách;
if (Chọn tác vụ xử lý vé?) then ([Xem và Tải vé QR])
  :Hiển thị chi tiết vé, mã ghế và hình ảnh QR Code;
  :Nhấn nút "Tải vé QR / Lưu hình ảnh";
  :Lưu file ảnh vé về thiết bị cá nhân;
else ([Hủy đơn vé])
  :Kiểm tra điều kiện thời gian hủy (trước giờ chiếu tối thiểu 60p);
  repeat :Chọn lý do hủy vé và xác nhận hủy;
  backward: Vi phạm thời gian hủy vé / Không thể hủy;
  repeat while (Hợp lệ hủy vé?) is ([Không hợp lệ]) not ([Hợp lệ])
  :Đổi trạng thái vé sang "Đã hủy" và nhả ghế về trống;
  :Gửi yêu cầu hoàn tiền tự động theo quy định;
endif
stop
@enduml
"""

# UC08: Bán vé tại quầy POS (tuần tự hóa bước hỏi combo bắp nước để loại bỏ hoàn toàn hình thoi gom luồng)
activities['activity_uc08_ban_ve_pos.puml'] = f"""@startuml
{header_act}
start
:Màn hình POS dành cho Thu ngân quầy vé;
:Thu ngân chọn phim, ngày chiếu và suất chiếu theo yêu cầu khách;
:Mở sơ đồ phòng chiếu và chọn ghế cho khách;
:Hỏi nhu cầu bắp nước và thêm combo vào đơn hàng (nếu có);
:Xác nhận tổng tiền thanh toán với khách hàng;
repeat :Chọn hình thức thanh toán (Tiền mặt / Quẹt thẻ / QR POS);
  :Thu ngân thực hiện giao dịch thu tiền;
backward: Giao dịch thẻ lỗi / Khách đổi ý;
repeat while (Thu tiền thành công?) is ([Chưa hoàn tất]) not ([Hoàn tất])
:Hệ thống ghi nhận đơn vé POS và khóa ghế chính thức;
:Máy in nhiệt POS tự động in vé xem phim cứng;
:Thu ngân trao vé cứng và hóa đơn cho khách hàng;
stop
@enduml
"""

# UC09: Quét mã QR soát vé
activities['activity_uc09_quet_ma_qr_camera.puml'] = f"""@startuml
{header_act}
start
:Ứng dụng Soát vé cầm tay của nhân viên soát vé;
repeat :Nhân viên hướng camera quét mã QR trên vé của khách;
  :Hệ thống giải mã token và đối chiếu vé trong CSDL;
backward: Mã QR sai định dạng / Không thể quét;
repeat while (Quét mã thành công?) is ([Lỗi đọc mã]) not ([Đọc mã thành công])
if (Kiểm tra tính hợp lệ của vé?) then ([Hợp lệ])
  :Kiểm tra trạng thái vé: Chưa soát vé (unused);
  :Đổi trạng thái vé sang "Đã soát vé (used)";
  :Màn hình hiện màu XANH và phát âm thanh "Hợp lệ";
  :Nhân viên mời khách vào phòng chiếu;
else ([Không hợp lệ / Đã dùng])
  :Màn hình hiện màu ĐỎ và phát âm báo cảnh báo gian lận;
  :Hiển thị thời gian vé đã từng quét trước đó;
  :Nhân viên từ chối cho khách vào phòng;
endif
stop
@enduml
"""

# UC10: Đối soát vé và phòng chống gian lận
activities['activity_uc10_doi_soat_ve_gian_lan.puml'] = f"""@startuml
{header_act}
start
:Màn hình Giám sát đối soát vé của Quản lý;
:Tải nhật ký quét vé thời gian thực của các phòng chiếu;
:Hệ thống chạy thuật toán phát hiện gian lận;
if (Phát hiện dấu hiệu bất thường?) then ([Có gian lận])
  :Hiển thị cảnh báo vé giả mạo hoặc vé quét trùng lặp;
  :Trích xuất hình ảnh camera tại cửa soát vé tương ứng;
  :Lập biên bản sự vụ và khóa quyền truy cập của vé;
  :Thông báo cho bộ phận an ninh xử lý;
else ([Bình thường])
  :Ghi nhận đối soát khớp 100% dữ liệu vé và số người;
  :Lưu báo cáo đối soát ca trực vào nhật ký hệ thống;
endif
stop
@enduml
"""

# UC11: Quản lý phim (2 nhánh nối thẳng vào stop)
activities['activity_uc11_quan_ly_phim.puml'] = f"""@startuml
{header_act}
start
:Màn hình Quản lý Phim của Quản trị viên;
:Hiển thị danh sách toàn bộ phim trong hệ thống;
if (Chọn tác vụ quản lý?) then ([Thêm phim mới])
  repeat :Nhập tên phim, thể loại, thời lượng, trailer, áp phích;
    :Nhấn nút "Lưu phim mới";
  backward: Thiếu thông tin bắt buộc / Thời lượng không hợp lệ;
  repeat while (Thông tin hợp lệ?) is ([Không hợp lệ]) not ([Hợp lệ])
  :Thêm bản ghi phim mới vào CSDL;
  :Cập nhật và làm mới danh sách phim hiển thị;
else ([Cập nhật / Ngừng chiếu])
  :Chọn phim cần chỉnh sửa trong danh sách;
  :Cập nhật trạng thái phim (Đang chiếu / Ngừng chiếu / Sắp chiếu);
  :Lưu thông tin thay đổi vào CSDL;
  :Cập nhật và làm mới danh sách phim hiển thị;
endif
stop
@enduml
"""

# UC12: Quản lý phòng chiếu & sơ đồ ghế (2 nhánh nối thẳng vào stop)
activities['activity_uc12_quan_ly_phong_ghe.puml'] = f"""@startuml
{header_act}
start
:Màn hình Cấu hình Phòng chiếu của Quản trị viên;
:Chọn cụm rạp và phòng chiếu cần quản lý;
if (Chọn thao tác cấu hình?) then ([Tạo phòng chiếu mới])
  repeat :Nhập tên phòng, loại máy chiếu (2D/3D/IMAX), số hàng ghế;
    :Thiết lập ma trận ghế (Thường, VIP, Đôi);
  backward: Tên phòng trùng lặp / Số ghế không hợp lệ;
  repeat while (Cấu hình hợp lệ?) is ([Không hợp lệ]) not ([Hợp lệ])
  :Khởi tạo phòng và ma trận ghế vào CSDL;
  :Hiển thị sơ đồ phòng chiếu đã được cập nhật;
else ([Bảo trì / Khóa ghế hỏng])
  :Mở sơ đồ ghế hiện tại của phòng chiếu;
  :Click chọn các vị trí ghế cần bảo trì;
  :Đổi trạng thái ghế sang "Tạm ngưng phục vụ";
  :Lưu trạng thái ghế vào CSDL;
  :Hiển thị sơ đồ phòng chiếu đã được cập nhật;
endif
stop
@enduml
"""

# UC13: Lập lịch chiếu & Kiểm tra xung đột
activities['activity_uc13_lap_suat_chieu_xung_dot.puml'] = f"""@startuml
{header_act}
start
:Màn hình Lập lịch chiếu phim;
:Chọn cụm rạp, phòng chiếu và ngày chiếu cần lập lịch;
repeat :Chọn phim và nhập giờ bắt đầu suất chiếu;
  :Hệ thống tự động tính giờ kết thúc (+15 phút dọn phòng);
  :Hệ thống quét kiểm tra trùng lặp lịch phòng chiếu;
backward: Xung đột khung giờ với suất chiếu khác trong cùng phòng;
repeat while (Kiểm tra xung đột?) is ([Bị trùng lịch]) not ([Không xung đột])
:Xác nhận và lưu suất chiếu mới vào CSDL;
:Đồng bộ lịch chiếu mới lên Website, App và hệ thống POS;
stop
@enduml
"""

# UC14: Thống kê doanh thu & báo cáo
activities['activity_uc14_thong_ke_doanh_thu.puml'] = f"""@startuml
{header_act}
start
:Màn hình Báo cáo Thống kê Doanh thu;
:Chọn khoảng thời gian báo cáo (Ngày / Tuần / Tháng / Năm);
:Chọn tiêu chí phân tích (Theo phim, Theo rạp, Theo loại ghế, F&B);
:Nhấn nút "Tạo báo cáo thống kê";
:Hệ thống tổng hợp và tính toán dữ liệu từ đơn hàng;
:Hiển thị biểu đồ trực quan và bảng số liệu doanh thu chi tiết;
if (Khách hàng muốn xuất file?) then ([Xuất Excel/PDF])
  :Khởi tạo định dạng file Excel hoặc PDF;
  :Tải file báo cáo thống kê về máy tính;
else ([Chỉ xem])
  :Kết thúc xem báo cáo trên hệ thống;
endif
stop
@enduml
"""

# UC15: Quản trị hệ thống & Phân quyền RBAC
activities['activity_uc15_quan_tri_rbac_cai_dat.puml'] = f"""@startuml
{header_act}
start
:Màn hình Quản trị người dùng & Phân quyền (RBAC);
:Tải danh sách tài khoản nhân viên và người dùng hệ thống;
:Chọn một tài khoản nhân viên cần phân quyền;
repeat :Gán vai trò (Quản trị viên / Thu ngân POS / Soát vé / Kế toán);
  :Tùy chỉnh danh sách quyền hạn chi tiết (Xem / Thêm / Sửa / Xóa);
  :Nhấn nút "Cập nhật phân quyền";
backward: Thiếu quyền quản trị tối cao / Thao tác bị từ chối;
repeat while (Xác nhận quyền hợp lệ?) is ([Không hợp lệ]) not ([Hợp lệ])
:Lưu cấu hình phân quyền mới vào CSDL;
:Ghi nhận hành động vào Nhật ký kiểm toán bảo mật (Audit Log);
:Thông báo phân quyền thành công và gửi thông báo cho nhân viên;
stop
@enduml
"""

print(f"1. Ghi {len(activities)} file PUML Activity Diagrams...")
for filename, content in activities.items():
    fpath = os.path.join(puml_dir, filename)
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)

print("2. Biên dịch PUML sang SVG bằng plantuml.jar...")
subprocess.run(['java', '-jar', 'plantuml.jar', '-tsvg', os.path.join(puml_dir, 'activity_uc*.puml')], check=True)

# Hàm loại bỏ merge diamond ở cuối và nối thẳng vào nút tròn stop
def clean_svg_endpoint(svg_path):
    tree = ET.parse(svg_path)
    root = tree.getroot()
    ns = 'http://www.w3.org/2000/svg'
    
    ellipses = root.findall(f'.//{{{ns}}}ellipse')
    if len(ellipses) < 2:
        return False
        
    stop_outer = ellipses[-2]
    stop_inner = ellipses[-1]
    
    rx = float(stop_outer.attrib.get('rx', stop_outer.attrib.get('r', 11)))
    old_stop_cx = float(stop_outer.attrib['cx'])
    old_stop_cy = float(stop_outer.attrib['cy'])
    
    polygons = root.findall(f'.//{{{ns}}}polygon')
    merge_diamonds = []
    for p in polygons:
        fill = p.attrib.get('fill', '').upper()
        if fill in ['#FCF0CC', '#FFF2CC', '#FEFECE']:
            coords = [float(c) for c in re.split(r'[, ]+', p.attrib['points'].strip()) if c]
            xs = coords[0::2]
            ys = coords[1::2]
            cx = (min(xs) + max(xs)) / 2.0
            cy = (min(ys) + max(ys)) / 2.0
            w = max(xs) - min(xs)
            h = max(ys) - min(ys)
            merge_diamonds.append((p, cx, cy, xs, ys, w, h, min(xs), max(xs), min(ys), max(ys)))
            
    if not merge_diamonds:
        return False
        
    # Lấy merge diamond cuối cùng (ở dưới đáy nhất)
    last_merge, mcx, mcy, mxs, mys, mw, mh, min_mx, max_mx, min_my, max_my = max(merge_diamonds, key=lambda item: item[2])
    
    # Chỉ xử lý nếu merge diamond này nằm ngay trước stop node (cách stop cũ không quá 150px)
    if abs(old_stop_cy - mcy) > 150:
        return False
        
    # Di chuyển stop node lên đúng vị trí tâm của merge diamond (mcx, mcy)
    stop_outer.attrib['cx'] = f"{mcx:.4f}"
    stop_outer.attrib['cy'] = f"{mcy:.4f}"
    stop_inner.attrib['cx'] = f"{mcx:.4f}"
    stop_inner.attrib['cy'] = f"{mcy:.4f}"
    
    # Xóa polygon merge diamond này
    for parent in root.iter():
        if last_merge in list(parent):
            parent.remove(last_merge)
            break
            
    target_left_x = mcx - rx
    target_right_x = mcx + rx
    target_top_y = mcy - rx
    
    # Xóa line dọc nối từ merge diamond xuống stop cũ
    lines = root.findall(f'.//{{{ns}}}line')
    for l in list(lines):
        x1, y1 = float(l.attrib.get('x1', 0)), float(l.attrib.get('y1', 0))
        x2, y2 = float(l.attrib.get('x2', 0)), float(l.attrib.get('y2', 0))
        if abs(x1 - mcx) < 8 and abs(x2 - mcx) < 8 and y1 >= mcy - 5 and y2 <= old_stop_cy + 10:
            for parent in root.iter():
                if l in list(parent):
                    parent.remove(l)
                    break
                    
    # Xóa arrowhead đi xuống stop cũ
    arrowheads = [p for p in root.findall(f'.//{{{ns}}}polygon') if p.attrib.get('fill') in ['#333333', '#000000', 'black', '#222222']]
    for a in list(arrowheads):
        coords = [float(c) for c in re.split(r'[, ]+', a.attrib['points'].strip()) if c]
        xs = coords[0::2]
        ys = coords[1::2]
        acx = sum(xs) / len(xs)
        acy = sum(ys) / len(ys)
        if abs(acx - mcx) < 8 and acy > mcy + 10:
            for parent in root.iter():
                if a in list(parent):
                    parent.remove(a)
                    break

    # Kéo dài các đường nối vào sườn của nút stop
    for l in lines:
        x1, y1 = float(l.attrib.get('x1', 0)), float(l.attrib.get('y1', 0))
        x2, y2 = float(l.attrib.get('x2', 0)), float(l.attrib.get('y2', 0))
        
        # Nhánh trái: đi ngang sang phải
        if abs(y2 - mcy) < 6 and abs(x2 - min_mx) < 6 and x1 < x2:
            l.attrib['x2'] = f"{target_left_x:.4f}"
            
        # Nhánh phải: đi ngang sang trái
        elif abs(y2 - mcy) < 6 and abs(x2 - max_mx) < 6 and x1 > x2:
            l.attrib['x2'] = f"{target_right_x:.4f}"
            
        # Nhánh giữa: đi dọc xuống
        elif abs(x2 - mcx) < 6 and abs(y2 - min_my) < 6 and y1 < y2:
            l.attrib['y2'] = f"{target_top_y:.4f}"

    # Dịch chuyển các arrowhead cắm vào viền nút stop
    for a in arrowheads:
        coords = [float(c) for c in re.split(r'[, ]+', a.attrib['points'].strip()) if c]
        xs = coords[0::2]
        ys = coords[1::2]
        
        # Nhánh trái (mũi tên trỏ sang phải)
        max_x = max(xs)
        if abs(max_x - min_mx) < 6 and abs(ys[xs.index(max_x)] - mcy) < 6:
            shift_x = target_left_x - max_x
            new_xs = [x + shift_x for x in xs]
            a.attrib['points'] = ','.join(f"{new_xs[i]:.4f},{ys[i]:.4f}" for i in range(len(xs)))
            
        # Nhánh phải (mũi tên trỏ sang trái)
        min_x = min(xs)
        if abs(min_x - max_mx) < 6 and abs(ys[xs.index(min_x)] - mcy) < 6:
            shift_x = target_right_x - min_x
            new_xs = [x + shift_x for x in xs]
            a.attrib['points'] = ','.join(f"{new_xs[i]:.4f},{ys[i]:.4f}" for i in range(len(xs)))
            
        # Nhánh trên (mũi tên trỏ xuống dưới)
        max_y = max(ys)
        if abs(max_y - min_my) < 6 and abs(xs[ys.index(max_y)] - mcx) < 6:
            shift_y = target_top_y - max_y
            new_ys = [y + shift_y for y in ys]
            a.attrib['points'] = ','.join(f"{xs[i]:.4f},{new_ys[i]:.4f}" for i in range(len(ys)))

    # Cập nhật viewBox và height
    diff_h = old_stop_cy - mcy
    if 'viewBox' in root.attrib:
        parts = [float(v) for v in root.attrib['viewBox'].split()]
        parts[3] = max(50.0, parts[3] - diff_h + 20)
        root.attrib['viewBox'] = " ".join(f"{p:.2f}" for p in parts)
    if 'height' in root.attrib:
        h_str = root.attrib['height']
        if h_str.endswith('px'):
            h_val = float(h_str[:-2])
            root.attrib['height'] = f"{max(50.0, h_val - diff_h + 20):.2f}px"

    tree.write(svg_path, encoding='utf-8', xml_declaration=True)
    return True

print("3. Tối ưu hóa các điểm kết thúc SVG (loại bỏ merge diamond ở cuối)...")
for filename in activities.keys():
    svg_name = filename.replace('.puml', '.svg')
    svg_path = os.path.join(puml_dir, svg_name)
    if os.path.exists(svg_path):
        modified = clean_svg_endpoint(svg_path)
        if modified:
            print(f"  - {svg_name:42}: Đã nối thẳng các nhánh vào nút stop!")
        else:
            print(f"  - {svg_name:42}: Đã là luồng chuẩn nối thẳng vào stop.")

print("\n4. Render toàn bộ 15 SVG sang PNG chất lượng cao qua Edge headless...")
edge_exe = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

for filename in activities.keys():
    svg_name = filename.replace('.puml', '.svg')
    png_name = filename.replace('.puml', '.png')
    svg_path = os.path.abspath(os.path.join(puml_dir, svg_name))
    png_path = os.path.abspath(os.path.join(img_dir, png_name))
    
    tree = ET.parse(svg_path)
    root = tree.getroot()
    vb = root.attrib.get('viewBox', '').split()
    if vb:
        w = int(float(vb[2]))
        h = int(float(vb[3]))
    else:
        w = 1000
        h = 1000

    html_file = os.path.abspath('temp_act_render.html')
    svg_rel = svg_path.replace('\\', '/')
    html_content = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  html, body {{
    margin: 0;
    padding: 25px;
    background: #FFFFFF;
    width: {w + 50}px;
    height: {h + 50}px;
  }}
  img {{
    display: block;
    width: {w}px;
    height: {h}px;
  }}
</style>
</head>
<body>
  <img src="file:///{svg_rel}" />
</body>
</html>
"""
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    temp_png = os.path.abspath('temp_act_raw.png')
    cmd = [
        edge_exe,
        "--headless",
        "--disable-gpu",
        f"--window-size={w + 50},{h + 50}",
        f"--screenshot={temp_png}",
        html_file
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    
    im = Image.open(temp_png)
    bbox = im.getbbox()
    if bbox:
        p = 15
        bbox_padded = (max(0, bbox[0]-p), max(0, bbox[1]-p), min(im.width, bbox[2]+p), min(im.height, bbox[3]+p))
        cropped = im.crop(bbox_padded)
        cropped.save(png_path)
    else:
        im.save(png_path)
        
    w_out, h_out = Image.open(png_path).size
    print(f"  - {png_name:42}: {w_out}x{h_out} px -> OK")

print("\n🎉 HOÀN TẤT BIÊN DỊCH VÀ XUẤT 15 BIỂU ĐỒ HOẠT ĐỘNG CHUẨN MẪU!")
