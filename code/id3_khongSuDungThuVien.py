# main.py
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from id3 import DecisionTreeID3

# Đọc file CSV và chuẩn bị dữ liệu
file_path = 'StudentPerformanceFactors_new.csv'
data = pd.read_csv(file_path)

# Sử dụng bản copy để tránh ảnh hưởng dữ liệu gốc khi mã hóa
data_encoded = data.copy()
# Duyệt qua từng cột trong dữ liệu
for column in data_encoded.columns:
    # Nếu cột có kiểu dữ liệu là chuỗi (object)
    if data_encoded[column].dtype == 'object':
        # Tạo một bộ mã hóa cho cột hiện tại
        le = LabelEncoder()
        # Mã hóa cột chuỗi thành số nguyên và cập nhật vào cột
        data_encoded[column] = le.fit_transform(data_encoded[column])

# Xác định các biến và cột
X = data_encoded.drop(columns=['Exam_Score'])
y = data_encoded['Exam_Score']
features = X.columns.tolist()

# Chia dữ liệu thành tập huấn luyện và kiểm tra
X_train, X_test, y_train, y_test = train_test_split(X.values, y.values, test_size=0.3, random_state=42)

# Huấn luyện mô hình ID3
clf = DecisionTreeID3(max_depth=4)
clf.fit(X_train, y_train, features)

# Dự đoán trên tập kiểm tra
y_pred = clf.predict(X_test)

# In kết quả dự đoán để kiểm tra
# print("Predictions:", y_pred)

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average='micro') # micro: tính toán tổng thể trên tất cả các lớp
recall = recall_score(y_test, y_pred, average='micro')
f1 = f1_score(y_test, y_pred, average='micro')
print("Accuracy:", accuracy)
print("Precison:", precision)
print("Recall:", recall)
print("F1:", f1)

clf.print_tree()
# print(clf.tree)