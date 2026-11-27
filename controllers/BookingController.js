const Showtime = require('../models/Showtime');
const Seat = require('../models/Seat');
const Combo = require('../models/Combo');
const SeatLock = require('../models/SeatLock');
const Booking = require('../models/Booking');
const Ticket = require('../models/Ticket');
const QRCode = require('qrcode');
const { getSystemSettings, getEnabledPaymentMethods, isAutoPaymentMethod } = require('../services/paymentConfig');
const { bookingEvents } = require('../services/bookingEvents');

class BookingController {
    // 1. Sơ đồ chọn ghế ngồi trực quan theo phòng
    static async selectSeats(req, res) {
        try {
            const showtimeId = req.params.showtimeId;
            const showtime = await Showtime.findById(showtimeId);

            if (!showtime) {
                return res.status(404).render('client/404', {
                    title: 'Không Tìm Thấy Suất Chiếu',
                    message: 'Suất chiếu này không tồn tại hoặc đã bị hủy.'
                });
            }

            // Lấy danh sách ghế cùng trạng thái (available, booked, locked, selected)
            const seats = await Seat.getSeatsWithStatusForShowtime(showtimeId, req.sessionID);

            // Nhóm các ghế theo từng hàng (A, B, C, ...)
            const seatsByRow = {};
            seats.forEach(s => {
                if (!seatsByRow[s.seat_row]) {
                    seatsByRow[s.seat_row] = [];
                }
                seatsByRow[s.seat_row].push(s);
            });

            const breadcrumbs = [
                { label: 'Phim', url: '/movies' },
                { label: showtime.movie_title, url: `/movies/${showtime.movie_id}` },
                { label: 'Chọn Ghế' }
            ];

            res.render('client/select-seats', {
                title: `Chọn Ghế - ${showtime.movie_title}`,
                showtime,
                seatsByRow,
                rows: Object.keys(seatsByRow),
                sessionId: req.sessionID,
                breadcrumbs
            });
        } catch (err) {
            console.error('Lỗi chọn ghế:', err);
            res.status(500).render('client/404', {
                title: '500 - Lỗi',
                message: 'Không thể tải sơ đồ phòng chiếu: ' + err.message
            });
        }
    }

    // 2. API Khóa giữ ghế tạm thời (5 phút) để tránh Race condition
    static async apiLockSeats(req, res) {
        try {
            const { showtimeId, seatIds } = req.body;

            if (!showtimeId || !seatIds || !Array.isArray(seatIds) || seatIds.length === 0) {
                return res.status(400).json({
                    success: false,
                    message: 'Vui lòng chọn ít nhất 1 ghế!'
                });
            }

            if (seatIds.length > 8) {
                return res.status(400).json({
                    success: false,
                    message: 'Mỗi lần đặt vé chỉ được chọn tối đa 8 ghế để tránh chiếm dụng chỗ!'
                });
            }

            const activeUser = req.currentUser || req.session.clientUser || req.session.user || null;
            const result = await SeatLock.lockSeats({
                showtimeId: Number(showtimeId),
                seatIds: seatIds.map(Number),
                sessionId: req.sessionID,
                userId: activeUser ? activeUser.id : null,
                minutes: 5
            });

            if (!result.success) {
                return res.status(409).json(result); // 409 Conflict
            }

            // Lưu danh sách ghế đã chọn vào session để chuyển tiếp các bước sau
            req.session.bookingData = {
                showtimeId: Number(showtimeId),
                seatIds: seatIds.map(Number),
                lockExpiresAt: result.expiresAt
            };

            return req.session.save((err) => {
                if (err) console.error('Session save error:', err);
                return res.json({
                    success: true,
                    message: 'Đã giữ ghế tạm thời trong 5 phút!',
                    expiresAt: result.expiresAt
                });
            });
        } catch (err) {
            console.error('Lỗi khóa ghế:', err);
            return res.status(500).json({ success: false, message: 'Lỗi khóa ghế: ' + err.message });
        }
    }

