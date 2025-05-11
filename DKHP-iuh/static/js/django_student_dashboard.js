// JavaScript cho trang dashboard sinh viên Django

document.addEventListener('DOMContentLoaded', function() {
    // Khởi tạo các thành phần Bootstrap
    initBootstrapComponents();
    
    // Tải dữ liệu dashboard
    loadDashboardData();
    
    // Thiết lập các sự kiện
    setupEventListeners();
    
    // Hiển thị thông báo chào mừng
    showWelcomeToast();
});

/**
 * Khởi tạo các thành phần Bootstrap
 */
function initBootstrapComponents() {
    // Khởi tạo tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Khởi tạo popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
}

/**
 * Tải dữ liệu dashboard từ API
 */
function loadDashboardData() {
    // Giả lập việc tải dữ liệu từ API
    console.log('Đang tải dữ liệu dashboard...');
    
    // Trong thực tế, đây sẽ là các cuộc gọi API đến backend Django
    // Ví dụ:
    // fetch('/api/student/dashboard')
    //     .then(response => response.json())
    //     .then(data => {
    //         updateDashboardUI(data);
    //     })
    //     .catch(error => {
    //         console.error('Lỗi khi tải dữ liệu dashboard:', error);
    //         showErrorToast('Không thể tải dữ liệu dashboard. Vui lòng thử lại sau.');
    //     });
    
    // Giả lập dữ liệu
    const mockData = {
        studentInfo: {
            name: 'Nguyễn Văn A',
            studentId: '2021001234',
            class: 'CNTT-K15',
            faculty: 'Công nghệ Thông tin',
            currentSemester: 'Học kỳ 1 - Năm học 2023-2024'
        },
        stats: {
            registeredCredits: 18,
            accumulatedCredits: 45,
            gpa: 3.2,
            tuitionDebt: 0
        },
        courses: [
            {
                code: 'INT1234',
                name: 'Lập trình Web',
                lecturer: 'TS. Nguyễn Văn B',
                schedule: 'Thứ 2, Tiết 1-3',
                room: 'P.301'
            },
            {
                code: 'INT1235',
                name: 'Cơ sở dữ liệu',
                lecturer: 'ThS. Trần Thị C',
                schedule: 'Thứ 3, Tiết 4-6',
                room: 'P.302'
            },
            {
                code: 'INT1236',
                name: 'Lập trình di động',
                lecturer: 'TS. Lê Văn D',
                schedule: 'Thứ 5, Tiết 1-3',
                room: 'P.303'
            },
            {
                code: 'INT1237',
                name: 'Mạng máy tính',
                lecturer: 'ThS. Phạm Thị E',
                schedule: 'Thứ 6, Tiết 4-6',
                room: 'P.304'
            }
        ],
        announcements: [
            {
                title: 'Lịch thi cuối kỳ học kỳ 1',
                content: 'Thông báo lịch thi cuối kỳ học kỳ 1 năm học 2023-2024...',
                date: '3 ngày trước'
            },
            {
                title: 'Hướng dẫn đăng ký học phần',
                content: 'Hướng dẫn chi tiết quy trình đăng ký học phần học kỳ 2...',
                date: '1 tuần trước'
            },
            {
                title: 'Thông báo về học phí',
                content: 'Thông báo về việc nộp học phí học kỳ 2 năm học 2023-2024...',
                date: '2 tuần trước'
            }
        ],
        upcomingEvents: [
            {
                title: 'Hạn cuối đăng ký học phần',
                description: 'Hạn cuối đăng ký học phần học kỳ 2 năm học 2023-2024',
                daysLeft: 5
            },
            {
                title: 'Thi cuối kỳ môn Lập trình Web',
                description: 'Thi cuối kỳ môn Lập trình Web - Phòng 301',
                daysLeft: 10
            },
            {
                title: 'Hạn cuối nộp học phí',
                description: 'Hạn cuối nộp học phí học kỳ 2 năm học 2023-2024',
                daysLeft: 15
            }
        ]
    };
    
    // Cập nhật UI với dữ liệu
    updateDashboardUI(mockData);
}

/**
 * Cập nhật UI với dữ liệu từ API
 * @param {Object} data - Dữ liệu từ API
 */
