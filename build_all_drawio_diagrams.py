# ==============================================================================
# SCRIPT TẠO 16 BIỂU ĐỒ USE CASE DẠNG FILE .DRAWIO CHUẨN XML
# Bao gồm:
# - 16 file .drawio riêng biệt trong report_assets/drawio/
# - 1 file Master: report_assets/drawio/CineStar_All_UseCases.drawio (16 Tab)
# ==============================================================================
import os
import xml.sax.saxutils as saxutils

out_dir = os.path.join("report_assets", "drawio")
os.makedirs(out_dir, exist_ok=True)

def escape_txt(txt):
    return saxutils.escape(txt).replace("\n", "&#xa;")

class DrawioDiagram:
    def __init__(self, diagram_id, diagram_name, width=1169, height=827):
        self.diagram_id = diagram_id
        self.diagram_name = diagram_name
        self.width = width
        self.height = height
        self.cells = []
        self.cell_counter = 2

    def add_cell(self, xml_str):
        self.cells.append(xml_str)

    def next_id(self, prefix="c"):
        cid = f"{prefix}_{self.cell_counter}"
        self.cell_counter += 1
        return cid

    def add_boundary(self, cid, title, x, y, w, h):
        esc_title = escape_txt(title)
        style = ("shape=rect;whiteSpace=wrap;html=1;verticalAlign=top;fontStyle=1;"
                 "fontSize=14;fontFamily=Times New Roman;fontColor=#1e293b;"
                 "strokeColor=#475569;strokeWidth=1.5;fillColor=#f8fafc;dashed=1;dashPattern=6 4;")
        xml = (f'        <mxCell id="{cid}" value="{esc_title}" style="{style}" '
               f'vertex="1" parent="1">\n'
               f'          <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" />\n'
               f'        </mxCell>')
        self.add_cell(xml)
        return cid

    def add_actor(self, cid, name, x, y, w=50, h=95):
        esc_name = escape_txt(name)
        style = ("shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;"
                 "outlineConnect=0;strokeColor=#1e293b;fillColor=#ffffff;strokeWidth=1.5;"
                 "fontFamily=Times New Roman;fontSize=12;fontStyle=1;fontColor=#0f172a;")
        xml = (f'        <mxCell id="{cid}" value="{esc_name}" style="{style}" '
               f'vertex="1" parent="1">\n'
               f'          <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" />\n'
               f'        </mxCell>')
        self.add_cell(xml)
        return cid

    def add_device(self, cid, name, x, y, w=70, h=80):
        esc_name = escape_txt(name)
        style = ("shape=rect;whiteSpace=wrap;html=1;verticalAlign=middle;"
                 "strokeColor=#475569;fillColor=#f1f5f9;strokeWidth=1.5;rounded=1;"
                 "fontFamily=Times New Roman;fontSize=11;fontStyle=1;fontColor=#0f172a;")
        xml = (f'        <mxCell id="{cid}" value="{esc_name}" style="{style}" '
               f'vertex="1" parent="1">\n'
               f'          <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" />\n'
               f'        </mxCell>')
        self.add_cell(xml)
        return cid

    def add_uc(self, cid, title, x, y, w=220, h=60, kind="normal"):
        esc_title = escape_txt(title)
        if kind == "main":
            style = ("ellipse;whiteSpace=wrap;html=1;fontFamily=Times New Roman;"
                     "fontSize=12;fontStyle=1;fontColor=#78350f;strokeColor=#d97706;"
                     "strokeWidth=1.6;fillColor=#fef3c7;")
        elif kind == "error":
            style = ("ellipse;whiteSpace=wrap;html=1;fontFamily=Times New Roman;"
                     "fontSize=12;fontColor=#9f1239;strokeColor=#f43f5e;"
                     "strokeWidth=1.2;fillColor=#fff1f2;")
        elif kind == "header":
            style = ("ellipse;whiteSpace=wrap;html=1;fontFamily=Times New Roman;"
                     "fontSize=12;fontStyle=1;fontColor=#78350f;strokeColor=#d97706;"
                     "strokeWidth=1.6;fillColor=#fef3c7;")
        else:
            style = ("ellipse;whiteSpace=wrap;html=1;fontFamily=Times New Roman;"
                     "fontSize=12;fontColor=#1e293b;strokeColor=#475569;"
                     "strokeWidth=1.2;fillColor=#ffffff;")
        xml = (f'        <mxCell id="{cid}" value="{esc_title}" style="{style}" '
               f'vertex="1" parent="1">\n'
               f'          <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" />\n'
               f'        </mxCell>')
        self.add_cell(xml)
        return cid

    def add_assoc(self, cid, source_id, target_id, exit_entry=None):
        extra = ""
        if exit_entry:
            extra = f'exitX={exit_entry[0]};exitY={exit_entry[1]};entryX={exit_entry[2]};entryY={exit_entry[3]};'
        style = f"endArrow=none;html=1;strokeColor=#334155;strokeWidth=1.5;{extra}"
        xml = (f'        <mxCell id="{cid}" style="{style}" edge="1" parent="1" '
               f'source="{source_id}" target="{target_id}">\n'
               f'          <mxGeometry relative="1" as="geometry" />\n'
               f'        </mxCell>')
        self.add_cell(xml)
        return cid

    def add_include(self, cid, source_id, target_id, exit_entry=None):
        extra = ""
        if exit_entry:
            extra = f'exitX={exit_entry[0]};exitY={exit_entry[1]};entryX={exit_entry[2]};entryY={exit_entry[3]};'
        style = (f"html=1;verticalAlign=bottom;labelBackgroundColor=#ffffff;"
                 f"endArrow=open;dashed=1;endSize=8;strokeColor=#0284c7;strokeWidth=1.2;"
                 f"fontFamily=Times New Roman;fontSize=11;fontStyle=2;fontColor=#0369a1;{extra}")
        val = "&amp;lt;&amp;lt;include&amp;gt;&amp;gt;"
        xml = (f'        <mxCell id="{cid}" value="{val}" style="{style}" edge="1" parent="1" '
               f'source="{source_id}" target="{target_id}">\n'
               f'          <mxGeometry relative="1" as="geometry" />\n'
               f'        </mxCell>')
        self.add_cell(xml)
        return cid

    def add_extend(self, cid, source_id, target_id, exit_entry=None):
        extra = ""
        if exit_entry:
            extra = f'exitX={exit_entry[0]};exitY={exit_entry[1]};entryX={exit_entry[2]};entryY={exit_entry[3]};'
        style = (f"html=1;verticalAlign=bottom;labelBackgroundColor=#ffffff;"
                 f"endArrow=open;dashed=1;endSize=8;strokeColor=#be123c;strokeWidth=1.2;"
                 f"fontFamily=Times New Roman;fontSize=11;fontStyle=2;fontColor=#be123c;{extra}")
        val = "&amp;lt;&amp;lt;extend&amp;gt;&amp;gt;"
        xml = (f'        <mxCell id="{cid}" value="{val}" style="{style}" edge="1" parent="1" '
               f'source="{source_id}" target="{target_id}">\n'
               f'          <mxGeometry relative="1" as="geometry" />\n'
               f'        </mxCell>')
        self.add_cell(xml)
        return cid

    def add_inherit(self, cid, source_id, target_id, label="Kế thừa quyền"):
        style = ("endArrow=block;endFill=0;endSize=10;html=1;strokeColor=#1e293b;"
                 "strokeWidth=1.5;fontFamily=Times New Roman;fontSize=11;fontStyle=0;fontColor=#1e293b;"
                 "labelBackgroundColor=#ffffff;verticalAlign=middle;")
        esc_label = escape_txt(label)
        xml = (f'        <mxCell id="{cid}" value="{esc_label}" style="{style}" edge="1" parent="1" '
               f'source="{source_id}" target="{target_id}">\n'
               f'          <mxGeometry relative="1" as="geometry" />\n'
               f'        </mxCell>')
        self.add_cell(xml)
        return cid

    def get_diagram_xml(self):
        cells_xml = "\n".join(self.cells)
        esc_name = escape_txt(self.diagram_name)
        return (f'  <diagram id="{self.diagram_id}" name="{esc_name}">\n'
                f'    <mxGraphModel dx="1422" dy="794" grid="1" gridSize="10" guides="1" '
                f'tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" '
                f'pageWidth="{self.width}" pageHeight="{self.height}" math="0" shadow="0">\n'
                f'      <root>\n'
                f'        <mxCell id="0" />\n'
                f'        <mxCell id="1" parent="0" />\n'
                f'{cells_xml}\n'
                f'      </root>\n'
                f'    </mxGraphModel>\n'
                f'  </diagram>')

    def save_standalone(self, filepath):
        diag_xml = self.get_diagram_xml()
        full_xml = (f'<mxfile host="app.diagrams.net" modified="2026-10-29T16:00:00.000Z" '
                    f'agent="Antigravity CineStar" version="24.0.0">\n'
                    f'{diag_xml}\n'
                    f'</mxfile>\n')
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(full_xml)
        print(f"Created standalone .drawio: {filepath}")