    // 3. Chọn Combo bắp nước
    static async selectCombos(req, res) {
        try {
            const showtimeId = req.params.showtimeId;
            const showtime = await Showtime.findById(showtimeId);
            const bookingData = req.session.bookingData;

            if (!showtime || !bookingData || Number(bookingData.showtimeId) !== Number(showtimeId)) {
                return res.redirect(`/booking/seats/${showtimeId}`);
            }

            // Lấy chi tiết các ghế đã chọn
            const allSeats = await Seat.getSeatsWithStatusForShowtime(showtimeId, req.sessionID);
            const selectedSeats = allSeats.filter(s => bookingData.seatIds.includes(s.id));
            const combos = await Combo.getAllActive();

            res.render('client/select-combos', {
                title: `Chọn Bắp Nước - ${showtime.movie_title}`,
                showtime,
                selectedSeats,
                combos
            });
        } catch (err) {
            console.error('Lỗi chọn combo:', err);
            res.redirect(`/booking/seats/${req.params.showtimeId}`);
        }
    }

    // Lưu combo vào session và chuyển sang thanh toán
    static saveCombosAndProceed(req, res) {
        const showtimeId = req.params.showtimeId;
        const combos = req.body.combos ? JSON.parse(req.body.combos) : [];

        if (req.session.bookingData) {
            req.session.bookingData.combos = combos;
        }

        res.redirect(`/booking/checkout/${showtimeId}`);
    }

    // 4. Trang Thanh toán vé & Đếm ngược 5 phút
    static async checkout(req, res) {
        try {
            const showtimeId = req.params.showtimeId;
            const showtime = await Showtime.findById(showtimeId);
            const bookingData = req.session.bookingData;

            if (!showtime || !bookingData || Number(bookingData.showtimeId) !== Number(showtimeId)) {
                return res.redirect(`/booking/seats/${showtimeId}`);
            }

            // Kiểm tra xem ghế đã bị hết hạn giữ chỗ chưa
            const now = new Date();
            const lockExpiry = new Date(bookingData.lockExpiresAt);
            if (now > lockExpiry) {
                delete req.session.bookingData;
                return res.redirect(`/booking/seats/${showtimeId}?error=` + encodeURIComponent('Thời gian giữ ghế (5 phút) đã hết! Vui lòng chọn lại ghế.'));
            }

            const remainingSeconds = Math.max(0, Math.floor((lockExpiry.getTime() - now.getTime()) / 1000));

            // Lấy thông tin chi tiết các ghế
            const allSeats = await Seat.getSeatsWithStatusForShowtime(showtimeId, req.sessionID);
            const selectedSeats = allSeats.filter(s => bookingData.seatIds.includes(s.id));
            const seatTotal = selectedSeats.reduce((sum, s) => sum + s.calculated_price, 0);

            // Lấy thông tin combo
            const selectedCombos = [];
            let comboTotal = 0;
            if (bookingData.combos && Array.isArray(bookingData.combos)) {
                for (const c of bookingData.combos) {
                    if (c.quantity > 0) {
                        const comboObj = await Combo.findById(c.id);
                        if (comboObj) {
                            const total = comboObj.price * c.quantity;
                            comboTotal += total;
                            selectedCombos.push({
                                id: comboObj.id,
                                name: comboObj.name,
                                price: comboObj.price,
                                quantity: c.quantity,
                                total
                            });
                        }
                    }
                }
            }

            const grandTotal = seatTotal + comboTotal;
            const paymentSettings = await getSystemSettings();
            const paymentMethods = getEnabledPaymentMethods(paymentSettings);
            const activeUser = req.currentUser || req.session.clientUser || req.session.user || null;
            const transferMemo = `DATVE ${showtime.id} ${(activeUser && activeUser.phone ? activeUser.phone : '')}`.trim();

            // Tạo QR code cục bộ cho VNPAY, MoMo, ZaloPay để hiển thị sắc nét kể cả offline
            const [vnpayQrData, momoQrData, zalopayQrData] = await Promise.all([
                QRCode.toDataURL(`VNPAY|TMN:${paymentSettings.payment_vnpay_tmn}|AMT:${grandTotal}|INFO:${transferMemo}`, { width: 220, margin: 2 }),
                QRCode.toDataURL(`2|99|${paymentSettings.payment_momo_phone}|${paymentSettings.payment_momo_owner}||0|0|${grandTotal}|${transferMemo}|transfer_myqr`, { width: 220, margin: 2 }),
                QRCode.toDataURL(`ZALOPAY|PHONE:${paymentSettings.payment_zalopay_phone}|OWNER:${paymentSettings.payment_zalopay_owner}|AMT:${grandTotal}|INFO:${transferMemo}`, { width: 220, margin: 2 })
            ]);

            const breadcrumbs = [
                { label: 'Phim', url: '/movies' },
                { label: showtime.movie_title, url: `/movies/${showtime.movie_id}` },
                { label: 'Thanh Toán Vé' }
            ];

            res.render('client/checkout', {
                title: `Thanh Toán Vé - ${showtime.movie_title}`,
                showtime,
                selectedSeats,
                seatTotal,
                selectedCombos,
                comboTotal,
                grandTotal,
                remainingSeconds,
                paymentSettings,
                paymentMethods,
                transferMemo,
                paymentQrs: {
                    vnpay: vnpayQrData,
                    momo: momoQrData,
                    zalopay: zalopayQrData
                },
                error: req.query.error || null,
                currentUser: activeUser,
                breadcrumbs
            });
        } catch (err) {
            console.error('Lỗi checkout:', err);
            res.redirect(`/booking/seats/${req.params.showtimeId}`);
        }
    }

