# Hệ thống Đăng ký Học phần IUH

Hệ thống quản lý đăng ký học phần cho trường Đại học Công nghiệp TP.HCM (IUH).

## Cài đặt

1. Clone repository:
```bash
git clone https://github.com/yourusername/DKHP-iuh.git
cd DKHP-iuh
```

2. Tạo môi trường ảo và kích hoạt:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

3. Cài đặt các thư viện cần thiết:
```bash
pip install -r requirements.txt
```

4. Tạo file .env từ mẫu:
```bash
cp .env.example .env
```

5. Chỉnh sửa file .env với các thông tin phù hợp:
```
# Django settings
SECRET_KEY=your_secret_key_here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database settings
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=

# Email settings
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@example.com
EMAIL_HOST_PASSWORD=your_email_password

# Static and media files
STATIC_URL=/static/
MEDIA_URL=/media/
STATIC_ROOT=staticfiles/
MEDIA_ROOT=media/

# Security settings
CSRF_COOKIE_SECURE=False
SESSION_COOKIE_SECURE=False
SECURE_SSL_REDIRECT=False
```

6. Tạo cơ sở dữ liệu:
```bash
python manage.py makemigrations
python manage.py migrate
```

7. Tạo tài khoản quản trị:
```bash
python manage.py createsuperuser
```

8. Chạy máy chủ phát triển:
```bash
python manage.py runserver
```

## Cấu trúc dự án

- `administrators/`: Ứng dụng quản lý thông tin khóa học và quản trị viên
- `students/`: Ứng dụng quản lý thông tin sinh viên và đăng ký học phần
- `scheduling/`: Ứng dụng quản lý lịch học
- `notifications/`: Ứng dụng quản lý thông báo

## Tính năng

- Đăng ký học phần
- Quản lý lịch học
- Thông báo
- Quản lý khóa học
- Quản lý sinh viên

## Bảo mật

- Sử dụng biến môi trường cho các thông tin nhạy cảm
- Bảo vệ CSRF
- Xác thực người dùng
- Phân quyền truy cập

## Phát triển

### Chạy kiểm tra

```bash
python manage.py test
```

### Tạo migrations

```bash
python manage.py makemigrations
```

### Áp dụng migrations

```bash
python manage.py migrate
```

## Đóng góp

1. Fork repository
2. Tạo nhánh mới (`git checkout -b feature/amazing-feature`)
3. Commit thay đổi (`git commit -m 'Add some amazing feature'`)
4. Push lên nhánh (`git push origin feature/amazing-feature`)
5. Tạo Pull Request

## Giấy phép

Dự án này được cấp phép theo giấy phép MIT - xem file [LICENSE](LICENSE) để biết thêm chi tiết. 