# ==============================================================================
# 0. USE CASE TỔNG QUÁT (15 USE CASES)
# ==============================================================================
def make_general_diagram():
    d = DrawioDiagram("UC_General", "Hình 4.2 - Use Case Tổng Quát", width=1600, height=1150)
    d.add_boundary("box_sys", "HỆ THỐNG ĐẶT VÉ VÀ QUẢN LÝ SUẤT CHIẾU CINESTAR CINEMA", 320, 50, 880, 1000)

    # Actors
    d.add_actor("act_client", "Khách hàng\n(Client)", 120, 240, 60, 110)
    d.add_actor("act_staff", "Nhân viên quầy\n(Staff)", 120, 700, 60, 110)
    d.add_actor("act_mgr", "Quản lý rạp\n(Manager)", 1320, 240, 60, 110)
    d.add_actor("act_admin", "Quản trị viên\n(Admin)", 1320, 700, 60, 110)

    # Kế thừa vai trò Admin -> Manager
    d.add_inherit("inh_adm_mgr", "act_admin", "act_mgr", "Kế thừa\nquyền")

    # Center UCs (Dùng chung)
    d.add_uc("uc01", "UC01. Đăng nhập hệ thống", 630, 100, 260, 55, kind="header")
    d.add_uc("uc02", "UC02. Đăng ký tài khoản", 630, 175, 260, 55, kind="header")
    d.add_uc("uc03", "UC03. Quản lý thông tin tài khoản", 630, 250, 260, 55, kind="header")

    # Left Column (Client & Staff)
    d.add_uc("uc04", "UC04. Tra cứu phim & Lịch chiếu", 370, 360, 260, 55)
    d.add_uc("uc05", "UC05. Đặt vé trực tuyến & Chọn ghế (5p)", 370, 440, 260, 55)
    d.add_uc("uc06", "UC06. Quản lý giỏ vé & Chọn combo F&B", 370, 520, 260, 55)
    d.add_uc("uc07", "UC07. Bán vé trực tiếp tại quầy POS", 370, 670, 260, 55)
    d.add_uc("uc08", "UC08. Soát vé QR & Cảnh báo gian lận", 370, 770, 260, 55)

    # Right Column (Manager & Admin)
    d.add_uc("uc09", "UC09. Quản lý danh mục phim", 890, 360, 260, 55)
    d.add_uc("uc10", "UC10. Quản lý phòng & Cấu hình ghế", 890, 440, 260, 55)
    d.add_uc("uc11", "UC11. Lập suất chiếu (Chống trùng)", 890, 520, 260, 55)
    d.add_uc("uc12", "UC12. Quản lý bảng giá & Combo F&B", 890, 600, 260, 55)
    d.add_uc("uc13", "UC13. Báo cáo doanh thu & Lấp đầy", 890, 680, 260, 55)
    d.add_uc("uc14", "UC14. Quản lý người dùng & RBAC", 890, 790, 260, 55)
    d.add_uc("uc15", "UC15. Cài đặt hệ thống & Audit Logs", 890, 880, 260, 55)

    # Client associations
    d.add_assoc("e_c_01", "act_client", "uc01")
    d.add_assoc("e_c_02", "act_client", "uc02")
    d.add_assoc("e_c_03", "act_client", "uc03")
    d.add_assoc("e_c_04", "act_client", "uc04")
    d.add_assoc("e_c_05", "act_client", "uc05")
    d.add_assoc("e_c_06", "act_client", "uc06")

    # Staff associations
    d.add_assoc("e_s_01", "act_staff", "uc01")
    d.add_assoc("e_s_03", "act_staff", "uc03")
    d.add_assoc("e_s_07", "act_staff", "uc07")
    d.add_assoc("e_s_08", "act_staff", "uc08")

    # Manager associations
    d.add_assoc("e_m_01", "act_mgr", "uc01")
    d.add_assoc("e_m_03", "act_mgr", "uc03")
    d.add_assoc("e_m_09", "act_mgr", "uc09")
    d.add_assoc("e_m_10", "act_mgr", "uc10")
    d.add_assoc("e_m_11", "act_mgr", "uc11")
    d.add_assoc("e_m_12", "act_mgr", "uc12")
    d.add_assoc("e_m_13", "act_mgr", "uc13")

    # Admin associations
    d.add_assoc("e_a_01", "act_admin", "uc01")
    d.add_assoc("e_a_03", "act_admin", "uc03")
    d.add_assoc("e_a_14", "act_admin", "uc14")
    d.add_assoc("e_a_15", "act_admin", "uc15")

    return d

