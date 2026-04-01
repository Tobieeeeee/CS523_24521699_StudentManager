# Thông tin cá nhân
* **Họ và Tên:** Nguyễn Văn Quốc Thịnh
* **Mã SV:** 24521699

---

# Ứng Dụng Quản Lý Sinh Viên - Cấu Trúc B-Tree

Ứng dụng quản lý sinh viên mô phỏng hoạt động của hệ quản trị cơ sở dữ liệu (DBMS). Dữ liệu chi tiết được lưu trữ tại Bảng gốc (Main Table), trong khi thao tác truy xuất và tìm kiếm được tăng tốc thông qua Cấu trúc chỉ mục B-Tree (Bậc 3).

## Tính năng nổi bật
- **Thêm sinh viên:** Tự động chèn dữ liệu vào bảng gốc và phân nhánh trên B-Tree.
- **Xóa sinh viên:** Cập nhật lại toàn bộ cây chỉ mục để tránh phân mảnh và lỗi trùng lặp tên.
- **Tìm kiếm siêu tốc:** Hỗ trợ tra cứu theo Mã SV và Họ Tên bằng thuật toán tìm kiếm của B-Tree.
- **Theo dõi thời gian thực (Real-time tracking):** Giao diện cập nhật trực tiếp sự biến đổi của B-Tree mỗi khi có thao tác làm thay đổi dữ liệu (tách node, gộp node).

## Cấu trúc thư mục
Dự án được thiết kế theo mô hình tách biệt logic và giao diện:

```text
CS523_24521699_StudentManager/
├── core/
│   ├── btree.py        # Lõi thuật toán Cấu trúc dữ liệu B-Tree
│   └── func.py         # Logic nghiệp vụ quản lý (Thêm, Xóa, Tìm kiếm)
└── main.py             # Giao diện đồ họa (GUI) sử dụng Tkinter
```

##  Hướng dẫn cài đặt và sử dụng
Ứng dụng sử dụng thư viện `tkinter` có sẵn của Python, không cần cài đặt thêm thư viện ngoài.

1. Clone repository này về máy:
```bash
git clone https://github.com/Tobieeeeee/CS523_24521699_StudentManager.git
```

2. Di chuyển vào thư mục dự án:
```bash
cd CS523_24521699_StudentManager
```

3. Chạy file giao diện chính:
```bash
python main.py
```
