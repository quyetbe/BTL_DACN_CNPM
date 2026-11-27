const { query } = require('../database/db');

const DEFAULT_SETTINGS = {
    cinema_name: 'CINESTAR CINEMA COMPLEX',
    address: 'Tòa nhà Landmark, 720A Điện Biên Phủ, Phường 22, Bình Thạnh, TP.HCM',
    hotline: '1900 6017',
    buffer_time: '15',
    seat_lock_time: '5',
    max_login_attempts: '5',
    payment_mbbank_enabled: '1',
    payment_bank_code: 'MB',
    payment_bank_name: 'Ngân hàng TMCP Quân đội (MBBank)',
    payment_bank_account: '033320012005',
    payment_bank_owner: 'NGUYEN MANH QUYET',
    payment_vnpay_enabled: '1',
    payment_vnpay_tmn: 'CINESTARVN01',
    payment_momo_enabled: '1',
    payment_momo_phone: '033320012005',
    payment_momo_owner: 'NGUYEN MANH QUYET',
    payment_zalopay_enabled: '1',
    payment_zalopay_phone: '033320012005',
    payment_zalopay_owner: 'NGUYEN MANH QUYET',
    payment_card_enabled: '1',
    payment_cash_enabled: '1',
    payment_cash_note: 'Vui lòng đến quầy vé trước giờ chiếu ít nhất 15 phút và xuất trình mã đơn để thanh toán tiền mặt và kích hoạt vé.'
};

const PAYMENT_METHOD_LABELS = {
    mbbank_qr: 'Chuyển khoản VietQR',
    vnpay: 'Cổng VNPAY / ATM Nội Địa',
    momo: 'Ví Điện Tử MoMo',
    zalopay: 'Ví Điện Tử ZaloPay',
    card: 'Thẻ Quốc Tế / ATM (Visa, MasterCard)',
    cash: 'Tiền mặt tại quầy'
};

// Các cổng thanh toán tự động (xác nhận thanh toán ngay lập tức, không cần Admin duyệt thủ công)
const AUTO_PAYMENT_METHODS = ['vnpay', 'momo', 'zalopay'];

function isAutoPaymentMethod(method) {
    return AUTO_PAYMENT_METHODS.includes(String(method || '').toLowerCase());
}

async function getSystemSettings() {
    try {
        const rows = await query('SELECT `key`, value FROM system_settings');
        const settings = { ...DEFAULT_SETTINGS };
        rows.forEach(r => {
            if (r && r.key) {
                settings[r.key] = r.value;
            }
        });
        return settings;
    } catch (err) {
        console.error('Lỗi đọc system_settings:', err.message);
        return { ...DEFAULT_SETTINGS };
    }
}

async function getMaxLoginAttempts() {
    const settings = await getSystemSettings();
    const parsed = parseInt(settings.max_login_attempts, 10);
    return Number.isFinite(parsed) && parsed > 0 ? parsed : 5;
}

function getEnabledPaymentMethods(settings) {
    const s = { ...DEFAULT_SETTINGS, ...(settings || {}) };
    const methods = [
        {
            id: 'vnpay',
            enabled: s.payment_vnpay_enabled !== '0',
            isAuto: true,
            badge: 'VNPAY',
            title: 'Cổng Thanh Toán VNPAY-QR / ATM Nội Địa',
            subtitle: `Thanh toán tự động tức thì • Mã điểm: ${s.payment_vnpay_tmn} • 40+ ngân hàng`
        },
        {
            id: 'momo',
            enabled: s.payment_momo_enabled !== '0',
            isAuto: true,
            badge: 'MOMO',
            title: 'Ví Điện Tử MoMo',
            subtitle: `Thanh toán tự động tức thì • SĐT: ${s.payment_momo_phone} • ${s.payment_momo_owner}`
        },
        {
            id: 'zalopay',
            enabled: s.payment_zalopay_enabled !== '0',
            isAuto: true,
            badge: 'ZALOPAY',
            title: 'Ví Điện Tử ZaloPay',
            subtitle: `Thanh toán tự động tức thì • SĐT: ${s.payment_zalopay_phone} • ${s.payment_zalopay_owner}`
        },
        {
            id: 'mbbank_qr',
            enabled: s.payment_mbbank_enabled !== '0',
            isAuto: false,
            badge: `${s.payment_bank_code || 'MB'} QR`,
            title: `Chuyển Khoản Ngân Hàng ${s.payment_bank_name || 'MBBank'} (VietQR 24/7)`,
            subtitle: `STK: ${s.payment_bank_account} • Chủ TK: ${s.payment_bank_owner} • Admin xác nhận`
        },
        {
            id: 'card',
            enabled: s.payment_card_enabled !== '0',
            isAuto: false,
            badge: 'VISA / ATM',
            title: 'Thẻ Quốc Tế / Thẻ ATM (Visa, MasterCard, JCB)',
            subtitle: 'Xác thực 3D-Secure • Admin đối soát và duyệt đơn'
        },
        {
            id: 'cash',
            enabled: s.payment_cash_enabled !== '0',
            isAuto: false,
            badge: 'TIỀN MẶT',
            title: 'Thanh Toán Tiền Mặt Tại Quầy Vé',
            subtitle: 'Giữ ghế trực tuyến và thanh toán tại rạp trước giờ chiếu'
        }
    ];

    const enabledList = methods.filter(m => m.enabled);
    return enabledList.length > 0 ? enabledList : methods;
}

function formatPaymentMethod(method) {
    return PAYMENT_METHOD_LABELS[method] || method || 'Khác';
}

module.exports = {
    DEFAULT_SETTINGS,
    PAYMENT_METHOD_LABELS,
    AUTO_PAYMENT_METHODS,
    isAutoPaymentMethod,
    getSystemSettings,
    getMaxLoginAttempts,
    getEnabledPaymentMethods,
    formatPaymentMethod
};
