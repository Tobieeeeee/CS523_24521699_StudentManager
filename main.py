# main.py
import tkinter as tk
from tkinter import messagebox
from core import func 

# --- CÁC HÀM XỬ LÝ GIAO DIỆN ĐỘNG ---

current_entries = {}

def clear_dynamic_frame():
    for widget in dynamic_frame.winfo_children():
        widget.destroy()
    current_entries.clear()

def show_default_message():
    clear_dynamic_frame()
    tk.Label(dynamic_frame, text="👇 Vui lòng chọn chức năng ở trên", font=("Arial", 10, "italic"), fg="gray").pack(pady=50)

def show_add_form():
    clear_dynamic_frame()
    tk.Label(dynamic_frame, text="--- THÊM SINH VIÊN ---", font=("Arial", 12, "bold"), fg="blue").pack(pady=10)
    
    fields = [("Mã SV", "id"), ("Họ và Tên", "name"), ("Giới tính", "gender"), ("Khoa", "faculty"), ("Ngành", "major")]
    for label_text, key in fields:
        tk.Label(dynamic_frame, text=label_text + ":").pack(anchor=tk.W)
        ent = tk.Entry(dynamic_frame, width=35)
        ent.pack(pady=2)
        current_entries[key] = ent
        
    tk.Button(dynamic_frame, text="Xác nhận Thêm", bg="lightblue", command=submit_add).pack(pady=15)

def show_delete_form():
    clear_dynamic_frame()
    tk.Label(dynamic_frame, text="--- XÓA SINH VIÊN ---", font=("Arial", 12, "bold"), fg="red").pack(pady=10)
    
    tk.Label(dynamic_frame, text="Nhập Mã SV cần xóa:").pack(anchor=tk.W)
    ent = tk.Entry(dynamic_frame, width=35)
    ent.pack(pady=2)
    current_entries["id"] = ent
    
    tk.Button(dynamic_frame, text="Xác nhận Xóa", bg="#ffcccc", command=submit_delete).pack(pady=15)

def show_search_id_form():
    clear_dynamic_frame()
    tk.Label(dynamic_frame, text="--- TÌM THEO MÃ SV ---", font=("Arial", 12, "bold")).pack(pady=10)
    
    tk.Label(dynamic_frame, text="Nhập Mã SV cần tìm:").pack(anchor=tk.W)
    ent = tk.Entry(dynamic_frame, width=35)
    ent.pack(pady=2)
    current_entries["id"] = ent
    
    tk.Button(dynamic_frame, text="Tìm Kiếm", bg="#e6e6e6", command=submit_search_id).pack(pady=15)

def show_search_name_form():
    clear_dynamic_frame()
    tk.Label(dynamic_frame, text="--- TÌM THEO TÊN ---", font=("Arial", 12, "bold")).pack(pady=10)
    
    tk.Label(dynamic_frame, text="Nhập Tên cần tìm:").pack(anchor=tk.W)
    ent = tk.Entry(dynamic_frame, width=35)
    ent.pack(pady=2)
    current_entries["name"] = ent
    
    tk.Button(dynamic_frame, text="Tìm Kiếm", bg="#e6e6e6", command=submit_search_name).pack(pady=15)


# --- CÁC HÀM XỬ LÝ LOGIC ---

def refresh_display(message=""):
    state_str = func.get_current_state_string()
    if message:
        state_str = f"--- THÔNG BÁO: {message} ---\n\n" + state_str
    txt_display.delete("1.0", tk.END)
    txt_display.insert(tk.END, state_str)

def submit_add():
    sv_id = current_entries["id"].get().strip()
    name = current_entries["name"].get().strip()
    gender = current_entries["gender"].get().strip()
    faculty = current_entries["faculty"].get().strip()
    major = current_entries["major"].get().strip()

    if not all([sv_id, name, gender, faculty, major]):
        messagebox.showwarning("Thiếu thông tin", "Vui lòng điền đủ 5 trường!")
        return

    success, msg = func.add_student(sv_id, name, gender, faculty, major)
    if success:
        for ent in current_entries.values():
            ent.delete(0, tk.END)
        refresh_display(msg)
    else:
        messagebox.showerror("Lỗi", msg)