    // 5. Xử lý Thanh toán vé:
    // - VNPAY, MoMo, ZaloPay: Thanh toán tự động -> lập tức 'paid' & 'confirmed'
    // - VietQR ngân hàng, Thẻ, Tiền mặt: Chờ Admin ấn 'Đã nhận tiền' -> 'pending'
    static async processPayment(req, res) {
        const {
            showtime_id,
            customer_name,
            customer_email,
            customer_phone,
            payment_method,
            vnpay_bank,
            card_type,
            card_number,
            card_holder,
            wallet_ref
        } = req.body;

        const bookingData = req.session.bookingData;
        if (!bookingData || Number(bookingData.showtimeId) !== Number(showtime_id)) {
            return res.redirect('/');
        }

        // Kiểm tra hết hạn giữ ghế
        const now = new Date();
        if (now > new Date(bookingData.lockExpiresAt)) {
            delete req.session.bookingData;
            return res.redirect(`/booking/seats/${showtime_id}?error=` + encodeURIComponent('Thời gian giữ chỗ đã hết! Vui lòng đặt lại.'));
        }

        const activeUser = req.currentUser || req.session.clientUser || req.session.user || null;
        const paymentSettings = await getSystemSettings();
        const enabledMethods = getEnabledPaymentMethods(paymentSettings).map(m => m.id);
        const selectedMethod = enabledMethods.includes(payment_method) ? payment_method : (enabledMethods[0] || 'vnpay');
        const isAutoPayment = isAutoPaymentMethod(selectedMethod);
        const autoTxCode = `${selectedMethod.toUpperCase()}-${Date.now().toString().slice(-6)}`;

        // Ghi chú thanh toán an toàn (không lưu số thẻ đầy đủ hoặc CVV)
        let paymentNote = null;
        if (selectedMethod === 'vnpay') {
            paymentNote = `Thanh toán tự động VNPAY${vnpay_bank ? ' (' + String(vnpay_bank).trim() + ')' : ''} • Mã GD: ${autoTxCode}`;
        } else if (selectedMethod === 'momo') {
            const ref = wallet_ref ? String(wallet_ref).trim() : autoTxCode;
            paymentNote = `Thanh toán tự động Ví MoMo • Mã GD: ${ref}`;
        } else if (selectedMethod === 'zalopay') {
            const ref = wallet_ref ? String(wallet_ref).trim() : autoTxCode;
            paymentNote = `Thanh toán tự động Ví ZaloPay • Mã GD: ${ref}`;
        } else if (selectedMethod === 'card') {
            const digits = String(card_number || '').replace(/\D/g, '');
            const last4 = digits.length >= 4 ? digits.slice(-4) : '****';
            paymentNote = `Thẻ ${(card_type || 'VISA').toUpperCase()} •••• ${last4}${card_holder ? ' (' + String(card_holder).trim().toUpperCase() + ')' : ''}`;
        } else if (selectedMethod === 'mbbank_qr') {
            paymentNote = `VietQR ${paymentSettings.payment_bank_code || 'MB'} - ${paymentSettings.payment_bank_account || ''}`;
        } else if (selectedMethod === 'cash') {
            paymentNote = 'Thanh toán tiền mặt tại quầy vé';
        }

        // Chuẩn bị dữ liệu ghế
        const allSeats = await Seat.getSeatsWithStatusForShowtime(showtime_id, req.sessionID);
        const selectedSeats = allSeats
            .filter(s => bookingData.seatIds.includes(s.id))
            .map(s => ({
                id: s.id,
                seat_code: s.seat_code,
                price: s.calculated_price
            }));

        // Chuẩn bị dữ liệu combo
        const comboList = [];
        if (bookingData.combos && Array.isArray(bookingData.combos)) {
            for (const c of bookingData.combos) {
                if (c.quantity > 0) {
                    const comboObj = await Combo.findById(c.id);
                    if (comboObj) {
                        comboList.push({
                            id: comboObj.id,
                            quantity: c.quantity,
                            price: comboObj.price
                        });
                    }
                }
            }
        }

        try {
            const result = await Booking.createBooking({
                userId: activeUser ? activeUser.id : null,
                customerName: customer_name || (activeUser ? activeUser.full_name : 'Khách hàng'),
                customerEmail: customer_email || (activeUser ? activeUser.email : 'guest@cinema.com'),
                customerPhone: customer_phone || (activeUser ? activeUser.phone : ''),
                showtimeId: Number(showtime_id),
                seats: selectedSeats,
                combos: comboList,
                paymentMethod: selectedMethod,
                bookingType: 'online',
                paymentStatus: isAutoPayment ? 'paid' : 'pending',
                bookingStatus: isAutoPayment ? 'confirmed' : 'pending',
                paymentNote,
                sessionId: req.sessionID
            });

            // Xóa session đặt vé tạm
            delete req.session.bookingData;

            return res.redirect(`/booking/success/${result.bookingCode}`);
        } catch (err) {
            console.error('Lỗi khi thanh toán booking:', err);
            return res.redirect(`/booking/checkout/${showtime_id}?error=` + encodeURIComponent('Có lỗi xảy ra trong quá trình thanh toán! Vui lòng thử lại.'));
        }
    }

