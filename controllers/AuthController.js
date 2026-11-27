const User = require('../models/User');
const { getMaxLoginAttempts } = require('../services/paymentConfig');

function isSafeRedirect(url) {
    if (!url || typeof url !== 'string') return false;
    return url.startsWith('/') && !url.startsWith('//') && !url.includes('\\');
}

class AuthController {
    static showLogin(req, res) {
        const portal = (req.query.portal === 'admin' || req.portalType === 'admin') ? 'admin' : 'client';

        if (portal === 'admin') {
            if (req.session.adminUser) {
                const role = req.session.adminUser.role_name;
                if (role === 'admin') return res.redirect('/admin/approvals');
                if (role === 'manager') return res.redirect('/manager/dashboard');
                return res.redirect('/staff/pos');
            }
        } else if (req.session.clientUser) {
            return res.redirect('/');
        }

        res.render('auth/login', {
            title: portal === 'admin'
                ? 'Đăng Nhập Cổng Quản Trị (Admin / Manager)'
                : 'Đăng Nhập - Hệ Thống Đặt Vé Xem Phim',
            portal,
            error: req.query.error || null,
            success: req.query.success || null,
            emailValue: '',
            returnTo: req.query.redirect || (portal === 'admin' ? req.session.adminReturnTo : req.session.returnTo) || ''
        });
    }

    static async processLogin(req, res) {
        const { email, password, returnTo } = req.body;
        const portal = (req.body.portal === 'admin' || req.portalType === 'admin') ? 'admin' : 'client';
        const normalizedEmail = (email || '').trim().toLowerCase();

        if (!normalizedEmail || !password) {
            return res.render('auth/login', {
                title: 'Đăng Nhập',
                portal,
                error: 'Vui lòng nhập đầy đủ Email và Mật khẩu!',
                success: null,
                emailValue: normalizedEmail,
                returnTo
            });
        }

        try {
            const maxAttempts = await getMaxLoginAttempts();
            const user = await User.findByEmail(normalizedEmail);
            if (!user) {
                return res.render('auth/login', {
                    title: 'Đăng Nhập',
                    portal,
                    error: 'Email hoặc mật khẩu không chính xác!',
                    success: null,
                    emailValue: normalizedEmail,
                    returnTo
                });
            }

            if (user.status === 'locked') {
                const lockedMsg = Number(user.failed_login_attempts || 0) >= maxAttempts
                    ? `Tài khoản của bạn đã bị KHÓA do nhập sai mật khẩu ${user.failed_login_attempts}/${maxAttempts} lần! Vui lòng liên hệ quản trị viên để được mở khóa.`
                    : 'Tài khoản của bạn đã bị khóa! Vui lòng liên hệ quản trị viên.';
                return res.render('auth/login', {
                    title: 'Đăng Nhập',
                    portal,
                    error: lockedMsg,
                    success: null,
                    emailValue: normalizedEmail,
                    returnTo
                });
            }

            const isValid = User.verifyPassword(password, user.password_hash);
            if (!isValid) {
                const failResult = await User.recordFailedLogin(user.id, maxAttempts);
                const errMsg = failResult.locked
                    ? `Bạn đã nhập sai mật khẩu ${failResult.attempts}/${maxAttempts} lần! Tài khoản đã bị KHÓA tự động để bảo mật. Vui lòng liên hệ quản trị viên để mở khóa.`
                    : `Mật khẩu không chính xác! Bạn đã nhập sai ${failResult.attempts}/${maxAttempts} lần (còn ${failResult.remaining} lần thử trước khi tài khoản bị khóa).`;

                return res.render('auth/login', {
                    title: 'Đăng Nhập',
                    portal,
                    error: errMsg,
                    success: null,
                    emailValue: normalizedEmail,
                    returnTo
                });
            }

            if (portal === 'admin' && user.role_name === 'client') {
                return res.render('auth/login', {
                    title: 'Đăng Nhập Quản Trị',
                    portal,
                    error: 'Tài khoản Khách hàng không có quyền đăng nhập vào cổng Quản trị (Admin / Manager / Staff)!',
                    success: null,
                    emailValue: normalizedEmail,
                    returnTo
                });
            }

            // Đăng nhập thành công -> reset bộ đếm sai mật khẩu về 0
            if (Number(user.failed_login_attempts || 0) > 0 || user.locked_at) {
                await User.resetFailedLogins(user.id);
            }

            const sessionPayload = {
                id: user.id,
                role_id: user.role_id,
                role_name: user.role_name,
                role_display: user.role_display,
                full_name: user.full_name,
                email: user.email,
                phone: user.phone,
                avatar: user.avatar
            };

            // Lưu vào phiên độc lập theo phân hệ để chạy song song Client và Admin/Manager
            const isBackofficeRole = ['admin', 'manager', 'staff'].includes(user.role_name);
            if (portal === 'admin' || isBackofficeRole) {
                req.session.adminUser = sessionPayload;
                if (isSafeRedirect(returnTo) && (returnTo.startsWith('/admin') || returnTo.startsWith('/manager') || returnTo.startsWith('/staff'))) {
                    delete req.session.adminReturnTo;
                    return res.redirect(returnTo);
                }
                if (user.role_name === 'admin') {
                    return res.redirect('/admin/approvals');
                } else if (user.role_name === 'manager') {
                    return res.redirect('/manager/dashboard');
                } else {
                    return res.redirect('/staff/pos');
                }
            } else {
                req.session.clientUser = sessionPayload;
                if (isSafeRedirect(returnTo)) {
                    delete req.session.returnTo;
                    return res.redirect(returnTo);
                }
                return res.redirect('/');
            }
        } catch (err) {
            console.error('Lỗi khi đăng nhập:', err);
            return res.render('auth/login', {
                title: 'Đăng Nhập',
                portal,
                error: 'Có lỗi xảy ra trong quá trình đăng nhập. Vui lòng thử lại!',
                success: null,
                emailValue: normalizedEmail,
                returnTo
            });
        }
    }