# ==============================================================================
# CÁC HÀM TẠO 15 BIỂU ĐỒ PHÂN RÃ (UC01 - UC15)
# ==============================================================================
def make_uc01():
    d = DrawioDiagram("UC01", "Hình 4.3 - UC01: Đăng nhập")
    d.add_boundary("box", "PHÂN RÃ USE CASE: UC01 - ĐĂNG NHẬP HỆ THỐNG", 240, 40, 820, 580)
    d.add_actor("act", "Người dùng\n(User)", 90, 270, 55, 100)

    d.add_uc("main1", "Đăng nhập\nvào hệ thống", 280, 210, 200, 65, kind="main")
    d.add_uc("main2", "Đăng xuất\nkhỏi hệ thống", 280, 440, 200, 60, kind="main")
    d.add_assoc("e_a_m1", "act", "main1")
    d.add_assoc("e_a_m2", "act", "main2")

    d.add_uc("sub1", "Nhập Email & Mật khẩu\n(Kiểm tra cú pháp)", 600, 80, 240, 55)
    d.add_uc("sub2", "Xác thực BCrypt\nvới CSDL bảng users", 600, 180, 240, 55)
    d.add_uc("sub3", "Khởi tạo Session\n& Điều hướng theo Role", 600, 280, 240, 55)
    d.add_uc("sub4", "Báo lỗi sai Email\nhoặc Mật khẩu", 600, 390, 240, 55, kind="error")
    d.add_uc("sub5", "Từ chối tài khoản bị khóa\n(status = 'locked')", 600, 490, 240, 55, kind="error")

    d.add_include("inc1", "main1", "sub1")
    d.add_include("inc2", "main1", "sub2")
    d.add_include("inc3", "main1", "sub3")
    d.add_extend("ext4", "sub4", "main1")
    d.add_extend("ext5", "sub5", "main1")
    return d

