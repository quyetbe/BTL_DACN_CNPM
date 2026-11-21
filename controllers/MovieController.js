const Movie = require('../models/Movie');
const Showtime = require('../models/Showtime');

class MovieController {
    static async detail(req, res) {
        try {
            const movieId = req.params.id;
            const movie = await Movie.findById(movieId);

            if (!movie) {
                return res.status(404).render('client/404', {
                    title: 'Không Tìm Thấy Phim',
                    message: 'Phim bạn đang tìm không tồn tại hoặc đã ngừng chiếu.'
                });
            }

            // Tạo danh sách 10 ngày tới
            const today = new Date();
            const dates = [];
            const daysOfWeek = ['Chủ Nhật', 'Thứ Hai', 'Thứ Ba', 'Thứ Tư', 'Thứ Năm', 'Thứ Sáu', 'Thứ Bảy'];

            for (let i = 0; i < 10; i++) {
                const d = new Date(today);
                d.setDate(d.getDate() + i);
                const pad = (n) => String(n).padStart(2, '0');
                const dateStr = `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
                const dayName = i === 0 ? 'Hôm nay' : (i === 1 ? 'Ngày mai' : daysOfWeek[d.getDay()]);
                const label = `${d.getDate()}/${d.getMonth() + 1}`;

                dates.push({
                    dateStr,
                    dayName,
                    label
                });
            }

            const selectedDate = req.query.date || dates[0].dateStr;

            // Nếu người dùng chọn một ngày xa hơn qua bộ chọn lịch, bổ sung tab đó vào danh sách
            if (req.query.date && !dates.some(d => d.dateStr === req.query.date)) {
                const parts = req.query.date.split('-');
                if (parts.length === 3) {
                    const selD = new Date(Number(parts[0]), Number(parts[1]) - 1, Number(parts[2]));
                    if (!isNaN(selD.getTime())) {
                        dates.push({
                            dateStr: req.query.date,
                            dayName: daysOfWeek[selD.getDay()],
                            label: `${selD.getDate()}/${selD.getMonth() + 1}`
                        });
                        dates.sort((a, b) => a.dateStr.localeCompare(b.dateStr));
                    }
                }
            }

            const showtimes = await Showtime.getByMovie(movieId, selectedDate);

            // Nhóm suất chiếu theo định dạng phòng (IMAX, 3D, 2D)
            const groupedShowtimes = {};
            showtimes.forEach(st => {
                const key = st.screen_type || '2D';
                if (!groupedShowtimes[key]) {
                    groupedShowtimes[key] = [];
                }
                groupedShowtimes[key].push(st);
            });

            const statusLabel = movie.status === 'now_showing' ? 'Phim Đang Chiếu' : 'Phim Sắp Chiếu';
            const breadcrumbs = [
                { label: 'Phim', url: '/movies' },
                { label: statusLabel, url: `/movies?status=${movie.status}` },
                { label: movie.title }
            ];

            res.render('client/movie-detail', {
                title: `${movie.title} - Lịch Chiếu & Đặt Vé`,
                movie,
                dates,
                selectedDate,
                groupedShowtimes,
                totalShowtimes: showtimes.length,
                breadcrumbs
            });
        } catch (err) {
            console.error('Lỗi chi tiết phim:', err);
            res.status(500).render('client/404', {
                title: '500 - Lỗi',
                message: 'Không thể tải chi tiết phim: ' + err.message
            });
        }
    }
}

module.exports = MovieController;
