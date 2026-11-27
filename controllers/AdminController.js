const User = require('../models/User');
const Booking = require('../models/Booking');
const { run } = require('../database/db');
const { getSystemSettings, formatPaymentMethod } = require('../services/paymentConfig');
const { bookingEvents } = require('../services/bookingEvents');

class AdminController {
    // 1. Quản lý Tài khoản & Phân quyền RBAC
    static async users(req, res) {
        try {
            const users = await User.getAll();
            const roles = await User.getAllRoles();

            res.render('admin/users', {
                title: 'Quản Lý Tài Khoản & Phân Quyền (RBAC)',
                users,
                roles,
                error: req.query.error || null,
                success: req.query.success || null
            });
        } catch (err) {
            console.error('Lỗi admin users:', err);
            res.redirect('/');
        }
    }

    static async createUserForm(req, res) {
        try {
            const roles = await User.getAllRoles();
            res.render('admin/user-form', {
                title: 'Tạo Tài Khoản Mới',
                roles,
                user: null,
                isEdit: false
            });
        } catch (err) {
            console.error('Lỗi createUserForm:', err);
            res.redirect('/admin/users');
        }
    }

    static async storeUser(req, res) {
        try {
            const { full_name, email, phone, role_id, password, status } = req.body;
            await User.create({
                full_name,
                email: email.trim().toLowerCase(),
                phone,
                role_id: Number(role_id),
                password,
                status: status || 'active'
            });
            res.redirect('/admin/users?success=' + encodeURIComponent('Tạo tài khoản người dùng thành công!'));
        } catch (err) {
            console.error('Lỗi tạo user:', err);
            res.redirect('/admin/users?error=' + encodeURIComponent('Lỗi tạo tài khoản (có thể email đã trùng)!'));
        }
    }

    static async editUserForm(req, res) {
        try {
            const user = await User.findById(req.params.id);
            const roles = await User.getAllRoles();
            if (!user) {
                return res.redirect('/admin/users?error=' + encodeURIComponent('Không tìm thấy tài khoản!'));
            }
            res.render('admin/user-form', {
                title: `Sửa Quyền & Thông Tin - ${user.full_name}`,
                roles,
                user,
                isEdit: true
            });
        } catch (err) {
            console.error('Lỗi editUserForm:', err);
            res.redirect('/admin/users');
        }
    }

    static async updateUser(req, res) {
        try {
            const { full_name, phone, role_id, status, password } = req.body;
            await User.update(req.params.id, {
                full_name,
                phone,
                role_id: Number(role_id),
                status,
                password
            });
            res.redirect('/admin/users?success=' + encodeURIComponent('Cập nhật tài khoản thành công!'));
        } catch (err) {
            res.redirect('/admin/users?error=' + encodeURIComponent('Lỗi cập nhật: ' + err.message));
        }
    }

    static async toggleStatus(req, res) {
        try {
            const activeAdmin = req.currentUser || req.session.adminUser || req.session.user;
            if (activeAdmin && Number(req.params.id) === Number(activeAdmin.id)) {
                return res.redirect('/admin/users?error=' + encodeURIComponent('Không thể tự khóa tài khoản quản trị đang đăng nhập!'));
            }
            const user = await User.findById(req.params.id);
            if (user) {
                const newStatus = user.status === 'active' ? 'locked' : 'active';
                await User.setStatus(user.id, newStatus);
            }
            res.redirect('/admin/users?success=' + encodeURIComponent(
                user && user.status === 'locked'
                    ? 'Đã mở khóa tài khoản và đặt lại số lần đăng nhập sai!'
                    : 'Đã khóa tài khoản người dùng!'
            ));
        } catch (err) {
            res.redirect('/admin/users');
        }
    }

    static async deleteUser(req, res) {
        try {
            const activeAdmin = req.currentUser || req.session.adminUser || req.session.user;
            if (activeAdmin && Number(req.params.id) === Number(activeAdmin.id)) {
                return res.redirect('/admin/users?error=' + encodeURIComponent('Không thể tự xóa tài khoản quản trị đang đăng nhập!'));
            }
            await User.delete(req.params.id);
            res.redirect('/admin/users?success=' + encodeURIComponent('Đã xóa tài khoản!'));
        } catch (err) {
            res.redirect('/admin/users?error=' + encodeURIComponent('Không thể xóa tài khoản đã có phát sinh giao dịch đặt vé!'));
        }
    }

    // 2. Cài đặt hệ thống & Cấu hình thanh toán
    static async settings(req, res) {
        try {
            const settings = await getSystemSettings();

            res.render('admin/settings', {
                title: 'Cài Đặt Cấu Hình Hệ Thống & Thanh Toán',
                settings,
                error: req.query.error || null,
                success: req.query.success || null
            });
        } catch (err) {
            console.error('Lỗi settings:', err);
            res.redirect('/');
        }
    }