function updateDashboardUI(data) {
    // Cập nhật thông tin sinh viên
    document.querySelector('.card-title').textContent = data.studentInfo.name;
    document.querySelectorAll('.card-text')[0].innerHTML = `<strong>MSSV:</strong> ${data.studentInfo.studentId}`;
    document.querySelectorAll('.card-text')[1].innerHTML = `<strong>Lớp:</strong> ${data.studentInfo.class}`;
    document.querySelectorAll('.card-text')[2].innerHTML = `<strong>Khoa:</strong> ${data.studentInfo.faculty}`;
    document.querySelectorAll('.card-text')[3].innerHTML = `<strong>Học kỳ hiện tại:</strong> ${data.studentInfo.currentSemester}`;
    
    // Cập nhật thống kê
    document.querySelectorAll('.bg-primary h2')[0].textContent = data.stats.registeredCredits;
    document.querySelectorAll('.bg-success h2')[0].textContent = data.stats.accumulatedCredits;
    document.querySelectorAll('.bg-warning h2')[0].textContent = data.stats.gpa;
    document.querySelectorAll('.bg-danger h2')[0].textContent = `${data.stats.tuitionDebt}đ`;
    
    // Cập nhật bảng học phần
    const coursesTableBody = document.querySelector('table tbody');
    coursesTableBody.innerHTML = '';
    
    data.courses.forEach(course => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${course.code}</td>
            <td>${course.name}</td>
            <td>${course.lecturer}</td>
            <td>${course.schedule}</td>
            <td>${course.room}</td>
        `;
        coursesTableBody.appendChild(row);
    });
    
    // Cập nhật thông báo
    const announcementsList = document.querySelector('.list-group-flush');
    announcementsList.innerHTML = '';
    
    data.announcements.forEach(announcement => {
        const item = document.createElement('a');
        item.className = 'list-group-item list-group-item-action';
        item.href = '#';
        item.innerHTML = `
            <div class="d-flex w-100 justify-content-between">
                <h6 class="mb-1">${announcement.title}</h6>
                <small class="text-muted">${announcement.date}</small>
            </div>
            <p class="mb-1">${announcement.content}</p>
        `;
        announcementsList.appendChild(item);
    });
    
    // Cập nhật sự kiện sắp tới
    const eventsList = document.querySelectorAll('.list-group-flush')[1];
    eventsList.innerHTML = '';
    
    data.upcomingEvents.forEach(event => {
        const item = document.createElement('div');
        item.className = 'list-group-item';
        item.innerHTML = `
            <div class="d-flex w-100 justify-content-between">
                <h6 class="mb-1">${event.title}</h6>
                <small class="text-danger">Còn ${event.daysLeft} ngày</small>
            </div>
            <p class="mb-1">${event.description}</p>
        `;
        eventsList.appendChild(item);
    });
}

/**
 * Thiết lập các sự kiện
 */
function setupEventListeners() {
    // Sự kiện cho các nút lọc thời gian
    const timeFilterButtons = document.querySelectorAll('.btn-group .btn');
    timeFilterButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Xóa active class từ tất cả các nút
            timeFilterButtons.forEach(btn => btn.classList.remove('active'));
            // Thêm active class cho nút được nhấp
            this.classList.add('active');
            
            // Trong thực tế, đây sẽ là nơi để lọc dữ liệu theo thời gian
            console.log(`Đã chọn lọc theo: ${this.textContent}`);
        });
    });
    
    // Sự kiện cho các liên kết trong sidebar
    const sidebarLinks = document.querySelectorAll('.sidebar .nav-link');
    sidebarLinks.forEach(link => {
        link.addEventListener('click', function() {
            // Xóa active class từ tất cả các liên kết
            sidebarLinks.forEach(l => l.classList.remove('active'));
            // Thêm active class cho liên kết được nhấp
            this.classList.add('active');
        });
    });
    
    // Sự kiện cho các thông báo
    const announcementLinks = document.querySelectorAll('.list-group-item-action');
    announcementLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const title = this.querySelector('h6').textContent;
            showInfoToast(`Đang mở thông báo: ${title}`);
        });
    });
}

/**
 * Hiển thị thông báo chào mừng
 */
function showWelcomeToast() {
    const toastContainer = document.querySelector('.toast-container');
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.setAttribute('aria-atomic', 'true');
    
    toast.innerHTML = `
        <div class="toast-header">
            <i class="fas fa-info-circle me-2 text-primary"></i>
            <strong class="me-auto">Chào mừng</strong>
            <small>Vừa xong</small>
            <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
        <div class="toast-body">
            Chào mừng bạn quay trở lại hệ thống đăng ký học phần!
        </div>
    `;
    
    toastContainer.appendChild(toast);
    const bsToast = new bootstrap.Toast(toast, { delay: 3000 });
    bsToast.show();
}

/**
 * Hiển thị thông báo thông tin
 * @param {string} message - Nội dung thông báo
 */
function showInfoToast(message) {
    const toastContainer = document.querySelector('.toast-container');
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.setAttribute('aria-atomic', 'true');
    
    toast.innerHTML = `
        <div class="toast-header">
            <i class="fas fa-info-circle me-2 text-primary"></i>
            <strong class="me-auto">Thông tin</strong>
            <small>Vừa xong</small>
            <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
        <div class="toast-body">
            ${message}
        </div>
    `;
    
    toastContainer.appendChild(toast);
    const bsToast = new bootstrap.Toast(toast, { delay: 3000 });
    bsToast.show();
}

/**
 * Hiển thị thông báo lỗi
 * @param {string} message - Nội dung thông báo lỗi
 */
function showErrorToast(message) {
    const toastContainer = document.querySelector('.toast-container');
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.setAttribute('aria-atomic', 'true');
    
    toast.innerHTML = `
        <div class="toast-header">
            <i class="fas fa-exclamation-circle me-2 text-danger"></i>
            <strong class="me-auto">Lỗi</strong>
            <small>Vừa xong</small>
            <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
        <div class="toast-body">
            ${message}
        </div>
    `;
    
    toastContainer.appendChild(toast);
    const bsToast = new bootstrap.Toast(toast, { delay: 5000 });
    bsToast.show();
} 