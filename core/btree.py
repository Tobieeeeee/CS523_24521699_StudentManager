# core/btree.py
MAX_KEYS = 2

def tao_node(is_leaf=False):
    """
    Tạo một node mới cho cấu trúc B-Tree.
    
    Args:
        is_leaf (bool): Xác định xem node mới tạo có phải là node lá hay không. Mặc định là False.
        
    Returns:
        dict: Một dictionary đại diện cho một node, bao gồm trạng thái lá (leaf), 
              danh sách các khóa (keys) và danh sách các nhánh con (children).
    """
    return {
        "leaf": is_leaf,
        "keys": [],       # Chứa các tuple: (key_val, student_id)
        "children": []    # Chứa các node con
    }

def tim_kiem_key(node, key):
    """
    Tìm kiếm một key cụ thể bên trong cây B-Tree.
    
    Args:
        node (dict): Node hiện tại đang được xét (thường bắt đầu từ root).
        key (str/int): Giá trị khóa cần tìm kiếm (có thể là Mã SV hoặc Họ Tên).
        
    Returns:
        tuple: Trả về tuple (key_val, student_id) nếu tìm thấy.
        None: Nếu đã duyệt hết các node lá mà không tìm thấy.
    """
    i = 0
    while i < len(node["keys"]) and key > node["keys"][i][0]:
        i += 1
    if i < len(node["keys"]) and key == node["keys"][i][0]:
        return node["keys"][i]
    elif node["leaf"]:
        return None
    else:
        return tim_kiem_key(node["children"][i], key)

def chia_node_con(x, i):
    """
    Chia tách (split) một node con khi node này đã chứa tối đa số lượng khóa cho phép.
    
    Args:
        x (dict): Node cha.
        i (int): Vị trí (index) của node con đang bị đầy bên trong danh sách children của node cha x.
    """
    t = (MAX_KEYS + 1) // 2
    y = x["children"][i]
    z = tao_node(y["leaf"])
    
    x["children"].insert(i + 1, z)
    x["keys"].insert(i, y["keys"][t])
    
    z["keys"] = y["keys"][t + 1:]
    y["keys"] = y["keys"][:t]
    
    if not y["leaf"]:
        z["children"] = y["children"][t + 1:]
        y["children"] = y["children"][:t + 1]

def them_tuple_vao_node_chua_day(x, k_tuple):
    """
    Chèn một phần tử mới vào một node khi biết chắc chắn rằng node đó chưa bị đầy.
    Hàm này có thể tự động duyệt đệ quy xuống các nhánh con để tìm đúng vị trí chèn.
    
    Args:
        x (dict): Node hiện tại đang xét.
        k_tuple (tuple): Dữ liệu cần chèn, định dạng (khóa, giá_trị).
    """
    i = len(x["keys"]) - 1
    if x["leaf"]:
        x["keys"].append((None, None))
        while i >= 0 and k_tuple[0] < x["keys"][i][0]:
            x["keys"][i + 1] = x["keys"][i]
            i -= 1
        x["keys"][i + 1] = k_tuple
    else:
        while i >= 0 and k_tuple[0] < x["keys"][i][0]:
            i -= 1
        i += 1
        if len(x["children"][i]["keys"]) == MAX_KEYS:
            chia_node_con(x, i)
            if k_tuple[0] > x["keys"][i][0]:
                i += 1
        them_tuple_vao_node_chua_day(x["children"][i], k_tuple)

def them_tuple_vao_btree(root, k_tuple):
    """
    Hàm điều phối chính để thêm phần tử vào cây B-Tree. 
    Kiểm tra tình trạng của Node gốc (root) trước tiên để đảm bảo cây luôn cân bằng.
    
    Args:
        root (dict): Node gốc hiện tại của cây.
        k_tuple (tuple): Dữ liệu cần thêm vào cây.
        
    Returns:
        dict: Node gốc mới của cây (root có thể bị thay đổi nếu xảy ra tràn node và tách).
    """
    if len(root["keys"]) == MAX_KEYS:
        new_root = tao_node()
        new_root["children"].insert(0, root)
        chia_node_con(new_root, 0)
        them_tuple_vao_node_chua_day(new_root, k_tuple)
        return new_root
    else:
        them_tuple_vao_node_chua_day(root, k_tuple)
        return root

def lay_tat_ca_tuple(node, items=None):
    """
    Duyệt cây theo thứ tự (In-order traversal) để thu thập tất cả các phần tử đang có.
    
    Args:
        node (dict): Node bắt đầu duyệt (thường là root).
        items (list): Danh sách lưu trữ các phần tử (dùng cho đệ quy).
        
    Returns:
        list: Một danh sách chứa tất cả các tuple (khóa, giá_trị) trong cây, đã được sắp xếp tăng dần.
    """
    if items is None:
        items = []
    for i in range(len(node["keys"])):
        if not node["leaf"]:
            lay_tat_ca_tuple(node["children"][i], items)
        items.append(node["keys"][i])
    if not node["leaf"]:
        lay_tat_ca_tuple(node["children"][len(node["keys"])], items)
    return items

def xay_dung_lai_btree_bo_qua_key(old_root, key_val):
    """
    Giải pháp đơn giản để xóa phần tử trên B-Tree: 
    Lấy toàn bộ dữ liệu ra, loại bỏ phần tử cần xóa, và xây dựng lại một cây hoàn toàn mới.
    
    Args:
        old_root (dict): Node gốc của cây B-Tree hiện tại.
        key_val (str/int): Giá trị khóa của phần tử cần loại bỏ.
        
    Returns:
        dict: Node gốc của cây B-Tree mới đã được dọn dẹp.
    """
    items = lay_tat_ca_tuple(old_root)
    new_root = tao_node(True)
    for item in items:
        if item[0] != key_val:
            new_root = them_tuple_vao_btree(new_root, item)
    return new_root