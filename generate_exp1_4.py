import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

os.makedirs("assets", exist_ok=True)
os.makedirs("data", exist_ok=True)

# Set consistent matplotlib styling matching the reference (white background, clear fonts)
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#333333'
plt.rcParams['axes.linewidth'] = 0.8

print("Generating Experiment 1: Matplotlib Basics")
# Dataset: retail_store_sales.csv
np.random.seed(42)
departments = ['Electronics', 'Apparel', 'Home & Kitchen', 'Footwear', 'Beauty & Health']
months = [f'Month {i}' for i in range(1, 21)]
store_df = pd.DataFrame({
    'transaction_id': range(101, 121),
    'month': months,
    'department': np.random.choice(departments, 20),
    'units_sold': np.random.randint(150, 950, 20),
    'revenue': np.random.randint(15000, 98000, 20),
    'rating': np.round(np.random.uniform(3.2, 4.9, 20), 1)
})
store_df.to_csv("data/store_sales.csv", index=False)

# 1. Line Chart: Revenue Trend across 20 Transactions
plt.figure(figsize=(7, 4.2))
plt.plot(store_df["revenue"], marker='o', color='darkblue', linestyle='-')
plt.title("Monthly Revenue Trend (20 Transactions)")
plt.xlabel("Transaction Index")
plt.ylabel("Revenue ($)")
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig("assets/exp1_line_chart.png", dpi=200)
plt.close()

# 2. Scatter Plot: Units Sold vs Revenue
plt.figure(figsize=(7, 4.2))
plt.scatter(store_df["units_sold"], store_df["revenue"], color="crimson", alpha=0.75, s=60)
plt.title("Units Sold vs Revenue")
plt.xlabel("Units Sold")
plt.ylabel("Revenue ($)")
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig("assets/exp1_scatter_plot.png", dpi=200)
plt.close()

# 3. Bar Chart: Revenue by Department
dept_rev = store_df.groupby("department")["revenue"].sum().sort_values(ascending=False)
plt.figure(figsize=(7, 4.2))
plt.bar(dept_rev.index, dept_rev.values, color='#4A90E2', edgecolor='black')
plt.title("Total Revenue by Department")
plt.xlabel("Department")
plt.ylabel("Revenue ($)")
plt.xticks(rotation=15)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig("assets/exp1_bar_chart.png", dpi=200)
plt.close()

# 4. Pie Chart: Percentage Distribution of Transactions by Department
dept_counts = store_df["department"].value_counts()
plt.figure(figsize=(5.5, 5))
plt.pie(dept_counts.values, labels=dept_counts.index, autopct="%1.1f%%", startangle=140,
        colors=['#5dade2', '#48c9b0', '#f5b041', '#eb984e', '#af7ac5'])
plt.title("Percentage Distribution by Department")
plt.tight_layout()
plt.savefig("assets/exp1_pie_chart.png", dpi=200)
plt.close()

# 5. Histogram: Distribution of Revenue
plt.figure(figsize=(7, 4.2))
plt.hist(store_df["revenue"], bins=8, color="#16a085", edgecolor="black")
plt.title("Distribution of Transaction Revenue")
plt.xlabel("Revenue ($)")
plt.ylabel("Frequency")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("assets/exp1_histogram.png", dpi=200)
plt.close()

print("Generating Experiment 2: Statistical Plots Using Seaborn")
# Dataset: student_performance.csv
np.random.seed(101)
n_students = 120
study_hours = np.random.normal(loc=25, scale=8, size=n_students)
study_hours = np.clip(study_hours, 5, 50)
exam_scores = 35 + 1.25 * study_hours + np.random.normal(0, 5, n_students)
exam_scores = np.clip(exam_scores, 40, 99)
# Add a few high scores
exam_scores[0] = 98.5
exam_scores[1] = 99.2
exam_scores[2] = 97.8

student_df = pd.DataFrame({
    'student_id': range(1001, 1001 + n_students),
    'study_hours': np.round(study_hours, 1),
    'exam_score': np.round(exam_scores, 1),
    'attendance_pct': np.random.randint(65, 100, n_students),
    'course_track': np.random.choice(['Data Science', 'AI & ML', 'Software Dev'], n_students)
})
student_df.to_csv("data/student_performance.csv", index=False)

# Seaborn Histplot with KDE
plt.figure(figsize=(7, 4.2))
sns.histplot(student_df["exam_score"], kde=True, bins=15, color="#2980b9")
plt.title("Distribution of Student Exam Scores")
plt.xlabel("Exam Score")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("assets/exp2_histplot.png", dpi=200)
plt.close()

# Seaborn Boxplot
plt.figure(figsize=(6, 4.2))
sns.boxplot(y=student_df["exam_score"], color="skyblue")
plt.title("Box Plot of Exam Scores")
plt.ylabel("Exam Score")
plt.tight_layout()
plt.savefig("assets/exp2_boxplot.png", dpi=200)
plt.close()

# Seaborn Regplot
plt.figure(figsize=(7, 4.2))
sns.regplot(data=student_df, x="study_hours", y="exam_score",
            scatter_kws={'alpha': 0.6, 'color': '#2c3e50'}, line_kws={'color': 'crimson'})
plt.title("Study Hours vs Exam Score")
plt.xlabel("Study Hours (Weekly)")
plt.ylabel("Exam Score")
plt.tight_layout()
plt.savefig("assets/exp2_regplot.png", dpi=200)
plt.close()

