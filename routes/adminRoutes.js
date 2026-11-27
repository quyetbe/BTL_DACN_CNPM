const express = require('express');
const router = express.Router();
const AdminController = require('../controllers/AdminController');
const { requireRole } = require('../middlewares/authMiddleware');

// Duyệt đơn thanh toán & Nhật ký giao dịch (cho phép cả Quản trị viên Admin và Quản lý rạp Manager)
const requireAdminOrManager = requireRole(['admin', 'manager']);
router.get('/approvals', requireAdminOrManager, AdminController.approvals);
router.get('/api/bookings', requireAdminOrManager, AdminController.apiBookings);
router.get('/api/bookings/stream', requireAdminOrManager, AdminController.apiBookingsStream);
router.get('/audit-logs', requireAdminOrManager, AdminController.auditLogs);
router.post('/bookings/:id/confirm-payment', requireAdminOrManager, AdminController.confirmBookingPayment);
router.post('/bookings/:id/cancel', requireAdminOrManager, AdminController.cancelBooking);

// Các chức năng còn lại chỉ Quản trị viên (admin) mới được vào
router.use(requireRole(['admin']));

// Quản lý người dùng & Phân quyền RBAC
router.get('/', (req, res) => res.redirect('/admin/users'));
router.get('/users', AdminController.users);
router.get('/users/create', AdminController.createUserForm);
router.post('/users/create', AdminController.storeUser);
router.get('/users/edit/:id', AdminController.editUserForm);
router.post('/users/edit/:id', AdminController.updateUser);
router.post('/users/toggle-status/:id', AdminController.toggleStatus);
router.post('/users/delete/:id', AdminController.deleteUser);

// Cấu hình hệ thống
router.get('/settings', AdminController.settings);
router.post('/settings', AdminController.updateSettings);

module.exports = router;
