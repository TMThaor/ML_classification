import arff
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import BernoulliNB
from sklearn import preprocessing
import sys
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
sys.setrecursionlimit(30000)

# Đọc file .arff
with open('StudentPerformanceFactors_new.arff', 'r') as f:
    dt = arff.load(f)

# Chuyển dữ liệu thành DataFrame
data = pd.DataFrame(dt['data'], columns=[attr[0] for attr in dt['attributes']])

le = preprocessing.LabelEncoder()
data = data.apply(le.fit_transform)

# Chia dữ liệu thành tập huấn luyện và kiểm tra
dt_Train, dt_Test = train_test_split(data, test_size=0.3, shuffle=True)
X_train = dt_Train.iloc[:, :-1]
y_train = dt_Train.iloc[:, -1]
X_test = dt_Test.iloc[:, :-1]
y_test = dt_Test.iloc[:, -1]

# Huấn luyện mô hình Naive Bayes GaussianNB
pla = GaussianNB()
pla.fit(X_train, y_train)

# Dự đoán trên tập kiểm tra
y_predict = pla.predict(X_test)
# In báo cáo phân loại
print(classification_report(y_test, y_predict))
# In ma trận tương quan
print("Ma trận tương quan:")
print(confusion_matrix(y_test, y_predict))
# Tính toán các chỉ số đánh giá
accuracy = accuracy_score(y_test, y_predict)
precision = precision_score(y_test, y_predict,average=None)
recall = recall_score(y_test, y_predict,average=None)
f1 = f1_score(y_test, y_predict,average=None)
print('Accuracy: ', accuracy)
print('Precision: ', precision)
print('Recall: ', recall)
print('F1 Score: ', f1)