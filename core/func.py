# core/func.py
from core import btree 

# Khởi tạo Bảng gốc và 2 cây chỉ mục B-Tree
main_table = {} 
root_id_index = btree.tao_node(True)
root_Ten_index = btree.tao_node(True)

def add_student(sv_id, Ten, gt, Khoa, Nganh):
    """
    Thêm một sinh viên mới vào hệ thống.
    Lưu dữ liệu chi tiết vào Bảng gốc và tạo khóa tra cứu trên 2 cây B-Tree Index.
    
    Args:
        sv_id (str): Mã sinh viên (Khóa chính, không được trùng lặp).
        Ten (str): Họ và Tên sinh viên.
        gt (str): Giới tính.
        Khoa (str): Khoa đang theo học.
        Nganh (str): Ngành học cụ thể.
        
    Returns:
        tuple (bool, str): Trạng thái thành công/thất bại và Thông báo tương ứng.
    """
    global root_id_index, root_Ten_index
    if sv_id in main_table:
        return False, "Lỗi: Mã sinh viên đã tồn tại!"
        
    # Lưu vào Bảng gốc
    main_table[sv_id] = {
        "Ten": Ten, "gt": gt, "Khoa": Khoa, "Nganh": Nganh
    }
    
    # Cập nhật 2 cây chỉ mục
    root_id_index = btree.them_tuple_vao_btree(root_id_index, (sv_id, sv_id))
    root_Ten_index = btree.them_tuple_vao_btree(root_Ten_index, (Ten, sv_id))
    return True, f"Đã thêm: {Ten}"

def delete_student(sv_id):
    """
    Xóa một sinh viên khỏi hệ thống dựa trên Mã sinh viên.
    Xóa dữ liệu ở Bảng gốc và xây dựng lại (rebuild) 2 cây B-Tree Index để đảm bảo đồng bộ.
    
    Args:
        sv_id (str): Mã sinh viên cần xóa.
        
    Returns:
        tuple (bool, str): Trạng thái thành công/thất bại và Thông báo tương ứng.
    """
    global root_id_index, root_Ten_index
    if sv_id not in main_table:
        return False, "Lỗi: Không tìm thấy sinh viên!"
    
    # Xóa khỏi Bảng gốc
    del main_table[sv_id]
    
    # Xây dựng lại TOÀN BỘ 2 cây chỉ mục từ Bảng gốc mới để tránh lỗi trùng tên
    root_id_index = btree.tao_node(True)
    root_Ten_index = btree.tao_node(True)
    
    for k_id, v_info in main_table.items():
        root_id_index = btree.them_tuple_vao_btree(root_id_index, (k_id, k_id))
        root_Ten_index = btree.them_tuple_vao_btree(root_Ten_index, (v_info["Ten"], k_id))
        
    return True, f"Đã xóa sinh viên mã: {sv_id}"

def search_student_by_id(sv_id):
    """
    Tra cứu thông tin sinh viên thông qua Chỉ mục Mã SV.
    
    Args:
        sv_id (str): Mã sinh viên cần tìm.
        
    Returns:
        tuple (bool, str, dict): Trạng thái thành công, Mã SV tìm được, và Dictionary chứa thông tin chi tiết. 
                                 Trả về (False, None, None) nếu không tìm thấy.
    """
    result = btree.tim_kiem_key(root_id_index, sv_id)
    if result:
        sv_info = main_table[result[1]]
        return True, result[1], sv_info
    return False, None, None

def search_student_by_Ten(Ten):
    """
    Tra cứu thông tin sinh viên thông qua Chỉ mục Họ và Tên.
    
    Args:
        Ten (str): Tên sinh viên cần tìm.
        
    Returns:
        tuple (bool, str, dict): Trạng thái thành công, Mã SV tương ứng, và Dictionary chứa thông tin chi tiết.
                                 Trả về (False, None, None) nếu không tìm thấy.
    """
    result = btree.tim_kiem_key(root_Ten_index, Ten)
    if result:
        sv_info = main_table[result[1]]
        return True, result[1], sv_info
    return False, None, None

def get_btree_string(node, l=0):
    """
    Hàm đệ quy hỗ trợ chuyển đổi cấu trúc cây B-Tree thành một chuỗi văn bản (String) 
    có lề (indentation) phân tầng để dễ dàng hiển thị lên màn hình giao diện.
    
    Args:
        node (dict): Node hiện tại đang được bóc tách.
        l (int): Mức độ sâu (level) của node để lùi lề.
        
    Returns:
        str: Chuỗi văn bản thể hiện cấu trúc rẽ nhánh của cây.
    """
    res = "  " * l + str([k[0] for k in node["keys"]]) + "\n"
    if not node["leaf"]:
        for child in node["children"]:
            res += get_btree_string(child, l + 1)
    return res

def get_current_state_string():
    """
    Tổng hợp toàn bộ trạng thái dữ liệu hiện tại (bao gồm Bảng gốc và Cấu trúc B-Tree)
    thành một khối văn bản dài để đổ trực tiếp lên màn hình đen của giao diện Tkinter.
    
    Returns:
        str: Khối văn bản báo cáo tình trạng toàn bộ hệ thống.
    """
    res = "=================================================\n"
    res += "TRẠNG THÁI DỮ LIỆU HIỆN TẠI\n"
    res += "1. BẢNG GỐC (Main Table):\n"
    if not main_table:
        res += "   (Trống)\n"
    for k, v in main_table.items():
        res += f"   [{k}]: {v['Ten']} - {v['gt']} - Khoa: {v['Khoa']} - Ngành: {v['Nganh']}\n"
    
    res += "\n2. CHỈ MỤC THEO MÃ SV (B-Tree Bậc 3):\n"
    if main_table:
        res += get_btree_string(root_id_index)
    else:
        res += "   (Trống)\n"
    res += "=================================================\n"
    return res