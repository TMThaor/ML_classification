import pandas as pd
import numpy as np
from sklearn import preprocessing
import arff
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, precision_score, recall_score,f1_score
from sklearn.model_selection import train_test_split

class NaiveBayes:
    def __init(self):
        self.class_priors = {} # chứa tất cả giá trị p(c)
        self.prob_by_class= {} # chứa tất cả giá trị p(x|c)

    def fit(self,X, y):
        class_counts = y.value_counts().to_dict() 
        total_count = len(X) 
        prob_by_class = {}
        for class_value in class_counts: #tính P(x|c)
            class_data = X[y == class_value]
            N_C = class_data.shape[0] 
            class_probs = {} #Lưu lại tất cả các giá trị p(xi|c) của nhãn đang xét
            for column in X.columns:
                value_counts = class_data[column].value_counts().to_dict() 
                col_probs = {} 
                for value, count in value_counts.items(): #tính p(xi|c)
                    d=len(value_counts) 
                    col_probs[value] = (count + 1) / (N_C + 1 * d) 
                class_probs[column] = col_probs 
            prob_by_class[class_value] = class_probs 
        class_priors = {class_value: class_counts[class_value] / total_count for class_value in class_counts} 
        self.prob_by_class, self.class_priors=prob_by_class,class_priors

    def predict(self,x):
        max_prob = -1
        best_class = None
        class_priors=self.class_priors
        probabilities_by_class=self.prob_by_class
        for class_value, priors in class_priors.items():
            total_prob = priors  
            for column in x.index:
                col_probs = probabilities_by_class[class_value][column]
                total_prob *= col_probs.get(x[column], 1e-9) 
            # Tìm nhãn có xác suất cao nhất
            if total_prob > max_prob:
                max_prob = total_prob
                best_class = class_value
        return best_class

with open('StudentPerformanceFactors_new.arff', 'r') as f:
    dt = arff.load(f)

data = pd.DataFrame(dt['data'], columns=[attr[0] for attr in dt['attributes']])

le = preprocessing.LabelEncoder()
data = data.apply(le.fit_transform)

dt_Train, dt_Test = train_test_split(data, test_size=0.3, shuffle=False)

X_train = dt_Train.iloc[:, :-1]
y_train = dt_Train.iloc[:, -1]
X_test = dt_Test.iloc[:, :-1]
y_test = dt_Test.iloc[:, -1]
unique_values = {col: dt_Train[col].nunique() for col in dt_Train.columns}

# Dự đoán cho tập kiểm tra
nb=NaiveBayes()
nb.fit(X_train,y_train)
y_predict = X_test.apply(lambda x: nb.predict(x), axis=1) 
# Đánh giá kết quả
print(classification_report(y_test, y_predict))
print("Ma trận tương quan")
print(confusion_matrix(y_test, y_predict))

accuracy = sum(y_predict == y_test) / len(y_test)
print("Accuracy:", accuracy)
precision = precision_score(y_test, y_predict, average=None)
recall = recall_score(y_test, y_predict, average=None)
f1 = f1_score(y_test, y_predict, average=None)
print("Precison:", precision)
print("Recall:", recall)
print("F1:", f1)