    static async updateSettings(req, res) {
        try {
            const body = req.body;
            const maxAttempts = Math.min(20, Math.max(1, parseInt(body.max_login_attempts, 10) || 5));

            const entries = [
                ['cinema_name', body.cinema_name || 'CINESTAR CINEMA COMPLEX'],
                ['address', body.address || ''],
                ['hotline', body.hotline || ''],
                ['buffer_time', body.buffer_time || '15'],
                ['seat_lock_time', body.seat_lock_time || '5'],
                ['max_login_attempts', String(maxAttempts)],
                // Cấu hình phương thức thanh toán
                ['payment_mbbank_enabled', body.payment_mbbank_enabled ? '1' : '0'],
                ['payment_bank_code', (body.payment_bank_code || 'MB').trim().toUpperCase()],
                ['payment_bank_name', (body.payment_bank_name || 'Ngân hàng TMCP Quân đội (MBBank)').trim()],
                ['payment_bank_account', (body.payment_bank_account || '').trim()],
                ['payment_bank_owner', (body.payment_bank_owner || '').trim().toUpperCase()],
                ['payment_vnpay_enabled', body.payment_vnpay_enabled ? '1' : '0'],
                ['payment_vnpay_tmn', (body.payment_vnpay_tmn || 'CINESTARVN01').trim()],
                ['payment_momo_enabled', body.payment_momo_enabled ? '1' : '0'],
                ['payment_momo_phone', (body.payment_momo_phone || '').trim()],
                ['payment_momo_owner', (body.payment_momo_owner || '').trim().toUpperCase()],
                ['payment_zalopay_enabled', body.payment_zalopay_enabled ? '1' : '0'],
                ['payment_zalopay_phone', (body.payment_zalopay_phone || '').trim()],
                ['payment_zalopay_owner', (body.payment_zalopay_owner || '').trim().toUpperCase()],
                ['payment_card_enabled', body.payment_card_enabled ? '1' : '0'],
                ['payment_cash_enabled', body.payment_cash_enabled ? '1' : '0'],
                ['payment_cash_note', (body.payment_cash_note || '').trim()]
            ];

            for (const [key, value] of entries) {
                await run(
                    'INSERT INTO system_settings (`key`, value) VALUES (?, ?) ON DUPLICATE KEY UPDATE value = VALUES(value)',
                    [key, value]
                );
            }

            res.redirect('/admin/settings?success=' + encodeURIComponent('Lưu cấu hình hệ thống & thanh toán thành công!'));
        } catch (err) {
            res.redirect('/admin/settings?error=' + encodeURIComponent(err.message));
        }
    }

    // 3. Trang Duyệt Đơn Thanh Toán (chỉ lọc các đơn chờ xác nhận tiền)
    static async approvals(req, res) {
        try {
            const bookings = await Booking.getAll('pending');
            const counts = await Booking.getStatusCounts();

            res.render('admin/audit-logs', {
                title: 'Duyệt Đơn Thanh Toán (Admin / Manager)',
                bookings,
                counts,
                statusFilter: 'pending',
                isApprovalMode: true,
                error: req.query.error || null,
                success: req.query.success || null
            });
        } catch (err) {
            console.error('Lỗi approvals:', err);
            res.redirect('/admin/audit-logs');
        }
    }

    // 4. Nhật ký giao dịch toàn hệ thống
    static async auditLogs(req, res) {
        try {
            const statusFilter = ['pending', 'paid', 'cancelled'].includes(req.query.status)
                ? req.query.status
                : 'all';
            const bookings = await Booking.getAll(statusFilter === 'all' ? null : statusFilter);
            const counts = await Booking.getStatusCounts();

            res.render('admin/audit-logs', {
                title: 'Nhật Ký Đơn Hàng & Giao Dịch',
                bookings,
                counts,
                statusFilter,
                isApprovalMode: false,
                error: req.query.error || null,
                success: req.query.success || null
            });
        } catch (err) {
            console.error('Lỗi auditLogs:', err);
            res.redirect('/');
        }
    }

    // API JSON lấy danh sách đơn hàng + bộ đếm thời gian thực (không cần reload trang)
    static async apiBookings(req, res) {
        try {
            const statusFilter = ['pending', 'paid', 'cancelled'].includes(req.query.status)
                ? req.query.status
                : 'all';
            const bookings = await Booking.getAll(statusFilter === 'all' ? null : statusFilter);
            const counts = await Booking.getStatusCounts();

            const enriched = bookings.map(b => ({
                ...b,
                payment_method_label: formatPaymentMethod(b.payment_method)
            }));

            return res.json({
                success: true,
                statusFilter,
                counts,
                bookings: enriched
            });
        } catch (err) {
            return res.status(500).json({ success: false, message: err.message });
        }
    }