def make_uc02():
    d = DrawioDiagram("UC02", "Hình 4.4 - UC02: Đăng ký tài khoản")
    d.add_boundary("box", "PHÂN RÃ USE CASE: UC02 - ĐĂNG KÝ TÀI KHOẢN", 240, 40, 820, 580)
    d.add_actor("act", "Khách hàng\nvãng lai", 90, 270, 55, 100)

    d.add_uc("main1", "Đăng ký\ntài khoản mới", 280, 270, 200, 65, kind="main")
    d.add_assoc("e_a_m1", "act", "main1")

    d.add_uc("sub1", "Nhập thông tin cá nhân\n(Tên, Email, SĐT, Pass)", 600, 80, 240, 55)
    d.add_uc("sub2", "Kiểm tra hợp lệ dữ liệu\n(Regex Email, SĐT, Pass>=6)", 600, 180, 240, 55)
    d.add_uc("sub3", "Kiểm tra trùng Email\ntrong CSDL users", 600, 280, 240, 55)
    d.add_uc("sub4", "Băm BCrypt & Lưu User\n(role_id=4: Client)", 600, 380, 240, 55)
    d.add_uc("sub5", "Báo lỗi trùng Email\nhoặc Pass không khớp", 600, 490, 240, 55, kind="error")

    d.add_include("inc1", "main1", "sub1")
    d.add_include("inc2", "main1", "sub2")
    d.add_include("inc3", "main1", "sub3")
    d.add_include("inc4", "main1", "sub4")
    d.add_extend("ext5", "sub5", "main1")
    return d

def make_uc03():
    d = DrawioDiagram("UC03", "Hình 4.5 - UC03: Quản lý thông tin tài khoản")
    d.add_boundary("box", "PHÂN RÃ USE CASE: UC03 - QUẢN LÝ THÔNG TIN TÀI KHOẢN", 240, 40, 820, 580)
    d.add_actor("act", "Người dùng\nđã đăng nhập", 90, 270, 55, 100)

    d.add_uc("main1", "Xem hồ sơ\ncá nhân", 280, 180, 200, 60, kind="main")
    d.add_uc("main2", "Đổi mật khẩu\ntài khoản", 280, 420, 200, 60, kind="main")
    d.add_assoc("e_a_m1", "act", "main1")
    d.add_assoc("e_a_m2", "act", "main2")

    d.add_uc("sub1", "Hiển thị thông tin\n(Họ tên, Email, SĐT, Role)", 600, 80, 240, 55)
    d.add_uc("sub2", "Cập nhật thông tin\n(Họ tên & Số điện thoại)", 600, 180, 240, 55)
    d.add_uc("sub3", "Xác thực mật khẩu cũ\nqua BCrypt.compare()", 600, 310, 240, 55)
    d.add_uc("sub4", "Cập nhật mật khẩu mới\n(Băm BCrypt & Lưu CSDL)", 600, 410, 240, 55)
    d.add_uc("sub5", "Báo lỗi khi mật khẩu cũ\nkhông chính xác", 600, 510, 240, 55, kind="error")

    d.add_include("inc1", "main1", "sub1")
    d.add_extend("ext2", "sub2", "main1")
    d.add_include("inc3", "main2", "sub3")
    d.add_include("inc4", "main2", "sub4")
    d.add_extend("ext5", "sub5", "main2")
    return d

def make_uc04():
    d = DrawioDiagram("UC04", "Hình 4.6 - UC04: Tra cứu phim & Lịch chiếu")
    d.add_boundary("box", "PHÂN RÃ USE CASE: UC04 - TRA CỨU PHIM & LỊCH CHIẾU", 240, 40, 820, 580)
    d.add_actor("act", "Khách hàng", 90, 270, 55, 100)

    d.add_uc("main1", "Tra cứu danh mục\nphim chiếu rạp", 280, 180, 200, 60, kind="main")
    d.add_uc("main2", "Xem lịch chiếu\ntheo ngày & rạp", 280, 420, 200, 60, kind="main")
    d.add_assoc("e_a_m1", "act", "main1")
    d.add_assoc("e_a_m2", "act", "main2")

    d.add_uc("sub1", "Lọc phim 'Đang chiếu'\nhoặc 'Sắp chiếu'", 600, 80, 240, 55)
    d.add_uc("sub2", "Xem chi tiết phim\n(Đạo diễn, trailer, thời lượng)", 600, 180, 240, 55)
    d.add_uc("sub3", "Chọn ngày xem phim\n(Lọc suất theo Date)", 600, 310, 240, 55)
    d.add_uc("sub4", "Xem danh sách phòng chiếu\nvà định dạng 2D/3D/IMAX", 600, 410, 240, 55)
    d.add_uc("sub5", "Chuyển sang màn hình\nchọn ghế ngồi (UC05)", 600, 510, 240, 55)

    d.add_include("inc1", "main1", "sub1")
    d.add_extend("ext2", "sub2", "main1")
    d.add_include("inc3", "main2", "sub3")
    d.add_include("inc4", "main2", "sub4")
    d.add_extend("ext5", "sub5", "main2")
    return d