    // 6. Vé điện tử & Hiển thị mã QR Code
    static async ticketSuccess(req, res) {
        try {
            const bookingCode = req.params.bookingCode;
            const booking = await Booking.findByCode(bookingCode);

            if (!booking) {
                return res.status(404).render('client/404', {
                    title: 'Không Tìm Thấy Vé',
                    message: 'Không tìm thấy thông tin đơn đặt vé!'
                });
            }

            const tickets = await Booking.getTicketsByBookingId(booking.id);
            const combos = await Booking.getCombosByBookingId(booking.id);
            const paymentSettings = await getSystemSettings();

            res.render('client/ticket-success', {
                title: `Vé Điện Tử - Mã Đơn ${booking.booking_code}`,
                booking,
                tickets,
                combos,
                paymentSettings
            });
        } catch (err) {
            console.error('Lỗi vé điện tử:', err);
            res.status(500).render('client/404', {
                title: '500 - Lỗi',
                message: 'Không thể xem vé: ' + err.message
            });
        }
    }

    // 7. Lịch sử đặt vé cá nhân của khách hàng
    static async myTickets(req, res) {
        try {
            const activeUser = req.currentUser || req.session.clientUser || req.session.user;
            const userId = activeUser.id;
            const bookings = await Booking.getByUserId(userId);

            res.render('client/my-tickets', {
                title: 'Lịch Sử Đặt Vé Của Tôi',
                bookings,
                breadcrumbs: [
                    { label: 'Tài Khoản' },
                    { label: 'Vé Đã Mua' }
                ]
            });
        } catch (err) {
            console.error('Lỗi lịch sử vé:', err);
            res.redirect('/');
        }
    }

