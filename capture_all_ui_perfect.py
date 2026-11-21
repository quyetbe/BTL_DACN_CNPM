import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image

output_dir = os.path.join('report_assets', 'images')
os.makedirs(output_dir, exist_ok=True)

options = Options()
options.add_argument('--headless=new')
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1440,900')
options.add_argument('--force-device-scale-factor=1.5')

driver = webdriver.Chrome(options=options)

def login_user(email, password):
    driver.get("http://localhost:3000/auth/logout")
    time.sleep(1)
    driver.get("http://localhost:3000/auth/login")
    time.sleep(1)
    driver.execute_script(f"""
        document.getElementById('inputEmail').value = '{email}';
        document.getElementById('inputPassword').value = '{password}';
        document.querySelector('form').submit();
    """)
    time.sleep(2)
    print(f"✅ Đăng nhập: {email} -> {driver.current_url}")

def shot(url, filename, wait_sec=2, execute_js=None):
    driver.get(url)
    time.sleep(wait_sec)
    if execute_js:
        try:
            driver.execute_script(execute_js)
            time.sleep(1)
        except Exception as e:
            print("  JS warning:", e)
            
    filepath = os.path.join(output_dir, filename)
    driver.save_screenshot(filepath)
    im = Image.open(filepath)
    print(f"📸 {filename:30}: {im.size[0]}x{im.size[1]} px tại {url}")

try:
    print("\n--- 1. Phân hệ Khách hàng (Client Portal) ---")
    login_user("client@cinema.com", "client123")
    
    # 1. Trang chủ (đóng modal chọn rạp nếu có)
    shot("http://localhost:3000/", "ui_client_home.png", wait_sec=2, execute_js="""
        var modal = bootstrap.Modal.getInstance(document.getElementById('cinemaModal'));
        if (modal) modal.hide();
        var backdrops = document.querySelectorAll('.modal-backdrop');
        backdrops.forEach(b => b.remove());
    """)
    
    # 2. Chi tiết phim
    shot("http://localhost:3000/movies/1", "ui_client_movie_detail.png", wait_sec=2)
    
    # 3. Sơ đồ chọn ghế ngồi
    shot("http://localhost:3000/booking/seats/1", "ui_client_select_seats.png", wait_sec=2)
    
    # 4. Vé cá nhân & QR Code
    shot("http://localhost:3000/my-tickets", "ui_client_my_tickets.png", wait_sec=2)

    print("\n--- 2. Phân hệ Quản lý (Manager Portal) ---")
    login_user("manager@cinema.com", "manager123")
    
    # 5. Dashboard quản lý
    shot("http://localhost:3000/manager/dashboard", "ui_manager_dashboard.png", wait_sec=3)
    
    # 6. Lập lịch suất chiếu chống xung đột
    shot("http://localhost:3000/manager/showtimes/create", "ui_manager_showtime_create.png", wait_sec=2)
    
    # 7. Quản lý danh mục phim
    shot("http://localhost:3000/manager/movies", "ui_manager_movies.png", wait_sec=2)
    
    # 8. Quản lý phòng chiếu & ma trận ghế
    shot("http://localhost:3000/manager/rooms", "ui_manager_rooms.png", wait_sec=2)

    print("\n--- 3. Phân hệ Nhân viên (Staff Portal) ---")
    login_user("staff@cinema.com", "staff123")
    
    # 9. Bán vé tại quầy POS
    shot("http://localhost:3000/staff/pos", "ui_staff_pos.png", wait_sec=2)
    
    # 10. Soát vé QR qua camera
    shot("http://localhost:3000/staff/scan", "ui_staff_scan_ticket.png", wait_sec=2)

    print("\n--- 4. Phân hệ Quản trị (Admin Portal) ---")
    login_user("admin@cinema.com", "admin123")
    
    # 11. Quản trị người dùng & Phân quyền RBAC
    shot("http://localhost:3000/admin/users", "ui_admin_users.png", wait_sec=2)
    
    # 12. Cấu hình tham số rạp
    shot("http://localhost:3000/admin/settings", "ui_admin_settings.png", wait_sec=2)

    # 13. Nhật ký kiểm toán Audit Logs
    shot("http://localhost:3000/admin/audit-logs", "ui_admin_audit_logs.png", wait_sec=2)

    print("\n🎉 ĐÃ CHỤP THÀNH CÔNG 100% ẢNH GIAO DIỆN WEB THỰC TẾ CỦA HỆ THỐNG!")

except Exception as e:
    print("Lỗi:", e)
finally:
    driver.quit()