def submit_delete():
    sv_id = current_entries["id"].get().strip()
    if not sv_id:
        messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập Mã SV!")
        return
    
    success, msg = func.delete_student(sv_id)
    if success:
        current_entries["id"].delete(0, tk.END)
        refresh_display(msg)
    else:
        messagebox.showerror("Lỗi", msg)

def submit_search_id():
    sv_id = current_entries["id"].get().strip()
    if not sv_id:
        messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập Mã SV!")
        return
    success, sv_id_res, sv_info = func.search_student_by_id(sv_id)
    show_search_result(success, sv_id_res, sv_info, f"Mã SV: {sv_id}")

def submit_search_name():
    name = current_entries["name"].get().strip()
    if not name:
        messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập Tên!")
        return
    success, sv_id_res, sv_info = func.search_student_by_Ten(name)
    show_search_result(success, sv_id_res, sv_info, f"Tên: {name}")

def show_search_result(success, sv_id_result, sv_info, search_term):
    if success:
        res_text = f"--- KẾT QUẢ TÌM KIẾM ({search_term}) ---\n"
        res_text += f"Tìm thấy trên Index. Thông tin từ Bảng Gốc:\n"
        res_text += f"[{sv_id_result}] {sv_info['Ten']} - {sv_info['gt']} - {sv_info['Khoa']} - {sv_info['Nganh']}\n\n"
        res_text += func.get_current_state_string()
        txt_display.delete("1.0", tk.END)
        txt_display.insert(tk.END, res_text)
    else:
        messagebox.showinfo("Kết quả", "Không tìm thấy sinh viên!")


# --- KHỞI TẠO CỬA SỔ CHÍNH ---

func.add_student("24521699", "Nguyen Van Quoc Thinh", "Nam", "KHMT", "KHMT")
func.add_student("24521437", "Le Thi Gi Do", "Nu", "HTTT", "HTTT")
func.add_student("24523543", "Nguyen Van Gi Do", "Nam", "KTMT", "KTMT")

root = tk.Tk()
root.title("Ứng Dụng Quản Lý Sinh Viên - B-Tree")
root.geometry("900x600")

# Bố cục Trái (Control) và Phải (Display)
left_panel = tk.Frame(root, width=300, padx=10, pady=10)
left_panel.pack(side=tk.LEFT, fill=tk.Y)

right_panel = tk.Frame(root, padx=10, pady=10)
right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# 1. Khu vực Nút bấm Chọn Chức Năng
btn_frame = tk.Frame(left_panel)
btn_frame.pack(fill=tk.X, pady=10)

tk.Button(btn_frame, text="Thêm SV", width=12, command=show_add_form).grid(row=0, column=0, padx=5, pady=5)
tk.Button(btn_frame, text="Xóa SV", width=12, command=show_delete_form).grid(row=0, column=1, padx=5, pady=5)
tk.Button(btn_frame, text="Tìm theo Mã", width=12, command=show_search_id_form).grid(row=1, column=0, padx=5, pady=5)
tk.Button(btn_frame, text="Tìm theo Tên", width=12, command=show_search_name_form).grid(row=1, column=1, padx=5, pady=5)

# Đường kẻ ngang phân cách
tk.Frame(left_panel, height=2, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, pady=10)

# 2. Khu vực Form nhập liệu Động (Thay đổi tùy nút bấm)
dynamic_frame = tk.Frame(left_panel)
dynamic_frame.pack(fill=tk.BOTH, expand=True)

# 3. Khu vực Màn hình Đen
tk.Label(right_panel, text="MÀN HÌNH THEO DÕI B-TREE & BẢNG GỐC", font=("Arial", 12, "bold")).pack(pady=5)
txt_display = tk.Text(right_panel, width=60, height=30, bg="#282c34", fg="white", font=("Courier", 11))
txt_display.pack(fill=tk.BOTH, expand=True)

# Khởi động app: Gọi hàm hiển thị thông báo "vui lòng chọn..." thay vì form Thêm
show_default_message()
refresh_display()

root.mainloop()