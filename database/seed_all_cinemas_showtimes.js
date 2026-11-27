const { pool } = require('./db');

async function seedAllCinemasShowtimes() {
    console.log('====================================================================');
    console.log('🎬 BỔ SUNG SUẤT CHIẾU ĐẦY ĐỦ CÁC NGÀY CHO TẤT CẢ 10 CƠ SỞ CINESTAR');
    console.log('====================================================================');

    const conn = await pool.getConnection();
    try {
        // 1. Lấy tất cả cụm rạp, phòng chiếu và phim đang chiếu
        const [cinemas] = await conn.query('SELECT id, name, city FROM cinemas WHERE status = "active" ORDER BY id ASC');
        const [rooms] = await conn.query('SELECT id, room_name, screen_type, cinema_id FROM rooms WHERE status = "active" ORDER BY cinema_id ASC, id ASC');
        const [movies] = await conn.query("SELECT id, title, duration FROM movies WHERE status = 'now_showing' ORDER BY id ASC");

        const roomsByCinema = new Map();
        for (const r of rooms) {
            if (!roomsByCinema.has(r.cinema_id)) roomsByCinema.set(r.cinema_id, []);
            roomsByCinema.get(r.cinema_id).push(r);
        }

        // 2. Tạo danh sách ngày từ hôm nay (theo giờ địa phương) đến hết 31/12/2026
        const now = new Date();
        const startDay = new Date(now.getFullYear(), now.getMonth(), now.getDate());
        const endDay = new Date(2026, 11, 31); // 31/12/2026
        const pad = (n) => String(n).padStart(2, '0');

        const dates = [];
        const cursor = new Date(startDay);
        while (cursor <= endDay) {
            const y = cursor.getFullYear();
            const m = cursor.getMonth() + 1;
            const d = cursor.getDate();
            dates.push({
                dateStr: `${y}-${pad(m)}-${pad(d)}`,
                year: y,
                month: m,
                day: d,
                isWeekend: cursor.getDay() === 0 || cursor.getDay() === 6
            });
            cursor.setDate(cursor.getDate() + 1);
        }

        console.log(`📌 Số cụm rạp: ${cinemas.length} | Phim đang chiếu: ${movies.length} | Số ngày: ${dates.length} (${dates[0].dateStr} -> ${dates[dates.length - 1].dateStr})`);

        // 3. Đọc các suất chiếu hiện có trong khoảng ngày để tránh chèn trùng (movie_id, cinema_id, date, HH:MM)
        const [existingRows] = await conn.query(`
            SELECT st.movie_id, r.cinema_id,
                   DATE_FORMAT(st.start_time, '%Y-%m-%d') as d_str,
                   DATE_FORMAT(st.start_time, '%H:%i') as t_str
            FROM showtimes st
            JOIN rooms r ON st.room_id = r.id
            WHERE st.status = 'scheduled'
              AND DATE(st.start_time) >= ?
              AND DATE(st.start_time) <= ?
        `, [dates[0].dateStr, dates[dates.length - 1].dateStr]);

        const existingPerKey = new Map(); // key: cinemaId|movieId|dateStr -> Set of HH:MM
        for (const row of existingRows) {
            const key = `${row.cinema_id}|${row.movie_id}|${row.d_str}`;
            if (!existingPerKey.has(key)) existingPerKey.set(key, new Set());
            existingPerKey.get(key).add(row.t_str);
        }

        // Các khung giờ chiếu tự nhiên (sáng, chiều, tối) để xoay vòng đa dạng giữa các phim/ngày
        const morningSlots = [
            [9, 0], [9, 20], [9, 45], [10, 10], [10, 30], [11, 0], [11, 30]
        ];
        const afternoonSlots = [
            [13, 15], [13, 45], [14, 15], [14, 45], [15, 15], [15, 45], [16, 20]
        ];
        const eveningSlots = [
            [18, 0], [18, 30], [19, 0], [19, 30], [20, 0], [20, 30], [21, 15], [21, 45]
        ];

        const toInsert = [];

        for (let dIdx = 0; dIdx < dates.length; dIdx++) {
            const { dateStr, year, month, day, isWeekend } = dates[dIdx];

            for (const cinema of cinemas) {
                const cinemaRooms = roomsByCinema.get(cinema.id) || [];
                if (cinemaRooms.length === 0) continue;

                for (let mIdx = 0; mIdx < movies.length; mIdx++) {
                    const movie = movies[mIdx];
                    const duration = Number(movie.duration) || 110;
                    const bufferMinutes = 15;
                    const key = `${cinema.id}|${movie.id}|${dateStr}`;
                    const usedTimes = existingPerKey.get(key) || new Set();

                    // Phim nổi bật (top 15) có 3 suất/ngày/cơ sở; các phim còn lại có 2 suất/ngày/cơ sở
                    const targetCount = mIdx < 15 ? 3 : 2;
                    if (usedTimes.size >= targetCount) continue;

                    const seed = (cinema.id * 11 + movie.id * 7 + dIdx * 3);
                    const candidateSlots = mIdx < 15
                        ? [
                            morningSlots[seed % morningSlots.length],
                            afternoonSlots[(seed + 2) % afternoonSlots.length],
                            eveningSlots[(seed + 4) % eveningSlots.length]
                        ]
                        : [
                            afternoonSlots[seed % afternoonSlots.length],
                            eveningSlots[(seed + 3) % eveningSlots.length]
                        ];

                    let added = usedTimes.size;
                    for (let sIdx = 0; sIdx < candidateSlots.length && added < targetCount; sIdx++) {
                        const [h, min] = candidateSlots[sIdx];
                        const timeTag = `${pad(h)}:${pad(min)}`;
                        if (usedTimes.has(timeTag)) continue;

                        const room = cinemaRooms[(mIdx + sIdx + dIdx) % cinemaRooms.length];
                        const startTotalMin = h * 60 + min;
                        const endTotalMin = startTotalMin + duration + bufferMinutes;

                        let endYear = year;
                        let endMonth = month;
                        let endDay = day;
                        let endH = Math.floor(endTotalMin / 60);
                        const endM = endTotalMin % 60;
                        if (endH >= 24) {
                            endH -= 24;
                            const nextD = new Date(year, month - 1, day + 1);
                            endYear = nextD.getFullYear();
                            endMonth = nextD.getMonth() + 1;
                            endDay = nextD.getDate();
                        }

                        const startTimeStr = `${dateStr} ${pad(h)}:${pad(min)}:00`;
                        const endTimeStr = `${endYear}-${pad(endMonth)}-${pad(endDay)} ${pad(endH)}:${pad(endM)}:00`;

                        const isEvening = h >= 17;
                        let basePrice = 80000;
                        if (room.screen_type === 'IMAX') {
                            basePrice = (isEvening || isWeekend) ? 140000 : 120000;
                        } else if (room.screen_type === '3D') {
                            basePrice = (isEvening || isWeekend) ? 110000 : 95000;
                        } else {
                            basePrice = (isEvening || isWeekend) ? 90000 : 80000;
                        }

                        toInsert.push([
                            movie.id,
                            room.id,
                            startTimeStr,
                            endTimeStr,
                            bufferMinutes,
                            basePrice,
                            'scheduled'
                        ]);
                        usedTimes.add(timeTag);
                        added++;
                    }
                }
            }
        }

        console.log(`📌 Số suất chiếu mới cần bổ sung: ${toInsert.length.toLocaleString('vi-VN')} suất`);

        const batchSize = 1000;
        for (let i = 0; i < toInsert.length; i += batchSize) {
            const batch = toInsert.slice(i, i + batchSize);
            await conn.query(
                'INSERT INTO showtimes (movie_id, room_id, start_time, end_time, buffer_minutes, base_price, status) VALUES ?',
                [batch]
            );
        }

        // Cập nhật end_date cho toàn bộ phim đang chiếu
        await conn.query("UPDATE movies SET end_date = '2026-12-31' WHERE status = 'now_showing'");

        const [summary] = await conn.query(`
            SELECT c.id, c.name,
                   COUNT(st.id) as total_shows,
                   COUNT(DISTINCT st.movie_id) as total_movies,
                   COUNT(DISTINCT DATE(st.start_time)) as total_days
            FROM cinemas c
            JOIN rooms r ON r.cinema_id = c.id
            JOIN showtimes st ON st.room_id = r.id
            WHERE st.status = 'scheduled' AND DATE(st.start_time) BETWEEN ? AND ?
            GROUP BY c.id, c.name
            ORDER BY c.id ASC
        `, [dates[0].dateStr, dates[dates.length - 1].dateStr]);

        console.log('\n✅ KẾT QUẢ PHỦ SUẤT CHIẾU TỪ ' + dates[0].dateStr + ' ĐẾN ' + dates[dates.length - 1].dateStr + ':');
        console.table(summary);
    } finally {
        conn.release();
        process.exit(0);
    }
}

seedAllCinemasShowtimes().catch(err => {
    console.error('❌ Lỗi khi sinh suất chiếu:', err);
    process.exit(1);
});
