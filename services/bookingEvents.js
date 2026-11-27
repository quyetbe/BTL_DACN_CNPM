const { EventEmitter } = require('events');

// Event bus thời gian thực chia sẻ giữa Cổng Khách Hàng (:3000) và Cổng Admin/Manager (:3001)
const bookingEvents = new EventEmitter();
bookingEvents.setMaxListeners(200);

function emitBookingEvent(type, payload) {
    bookingEvents.emit('booking_change', {
        type,
        timestamp: Date.now(),
        ...payload
    });
}

module.exports = {
    bookingEvents,
    emitBookingEvent
};
