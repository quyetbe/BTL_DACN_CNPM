const { pool, query } = require('./db');

async function addShowtimes() {
    console.log('====================================================================');
    console.log('🎬 BẮT ĐẦU TẠO SUẤT CHIẾU CHO TẤT CẢ PHIM ĐANG CHIẾU ĐẾN 31/12/2026');
    console.log('====================================================================\n');

    const conn = await pool.getConnection();

    try {
        // 1. Cập nhật ngày kết thúc (end_date) cho tất cả phim đang chiếu thành 31/12/2026
        console.log('📌 1. Cập nhật thời hạn chiếu (end_date = 2026-12-31) cho toàn bộ phim đang chiếu...');
        const updateEndDateResult = await conn.query(
            "UPDATE movies SET end_date = '2026-12-31' WHERE status = 'now_showing'"
        );
        console.log(`   ✅ Đã cập nhật thời hạn chiếu cho các phim đang chiếu.`);

        // 2. Lấy danh sách phim đang chiếu và phòng chiếu
        console.log('\n📌 2. Truy vấn danh sách phim và phòng rạp...');
        const [movies] = await conn.query(
            "SELECT id, title, duration, genre FROM movies WHERE status = 'now_showing' ORDER BY id ASC"
        );
        const [rooms] = await conn.query(
            "SELECT id, room_name, screen_type, cinema_id FROM rooms ORDER BY id ASC"
        );
        const [cinemas] = await conn.query(
            "SELECT id, name, city FROM cinemas ORDER BY id ASC"
        );

        console.log(`   - Số lượng phim đang chiếu: ${movies.length} phim (ID: ${movies[0].id} -> ${movies[movies.length - 1].id})`);
        console.log(`   - Số lượng phòng chiếu: ${rooms.length} phòng`);
        console.log(`   - Số lượng cụm rạp: ${cinemas.length} cụm rạp (Hà Nội & TP.HCM)`);

        const movieMap = new Map(movies.map(m => [m.id, m]));
        const movieIds = movies.map(m => m.id);

        // 3. Khởi tạo danh sách ngày từ 2026-10-21 đến 2026-12-31 (72 ngày)
        const dates = [];
        const curDate = new Date(2026, 9, 21); // Month is 0-indexed: 9 = October
        const stopDate = new Date(2026, 11, 31); // 11 = December

        while (curDate <= stopDate) {
            const y = curDate.getFullYear();
            const m = String(curDate.getMonth() + 1).padStart(2, '0');
            const d = String(curDate.getDate()).padStart(2, '0');
            dates.push({
                dateStr: `${y}-${m}-${d}`,
                year: y,
                month: curDate.getMonth() + 1,
                day: curDate.getDate(),
                dayOfWeek: curDate.getDay() // 0 = Chủ nhật, 6 = Thứ 7
            });
            curDate.setDate(curDate.getDate() + 1);
        }

        console.log(`\n📌 3. Khoảng thời gian sinh suất chiếu:`);
        console.log(`   - Từ ngày: ${dates[0].dateStr}`);
        console.log(`   - Đến ngày: ${dates[dates.length - 1].dateStr}`);
        console.log(`   - Tổng cộng: ${dates.length} ngày`);

        // Độ lệch giờ mở rạp của từng phòng để lịch chiếu so le tự nhiên
        const roomStartOffsets = [
            0, 15, 30, 45, // Cầu Giấy (Phòng 1-4)
            0, 30,         // Hoàn Kiếm (Phòng 5-6)
            15, 45,        // Thanh Xuân (Phòng 7-8)
            0, 30,         // Hai Bà Trưng HN (Phòng 9-10)
            15, 45,        // Đống Đa (Phòng 11-12)
            0, 30,         // Q1 (Phòng 13-14)
            15, 45,        // Q3 (Phòng 15-16)
            0, 30,         // Q4 (Phòng 17-18)
            15, 45,        // Q5 (Phòng 19-20)
            0, 30          // Q10 (Phòng 21-22)
        ];

        const pad = (n) => String(n).padStart(2, '0');

        const allNewShowtimes = [];
        const movieShowtimeCount = new Map(movieIds.map(id => [id, 0]));

        console.log('\n📌 4. Đang lập lịch và tính toán giờ chiếu tối ưu (Chống xung đột phòng)...');

        for (let dayIdx = 0; dayIdx < dates.length; dayIdx++) {
            const { dateStr, year, month, day, dayOfWeek } = dates[dayIdx];
            const isWeekend = (dayOfWeek === 0 || dayOfWeek === 6);

            // Xây dựng danh sách phim chiếu trong ngày (Daily Pool)
            // Đảm bảo toàn bộ 60 phim đều xuất hiện ít nhất 2 lần/ngày
            const dayPool = [];
            // Vòng 1: Tất cả 60 phim xoay tua theo offset ngày
            for (let i = 0; i < 60; i++) {
                dayPool.push(movieIds[(i + dayIdx * 7) % 60]);
            }
            // Vòng 2: Tất cả 60 phim xoay tua theo offset thứ 2
            for (let i = 0; i < 60; i++) {
                dayPool.push(movieIds[(i + dayIdx * 13 + 31) % 60]);
            }
            // Vòng 3: Bổ sung 40 suất cho các phim hot/bom tấn
            for (let i = 0; i < 40; i++) {
                dayPool.push(movieIds[(i + dayIdx * 19 + 5) % 60]);
            }

            let poolPointer = 0;

            for (let rIdx = 0; rIdx < rooms.length; rIdx++) {
                const room = rooms[rIdx];
                const offsetMin = roomStartOffsets[rIdx] || 0;

                // Suất đầu tiên trong ngày bắt đầu từ 08:30 + offset phòng
                let currentTotalMinutes = 8 * 60 + 30 + offsetMin;

                // Lập lịch các suất chiếu đến trước 23:30 (suất muộn nhất có thể bắt đầu lúc 23:15 - 23:30)
                while (currentTotalMinutes <= 23 * 60 + 20) {
                    const movieId = dayPool[poolPointer % dayPool.length];
                    poolPointer++;

                    const movie = movieMap.get(movieId);
                    const duration = movie ? movie.duration : 110;
                    const bufferMinutes = 15;

                    // Tính thời gian bắt đầu
                    const startH = Math.floor(currentTotalMinutes / 60);
                    const startM = currentTotalMinutes % 60;
                    const startTimeStr = `${dateStr} ${pad(startH)}:${pad(startM)}:00`;

                    // Tính thời gian kết thúc = bắt đầu + thời lượng phim + thời gian đệm dọn phòng
                    const endTotalMinutes = currentTotalMinutes + duration + bufferMinutes;
                    
                    // Xử lý chuyển ngày nếu suất chiếu kết thúc qua nửa đêm
                    let endYear = year;
                    let endMonth = month;
                    let endDay = day;
                    let endH = Math.floor(endTotalMinutes / 60);
                    let endM = endTotalMinutes % 60;

                    if (endH >= 24) {
                        endH -= 24;
                        const nextD = new Date(year, month - 1, day + 1);
                        endYear = nextD.getFullYear();
                        endMonth = nextD.getMonth() + 1;
                        endDay = nextD.getDate();
                    }
                    const endTimeStr = `${endYear}-${pad(endMonth)}-${pad(endDay)} ${pad(endH)}:${pad(endM)}:00`;

                    // Tính giá vé cơ bản theo loại màn chiếu và khung giờ
                    const isEvening = (startH >= 17);
                    let basePrice = 80000;

                    if (room.screen_type === 'IMAX') {
                        basePrice = (isEvening || isWeekend) ? 140000 : 120000;
                    } else if (room.screen_type === '3D') {
                        basePrice = (isEvening || isWeekend) ? 110000 : 95000;
                    } else {
                        // 2D
                        basePrice = (isEvening || isWeekend) ? 90000 : 80000;
                    }

                    allNewShowtimes.push([
                        movieId,
                        room.id,
                        startTimeStr,
                        endTimeStr,
                        bufferMinutes,
                        basePrice,
                        'scheduled'
                    ]);

                    movieShowtimeCount.set(movieId, (movieShowtimeCount.get(movieId) || 0) + 1);

                    // Suất tiếp theo bắt đầu sau khi suất hiện tại kết thúc (làm tròn lên bội số 5 phút)
                    // Đảm bảo startTime tiếp theo luôn >= endTime hiện tại => 100% KHÔNG BAO GIỜ XUNG ĐỘT
                    currentTotalMinutes = Math.ceil(endTotalMinutes / 5) * 5;
                }
            }
        }

        console.log(`   ✅ Đã sinh thành công ${allNewShowtimes.length} suất chiếu mới!`);
        console.log(`   - Trung bình: ${Math.round(allNewShowtimes.length / dates.length)} suất chiếu/ngày trên 22 phòng.`);

        // 5. Kiểm tra phân bổ phim
        let minMovieShows = Infinity;
        let maxMovieShows = -Infinity;
        movieShowtimeCount.forEach((count, mId) => {
            if (count < minMovieShows) minMovieShows = count;
            if (count > maxMovieShows) maxMovieShows = count;
        });
        console.log(`   - Mỗi phim có từ ${minMovieShows} đến ${maxMovieShows} suất chiếu (trung bình ~${Math.round(allNewShowtimes.length / 60)} suất/phim).`);

        // 6. Chèn vào CSDL MySQL theo từng Batch 500 bản ghi để tối ưu tốc độ
        console.log('\n📌 5. Đang nạp dữ liệu vào bảng showtimes trong MySQL (Batch Insert)...');
        const batchSize = 500;
        let insertedCount = 0;

        for (let i = 0; i < allNewShowtimes.length; i += batchSize) {
            const batch = allNewShowtimes.slice(i, i + batchSize);
            const sql = 'INSERT INTO showtimes (movie_id, room_id, start_time, end_time, buffer_minutes, base_price, status) VALUES ?';
            await conn.query(sql, [batch]);
            insertedCount += batch.length;
            if (insertedCount % 2000 === 0 || insertedCount === allNewShowtimes.length) {
                console.log(`   -> Đã nạp ${insertedCount} / ${allNewShowtimes.length} suất chiếu (${Math.round(insertedCount / allNewShowtimes.length * 100)}%)...`);
            }
        }

        // 7. Tổng kết cơ sở dữ liệu
        const [totalSt] = await conn.query('SELECT COUNT(*) as count, MIN(start_time) as min_date, MAX(start_time) as max_date FROM showtimes');
        console.log('\n====================================================================');
        console.log('🎉 HOÀN THÀNH THÊM SUẤT CHIẾU CHO TẤT CẢ PHIM ĐANG CHIẾU!');
        console.log(`- Tổng số suất chiếu hiện có trong CSDL: ${totalSt[0].count} suất`);
        console.log(`- Suất chiếu sớm nhất: ${totalSt[0].min_date}`);
        console.log(`- Suất chiếu muộn nhất: ${totalSt[0].max_date}`);
        console.log('====================================================================\n');

    } catch (err) {
        console.error('❌ LỖI TRONG QUÁ TRÌNH TẠO SUẤT CHIẾU:', err);
    } finally {
        if (conn) conn.release();
        process.exit(0);
    }
}

addShowtimes();
