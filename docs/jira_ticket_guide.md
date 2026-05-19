# 🎫 Hướng Dẫn Tạo Jira Ticket Chuẩn Cho QA Pipeline

## ✅ Quy Tắc Quan Trọng

Để AI **parse chính xác**, description phải có **3 section** với tên chuẩn:

| Section | Tên chấp nhận | Bắt buộc? |
|---------|--------------|-----------|
| Preconditions | `Preconditions` / `Precondition` / `Setup` / `Given` | Khuyến nghị |
| Steps | `Steps to Reproduce` / `Steps` / `When` | **BẮT BUỘC** |
| Expected | `Expected Result` / `Expected Results` / `Then` | **BẮT BUỘC** |

---

## 📋 Template Chuẩn – Copy vào Jira Description

> Dùng format **Jira Wiki Markup** hoặc **Atlassian Document Format**

```
h3. Preconditions
* <điều kiện 1>
* <điều kiện 2>
* <điều kiện 3>

h3. Steps to Reproduce
1. <bước 1>
2. <bước 2>
3. <bước 3>
4. <bước 4>
5. <bước 5>

h3. Expected Result
* <kết quả mong đợi 1>
* <kết quả mong đợi 2>
* <kết quả mong đợi 3>

h3. Actual Result
* <mô tả lỗi thực tế>
```

---

## 🐛 Mẫu 1 – Bug Report (Login Crash)

**Summary:**
```
[Android] Login screen crashes when tapping Login with empty password field
```

**Description:**
```
h3. Preconditions
* App đã được cài đặt trên thiết bị Android (API 31+)
* User đang ở màn hình Login (chưa đăng nhập)
* App đang ở trạng thái fresh install (chưa có session)

h3. Steps to Reproduce
1. Mở ứng dụng
2. Chờ màn hình Login hiển thị
3. Nhập email hợp lệ vào field Email: testuser@company.com
4. Để trống field Password (không nhập gì)
5. Tap vào nút "Login"

h3. Expected Result
* App hiển thị thông báo validation: "Password cannot be empty"
* App KHÔNG bị crash hoặc force close
* User vẫn ở lại màn hình Login
* Error message hiển thị màu đỏ phía dưới field Password

h3. Actual Result
* App bị crash ngay lập tức (force close)
* Xuất hiện dialog "App has stopped"
* User bị đẩy ra ngoài màn hình Login
```

**Các field:**
- Issue Type: `Bug`
- Priority: `High`
- Component: `authentication, login-screen`
- Label: `android, regression, P1`

---

## 📸 Mẫu 2 – Bug Report (Upload Không Có Progress)

**Summary:**
```
[iOS] Profile photo upload shows no progress indicator on slow network
```

**Description:**
```
h3. Preconditions
* User đã đăng nhập thành công
* User đang ở màn hình Profile  
* Thiết bị đang dùng kết nối 3G/slow network (có thể dùng network throttling)

h3. Steps to Reproduce
1. Tap vào avatar icon trên màn hình Profile
2. Chọn "Change Photo" từ bottom sheet menu
3. Chọn ảnh từ thư viện (kích thước > 2MB)
4. Tap "Confirm" để bắt đầu upload
5. Chờ và quan sát UI trong quá trình upload

h3. Expected Result
* Hiển thị progress bar/spinner trong khi upload đang diễn ra
* App KHÔNG bị freeze hoặc timeout mà không có feedback cho user
* Khi upload thành công: toast message "Photo updated successfully"
* Khi upload thất bại: hiển thị nút Retry kèm error message rõ ràng

h3. Actual Result
* Không có bất kỳ progress indicator nào
* App bị treo khoảng 30 giây rồi tự về màn hình Profile
* Không có toast success hoặc error message nào
```

**Các field:**
- Issue Type: `Bug`
- Priority: `Medium`
- Component: `profile, media-upload`
- Label: `ios, android, performance, regression`

---

## ✨ Mẫu 3 – Feature / Story (Biometric Login)

**Summary:**
```
[Feature] Add biometric authentication (Face ID / Fingerprint) to Login screen
```

**Description:**
```
h3. Preconditions
* User đã có tài khoản hợp lệ trong hệ thống
* Thiết bị đã được cài đặt biometric authentication (Face ID hoặc Fingerprint)
* User chưa đăng nhập (đang ở màn hình Login)

h3. Steps to Reproduce
1. Mở ứng dụng và vào màn hình Login
2. Tap vào nút "Login with Biometric" (Face ID / Touch ID)
3. Thực hiện xác thực biometric
4. Quan sát kết quả

h3. Expected Result
* Nút "Login with Biometric" hiển thị trên màn hình Login
* System prompt xác thực biometric (Face ID hoặc Fingerprint scan)
* Khi xác thực thành công: tự động đăng nhập và navigate sang Home screen
* Khi xác thực thất bại/cancel: hiển thị error message, user vẫn ở Login screen
* Biometric login hoạt động trên cả Android (Fingerprint) và iOS (Face ID / Touch ID)

h3. Acceptance Criteria
* Button biometric chỉ hiện khi device hỗ trợ và đã setup biometric
* Không lưu password trong local storage
* Fallback về email/password nếu biometric fail 3 lần
```

**Các field:**
- Issue Type: `Story`
- Priority: `High`
- Component: `authentication, security`
- Label: `android, ios, feature, smoke`

---

## 💡 Tips Để AI Parse Tốt Nhất

1. **Dùng heading h3.** trước mỗi section
2. **Số thứ tự cho Steps** (1. 2. 3.) – AI nhận dạng rõ hơn
3. **Dấu * cho bullet** trong Preconditions và Expected
4. **Label platform**: thêm `android` hoặc `ios` để AI detect đúng platform
5. **Label priority**: thêm `P1`, `P2` để map test priority
6. **Tránh**: viết tắt khó hiểu, không có section header

---

## 🔑 Cấu Trúc Field Jira Cần Set

```
Issue Type   : Bug / Story / Task
Summary      : [Platform] Mô tả ngắn gọn vấn đề
Description  : Theo template trên (có Preconditions + Steps + Expected)
Priority     : Highest / High / Medium / Low
Component/s  : tên module bị ảnh hưởng
Labels       : android, ios, regression, smoke, P1, P2, bug, feature
Assignee     : developer phụ trách
Reporter     : QA tạo ticket
```