    static showRegister(req, res) {
        if (req.session.clientUser) {
            return res.redirect('/');
        }
        res.render('auth/register', {
            title: 'Đăng Ký Tài Khoản Khách Hàng',
            error: req.query.error || null,
            formData: {},
            returnTo: req.query.redirect || req.session.returnTo || ''
        });
    }

    static async processRegister(req, res) {
        const { full_name, email, phone, password, confirm_password, returnTo } = req.body;

        if (!full_name || !email || !password) {
            return res.render('auth/register', {
                title: 'Đăng Ký Tài Khoản',
                error: 'Vui lòng điền đầy đủ các thông tin bắt buộc!',
                formData: req.body,
                returnTo: returnTo || ''
            });
        }

        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email.trim())) {
            return res.render('auth/register', {
                title: 'Đăng Ký Tài Khoản',
                error: 'Địa chỉ Email không đúng định dạng hợp lệ!',
                formData: req.body,
                returnTo: returnTo || ''
            });
        }

        if (phone && phone.trim()) {
            const phoneRegex = /^[0-9+() -]{8,20}$/;
            if (!phoneRegex.test(phone.trim())) {
                return res.render('auth/register', {
                    title: 'Đăng Ký Tài Khoản',
                    error: 'Số điện thoại không đúng định dạng hợp lệ!',
                    formData: req.body,
                    returnTo: returnTo || ''
                });
            }
        }

        if (password !== confirm_password) {
            return res.render('auth/register', {
                title: 'Đăng Ký Tài Khoản',
                error: 'Mật khẩu xác nhận không khớp!',
                formData: req.body,
                returnTo: returnTo || ''
            });
        }

        if (password.length < 6) {
            return res.render('auth/register', {
                title: 'Đăng Ký Tài Khoản',
                error: 'Mật khẩu phải chứa ít nhất 6 ký tự!',
                formData: req.body,
                returnTo: returnTo || ''
            });
        }

        try {
            const existingUser = await User.findByEmail(email.trim().toLowerCase());
            if (existingUser) {
                return res.render('auth/register', {
                    title: 'Đăng Ký Tài Khoản',
                    error: 'Email này đã được sử dụng trên hệ thống!',
                    formData: req.body,
                    returnTo: returnTo || ''
                });
            }

            // Role ID 4 là Khách hàng (client)
            const userId = await User.create({
                role_id: 4,
                full_name: full_name.trim(),
                email: email.trim().toLowerCase(),
                phone: phone ? phone.trim() : '',
                password
            });

            // Tự động đăng nhập phiên Khách hàng (không ảnh hưởng phiên Admin/Manager đang mở song song)
            const newUser = await User.findById(userId);
            req.session.clientUser = {
                id: newUser.id,
                role_id: newUser.role_id,
                role_name: newUser.role_name,
                role_display: newUser.role_display,
                full_name: newUser.full_name,
                email: newUser.email,
                phone: newUser.phone,
                avatar: newUser.avatar
            };

            // Nếu đang trong luồng mua vé, điều hướng an toàn (Chống Open Redirect)
            if (isSafeRedirect(returnTo)) {
                delete req.session.returnTo;
                return res.redirect(returnTo);
            }

            return res.redirect('/?welcome=1');
        } catch (err) {
            console.error('Lỗi khi đăng ký:', err);
            return res.render('auth/register', {
                title: 'Đăng Ký Tài Khoản',
                error: 'Có lỗi xảy ra khi tạo tài khoản. Vui lòng thử lại!',
                formData: req.body,
                returnTo: returnTo || ''
            });
        }
    }

    static logout(req, res) {
        const portal = req.query.portal || req.portalType || 'client';
        delete req.session.user;

        if (portal === 'admin') {
            delete req.session.adminUser;
            return req.session.save(() => {
                res.redirect('/auth/login?portal=admin');
            });
        } else {
            delete req.session.clientUser;
            delete req.session.bookingData;
            if (!req.session.adminUser) {
                return req.session.destroy(() => {
                    res.redirect('/');
                });
            }
            return req.session.save(() => {
                res.redirect('/');
            });
        }
    }

    static async showProfile(req, res) {
        try {
            const activeUser = req.currentUser || req.session.clientUser || req.session.adminUser;
            const user = await User.findById(activeUser.id);
            res.render('client/profile', {
                title: 'Hồ Sơ Cá Nhân',
                user,
                error: null,
                success: req.query.success || null
            });
        } catch (err) {
            console.error('Lỗi xem hồ sơ:', err);
            res.redirect('/');
        }
    }

    static async updateProfile(req, res) {
        try {
            const { full_name, phone } = req.body;
            const activeUser = req.currentUser || req.session.clientUser || req.session.adminUser;
            const userId = activeUser.id;

            await User.updateProfile(userId, { full_name, phone });
            
            // Cập nhật lại session tương ứng
            if (req.session.clientUser && req.session.clientUser.id === userId) {
                req.session.clientUser.full_name = full_name;
                req.session.clientUser.phone = phone;
            }
            if (req.session.adminUser && req.session.adminUser.id === userId) {
                req.session.adminUser.full_name = full_name;
                req.session.adminUser.phone = phone;
            }

            res.redirect('/profile?success=' + encodeURIComponent('Cập nhật thông tin thành công!'));
        } catch (err) {
            console.error('Lỗi cập nhật hồ sơ:', err);
            res.redirect('/profile');
        }
    }

    static async changePassword(req, res) {
        try {
            const { current_password, new_password, confirm_password } = req.body;
            const activeUser = req.currentUser || req.session.clientUser || req.session.adminUser;
            const userId = activeUser.id;
            const user = await User.findById(userId);

            if (!User.verifyPassword(current_password, user.password_hash)) {
                return res.render('client/profile', {
                    title: 'Hồ Sơ Cá Nhân',
                    user,
                    error: 'Mật khẩu hiện tại không chính xác!',
                    success: null
                });
            }

            if (new_password !== confirm_password) {
                return res.render('client/profile', {
                    title: 'Hồ Sơ Cá Nhân',
                    user,
                    error: 'Mật khẩu mới và xác nhận mật khẩu không khớp!',
                    success: null
                });
            }

            if (new_password.length < 6) {
                return res.render('client/profile', {
                    title: 'Hồ Sơ Cá Nhân',
                    user,
                    error: 'Mật khẩu mới phải có tối thiểu 6 ký tự!',
                    success: null
                });
            }

            await User.changePassword(userId, new_password);
            res.redirect('/profile?success=' + encodeURIComponent('Đổi mật khẩu thành công!'));
        } catch (err) {
            console.error('Lỗi đổi mật khẩu:', err);
            res.redirect('/profile');
        }
    }
}

module.exports = AuthController;
