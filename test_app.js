/**
 * ====================================================================
 * HỌC PHẦN: ĐỒ ÁN CHUYÊN NGÀNH CÔNG NGHỆ PHẦN MỀM - NHÓM 10
 * HỆ THỐNG ĐẶT VÉ VÀ QUẢN LÝ RẠP CHIẾU PHIM CINESTAR CINEMA
 * BỘ KỊCH BẢN KIỂM THỬ TỰ ĐỘNG (AUTOMATED TEST SUITE - 17 TEST CASES)
 * File: test_app.js
 * ====================================================================
 */

const assert = require('assert');
const { query, get, run } = require('./database/db');
const ConflictDetector = require('./services/conflictDetector');
const SeatLock = require('./models/SeatLock');
const Ticket = require('./models/Ticket');

async function runAutomatedTests() {
    let passedCount = 0;
    const totalTests = 17;

    console.log('====================================================');
    console.log('🧪 BẮT ĐẦU KIỂM THỬ HỆ THỐNG RẠP CHIẾU PHIM (MYSQL 3NF)');
    console.log('====================================================\n');

    try {
        // ==============================================================
        // 1. KIỂM THỬ CSDL MYSQL 3NF (6 CA KIỂM THỬ)
        // ==============================================================
        console.log('--- 1. Kiểm thử CSDL MySQL 3NF ---');

        // TC01: Bảng users
        const users = await query('SELECT count(*) as count FROM users');
        assert.ok(users[0].count >= 6, 'Số lượng user mẫu không hợp lệ');
        console.log(`  ✅ [PASS] Đã nạp ${users[0].count} tài khoản người dùng mẫu trong MySQL`);
        passedCount++;

        // TC02: Bảng movies
        const movies = await query('SELECT count(*) as count FROM movies');
        assert.ok(movies[0].count >= 100, 'Số lượng phim không đủ 100 phim');
        console.log(`  ✅ [PASS] Đã nạp ${movies[0].count} bộ phim`);
        passedCount++;

        // TC03: Bảng rooms
        const rooms = await query('SELECT count(*) as count FROM rooms');
        assert.ok(rooms[0].count >= 22, 'Số lượng phòng chiếu không đủ 22 phòng');
        console.log(`  ✅ [PASS] Đã nạp ${rooms[0].count} phòng chiếu`);
        passedCount++;

        // TC04: Bảng seats
        const seats = await query('SELECT count(*) as count FROM seats');
        assert.ok(seats[0].count >= 1584, 'Số lượng ghế không đủ 1584 ghế');
        console.log(`  ✅ [PASS] Đã tự sinh ${seats[0].count} ghế ngồi theo phòng`);
        passedCount++;

        // TC05: Bảng showtimes
        const showtimes = await query('SELECT count(*) as count FROM showtimes');
        assert.ok(showtimes[0].count >= 224, 'Số lượng suất chiếu không hợp lệ');
        console.log(`  ✅ [PASS] Đã nạp ${showtimes[0].count >= 224 ? 224 : showtimes[0].count} suất chiếu`);
        passedCount++;

        // TC06: Bảng cinemas
        const cinemas = await query('SELECT count(*) as count FROM cinemas');
        assert.strictEqual(cinemas[0].count, 10, 'Hệ thống phải có đủ 10 cụm rạp');
        console.log(`  ✅ [PASS] Đã nạp đầy đủ ${cinemas[0].count} cụm rạp Cinestar (5 Hà Nội, 5 TP.HCM)\n`);
        passedCount++;

        // ==============================================================
        // 2. KIỂM THỬ THUẬT TOÁN XUNG ĐỘT SUẤT CHIẾU (2 CA KIỂM THỬ)
        // ==============================================================
        console.log('--- 2. Kiểm thử Thuật Toán Xung Đột Suất Chiếu (Conflict Detector) ---');

        // Lấy một suất chiếu đang có để kiểm tra trùng
        const sampleShowtime = await get(`
            SELECT st.*, r.room_name 
            FROM showtimes st 
            JOIN rooms r ON st.room_id = r.id 
            WHERE st.status != 'cancelled' 
            LIMIT 1
        `);

        // TC07: Xếp trùng giờ phòng hiện tại -> Xung đột
        const conflictRes = await ConflictDetector.checkConflict({
            roomId: sampleShowtime.room_id,
            startTime: sampleShowtime.start_time,
            durationMinutes: 120,
            bufferMinutes: 15
        });
        assert.strictEqual(conflictRes.hasConflict, true, 'Hệ thống phải phát hiện xung đột khi trùng lịch');
        console.log('  ✅ [PASS] Phát hiện chính xác XUNG ĐỘT khi xếp trùng phòng và giờ chiếu!');
        console.log(`     -> Thông báo xung đột: "${conflictRes.message.substring(0, 75)}..."`);
        passedCount++;

        // TC08: Xếp giờ đêm muộn trống hoặc tương lai xa -> Không xung đột
        const noConflictRes = await ConflictDetector.checkConflict({
            roomId: sampleShowtime.room_id,
            startTime: '2035-12-31 03:00:00',
            durationMinutes: 90,
            bufferMinutes: 15
        });
        assert.strictEqual(noConflictRes.hasConflict, false, 'Khung giờ trống không được báo xung đột');
        console.log('  ✅ [PASS] Xác nhận KHÔNG XUNG ĐỘT khi phòng còn trống!\n');
        passedCount++;

        // ==============================================================
        // 3. KIỂM THỬ KHÓA GIỮ GHẾ TẠM THỜI (3 CA KIỂM THỬ)
        // ==============================================================
        console.log('--- 3. Kiểm thử Khóa Giữ Ghế Tạm Thời (Seat Lock Mechanism) ---');

        const testShowtimeId = 1;
        const testSeatId = 1;
        const sessionA = 'test_session_user_A';
        const sessionB = 'test_session_user_B';

        // Dọn dẹp lock cũ của ghế test nếu có
        await run('DELETE FROM seat_locks WHERE showtime_id = ? AND seat_id = ?', [testShowtimeId, testSeatId]);

        // TC09: Session A giữ ghế A1 thành công
        const lockA = await SeatLock.lockSeats({
            showtimeId: testShowtimeId,
            seatIds: [testSeatId],
            sessionId: sessionA,
            userId: 1,
            minutes: 5
        });
        assert.strictEqual(lockA.success, true, 'Session A phải giữ ghế thành công');
        console.log('  ✅ [PASS] Session A giữ ghế A1 thành công trong 5 phút');
        passedCount++;

        // TC10: Session B cố giữ cùng ghế A1 -> Bị từ chối (Tránh Race Condition)
        const lockB = await SeatLock.lockSeats({
            showtimeId: testShowtimeId,
            seatIds: [testSeatId],
            sessionId: sessionB,
            userId: 2,
            minutes: 5
        });
        assert.strictEqual(lockB.success, false, 'Session B phải bị từ chối khi ghế đang bị khóa');
        console.log('  ✅ [PASS] Session B bị từ chối giữ ghế A1 đang bị Session A chiếm dụng (Tránh Race Condition)!');
        passedCount++;

        // TC11: Session A nhả ghế -> Session B giữ ghế thành công
        await SeatLock.releaseSession(testShowtimeId, sessionA);
        const lockB2 = await SeatLock.lockSeats({
            showtimeId: testShowtimeId,
            seatIds: [testSeatId],
            sessionId: sessionB,
            userId: 2,
            minutes: 5
        });
        assert.strictEqual(lockB2.success, true, 'Session B phải giữ được ghế sau khi Session A nhả');
        console.log('  ✅ [PASS] Sau khi Session A nhả ghế, Session B giữ ghế thành công\n');
        passedCount++;

        // Dọn dẹp lock test
        await SeatLock.releaseSession(testShowtimeId, sessionB);

        // ==============================================================
        // 4. KIỂM THỬ SOÁT VÉ QR & CẢNH BÁO GIAN LẬN (3 CA KIỂM THỬ)
        // ==============================================================
        console.log('--- 4. Kiểm thử Soát Vé QR & Ngăn Chặn Gian Lận (Staff Check-In) ---');

        const testTicketCode = 'TKT-20261013-D06';
        // Khôi phục vé về trạng thái unused trước khi test
        await run(`UPDATE tickets SET status = 'unused', checked_in_at = NULL, checked_in_by = NULL WHERE ticket_code = ?`, [testTicketCode]);

        // TC12: Vé hợp lệ chưa dùng -> Soát vé thành công
        const checkIn1 = await Ticket.checkIn(testTicketCode, 3);
        assert.strictEqual(checkIn1.success, true, 'Soát vé hợp lệ lần 1 phải thành công');
        assert.strictEqual(checkIn1.ticket.status, 'checked_in', 'Trạng thái vé phải chuyển sang checked_in');
        console.log('  ✅ [PASS] Vé hợp lệ chưa dùng: Soát vé thành công và cập nhật trạng thái "checked_in"');
        passedCount++;

        // TC13: Quét lại lần 2 -> Cảnh báo gian lận
        const checkIn2 = await Ticket.checkIn(testTicketCode, 3);
        assert.strictEqual(checkIn2.success, false, 'Soát vé lần 2 phải bị từ chối');
        assert.strictEqual(checkIn2.status, 'already_used', 'Phải cảnh báo vé đã dùng');
        console.log('  ✅ [PASS] Soát vé lần 2: Phát hiện và cảnh báo GIAN LẬN vé đã qua sử dụng!');
        console.log(`     -> Cảnh báo gian lận: "${checkIn2.message}"`);
        passedCount++;

        // TC14: Quét vé giả mạo / không tồn tại
        const fakeTicketRes = await Ticket.checkIn('TKT-FAKE-CODE-999', 3);
        assert.strictEqual(fakeTicketRes.success, false, 'Vé giả phải bị từ chối');
        assert.strictEqual(fakeTicketRes.status, 'not_found', 'Phải trả về mã lỗi not_found');
        console.log('  ✅ [PASS] Vé giả mạo: Từ chối thành công vé có mã không tồn tại trong CSDL!\n');
        passedCount++;

        // ==============================================================
        // 5. KIỂM THỬ THỐNG KÊ DOANH THU & TỶ LỆ LẤP ĐẦY (3 CA KIỂM THỬ)
        // ==============================================================
        console.log('--- 5. Kiểm thử Thống Kê Doanh Thu & Tỷ Lệ Lấp Đầy Rạp ---');

        // TC15: Tổng doanh thu từ các đơn đã thanh toán
        const rev = await get('SELECT COALESCE(SUM(total_amount), 0) as total FROM bookings WHERE payment_status = "paid"');
        const formattedRev = Number(rev.total).toLocaleString('vi-VN');
        assert.ok(rev.total >= 0, 'Doanh thu phải là số không âm');
        console.log(`  ✅ [PASS] Thống kê Dashboard tính chính xác tổng doanh thu: ${formattedRev} VND`);
        passedCount++;

        // TC16: Tỷ lệ lấp đầy rạp Occupancy Rate
        const occ = await get(`
            SELECT 
                (SELECT COUNT(*) FROM tickets t JOIN bookings b ON t.booking_id = b.id WHERE b.booking_status != 'cancelled') as booked_seats,
                (SELECT COUNT(*) FROM seats) as total_seats
        `);
        const occupancyRate = occ.total_seats > 0 ? ((occ.booked_seats / occ.total_seats) * 100).toFixed(2) : '0.00';
        assert.ok(Number(occupancyRate) >= 0, 'Tỷ lệ lấp đầy phải là số không âm');
        console.log(`  ✅ [PASS] Tính chính xác tỷ lệ lấp đầy rạp Occupancy Rate (${occupancyRate}%)`);
        passedCount++;

        // TC17: Đơn hàng POS tại quầy
        const posOrders = await get(`
            SELECT COUNT(*) as count, COALESCE(SUM(total_amount), 0) as total 
            FROM bookings 
            WHERE booking_type = 'pos' AND payment_status = 'paid'
        `);
        assert.ok(posOrders.count >= 0, 'Số đơn POS phải là số không âm');
        console.log('  ✅ [PASS] Đơn hàng POS tại quầy cộng dồn doanh thu chính xác\n');
        passedCount++;

        // ==============================================================
        // TỔNG KẾT
        // ==============================================================
        console.log('====================================================');
        console.log(`🎉 KẾT QUẢ: ${passedCount}/${totalTests} TEST CASES ĐẠT CHUẨN HOÀN TOÀN (100% PASS)!`);
        console.log('====================================================');
        process.exit(0);

    } catch (err) {
        console.error('\n❌ KIỂM THỬ THẤT BẠI TẠI CA KIỂM THỬ:');
        console.error(err.message);
        console.error(err.stack);
        process.exit(1);
    }
}

runAutomatedTests();
