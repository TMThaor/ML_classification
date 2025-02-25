import pandas as pd
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt

# Đọc dữ liệu từ tệp CSV
data = pd.read_csv("StudentPerformanceFactors_new.csv")  # Đổi đường dẫn này nếu cần

# Xác định cột đặc trưng và nhãn
X = data.drop(columns=['Exam_Score'])  # Các cột đặc trưng (trừ Exam_Score)
y = data['Exam_Score']                 # Cột nhãn (Exam_Score)

# Label Encoding cho các cột đặc trưng dạng chuỗi
for column in X.columns:
    if X[column].dtype == 'object':  # Kiểm tra xem cột có kiểu chuỗi không
        le = LabelEncoder()
        X[column] = le.fit_transform(X[column])

# Chia dữ liệu thành tập huấn luyện và tập kiểm tra
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Tạo và huấn luyện cây quyết định với tiêu chí 'entropy' (ID3) và độ sâu tối đa
clf = DecisionTreeClassifier(criterion='entropy', max_depth=3, random_state=42)
clf.fit(X_train, y_train)

# Dự đoán và đánh giá độ chính xác
y_pred = clf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy * 100:.2f}%")

# Vẽ cây quyết định
plt.figure(figsize=(20, 12))
plot_tree(clf, feature_names=X.columns, class_names=clf.classes_.astype(str), filled=True)
plt.show()
# Đọc dữ liệu từ tệp CSV
data = pd.read_csv("StudentPerformanceFactors_new.csv")  # Đổi đường dẫn này nếu cần

# Xác định cột đặc trưng và nhãn
X = data.drop(columns=['Exam_Score'])  # Các cột đặc trưng (trừ Exam_Score)
y = data['Exam_Score']                 # Cột nhãn (Exam_Score)

# Label Encoding cho các cột đặc trưng dạng chuỗi
for column in X.columns:
    if X[column].dtype == 'object':  # Kiểm tra xem cột có kiểu chuỗi không
        le = LabelEncoder()
        X[column] = le.fit_transform(X[column])

# Chia dữ liệu thành tập huấn luyện và tập kiểm tra
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Tạo và huấn luyện cây quyết định với tiêu chí 'entropy' (ID3)
clf = DecisionTreeClassifier(criterion='entropy', random_state=42)
clf.fit(X_train, y_train)

# Dự đoán và đánh giá độ chính xác
y_pred = clf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy * 100:.2f}%")

# Vẽ cây quyết định
plt.figure(figsize=(20, 12))
plot_tree(clf, feature_names=X.columns, class_names=clf.classes_.astype(str), filled=True)
plt.show()