def make_uc05():
    d = DrawioDiagram("UC05", "Hình 4.7 - UC05: Đặt vé & Chọn ghế")
    d.add_boundary("box", "PHÂN RÃ USE CASE: UC05 - ĐẶT VÉ TRỰC TUYẾN & CHỌN GHẾ (KHÓA 5P)", 240, 40, 820, 580)
    d.add_actor("act", "Khách hàng", 90, 270, 55, 100)

    d.add_uc("main1", "Chọn ghế ngồi\ntrực quan theo phòng", 280, 270, 210, 65, kind="main")
    d.add_assoc("e_a_m1", "act", "main1")

    d.add_uc("sub1", "Tải sơ đồ ma trận ghế\n(Trạng thái trống/đã đặt/VIP)", 600, 80, 240, 55)
    d.add_uc("sub2", "Khóa giữ ghế 5 phút\n(Ghi nhận bảng seat_locks)", 600, 180, 240, 55)
    d.add_uc("sub3", "Đếm ngược thời gian giữ ghế\n(Countdown Timer 5:00)", 600, 280, 240, 55)
    d.add_uc("sub4", "Hủy khóa giữ ghế\nkhi hết hạn 5 phút (Release)", 600, 380, 240, 55)
    d.add_uc("sub5", "Cảnh báo ghế vừa được\nkhách khác chọn giữ chỗ", 600, 490, 240, 55, kind="error")

    d.add_include("inc1", "main1", "sub1")
    d.add_include("inc2", "main1", "sub2")
    d.add_include("inc3", "main1", "sub3")
    d.add_extend("ext4", "sub4", "main1")
    d.add_extend("ext5", "sub5", "main1")
    return d

def make_uc06():
    d = DrawioDiagram("UC06", "Hình 4.8 - UC06: Giỏ vé, Combo & Thanh toán", width=1280, height=827)
    d.add_boundary("box", "PHÂN RÃ USE CASE: UC06 - QUẢN LÝ GIỎ VÉ, CHỌN COMBO F&B & THANH TOÁN", 230, 40, 860, 580)
    d.add_actor("act", "Khách hàng", 80, 270, 55, 100)
    d.add_actor("act_pay", "Cổng thanh toán\n(VNPAY / MoMo)", 1130, 270, 60, 100)

    d.add_uc("main1", "Quản lý giỏ vé\n& Chọn combo F&B", 270, 180, 200, 60, kind="main")
    d.add_uc("main2", "Thanh toán đơn hàng\n& Nhận vé điện tử", 270, 420, 200, 60, kind="main")
    d.add_assoc("e_a_m1", "act", "main1")
    d.add_assoc("e_a_m2", "act", "main2")

    d.add_uc("sub1", "Chọn số lượng combo\n(Bắp rang, nước ngọt)", 580, 80, 240, 55)
    d.add_uc("sub2", "Tính tổng tiền đơn hàng\n(Tiền vé + Tiền combo)", 580, 180, 240, 55)
    d.add_uc("sub3", "Chuyển hướng cổng VNPAY/MoMo\n& Nhận IPN Callback", 580, 300, 240, 55)
    d.add_uc("sub4", "Sinh mã QR Code bảo mật\ncho từng vé điện tử", 580, 410, 240, 55)
    d.add_uc("sub5", "Quản lý lịch sử vé\ntrong mục 'Vé của tôi'", 580, 510, 240, 55)

    d.add_extend("ext1", "sub1", "main1")
    d.add_include("inc2", "main1", "sub2")
    d.add_include("inc3", "main2", "sub3")
    d.add_include("inc4", "main2", "sub4")
    d.add_extend("ext5", "sub5", "main2")

    # Connect secondary actor to sub3
    d.add_assoc("e_pay_sub3", "act_pay", "sub3")
    return d

def make_uc07():
    d = DrawioDiagram("UC07", "Hình 4.9 - UC07: Bán vé quầy POS")
    d.add_boundary("box", "PHÂN RÃ USE CASE: UC07 - BÁN VÉ TRỰC TIẾP TẠI QUẦY POS", 240, 40, 820, 580)
    d.add_actor("act", "Nhân viên quầy\n(Staff)", 90, 270, 55, 100)

    d.add_uc("main1", "Bán vé trực tiếp\ntại quầy POS", 280, 270, 210, 65, kind="main")
    d.add_assoc("e_a_m1", "act", "main1")

    d.add_uc("sub1", "Lọc suất chiếu hôm nay\ntheo phim và phòng", 600, 80, 240, 55)
    d.add_uc("sub2", "Chọn vị trí ghế trống\ntrên màn hình POS", 600, 180, 240, 55)
    d.add_uc("sub3", "Bán kèm combo bắp nước\n(Chọn bắp/nước tại quầy)", 600, 280, 240, 55)
    d.add_uc("sub4", "Thu tiền mặt / Quét mã QR\ntại quầy thu ngân", 600, 380, 240, 55)
    d.add_uc("sub5", "In vé nhiệt kèm mã QR\nvà hóa đơn cho khách", 600, 490, 240, 55)

    d.add_include("inc1", "main1", "sub1")
    d.add_include("inc2", "main1", "sub2")
    d.add_extend("ext3", "sub3", "main1")
    d.add_include("inc4", "main1", "sub4")
    d.add_include("inc5", "main1", "sub5")
    return d

