const { query, get, run } = require('../database/db');

class Ticket {
    static async findByCode(code) {
        if (!code) return null;
        code = code.trim();

        // 1. Tìm chính xác theo ticket_code (TKT-...)
        let ticket = await get(`
            SELECT t.*, 
                   s.seat_code, s.seat_row, s.seat_number, s.seat_type,
                   st.start_time, st.end_time,
                   m.title as movie_title, m.poster_url, m.age_rating, m.duration,
                   r.room_name, r.screen_type,
                   b.booking_code, b.customer_name, b.customer_phone, b.payment_status,
                   u.full_name as staff_name
            FROM tickets t
            JOIN seats s ON t.seat_id = s.id
            JOIN showtimes st ON t.showtime_id = st.id
            JOIN movies m ON st.movie_id = m.id
            JOIN rooms r ON st.room_id = r.id
            JOIN bookings b ON t.booking_id = b.id
            LEFT JOIN users u ON t.checked_in_by = u.id
            WHERE t.ticket_code = ?
        `, [code]);

        if (ticket) return ticket;

        // 2. Tìm theo booking_code (cho phép soát vé bằng mã đơn hàng BKG-... khi bán tại quầy POS)
        const tickets = await query(`
            SELECT t.*, 
                   s.seat_code, s.seat_row, s.seat_number, s.seat_type,
                   st.start_time, st.end_time,
                   m.title as movie_title, m.poster_url, m.age_rating, m.duration,
                   r.room_name, r.screen_type,
                   b.booking_code, b.customer_name, b.customer_phone, b.payment_status,
                   u.full_name as staff_name
            FROM tickets t
            JOIN seats s ON t.seat_id = s.id
            JOIN showtimes st ON t.showtime_id = st.id
            JOIN movies m ON st.movie_id = m.id
            JOIN rooms r ON st.room_id = r.id
            JOIN bookings b ON t.booking_id = b.id
            LEFT JOIN users u ON t.checked_in_by = u.id
            WHERE b.booking_code = ?
            ORDER BY t.id ASC
        `, [code]);

        if (tickets && tickets.length > 0) {
            if (tickets.length === 1) {
                return tickets[0];
            }
            // Đơn hàng có nhiều vé (VD: đặt 2-4 ghế cùng lúc)
            const primary = { ...tickets[0] };
            primary.all_tickets = tickets;
            primary.seat_code = tickets.map(t => t.seat_code).join(', ');
            primary.ticket_count = tickets.length;
            primary.is_booking_group = true;
            
            const allCheckedIn = tickets.every(t => t.status === 'checked_in');
            const anyUnused = tickets.some(t => t.status === 'unused');
            primary.status = anyUnused ? 'unused' : (allCheckedIn ? 'checked_in' : tickets[0].status);
            return primary;
        }

        return null;
    }

    static async checkIn(code, staffId) {
        const ticket = await this.findByCode(code);
        if (!ticket) {
            return {
                success: false,
                status: 'not_found',
                message: 'Không tìm thấy vé trong hệ thống! Vui lòng kiểm tra lại mã vé hoặc mã đơn hàng.'
            };
        }

        // Xử lý đơn hàng có nhiều vé (soát theo mã đơn hàng BKG-...)
        if (ticket.all_tickets && ticket.all_tickets.length > 0) {
            const unusedTickets = ticket.all_tickets.filter(t => t.status === 'unused');
            if (unusedTickets.length === 0) {
                return {
                    success: false,
                    status: 'already_used',
                    message: `CẢNH BÁO: Toàn bộ ${ticket.all_tickets.length} vé trong đơn hàng ${ticket.booking_code} đã được soát trước đó!`,
                    ticket
                };
            }

            const now = new Date().toISOString().replace('T', ' ').substring(0, 19);
            for (const tkt of unusedTickets) {
                await run(`
                    UPDATE tickets
                    SET status = 'checked_in', checked_in_at = ?, checked_in_by = ?
                    WHERE id = ?
                `, [now, staffId, tkt.id]);
            }

            const updatedTicket = await this.findByCode(ticket.booking_code);
            return {
                success: true,
                status: 'success',
                message: `Soát vé THÀNH CÔNG cho đơn hàng ${ticket.booking_code}! Đã xác nhận ${unusedTickets.length} vé (${unusedTickets.map(t => t.seat_code).join(', ')}) vào phòng chiếu.`,
                ticket: updatedTicket
            };
        }

        // Soát vé đơn lẻ
        if (ticket.status === 'checked_in') {
            return {
                success: false,
                status: 'already_used',
                message: `CẢNH BÁO: Vé đã được sử dụng vào lúc ${ticket.checked_in_at || 'trước đó'} bởi nhân viên ${ticket.staff_name || 'quầy'}!`,
                ticket
            };
        }

        if (ticket.status === 'cancelled') {
            return {
                success: false,
                status: 'cancelled',
                message: 'Vé này đã bị hủy!',
                ticket
            };
        }

        const now = new Date().toISOString().replace('T', ' ').substring(0, 19);
        await run(`
            UPDATE tickets
            SET status = 'checked_in', checked_in_at = ?, checked_in_by = ?
            WHERE id = ?
        `, [now, staffId, ticket.id]);

        const updatedTicket = await this.findByCode(ticket.ticket_code);
        return {
            success: true,
            status: 'success',
            message: `Soát vé THÀNH CÔNG! Ghế ${ticket.seat_code}. Cho phép khách vào phòng chiếu.`,
            ticket: updatedTicket
        };
    }

    static async getTodayScanned(staffId = null) {
        let sql = `
            SELECT t.*, 
                   s.seat_code,
                   m.title as movie_title,
                   r.room_name,
                   st.start_time,
                   u.full_name as staff_name
            FROM tickets t
            JOIN seats s ON t.seat_id = s.id
            JOIN showtimes st ON t.showtime_id = st.id
            JOIN movies m ON st.movie_id = m.id
            JOIN rooms r ON st.room_id = r.id
            LEFT JOIN users u ON t.checked_in_by = u.id
            WHERE t.status = 'checked_in' AND DATE(t.checked_in_at) = CURDATE()
        `;
        const params = [];
        if (staffId) {
            sql += ' AND t.checked_in_by = ?';
            params.push(staffId);
        }
        sql += ' ORDER BY t.checked_in_at DESC LIMIT 50';
        return await query(sql, params);
    }
}

module.exports = Ticket;