    // 8. API JSON kiểm tra trạng thái đơn hàng thời gian thực (cho Client không cần reload)
    static async apiBookingStatus(req, res) {
        try {
            const booking = await Booking.findByCode(req.params.bookingCode);
            if (!booking) {
                return res.status(404).json({ success: false, message: 'Không tìm thấy đơn hàng!' });
            }
            return res.json({
                success: true,
                booking_code: booking.booking_code,
                payment_status: booking.payment_status,
                booking_status: booking.booking_status,
                total_amount: booking.total_amount,
                payment_note: booking.payment_note || '',
                confirmed_at: booking.confirmed_at || null,
                confirmed_by_name: booking.confirmed_by_name || null
            });
        } catch (err) {
            return res.status(500).json({ success: false, message: err.message });
        }
    }

    // 9. SSE Stream thời gian thực cho trang chi tiết vé (/booking/success/:bookingCode)
    static apiBookingStream(req, res) {
        const targetCode = req.params.bookingCode;
        res.setHeader('Content-Type', 'text/event-stream');
        res.setHeader('Cache-Control', 'no-cache, no-transform');
        res.setHeader('Connection', 'keep-alive');
        res.flushHeaders?.();

        res.write(`data: ${JSON.stringify({ type: 'connected', bookingCode: targetCode })}\n\n`);

        const onChange = (payload) => {
            if (payload && payload.bookingCode === targetCode) {
                res.write(`data: ${JSON.stringify(payload)}\n\n`);
            }
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

    // 10. API JSON & SSE Stream cập nhật danh sách vé của tôi (/my-tickets) không cần reload
    static async apiMyTicketsStatus(req, res) {
        try {
            const activeUser = req.currentUser || req.session.clientUser;
            if (!activeUser) return res.status(401).json({ success: false });
            const bookings = await Booking.getByUserId(activeUser.id);
            return res.json({
                success: true,
                bookings: bookings.map(b => ({
                    id: b.id,
                    booking_code: b.booking_code,
                    payment_status: b.payment_status,
                    booking_status: b.booking_status
                }))
            });
        } catch (err) {
            return res.status(500).json({ success: false, message: err.message });
        }
    }

    static apiMyTicketsStream(req, res) {
        const activeUser = req.currentUser || req.session.clientUser;
        if (!activeUser) return res.status(401).end();

        res.setHeader('Content-Type', 'text/event-stream');
        res.setHeader('Cache-Control', 'no-cache, no-transform');
        res.setHeader('Connection', 'keep-alive');
        res.flushHeaders?.();

        res.write(`data: ${JSON.stringify({ type: 'connected' })}\n\n`);

        const onChange = (payload) => {
            if (payload && (!payload.userId || Number(payload.userId) === Number(activeUser.id))) {
                res.write(`data: ${JSON.stringify(payload)}\n\n`);
            }
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
}

module.exports = BookingController;
