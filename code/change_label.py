import pandas as pd

# Tải file CSV và lưu dữ liệu vào DataFrame df
file_path = 'dataa.csv'
df = pd.read_csv(file_path)

# Ánh xạ 'Hours_Studied', 'Attendance', 'Sleep_Hours',... thành 'Thấp', 'Trung bình', 'Cao'.
df['Hours_Studied'] = pd.cut(df['Hours_Studied'], bins=3, labels=['Low', 'Medium', 'High'])
df['Attendance'] = pd.cut(df['Attendance'], bins=3, labels=['Low', 'Medium', 'High'])
df['Sleep_Hours'] = pd.cut(df['Sleep_Hours'], bins=3, labels=['Low', 'Medium', 'High'])
df['Physical_Activity'] = pd.cut(df['Physical_Activity'], bins=3, labels=['Low', 'Medium', 'High'])
df['Tutoring_Sessions'] = pd.cut(df['Tutoring_Sessions'], bins=3, labels=['Low', 'Medium', 'High'])

# Ánh xạ 'Previous_Scores' và 'Exam_Score' thành 'A', 'B', 'C' dựa trên các giá trị cụ thể.
score_mapping = {0: 'F', 1: 'D', 2: 'C', 3: 'B',4:'A'}  
df['Previous_Scores'] = df['Previous_Scores'].map(score_mapping)
df['Exam_Score'] = df['Exam_Score'].map(score_mapping)

# Lưu DataFrame vào file CSV mới
df.to_csv('StudentPerformanceFactors_new.csv', index=False)
