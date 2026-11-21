# ==============================================================================
# SCRIPT CẬP NHẬT 16 ẢNH BIỂU ĐỒ DRAW.IO VÀO FILE BTL_DACN_CNPM_3.DOCX
# ==============================================================================
import os
import zipfile
import shutil

doc_path = "BTL_DACN_CNPM_3.docx"
temp_docx = "BTL_DACN_CNPM_3_temp.docx"

replacements = {
    'word/media/image48.png': 'report_assets/drawio_exported_images/drawio_uc_tong_quat.png',
    'word/media/image49.png': 'report_assets/drawio_exported_images/drawio_uc01_dang_nhap.png',
    'word/media/image50.png': 'report_assets/drawio_exported_images/drawio_uc02_dang_ky.png',
    'word/media/image51.png': 'report_assets/drawio_exported_images/drawio_uc03_ho_so_doi_mk.png',
    'word/media/image52.png': 'report_assets/drawio_exported_images/drawio_uc04_tra_cuu_phim.png',
    'word/media/image53.png': 'report_assets/drawio_exported_images/drawio_uc05_dat_ve_chon_ghe.png',
    'word/media/image54.png': 'report_assets/drawio_exported_images/drawio_uc06_gio_ve_thanh_toan.png',
    'word/media/image55.png': 'report_assets/drawio_exported_images/drawio_uc07_ban_ve_pos.png',
    'word/media/image56.png': 'report_assets/drawio_exported_images/drawio_uc08_soat_ve_qr.png',
    'word/media/image57.png': 'report_assets/drawio_exported_images/drawio_uc09_quan_ly_phim.png',
    'word/media/image58.png': 'report_assets/drawio_exported_images/drawio_uc10_phong_chieu_ghe.png',
    'word/media/image59.png': 'report_assets/drawio_exported_images/drawio_uc11_lap_suat_chieu.png',
    'word/media/image60.png': 'report_assets/drawio_exported_images/drawio_uc12_gia_ve_combo.png',
    'word/media/image61.png': 'report_assets/drawio_exported_images/drawio_uc13_thong_ke_doanh_thu.png',
    'word/media/image62.png': 'report_assets/drawio_exported_images/drawio_uc14_quan_ly_nguoi_dung.png',
    'word/media/image63.png': 'report_assets/drawio_exported_images/drawio_uc15_cau_hinh_audit.png',
}

# Verify all source images exist
for target_name, src_file in replacements.items():
    if not os.path.exists(src_file):
        raise FileNotFoundError(f"Missing source image: {src_file}")

print(f"Bắt đầu thay thế {len(replacements)} ảnh biểu đồ Draw.io vào {doc_path}...")

with zipfile.ZipFile(doc_path, 'r') as zin:
    with zipfile.ZipFile(temp_docx, 'w', compression=zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            if item.filename in replacements:
                src_path = replacements[item.filename]
                with open(src_path, 'rb') as f_img:
                    img_data = f_img.read()
                zout.writestr(item, img_data)
                print(f"✓ Đã cập nhật {item.filename} từ {os.path.basename(src_path)} ({len(img_data)/1024:.1f} KB)")
            else:
                zout.writestr(item, zin.read(item.filename))

# Replace original with updated file
shutil.move(temp_docx, doc_path)
print(f"🎉 Hoàn thành cập nhật ảnh biểu đồ Draw.io vào {doc_path} ({os.path.getsize(doc_path)/(1024*1024):.2f} MB)!")
