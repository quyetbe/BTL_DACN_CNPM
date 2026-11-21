# ==============================================================================
# SCRIPT TẠO FILE DRAWIO CHO ERD DATABASE 3NF (12 BẢNG THỰC TẾ)
# ==============================================================================
import os
import xml.sax.saxutils as saxutils

out_path = os.path.join("report_assets", "drawio", "ERD_database_3NF.drawio")

def esc(txt):
    return saxutils.escape(txt).replace("\n", "&#xa;")

tables_data = [
    # (id, name, x, y, w, h, content)
    ("tbl_roles", "ROLES (Vai trò)", 80, 100, 190, 95,
     "+ id: INT (PK)\n  role_name: VARCHAR(50)\n  description: TEXT"),
    
    ("tbl_users", "USERS (Người dùng)", 80, 260, 210, 155,
     "+ id: INT (PK)\n# role_id: INT (FK)\n  full_name: VARCHAR(100)\n  email: VARCHAR(100)\n  password_hash: VARCHAR(255)\n  phone: VARCHAR(20)\n  status: VARCHAR(20)\n  created_at: DATETIME"),

    ("tbl_movies", "MOVIES (Phim chiếu)", 360, 80, 210, 155,
     "+ id: INT (PK)\n  title: VARCHAR(255)\n  duration: INT\n  genre: VARCHAR(100)\n  release_date: DATE\n  poster_url: VARCHAR(255)\n  trailer_url: VARCHAR(255)\n  status: VARCHAR(20)"),

    ("tbl_rooms", "ROOMS (Phòng chiếu)", 640, 80, 200, 120,
     "+ id: INT (PK)\n  room_name: VARCHAR(50)\n  room_type: VARCHAR(20)\n  total_seats: INT\n  is_active: TINYINT(1)"),

    ("tbl_seats", "SEATS (Ghế ngồi)", 910, 80, 200, 135,
     "+ id: INT (PK)\n# room_id: INT (FK)\n  row_label: VARCHAR(5)\n  seat_number: INT\n  seat_type: VARCHAR(20)\n  is_active: TINYINT(1)"),

    ("tbl_showtimes", "SHOWTIMES (Lịch chiếu)", 500, 300, 220, 150,
     "+ id: INT (PK)\n# movie_id: INT (FK)\n# room_id: INT (FK)\n  start_time: DATETIME\n  end_time: DATETIME\n  price: DECIMAL(10,2)\n  status: VARCHAR(20)"),

    ("tbl_seat_locks", "SEAT_LOCKS (Khóa ghế 5p)", 840, 280, 210, 135,
     "+ id: INT (PK)\n# showtime_id: INT (FK)\n# seat_id: INT (FK)\n# user_id: INT (FK)\n  lock_time: DATETIME\n  expires_at: DATETIME"),

    ("tbl_combos", "COMBOS (Bắp nước F&B)", 80, 480, 200, 115,
     "+ id: INT (PK)\n  combo_name: VARCHAR(100)\n  description: TEXT\n  price: DECIMAL(10,2)\n  is_active: TINYINT(1)"),

    ("tbl_bookings", "BOOKINGS (Đơn đặt vé)", 360, 520, 220, 165,
     "+ id: INT (PK)\n# user_id: INT (FK)\n# showtime_id: INT (FK)\n  total_amount: DECIMAL(10,2)\n  payment_method: VARCHAR(50)\n  payment_status: VARCHAR(50)\n  booking_type: VARCHAR(20)\n  booking_code: VARCHAR(50)\n  created_at: DATETIME"),

    ("tbl_booking_combos", "BOOKING_COMBOS (Chi tiết)", 80, 660, 210, 115,
     "+ id: INT (PK)\n# booking_id: INT (FK)\n# combo_id: INT (FK)\n  quantity: INT\n  unit_price: DECIMAL(10,2)"),

    ("tbl_tickets", "TICKETS (Vé xem phim QR)", 660, 520, 220, 160,
     "+ id: INT (PK)\n# booking_id: INT (FK)\n# seat_id: INT (FK)\n  ticket_code: VARCHAR(50)\n  qr_code_url: VARCHAR(255)\n  price: DECIMAL(10,2)\n  status: VARCHAR(20)\n  checked_in_at: DATETIME"),

    ("tbl_system_settings", "SYSTEM_SETTINGS (Cấu hình)", 950, 480, 210, 115,
     "+ id: INT (PK)\n  setting_key: VARCHAR(50)\n  setting_value: TEXT\n  description: TEXT\n  updated_at: DATETIME")
]