def make_uc08():
    d = DrawioDiagram("UC08", "Hình 4.10 - UC08: Soát vé QR & Gian lận", width=1280, height=827)
    d.add_boundary("box", "PHÂN RÃ USE CASE: UC08 - SOÁT VÉ QR & CẢNH BÁO GIAN LẬN", 230, 40, 860, 580)
    d.add_actor("act", "Nhân viên quầy\n(Staff)", 80, 270, 55, 100)
    d.add_device("dev", "Thiết bị quét\nCamera / Scanner", 1120, 100, 80, 70)

    d.add_uc("main1", "Soát vé xem phim\nqua mã QR Code", 270, 200, 200, 60, kind="main")
    d.add_uc("main2", "Xem lịch sử soát vé\ntheo ca trực", 270, 440, 200, 60, kind="main")
    d.add_assoc("e_a_m1", "act", "main1")
    d.add_assoc("e_a_m2", "act", "main2")

    d.add_uc("sub1", "Quét mã QR từ vé giấy\nhoặc điện thoại khách", 580, 80, 240, 55)
    d.add_uc("sub2", "Xác thực mã vé & cập nhật\nstatus = 'checked_in'", 580, 180, 240, 55)
    d.add_uc("sub3", "Cảnh báo gian lận:\nVé đã dùng hoặc sai phòng", 580, 290, 240, 55, kind="error")
    d.add_uc("sub4", "Xem thống kê số vé\nđã soát trong ca trực", 580, 400, 240, 55)
    d.add_uc("sub5", "Đối soát danh sách khách\nđã vào phòng chiếu", 580, 500, 240, 55)

    d.add_include("inc1", "main1", "sub1")
    d.add_include("inc2", "main1", "sub2")
    d.add_extend("ext3", "sub3", "main1")
    d.add_include("inc4", "main2", "sub4")
    d.add_extend("ext5", "sub5", "main2")

    # Connect device to sub1
    d.add_assoc("e_dev_sub1", "dev", "sub1")
    return d

def make_uc09():
    d = DrawioDiagram("UC09", "Hình 4.11 - UC09: Quản lý danh mục phim")
    d.add_boundary("box", "PHÂN RÃ USE CASE: UC09 - QUẢN LÝ DANH MỤC PHIM CHIẾU RẠP", 240, 40, 820, 580)
    d.add_actor("act", "Quản lý rạp\n(Manager)", 90, 270, 55, 100)

    d.add_uc("main1", "Quản lý danh mục\nphim chiếu rạp", 280, 270, 210, 65, kind="main")
    d.add_assoc("e_a_m1", "act", "main1")

    d.add_uc("sub1", "Thêm phim mới vào hệ thống\n(Tiêu đề, thời lượng, thể loại)", 600, 80, 240, 55)
    d.add_uc("sub2", "Tải lên Poster phim\nqua thư viện Multer", 600, 180, 240, 55)
    d.add_uc("sub3", "Nhúng liên kết Video Trailer\nYouTube trực tuyến", 600, 280, 240, 55)
    d.add_uc("sub4", "Cập nhật thông tin & đổi\ntrạng thái (now/coming/ended)", 600, 380, 240, 55)
    d.add_uc("sub5", "Xóa phim khỏi danh mục\n(Ràng buộc toàn vẹn CSDL)", 600, 490, 240, 55, kind="error")

    d.add_include("inc1", "main1", "sub1")
    d.add_include("inc2", "main1", "sub2")
    d.add_include("inc3", "main1", "sub3")
    d.add_include("inc4", "main1", "sub4")
    d.add_extend("ext5", "sub5", "main1")
    return d

def make_uc10():
    d = DrawioDiagram("UC10", "Hình 4.12 - UC10: Quản lý phòng & Ma trận ghế")
    d.add_boundary("box", "PHÂN RÃ USE CASE: UC10 - QUẢN LÝ PHÒNG CHIẾU & CẤU HÌNH GHẾ", 240, 40, 820, 580)
    d.add_actor("act", "Quản lý rạp\n(Manager)", 90, 270, 55, 100)

    d.add_uc("main1", "Quản lý danh sách\nphòng chiếu phim", 280, 180, 200, 60, kind="main")
    d.add_uc("main2", "Cấu hình ma trận ghế\ntheo phòng chiếu", 280, 420, 200, 60, kind="main")
    d.add_assoc("e_a_m1", "act", "main1")
    d.add_assoc("e_a_m2", "act", "main2")

    d.add_uc("sub1", "Thêm/Sửa phòng chiếu\n(Định dạng 2D/3D/IMAX/4DX)", 600, 80, 240, 55)
    d.add_uc("sub2", "Khởi tạo ma trận ghế A-G\nvới 70-150 ghế/phòng", 600, 190, 240, 55)
    d.add_uc("sub3", "Phân loại ghế ngồi:\nThường, VIP, Sweetbox đôi", 600, 300, 240, 55)
    d.add_uc("sub4", "Chuyển trạng thái bảo trì\nghế hỏng (active/maintenance)", 600, 410, 240, 55)
    d.add_uc("sub5", "Kiểm tra ràng buộc phòng\nđang có suất chiếu hoạt động", 600, 510, 240, 55, kind="error")

    d.add_include("inc1", "main1", "sub1")
    d.add_include("inc2", "main2", "sub2")
    d.add_include("inc3", "main2", "sub3")
    d.add_extend("ext4", "sub4", "main2")
    d.add_extend("ext5", "sub5", "main1")
    return d

