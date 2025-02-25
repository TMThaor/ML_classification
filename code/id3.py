import numpy as np
from collections import Counter

# Lớp xây dựng Cây quyết định ID3
class DecisionTreeID3:
    def __init__(self, max_depth=None, min_samples_split=5):
        # Khởi tạo độ sâu tối đa của cây và số lượng mẫu tối thiểu để tiếp tục chia
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.tree = None  # Cây sẽ được xây dựng và lưu ở đây
        self.most_common_label = None

    def fit(self, X, y, feature_names):
        # Lưu tên thuộc tính và bắt đầu xây dựng cây quyết định
        self.feature_names = feature_names
        self.most_common_label = Counter(y).most_common(1)[0][0]  # Lưu nhãn phổ biến nhất
        self.tree = self.build_tree(X, y)

    # Hàm đệ quy để xây dựng cây quyết định
    def build_tree(self, X, y, depth=0):
        # Điều kiện dừng 1: Nếu tất cả nhãn giống nhau, trả về nhãn đó
        if len(set(y)) == 1:
            return y[0]
        
        # Điều kiện dừng 2: Nếu số mẫu nhỏ hơn ngưỡng tối thiểu, trả về nhãn phổ biến nhất
        if len(y) < self.min_samples_split:
            return self.most_common_label
        
        # Điều kiện dừng 3: Nếu đã đạt đến độ sâu tối đa, trả về nhãn phổ biến nhất
        if self.max_depth is not None and depth >= self.max_depth:
            return self.most_common_label

        # Bước 1: Chọn thuộc tính (feature) có ích nhất dựa trên độ đo thông tin
        best_feature_index = self.best_feature_index(X, y)
        best_feature = self.feature_names[best_feature_index]

        # Bước 2: Tạo một nút mới trong cây, với thuộc tính tốt nhất là nút cha
        tree = {best_feature: {}}

        # Bước 3: Chia dữ liệu dựa trên các giá trị của thuộc tính tốt nhất
        for value in np.unique(X[:, best_feature_index]):
            X_sub = X[X[:, best_feature_index] == value]  # Tập con của X với giá trị hiện tại của thuộc tính
            y_sub = y[X[:, best_feature_index] == value]  # Nhãn tương ứng của tập con
            
            # Bước 4: Gọi đệ quy để xây dựng cây con cho tập con
            if len(y_sub) > 0:
                subtree = self.build_tree(X_sub, y_sub, depth + 1)
                tree[best_feature][value] = subtree  # Cập nhật cây với nhánh mới
        
        return tree

    # Hàm xác định thuộc tính tốt nhất dựa trên độ lợi thông tin
    def best_feature_index(self, X, y):
        num_features = X.shape[1]  # Số lượng thuộc tính
        best_gain = -1  # Giá trị độ lợi cao nhất
        best_feature_index = -1  # "Chỉ" số của thuộc tính tốt nhất

        # Duyệt qua từng thuộc tính và tính độ lợi
        for feature_index in range(num_features):
            gain = self.information_gain(X, y, feature_index)
            if gain > best_gain:
                best_gain = gain
                best_feature_index = feature_index
    
        return best_feature_index

    # Hàm tính độ lợi thông tin của một thuộc tính
    def information_gain(self, X, y, feature_index):
        # Tính entropy của tập dữ liệu gốc
        total_entropy = self.entropy(y)
        values, counts = np.unique(X[:, feature_index], return_counts=True)
        weighted_entropy = 0

        # Tính entropy có trọng số cho từng giá trị của thuộc tính
        for value, count in zip(values, counts):
            y_subset = y[X[:, feature_index] == value]
            weighted_entropy += (count / len(y)) * self.entropy(y_subset)
        
        return total_entropy - weighted_entropy  # Độ lợi thông tin

    # Hàm tính entropy của một tập nhãn
    def entropy(self, y):
        # Đếm số lần xuất hiện của mỗi nhãn trong y
        counts = np.bincount(y)
    
        # Tính tổng số mẫu
        total_samples = len(y)
    
        # Tính xác suất của mỗi nhãn bằng cách chia số lượng xuất hiện cho tổng số mẫu
        probabilities = counts / total_samples
    
        # Tính entropy
        entropy_value = 0  # Khởi tạo giá trị entropy
        for p in probabilities:
            if p > 0:  # Chỉ tính khi xác suất lớn hơn 0
                entropy_value -= p * np.log2(p)  # Cộng dồn vào entropy
    
        return entropy_value  # Trả về giá trị entropy tính được

    # Hàm dự đoán
    def predict(self, X):
        predictions = []  # Danh sách lưu trữ các dự đoán
        for instance in X:
            tree = self.tree  # Bắt đầu từ cây gốc
            while isinstance(tree, dict):  # Trong khi chưa đến lá cây
                feature = next(iter(tree))  # Lấy thuộc tính hiện tại
                feature_index = self.feature_names.index(feature)  # Tìm chỉ số thuộc tính
                feature_value = instance[feature_index]  # Giá trị của thuộc tính trong mẫu

                # Kiểm tra nhánh dựa trên giá trị thuộc tính
                if feature_value in tree[feature]:
                    tree = tree[feature][feature_value]  # Đi vào nhánh con
                else:
                    # Nếu không tìm thấy nhánh phù hợp, dùng nhãn phổ biến của nhánh
                    predictions.append(self.most_common_label)
                    break
            else:
                # Nếu đã đến lá cây
                predictions.append(tree)
        
        return np.array(predictions)  # Trả về danh sách dự đoán

    # Hàm in cây ra màn hình
    def print_tree(self, tree=None, depth=0):
        if tree is None:
            tree = self.tree
        for key, value in tree.items():
            print("\t" * depth + str(key))  # In thuộc tính
            if isinstance(value, dict):
                self.print_tree(value, depth + 1)  # Đệ quy cho cây con
            else:
                print("\t" * (depth + 1) + "-> " + str(value))  # In nhãn nếu là lá cây