    // SSE Stream phát sự kiện đơn hàng mới / đã duyệt ngay lập tức tới giao diện Admin
    static apiBookingsStream(req, res) {
        res.setHeader('Content-Type', 'text/event-stream');
        res.setHeader('Cache-Control', 'no-cache, no-transform');
        res.setHeader('Connection', 'keep-alive');
        res.flushHeaders?.();

        res.write(`data: ${JSON.stringify({ type: 'connected', ts: Date.now() })}\n\n`);

        const onChange = (payload) => {
            res.write(`data: ${JSON.stringify(payload)}\n\n`);
        };
        bookingEvents.on('booking_change', onChange);

        const heartbeat = setInterval(() => {
            res.write(': ping\n\n');
        }, 25000);

        req.on('close', () => {
            clearInterval(heartbeat);
            bookingEvents.off('booking_change', onChange);
        });
    }

    // Xác nhận đã nhận tiền cho đơn hàng (hỗ trợ cả AJAX JSON lẫn form submit thường)
    static async confirmBookingPayment(req, res) {
        const wantsJson = Boolean(req.xhr || (req.headers.accept && req.headers.accept.includes('application/json')));
        try {
            const bookingId = Number(req.params.id);
            const activeAdmin = req.currentUser || req.session.adminUser || req.session.user;
            const adminId = activeAdmin ? activeAdmin.id : null;
            const result = await Booking.confirmPayment(bookingId, adminId);

            if (wantsJson) {
                const counts = await Booking.getStatusCounts();
                return res.status(result.success ? 200 : 400).json({ ...result, counts });
            }

            const returnBase = req.body.return_base === '/admin/approvals' ? '/admin/approvals' : '/admin/audit-logs';
            const returnStatus = req.body.return_status || '';
            const qs = returnBase === '/admin/audit-logs' && returnStatus && returnStatus !== 'all'
                ? `&status=${encodeURIComponent(returnStatus)}`
                : '';

            if (!result.success) {
                return res.redirect(`${returnBase}?error=` + encodeURIComponent(result.message) + qs);
            }
            return res.redirect(`${returnBase}?success=` + encodeURIComponent(result.message) + qs);
        } catch (err) {
            console.error('Lỗi xác nhận thanh toán:', err);
            if (wantsJson) {
                return res.status(500).json({ success: false, message: 'Lỗi xác nhận thanh toán: ' + err.message });
            }
            return res.redirect('/admin/approvals?error=' + encodeURIComponent('Lỗi xác nhận thanh toán: ' + err.message));
        }
    }

    // Từ chối / Hủy đơn hàng chưa thanh toán (hỗ trợ cả AJAX JSON lẫn form submit thường)
    static async cancelBooking(req, res) {
        const wantsJson = Boolean(req.xhr || (req.headers.accept && req.headers.accept.includes('application/json')));
        try {
            const bookingId = Number(req.params.id);
            const activeAdmin = req.currentUser || req.session.adminUser || req.session.user;
            const adminId = activeAdmin ? activeAdmin.id : null;
            const reason = (req.body && req.body.reason) || 'Admin hủy đơn do chưa nhận được thanh toán';
            const result = await Booking.cancelBooking(bookingId, adminId, reason);

            if (wantsJson) {
                const counts = await Booking.getStatusCounts();
                return res.status(result.success ? 200 : 400).json({ ...result, counts });
            }

            const returnBase = req.body.return_base === '/admin/approvals' ? '/admin/approvals' : '/admin/audit-logs';
            const returnStatus = req.body.return_status || '';
            const qs = returnBase === '/admin/audit-logs' && returnStatus && returnStatus !== 'all'
                ? `&status=${encodeURIComponent(returnStatus)}`
                : '';

            if (!result.success) {
                return res.redirect(`${returnBase}?error=` + encodeURIComponent(result.message) + qs);
            }
            return res.redirect(`${returnBase}?success=` + encodeURIComponent(result.message) + qs);
        } catch (err) {
            console.error('Lỗi hủy đơn hàng:', err);
            if (wantsJson) {
                return res.status(500).json({ success: false, message: 'Lỗi hủy đơn hàng: ' + err.message });
            }
            return res.redirect('/admin/approvals?error=' + encodeURIComponent('Lỗi hủy đơn hàng: ' + err.message));
        }
    }
}

module.exports = AdminController;