print("Generating Experiment 3: Data Cleaning in Python")
# Dataset: employee_payroll.csv with intentional missing values and extreme outlier
np.random.seed(42)
n_emp = 60
base_salaries = np.random.normal(loc=55000, scale=12000, size=n_emp).round(2)
base_salaries[base_salaries < 25000] = 30000
# Inject 3 extreme outliers
base_salaries[5] = 420000.00
base_salaries[18] = 385000.00
base_salaries[44] = 490000.00

dept_choices = ['Engineering', 'Marketing', 'Finance', 'Human Resources', 'Operations']
depts = np.random.choice(dept_choices, n_emp).tolist()
# Introduce missing values in depts and salary
depts[2] = None
depts[14] = None
depts[31] = None
base_salaries[7] = np.nan
base_salaries[22] = np.nan
base_salaries[39] = np.nan

raw_payroll = pd.DataFrame({
    'emp_id': range(5001, 5001 + n_emp),
    'department': depts,
    'experience_yrs': np.random.randint(1, 15, n_emp),
    'salary': base_salaries,
    'rating': np.round(np.random.uniform(2.5, 5.0, n_emp), 1)
})
raw_payroll.to_csv("data/employee_payroll_raw.csv", index=False)

# Cleaning process
original_df = raw_payroll.copy()
df_clean = raw_payroll.copy()
# Fill numerical with median
num_cols = df_clean.select_dtypes(include="number").columns
df_clean[num_cols] = df_clean[num_cols].fillna(df_clean[num_cols].median())
# Fill categorical with mode
cat_cols = df_clean.select_dtypes(include=["object"]).columns
for col in cat_cols:
    df_clean[col] = df_clean[col].fillna(df_clean[col].mode()[0])

# Outlier treatment using IQR
q1 = df_clean['salary'].quantile(0.25)
q3 = df_clean['salary'].quantile(0.75)
iqr = q3 - q1
upper_bound = q3 + 1.5 * iqr
clean_filtered_df = df_clean[df_clean['salary'] <= upper_bound]

# Plot before and after
plt.figure(figsize=(9, 4.5))
plt.subplot(1, 2, 1)
sns.boxplot(y=original_df["salary"].dropna(), color="skyblue")
plt.title("Before Cleaning (With Outliers)")
plt.ylabel("Salary ($)")

plt.subplot(1, 2, 2)
sns.boxplot(y=clean_filtered_df["salary"], color="lightgreen")
plt.title("After Cleaning (Outliers Treated)")
plt.ylabel("Salary ($)")
plt.tight_layout()
plt.savefig("assets/exp3_cleaning_boxplot.png", dpi=200)
plt.close()

print("Generating Experiment 4: Interactive Charts with Plotly")
import plotly.express as px

# Dataset: tech_products_sales.csv
tech_df = pd.DataFrame({
    'Product': ['Smart Watch X', 'Noise-Cancel Headphones', 'Wireless Earbuds', 'Fitness Tracker',
                'Tablet Pro 11', 'Ultra Laptop 14', 'Gaming Mouse', 'Mechanical Keyboard',
                '4K Webcam', 'Bluetooth Speaker'],
    'Category': ['Wearables', 'Audio', 'Audio', 'Wearables', 'Computing', 'Computing', 'Accessories', 'Accessories', 'Accessories', 'Audio'],
    'Units_Sold': [450, 320, 780, 520, 210, 140, 620, 480, 390, 510],
    'Unit_Price': [180, 240, 85, 95, 650, 1100, 55, 110, 80, 70],
    'Revenue': [81000, 76800, 66300, 49400, 136500, 154000, 34100, 52800, 31200, 35700],
    'Rating': [4.5, 4.8, 4.3, 4.1, 4.7, 4.6, 4.4, 4.6, 4.2, 4.3],
    'Return_Rate': [2.1, 1.5, 3.2, 2.8, 1.1, 0.9, 2.4, 1.8, 2.0, 1.6]
})
tech_df.to_csv("data/tech_products_sales.csv", index=False)

# Chart 1: Scatter Plot (Unit Price vs Revenue)
fig1 = px.scatter(
    tech_df,
    x="Unit_Price",
    y="Revenue",
    color="Category",
    size="Units_Sold",
    hover_data=["Product", "Rating", "Return_Rate"],
    title="Product Price vs Revenue (Bubble Size = Units Sold)",
    template="plotly_white"
)
fig1.update_layout(width=750, height=450)
fig1.write_image("assets/exp4_plotly_scatter.png", scale=2)

# Chart 2: Line / Marker Chart (Product vs Revenue)
fig2 = px.line(
    tech_df,
    x="Product",
    y="Revenue",
    color="Category",
    markers=True,
    hover_data=["Units_Sold", "Rating"],
    title="Revenue Distribution by Product",
    template="plotly_white"
)
fig2.update_layout(width=750, height=450)
fig2.write_image("assets/exp4_plotly_line.png", scale=2)

# Chart 3: Interactive Bar Chart (Units Sold by Product)
fig3 = px.bar(
    tech_df,
    x="Product",
    y="Units_Sold",
    color="Category",
    hover_data=["Unit_Price", "Revenue", "Rating"],
    title="Total Units Sold by Product",
    template="plotly_white"
)
fig3.update_layout(width=750, height=450)
fig3.write_image("assets/exp4_plotly_bar.png", scale=2)

print("Experiment 1 to 4 generated successfully!")