def make_uc11():
    d = DrawioDiagram("UC11", "Hình 4.13 - UC11: Lập suất chiếu chống trùng")
    d.add_boundary("box", "PHÂN RÃ USE CASE: UC11 - LẬP LỊCH SUẤT CHIẾU & CHỐNG XUNG ĐỘT", 240, 40, 820, 580)
    d.add_actor("act", "Quản lý rạp\n(Manager)", 90, 270, 55, 100)

    d.add_uc("main1", "Lập lịch suất chiếu\ncho các phòng", 280, 270, 210, 65, kind="main")
    d.add_assoc("e_a_m1", "act", "main1")

    d.add_uc("sub1", "Chọn phim, phòng chiếu\nvà ngày/giờ bắt đầu", 600, 80, 240, 55)
    d.add_uc("sub2", "Tự động tính giờ kết thúc\n(start + duration + buffer 15p)", 600, 180, 240, 55)
    d.add_uc("sub3", "Kiểm tra trùng phòng/giờ chiếu\n(Thuật toán ConflictDetector)", 600, 280, 240, 55)
    d.add_uc("sub4", "Lưu suất chiếu mới hợp lệ\nvào bảng showtimes", 600, 380, 240, 55)
    d.add_uc("sub5", "Cảnh báo xung đột thời gian\nvà gợi ý khung giờ trống", 600, 490, 240, 55, kind="error")

    d.add_include("inc1", "main1", "sub1")
    d.add_include("inc2", "main1", "sub2")
    d.add_include("inc3", "main1", "sub3")
    d.add_include("inc4", "main1", "sub4")
    d.add_extend("ext5", "sub5", "main1")
    return d

def make_uc12():
    d = DrawioDiagram("UC12", "Hình 4.14 - UC12: Bảng giá vé & Combo F&B")
    d.add_boundary("box", "PHÂN RÃ USE CASE: UC12 - QUẢN LÝ BẢNG GIÁ VÉ & COMBO F&B", 240, 40, 820, 580)
    d.add_actor("act", "Quản lý rạp\n(Manager)", 90, 270, 55, 100)

    d.add_uc("main1", "Quản lý bảng giá vé\nxem phim", 280, 180, 200, 60, kind="main")
    d.add_uc("main2", "Quản lý danh mục\ncombo bắp nước (F&B)", 280, 420, 200, 60, kind="main")
    d.add_assoc("e_a_m1", "act", "main1")
    d.add_assoc("e_a_m2", "act", "main2")

    d.add_uc("sub1", "Cấu hình giá vé cơ sở\ntheo loại màn hình 2D/3D/IMAX", 600, 80, 240, 55)
    d.add_uc("sub2", "Thiết lập hệ số phụ thu\ncho ghế VIP và Sweetbox", 600, 190, 240, 55)
    d.add_uc("sub3", "Thêm combo bắp nước mới\n(Tên combo, giá bán, mô tả)", 600, 300, 240, 55)
    d.add_uc("sub4", "Cập nhật giá và tồn kho\ncombo bắp rang / nước ngọt", 600, 400, 240, 55)
    d.add_uc("sub5", "Bật/Tắt trạng thái mở bán\ncombo (is_active: 1 / 0)", 600, 500, 240, 55)

    d.add_include("inc1", "main1", "sub1")
    d.add_include("inc2", "main1", "sub2")
    d.add_include("inc3", "main2", "sub3")
    d.add_include("inc4", "main2", "sub4")
    d.add_extend("ext5", "sub5", "main2")
    return d

def make_uc13():
    d = DrawioDiagram("UC13", "Hình 4.15 - UC13: Thống kê doanh thu & Lấp đầy")
    d.add_boundary("box", "PHÂN RÃ USE CASE: UC13 - BÁO CÁO THỐNG KÊ DOANH THU & LẤP ĐẦY", 240, 40, 820, 580)
    d.add_actor("act", "Quản lý rạp\n(Manager)", 90, 270, 55, 100)

    d.add_uc("main1", "Xem báo cáo thống kê\n& Dashboard quản lý", 280, 270, 210, 65, kind="main")
    d.add_assoc("e_a_m1", "act", "main1")

    d.add_uc("sub1", "Xem Dashboard KPI hôm nay\n(Doanh thu, vé bán, suất chiếu)", 600, 80, 240, 55)
    d.add_uc("sub2", "Theo dõi biểu đồ cột 7 ngày\n(Chart.js trực quan doanh thu)", 600, 180, 240, 55)
    d.add_uc("sub3", "Thống kê doanh thu theo phim\n(Doanh thu vé + F&B combo)", 600, 280, 240, 55)
    d.add_uc("sub4", "Tính Tỷ lệ lấp đầy phòng chiếu\n(Occupancy Rate % theo suất)", 600, 380, 240, 55)
    d.add_uc("sub5", "Lọc báo cáo theo khoảng thời gian\n(Hôm nay, 7 ngày, tháng này)", 600, 490, 240, 55)

    d.add_include("inc1", "main1", "sub1")
    d.add_include("inc2", "main1", "sub2")
    d.add_include("inc3", "main1", "sub3")
    d.add_include("inc4", "main1", "sub4")
    d.add_extend("ext5", "sub5", "main1")
    return d