relations_data = [
    # (id, source, target, startLabel, endLabel)
    ("rel_roles_users", "tbl_roles", "tbl_users", "1", "0..*"),
    ("rel_users_bookings", "tbl_users", "tbl_bookings", "1", "0..*"),
    ("rel_users_seatlocks", "tbl_users", "tbl_seat_locks", "1", "0..*"),
    ("rel_movies_showtimes", "tbl_movies", "tbl_showtimes", "1", "0..*"),
    ("rel_rooms_showtimes", "tbl_rooms", "tbl_showtimes", "1", "0..*"),
    ("rel_rooms_seats", "tbl_rooms", "tbl_seats", "1", "1..*"),
    ("rel_showtimes_bookings", "tbl_showtimes", "tbl_bookings", "1", "0..*"),
    ("rel_showtimes_seatlocks", "tbl_showtimes", "tbl_seat_locks", "1", "0..*"),
    ("rel_seats_seatlocks", "tbl_seats", "tbl_seat_locks", "1", "0..*"),
    ("rel_seats_tickets", "tbl_seats", "tbl_tickets", "1", "0..*"),
    ("rel_bookings_tickets", "tbl_bookings", "tbl_tickets", "1", "1..*"),
    ("rel_bookings_bookingcombos", "tbl_bookings", "tbl_booking_combos", "1", "0..*"),
    ("rel_combos_bookingcombos", "tbl_combos", "tbl_booking_combos", "1", "0..*"),
]

def generate_erd_drawio():
    cells = []
    
    # Title
    title_xml = (
        '        <mxCell id="title" value="SƠ ĐỒ QUAN HỆ THỰC THỂ (ERD) CHUẨN HÓA 3NF - CINESTAR CINEMA" '
        'style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;'
        'whiteSpace=wrap;rounded=0;fontStyle=1;fontSize=16;fontFamily=Times New Roman;fontColor=#1e293b;" '
        'vertex="1" parent="1">\n'
        '          <mxGeometry x="300" y="20" width="650" height="40" as="geometry" />\n'
        '        </mxCell>'
    )
    cells.append(title_xml)

    # Tables
    for tid, name, x, y, w, h, content in tables_data:
        tbl_xml = (
            f'        <mxCell id="{tid}" value="{esc(name)}" style="swimlane;fontStyle=1;align=center;'
            f'verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=26;horizontalStack=0;'
            f'resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=1;marginBottom=0;'
            f'strokeColor=#475569;fillColor=#e2e8f0;fontFamily=Times New Roman;fontSize=11;fontColor=#0f172a;" '
            f'vertex="1" parent="1">\n'
            f'          <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" />\n'
            f'        </mxCell>\n'
            f'        <mxCell id="{tid}_fields" value="{esc(content)}" '
            f'style="text;strokeColor=none;fillColor=#ffffff;align=left;verticalAlign=top;spacingLeft=6;'
            f'spacingRight=4;overflow=hidden;rotatable=0;fontFamily=Times New Roman;fontSize=10;'
            f'fontColor=#1e293b;" vertex="1" parent="{tid}">\n'
            f'          <mxGeometry y="26" width="{w}" height="{h-26}" as="geometry" />\n'
            f'        </mxCell>'
        )
        cells.append(tbl_xml)

    # Relations
    for rid, src, tgt, s_lbl, e_lbl in relations_data:
        edge_style = (
            "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;"
            "strokeColor=#334155;strokeWidth=1.2;fontFamily=Times New Roman;fontSize=10;"
            "endArrow=ERmany;startArrow=ERone;"
        )
        edge_xml = (
            f'        <mxCell id="{rid}" style="{edge_style}" edge="1" parent="1" '
            f'source="{src}" target="{tgt}">\n'
            f'          <mxGeometry relative="1" as="geometry" />\n'
            f'        </mxCell>'
        )
        cells.append(edge_xml)

    cells_str = "\n".join(cells)
    full_xml = (
        f'<mxfile host="app.diagrams.net" modified="2026-10-29T16:00:00.000Z" '
        f'agent="Antigravity CineStar" version="24.0.0">\n'
        f'  <diagram id="ERD_Diagram" name="Sơ đồ ERD CSDL Chuẩn 3NF">\n'
        f'    <mxGraphModel dx="1422" dy="794" grid="1" gridSize="10" guides="1" '
        f'tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" '
        f'pageWidth="1250" pageHeight="850" math="0" shadow="0">\n'
        f'      <root>\n'
        f'        <mxCell id="0" />\n'
        f'        <mxCell id="1" parent="0" />\n'
        f'{cells_str}\n'
        f'      </root>\n'
        f'    </mxGraphModel>\n'
        f'  </diagram>\n'
        f'</mxfile>\n'
    )

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(full_xml)
    print(f"✅ Đã tạo thành công file ERD Drawio: {out_path}")

if __name__ == "__main__":
    generate_erd_drawio()
