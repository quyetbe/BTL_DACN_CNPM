require('dotenv').config();
const mysql = require('mysql2/promise');
const path = require('path');
const fs = require('fs');

// Cấu hình kết nối MySQL Database
const pool = mysql.createPool({
    host: process.env.DB_HOST || '127.0.0.1',
    user: process.env.DB_USER || 'root',
    password: process.env.DB_PASSWORD || '',
    database: process.env.DB_NAME || 'cinema_db',
    port: Number(process.env.DB_PORT) || 3306,
    waitForConnections: true,
    connectionLimit: 15,
    queueLimit: 0,
    charset: 'utf8mb4',
    multipleStatements: true,
    decimalNumbers: true
});

// Tự động kiểm tra và khởi tạo bảng MySQL nếu chưa có
async function ensureColumn(tableName, columnName, columnDef) {
    const [cols] = await pool.query(
        `SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS
         WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = ? AND COLUMN_NAME = ?`,
        [tableName, columnName]
    );
    if (cols.length === 0) {
        await pool.query(`ALTER TABLE \`${tableName}\` ADD COLUMN ${columnDef}`);
        console.log(`✅ Đã tự động thêm cột ${tableName}.${columnName}`);
    }
}

async function seedDefaultPaymentSettings() {
    const defaults = [
        ['payment_mbbank_enabled', '1', 'Bật thanh toán chuyển khoản VietQR Ngân hàng'],
        ['payment_bank_code', 'MB', 'Mã ngân hàng nhận VietQR (VD: MB, VCB, TCB, BIDV, ACB)'],
        ['payment_bank_name', 'Ngân hàng TMCP Quân đội (MBBank)', 'Tên đầy đủ ngân hàng nhận tiền'],
        ['payment_bank_account', '033320012005', 'Số tài khoản ngân hàng nhận tiền'],
        ['payment_bank_owner', 'NGUYEN MANH QUYET', 'Chủ tài khoản ngân hàng'],
        ['payment_vnpay_enabled', '1', 'Bật cổng thanh toán VNPAY'],
        ['payment_vnpay_tmn', 'CINESTARVN01', 'Mã Terminal VNPAY (TMN Code)'],
        ['payment_momo_enabled', '1', 'Bật ví điện tử MoMo'],
        ['payment_momo_phone', '033320012005', 'Số điện thoại ví MoMo nhận tiền'],
        ['payment_momo_owner', 'NGUYEN MANH QUYET', 'Tên chủ ví MoMo'],
        ['payment_zalopay_enabled', '1', 'Bật ví điện tử ZaloPay'],
        ['payment_zalopay_phone', '033320012005', 'Số điện thoại ví ZaloPay nhận tiền'],
        ['payment_zalopay_owner', 'NGUYEN MANH QUYET', 'Tên chủ ví ZaloPay'],
        ['payment_card_enabled', '1', 'Bật thanh toán thẻ ATM / Visa / MasterCard'],
        ['payment_cash_enabled', '1', 'Bật thanh toán tiền mặt tại quầy'],
        ['payment_cash_note', 'Vui lòng đến quầy vé trước giờ chiếu ít nhất 15 phút và xuất trình mã đơn để thanh toán tiền mặt và kích hoạt vé.', 'Hướng dẫn thanh toán tiền mặt tại quầy'],
        ['max_login_attempts', '5', 'Số lần nhập sai mật khẩu tối đa trước khi tự động khóa tài khoản']
    ];

    for (const [key, value, description] of defaults) {
        await pool.query(
            'INSERT IGNORE INTO system_settings (`key`, value, description) VALUES (?, ?, ?)',
            [key, value, description]
        );
    }
}

async function initDatabase() {
    try {
        const [tables] = await pool.query("SHOW TABLES LIKE 'movies'");
        if (tables.length === 0) {
            console.log('📌 Chưa tìm thấy các bảng trong MySQL cinema_db, đang tự động nạp schema_mysql.sql...');
            const schemaPath = path.join(__dirname, 'schema_mysql.sql');
            if (fs.existsSync(schemaPath)) {
                const schemaSql = fs.readFileSync(schemaPath, 'utf8');
                await pool.query(schemaSql);
                console.log('✅ Khởi tạo cấu trúc bảng MySQL cinema_db thành công!');
            }
        }

        // Migration an toàn cho khóa tài khoản sai mật khẩu & duyệt thanh toán đơn hàng
        await ensureColumn('users', 'failed_login_attempts', 'failed_login_attempts INT NOT NULL DEFAULT 0');
        await ensureColumn('users', 'locked_at', 'locked_at DATETIME NULL');
        await ensureColumn('bookings', 'confirmed_by', 'confirmed_by INT NULL');
        await ensureColumn('bookings', 'confirmed_at', 'confirmed_at DATETIME NULL');
        await ensureColumn('bookings', 'payment_note', 'payment_note VARCHAR(255) NULL');

        await seedDefaultPaymentSettings();
    } catch (err) {
        console.error('⚠️ Lỗi kiểm tra / khởi tạo CSDL MySQL:', err.message);
    }
}

const initReady = initDatabase();

module.exports = {
    pool,
    initReady,
    // Helper lấy danh sách nhiều bản ghi
    async query(sql, params = []) {
        const [rows] = await pool.query(sql, params);
        return rows;
    },
    // Helper lấy 1 bản ghi duy nhất
    async get(sql, params = []) {
        const [rows] = await pool.query(sql, params);
        return rows && rows.length > 0 ? rows[0] : null;
    },
    // Helper thực thi INSERT, UPDATE, DELETE
    async run(sql, params = []) {
        const [result] = await pool.query(sql, params);
        return {
            lastInsertRowid: result.insertId,
            changes: result.affectedRows,
            insertId: result.insertId,
            affectedRows: result.affectedRows
        };
    },
    // Helper chạy raw script hoặc multi-statements
    async exec(sql) {
        return pool.query(sql);
    },
    // Shim tương thích cú pháp db.prepare cho các truy vấn cũ
    db: {
        prepare(sql) {
            return {
                run: async (...params) => {
                    const [res] = await pool.query(sql, params);
                    return {
                        lastInsertRowid: res.insertId,
                        changes: res.affectedRows,
                        insertId: res.insertId,
                        affectedRows: res.affectedRows
                    };
                },
                all: async (...params) => {
                    const [rows] = await pool.query(sql, params);
                    return rows;
                },
                get: async (...params) => {
                    const [rows] = await pool.query(sql, params);
                    return rows && rows.length > 0 ? rows[0] : null;
                }
            };
        }
    }
};