def make_uc14():
    d = DrawioDiagram("UC14", "Hình 4.16 - UC14: Quản lý người dùng & RBAC")
    d.add_boundary("box", "PHÂN RÃ USE CASE: UC14 - QUẢN LÝ NGƯỜI DÙNG & PHÂN QUYỀN RBAC", 240, 40, 820, 580)
    d.add_actor("act", "Quản trị viên\n(Admin)", 90, 270, 55, 100)

    d.add_uc("main1", "Quản lý người dùng\n& Phân quyền RBAC", 280, 270, 210, 65, kind="main")
    d.add_assoc("e_a_m1", "act", "main1")

    d.add_uc("sub1", "Xem danh sách & Lọc người dùng\ntheo vai trò (Admin, Mgr, Staff, Client)", 600, 80, 240, 55)
    d.add_uc("sub2", "Tạo mới tài khoản nhân viên\nhoặc quản lý rạp", 600, 180, 240, 55)
    d.add_uc("sub3", "Phân quyền vai trò RBAC\n(Cập nhật role_id trong users)", 600, 280, 240, 55)
    d.add_uc("sub4", "Khóa / Mở khóa tài khoản\n(Chuyển đổi status: active / locked)", 600, 380, 240, 55)
    d.add_uc("sub5", "Xóa tài khoản người dùng\n(Bảo vệ tài khoản quản trị chính)", 600, 490, 240, 55, kind="error")

    d.add_include("inc1", "main1", "sub1")
    d.add_extend("ext2", "sub2", "main1")
    d.add_include("inc3", "main1", "sub3")
    d.add_extend("ext4", "sub4", "main1")
    d.add_extend("ext5", "sub5", "main1")
    return d

def make_uc15():
    d = DrawioDiagram("UC15", "Hình 4.17 - UC15: Cấu hình tham số & Audit Log")
    d.add_boundary("box", "PHÂN RÃ USE CASE: UC15 - CẤU HÌNH THAM SỐ RẠP & AUDIT LOGS", 240, 40, 820, 580)
    d.add_actor("act", "Quản trị viên\n(Admin)", 90, 270, 55, 100)

    d.add_uc("main1", "Cấu hình tham số\nvận hành rạp", 280, 180, 200, 60, kind="main")
    d.add_uc("main2", "Giám sát nhật ký\nkiểm toán (Audit Log)", 280, 420, 200, 60, kind="main")
    d.add_assoc("e_a_m1", "act", "main1")
    d.add_assoc("e_a_m2", "act", "main2")

    d.add_uc("sub1", "Cấu hình thời gian đệm dọn phòng\n(buffer_minutes = 15 phút)", 600, 80, 240, 55)
    d.add_uc("sub2", "Cấu hình thời gian giữ ghế tạm\n(hold_time = 5 phút)", 600, 180, 240, 55)
    d.add_uc("sub3", "Cập nhật thông tin rạp chiếu\n(Tên rạp, hotline, địa chỉ)", 600, 280, 240, 55)
    d.add_uc("sub4", "Xem lịch sử thao tác hệ thống\n(Timestamp, User, Hành động, IP)", 600, 400, 240, 55)
    d.add_uc("sub5", "Lọc và tra cứu nhật ký\nkiểm toán theo thời gian", 600, 500, 240, 55)

    d.add_include("inc1", "main1", "sub1")
    d.add_include("inc2", "main1", "sub2")
    d.add_include("inc3", "main1", "sub3")
    d.add_include("inc4", "main2", "sub4")
    d.add_extend("ext5", "sub5", "main2")
    return d

# ==============================================================================
# MAIN EXECUTION
# ==============================================================================
def main():
    generators = [
        ("UseCase_tong_quat.drawio", make_general_diagram),
        ("UC01_dang_nhap.drawio", make_uc01),
        ("UC02_dang_ky.drawio", make_uc02),
        ("UC03_ho_so_doi_mk.drawio", make_uc03),
        ("UC04_tra_cuu_phim.drawio", make_uc04),
        ("UC05_dat_ve_chon_ghe.drawio", make_uc05),
        ("UC06_gio_ve_thanh_toan.drawio", make_uc06),
        ("UC07_ban_ve_pos.drawio", make_uc07),
        ("UC08_soat_ve_qr.drawio", make_uc08),
        ("UC09_quan_ly_phim.drawio", make_uc09),
        ("UC10_phong_chieu_ghe.drawio", make_uc10),
        ("UC11_lap_suat_chieu.drawio", make_uc11),
        ("UC12_gia_ve_combo.drawio", make_uc12),
        ("UC13_thong_ke_doanh_thu.drawio", make_uc13),
        ("UC14_quan_ly_nguoi_dung.drawio", make_uc14),
        ("UC15_cau_hinh_audit.drawio", make_uc15),
    ]

    all_diagrams = []

    print("🚀 Bắt đầu tạo 16 file .drawio độc lập...")
    for filename, gen_func in generators:
        diag = gen_func()
        all_diagrams.append(diag)
        path = os.path.join(out_dir, filename)
        diag.save_standalone(path)

    # Tạo Master Project file chứa toàn bộ 16 Tab
    master_path = os.path.join(out_dir, "CineStar_All_UseCases.drawio")
    print(f"\n🚀 Đang tạo file Master tổng hợp 16 Tab: {master_path}...")
    tabs_xml = "\n".join([d.get_diagram_xml() for d in all_diagrams])
    master_xml = (f'<mxfile host="app.diagrams.net" modified="2026-10-29T16:00:00.000Z" '
                  f'agent="Antigravity CineStar Cinema Suite" version="24.0.0">\n'
                  f'{tabs_xml}\n'
                  f'</mxfile>\n')

    with open(master_path, "w", encoding="utf-8") as f:
        f.write(master_xml)
    print(f"✅ Đã tạo thành công Master project: {master_path}")

if __name__ == "__main__":
    main()
