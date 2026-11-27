/**
 * Phân quyền truy cập dựa trên vai trò (Role-Based Access Control - RBAC)
 * Các vai trò: 'admin', 'manager', 'staff', 'client'
 */

function formatTime(val) {
    if (!val) return '';
    if (val instanceof Date) {
        const h = String(val.getHours()).padStart(2, '0');
        const m = String(val.getMinutes()).padStart(2, '0');
        return `${h}:${m}`;
    }
    const str = String(val);
    if (str.includes(' ')) {
        const parts = str.split(' ');
        if (parts[1]) return parts[1].substring(0, 5);
    }
    if (str.includes('T')) {
        const timePart = str.split('T')[1];
        return timePart.substring(0, 5);
    }
    return str.substring(0, 5);
}

function formatDate(val) {
    if (!val) return '';
    if (val instanceof Date) {
        const d = String(val.getDate()).padStart(2, '0');
        const m = String(val.getMonth() + 1).padStart(2, '0');
        const y = val.getFullYear();
        return `${d}/${m}/${y}`;
    }
    const str = String(val);
    const datePart = str.split(' ')[0].split('T')[0];
    const parts = datePart.split('-');
    if (parts.length === 3) return `${parts[2]}/${parts[1]}/${parts[0]}`;
    return str;
}

function formatDateTime(val) {
    if (!val) return '';
    return `${formatTime(val)} ${formatDate(val)}`;
}

function formatPrice(val) {
    return Number(val || 0).toLocaleString('vi-VN') + ' đ';
}

const { query, get } = require('../database/db');
const { formatPaymentMethod } = require('../services/paymentConfig');

let cachedCinemas = null;
async function getCinemasMap() {
    if (!cachedCinemas) {
        try {
            const list = await query('SELECT * FROM cinemas');
            cachedCinemas = {};
            list.forEach(c => {
                cachedCinemas[c.id] = c;
            });
        } catch (e) {
            cachedCinemas = {};
        }
    }
    return cachedCinemas;
}

const CLIENT_PORT = Number(process.env.PORT || 3000);
const ADMIN_PORT = Number(process.env.ADMIN_PORT || 3001);

function isAdminPortalRequest(req) {
    const localPort = req.socket ? req.socket.localPort : null;
    if (localPort === ADMIN_PORT) return true;
    const p = req.path || '';
    if (p.startsWith('/admin') || p.startsWith('/manager') || p.startsWith('/staff')) return true;
    if ((req.query && req.query.portal === 'admin') || (req.body && req.body.portal === 'admin')) return true;
    return false;
}

async function checkAuth(req, res, next) {
    // Tương thích ngược với session cũ (req.session.user)
    if (req.session && req.session.user && !req.session.clientUser && !req.session.adminUser) {
        if (['admin', 'manager', 'staff'].includes(req.session.user.role_name)) {
            req.session.adminUser = req.session.user;
        } else {
            req.session.clientUser = req.session.user;
        }
    }

    const portalType = isAdminPortalRequest(req) ? 'admin' : 'client';
    const clientUser = (req.session && req.session.clientUser) || null;
    const adminUser = (req.session && req.session.adminUser) || null;

    // Tách phiên song song HOÀN TOÀN ĐỘC LẬP:
    // - Cổng Admin/Manager/Staff (:3001 hoặc /admin, /manager, /staff) chỉ dùng adminUser
    // - Cổng Khách hàng (:3000) chỉ dùng clientUser (đăng xuất Client sẽ về trạng thái khách vãng lai, KHÔNG hiện thành Admin/Manager)
    const activeUser = portalType === 'admin' ? adminUser : clientUser;

    req.portalType = portalType;
    req.currentUser = activeUser;

    res.locals.portalType = portalType;
    res.locals.currentUser = activeUser;
    res.locals.clientUser = clientUser;
    res.locals.adminUser = adminUser;
    res.locals.clientPort = CLIENT_PORT;
    res.locals.adminPort = ADMIN_PORT;
    res.locals.currentPath = req.path;
    res.locals.formatTime = formatTime;
    res.locals.formatDate = formatDate;
    res.locals.formatDateTime = formatDateTime;
    res.locals.formatPrice = formatPrice;
    res.locals.formatPaymentMethod = formatPaymentMethod;
    res.locals.pendingBookingsCount = 0;

    if (adminUser && ['admin', 'manager'].includes(adminUser.role_name)) {
        try {
            const row = await get(
                "SELECT COUNT(*) as count FROM bookings WHERE payment_status = 'pending' AND booking_status != 'cancelled'"
            );
            res.locals.pendingBookingsCount = row ? Number(row.count || 0) : 0;
        } catch (e) {
            res.locals.pendingBookingsCount = 0;
        }
    }

    const cinemaId = req.cookies.selectedCinemaId || null;
    res.locals.selectedCinemaId = cinemaId;
    if (cinemaId) {
        const map = await getCinemasMap();
        res.locals.selectedCinema = map[cinemaId] || null;
    } else {
        res.locals.selectedCinema = null;
    }
    next();
}

function requireLogin(req, res, next) {
    const activeUser = req.currentUser;
    if (!activeUser) {
        if (req.headers['content-type']?.includes('application/json') || req.xhr) {
            return res.status(401).json({
                success: false,
                requireLogin: true,
                message: 'Vui lòng đăng nhập hoặc đăng ký tài khoản thành viên để đặt vé xem phim!'
            });
        }
        req.session.returnTo = req.originalUrl;
        return res.redirect('/auth/login?redirect=' + encodeURIComponent(req.originalUrl) + '&error=' + encodeURIComponent('Vui lòng đăng nhập hoặc đăng ký tài khoản thành viên để đặt vé xem phim!'));
    }
    next();
}

function requireRole(roles = []) {
    return (req, res, next) => {
        const adminUser = (req.session && req.session.adminUser) || null;
        if (!adminUser) {
            req.session.adminReturnTo = req.originalUrl;
            return res.redirect('/auth/login?portal=admin&redirect=' + encodeURIComponent(req.originalUrl) + '&error=' + encodeURIComponent('Vui lòng đăng nhập tài khoản Quản trị / Quản lý / Nhân viên!'));
        }

        const userRole = adminUser.role_name;
        // Quản trị viên (admin) luôn có quyền truy cập tất cả
        if (userRole === 'admin') {
            return next();
        }

        if (Array.isArray(roles) ? roles.includes(userRole) : roles === userRole) {
            return next();
        }

        return res.status(403).render('auth/forbidden', {
            title: '403 - Không Có Quyền Truy Cập',
            message: 'Tài khoản của bạn không có quyền truy cập khu vực này!'
        });
    };
}

module.exports = {
    checkAuth,
    requireLogin,
    requireRole
};
