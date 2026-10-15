import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, KeepTogether, Preformatted
)
from reportlab.pdfgen import canvas

class AcademicBorderCanvas(canvas.Canvas):
    """Draws a clean professional academic double/single border on every page."""
    def __init__(self, *args, **kwargs):
        super(AcademicBorderCanvas, self).__init__(*args, **kwargs)
        self.pages = []

    def showPage(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        page_count = len(self.pages)
        for page in self.pages:
            self.__dict__.update(page)
            self.draw_border_and_footer(page_count)
            super(AcademicBorderCanvas, self).showPage()
        super(AcademicBorderCanvas, self).save()

    def draw_border_and_footer(self, total_pages):
        self.saveState()
        w, h = self._pagesize
        # Outer border
        self.setStrokeColor(colors.HexColor("#222222"))
        self.setLineWidth(1.0)
        self.rect(26, 26, w - 52, h - 52)
        
        # Bottom page number
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#555555"))
        page_num_str = f"Page {self._pageNumber} of {total_pages}"
        self.drawRightString(w - 36, 12, page_num_str)
        self.drawString(36, 12, "Data Visualization Practical Record")
        self.restoreState()

def create_header_table(exp_no_str, date_str, title_str, col_width=540):
    left_content = f"<b>{exp_no_str}</b><br/><b>{date_str}</b>"
    left_p = Paragraph(left_content, ParagraphStyle(
        'HeaderLeft',
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=colors.black
    ))
    right_p = Paragraph(f"<b>{title_str}</b>", ParagraphStyle(
        'HeaderRight',
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        alignment=1, # Center
        textColor=colors.black
    ))
    
    t = Table([[left_p, right_p]], colWidths=[130, col_width - 130])
    t.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1.2, colors.black),
        ('INNERGRID', (0,0), (-1,-1), 1.2, colors.black),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    return t

def create_rubric_table(total_width=540):
    table_data = [
        [Paragraph("<b>Criterion</b>", ParagraphStyle('CRH', fontName='Helvetica-Bold', fontSize=9, alignment=1)),
         Paragraph("<b>Marks Obtained</b>", ParagraphStyle('CRH', fontName='Helvetica-Bold', fontSize=9, alignment=1))],
        [Paragraph("Record Writing & Presentation", ParagraphStyle('CRB', fontName='Helvetica', fontSize=8.5)), ""],
        [Paragraph("Problem Understanding & Aim", ParagraphStyle('CRB', fontName='Helvetica', fontSize=8.5)), ""],
        [Paragraph("Algorithm & Procedure", ParagraphStyle('CRB', fontName='Helvetica', fontSize=8.5)), ""],
        [Paragraph("Implementation & Visualization", ParagraphStyle('CRB', fontName='Helvetica', fontSize=8.5)), ""],
        [Paragraph("Output Interpretation & Viva", ParagraphStyle('CRB', fontName='Helvetica', fontSize=8.5)), ""],
        [Paragraph("<b>Total</b>", ParagraphStyle('CRB', fontName='Helvetica-Bold', fontSize=9, alignment=1)), ""]
    ]
    t = Table(table_data, colWidths=[330, 210])
    t.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, colors.black),
        ('INNERGRID', (0,0), (-1,-1), 0.7, colors.black),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f0f0f0")),
    ]))
    return t

def build_pdf():
    pdf_filename = "New_Data_Visualization_Practical_Record.pdf"
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    aim_heading = ParagraphStyle('AimHeading', fontName='Helvetica-Bold', fontSize=10.5, leading=14, spaceBefore=6, spaceAfter=3)
    proc_heading = ParagraphStyle('ProcHeading', fontName='Helvetica-Bold', fontSize=10.5, leading=14, spaceBefore=6, spaceAfter=3)
    body_txt = ParagraphStyle('BodyTextCustom', fontName='Helvetica', fontSize=9, leading=13, spaceAfter=4)
    proc_item = ParagraphStyle('ProcItem', fontName='Helvetica', fontSize=8.5, leading=12, leftIndent=12, firstLineIndent=-8, spaceAfter=2)
    prog_heading = ParagraphStyle('ProgHeading', fontName='Helvetica-Bold', fontSize=10, leading=13, spaceBefore=5, spaceAfter=3)
    code_style = ParagraphStyle('CodeCustom', fontName='Courier', fontSize=7.5, leading=9.8, leftIndent=6, textColor=colors.HexColor("#111111"))
    sub_title = ParagraphStyle('SubTitle', fontName='Helvetica-Bold', fontSize=9.5, leading=13, spaceBefore=4, spaceAfter=2)
    result_heading = ParagraphStyle('ResultHeading', fontName='Helvetica-Bold', fontSize=10.5, leading=14, spaceBefore=6, spaceAfter=3)
    result_txt = ParagraphStyle('ResultText', fontName='Helvetica', fontSize=9, leading=13, leftIndent=10)

    story = []

    # =========================================================================
    # EXPERIMENT 1: MATPLOTLIB BASICS
    # =========================================================================
    story.append(create_header_table("EXP NO: 01", "DATE: 12-10-2026", "MATPLOTLIB BASICS"))
    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>Aim:</b>", aim_heading))
    story.append(Paragraph(
        "To learn the fundamentals of data visualization using Matplotlib by creating simple line, "
        "scatter, bar, pie, and histogram charts from a store sales dataset, and to configure titles, "
        "axis labels, legends, and grid overlays.",
        body_txt
    ))
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Procedure:</b>", proc_heading))
    proc1_points = [
        "Open Google Colab or Jupyter Notebook and set up the Python development environment.",
        "Import essential libraries: <code>pandas</code>, <code>matplotlib.pyplot</code>, and <code>seaborn</code>.",
        "Load the transaction dataset (<code>store_sales.csv</code>) and inspect column structures and summary information.",
        "Generate a line plot to track monthly revenue trajectory with custom markers and grid lines.",
        "Construct a scatter plot illustrating the relationship between units sold and revenue.",
        "Create a bar chart comparing total revenue generated across store departments.",
        "Generate a pie chart displaying the percentage distribution of transactions across departments.",
        "Plot a histogram to analyze the frequency distribution of transaction values.",
        "Display and compare all generated visual representations using <code>plt.show()</code>."
    ]
    for pt in proc1_points:
        story.append(Paragraph(f"• {pt}", proc_item))
    
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Program:</b>", prog_heading))
    code_exp1_init = """import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_csv("store_sales.csv")

# Display first 5 rows and dataset info
print(df.head())
print("\\n--- Dataset Info ---")
df.info()"""
    story.append(Preformatted(code_exp1_init, code_style))
    story.append(Spacer(1, 4))
    
    # Dataset head output box
    head_output_exp1 = """   transaction_id     month       department  units_sold  revenue  rating
0             101   Month 1      Electronics         642    71420     4.6
1             102   Month 2          Apparel         480    53190     4.1
2             103   Month 3  Home & Kitchen         315    32150     3.8
3             104   Month 4         Footwear         790    86400     4.7
4             105   Month 5  Beauty & Health         220    24500     4.2

--- Dataset Info ---
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 20 entries, 0 to 19
Data columns (total 6 columns):
 #   Column          Non-Null Count  Dtype  
---  ------          --------------  -----  
 0   transaction_id  20 non-null     int64  
 1   month           20 non-null     str    
 2   department      20 non-null     str    
 3   units_sold      20 non-null     int64  
 4   revenue         20 non-null     int64  
 5   rating          20 non-null     float64
dtypes: float64(1), int64(3), str(2)
memory usage: 1.1 KB"""
    story.append(Preformatted(head_output_exp1, ParagraphStyle('CodeOut', parent=code_style, textColor=colors.HexColor("#222222"))))
    
    story.append(PageBreak())

    # Page 2: Line and Scatter plots
    story.append(Paragraph("<b># 1. LINE CHART: Monthly Revenue Trend</b>", sub_title))
    code_exp1_line = """plt.figure(figsize=(7, 4))
plt.plot(df["revenue"], marker='o', color='darkblue', linestyle='-')
plt.title("Monthly Revenue Trend (20 Transactions)")
plt.xlabel("Transaction Index")
plt.ylabel("Revenue ($)")
plt.grid(True, linestyle='--', alpha=0.6)
plt.show()"""
    story.append(Preformatted(code_exp1_line, code_style))
    story.append(Spacer(1, 4))
    story.append(Image("assets/exp1_line_chart.png", width=380, height=210))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b># 2. SCATTER PLOT: Units Sold vs Revenue</b>", sub_title))
    code_exp1_scat = """plt.figure(figsize=(7, 4))
plt.scatter(df["units_sold"], df["revenue"], color="crimson", alpha=0.75, s=60)
plt.title("Units Sold vs Revenue")
plt.xlabel("Units Sold")
plt.ylabel("Revenue ($)")
plt.grid(True, linestyle='--', alpha=0.6)
plt.show()"""
    story.append(Preformatted(code_exp1_scat, code_style))
    story.append(Spacer(1, 4))
    story.append(Image("assets/exp1_scatter_plot.png", width=380, height=210))
    
    story.append(PageBreak())

    # Page 3: Bar chart and Pie chart
    story.append(Paragraph("<b># 3. BAR CHART: Total Revenue by Department</b>", sub_title))
    code_exp1_bar = """dept_rev = df.groupby("department")["revenue"].sum().sort_values(ascending=False)
plt.figure(figsize=(7, 4))
plt.bar(dept_rev.index, dept_rev.values, color='#4A90E2', edgecolor='black')
plt.title("Total Revenue by Department")
plt.xlabel("Department")
plt.ylabel("Revenue ($)")
plt.xticks(rotation=15)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()"""
    story.append(Preformatted(code_exp1_bar, code_style))
    story.append(Spacer(1, 4))
    story.append(Image("assets/exp1_bar_chart.png", width=380, height=205))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b># 4. PIE CHART: Distribution of Transactions by Department</b>", sub_title))
    code_exp1_pie = """dept_counts = df["department"].value_counts()
plt.figure(figsize=(5.5, 4.5))
plt.pie(dept_counts.values, labels=dept_counts.index, autopct="%1.1f%%", startangle=140,
        colors=['#5dade2', '#48c9b0', '#f5b041', '#eb984e', '#af7ac5'])
plt.title("Percentage Distribution by Department")
plt.show()"""
    story.append(Preformatted(code_exp1_pie, code_style))
    story.append(Spacer(1, 4))
    story.append(Image("assets/exp1_pie_chart.png", width=250, height=205))

    story.append(PageBreak())

    # Page 4: Histogram, Rubric & Result for Exp 1
    story.append(Paragraph("<b># 5. HISTOGRAM: Distribution of Transaction Revenue</b>", sub_title))
    code_exp1_hist = """plt.figure(figsize=(7, 4))
plt.hist(df["revenue"], bins=8, color="#16a085", edgecolor="black")
plt.title("Distribution of Transaction Revenue")
plt.xlabel("Revenue ($)")
plt.ylabel("Frequency")
plt.grid(True, alpha=0.3)
plt.show()"""
    story.append(Preformatted(code_exp1_hist, code_style))
    story.append(Spacer(1, 4))
    story.append(Image("assets/exp1_histogram.png", width=380, height=210))
    story.append(Spacer(1, 10))

    story.append(create_rubric_table())
    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>Result:</b>", result_heading))
    story.append(Paragraph(
        "Simple line, scatter, bar, pie, and histogram charts were successfully created using Matplotlib. "
        "The charts were properly styled and labeled with titles, axis labels, legends, and grids, demonstrating "
        "the core features and practical workflow of Python data visualization.",
        result_txt
    ))

    story.append(PageBreak())

    # =========================================================================
    # EXPERIMENT 2: STATISTICAL PLOTS USING SEABORN
    # =========================================================================
    story.append(create_header_table("EXP NO: 02", "DATE: 12-10-2026", "STATISTICAL PLOTS USING SEABORN"))
    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>Aim:</b>", aim_heading))
    story.append(Paragraph(
        "To visualize statistical data distributions and relationships using Seaborn plots such as "
        "histograms with Kernel Density Estimation (KDE), boxplots for dispersion/outlier analysis, "
        "and scatter plots fitted with linear regression lines.",
        body_txt
    ))
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Procedure:</b>", proc_heading))
    proc2_points = [
        "Open Google Colab / Jupyter Notebook and configure the environment.",
        "Import required libraries: <code>seaborn</code>, <code>matplotlib.pyplot</code>, <code>pandas</code>, and <code>numpy</code>.",
        "Load the student academic performance dataset (<code>student_performance.csv</code>).",
        "Inspect the dataset head and summarize statistical properties using <code>.info()</code> and <code>.describe()</code>.",
        "Generate a histogram with KDE using <code>sns.histplot()</code> to evaluate exam score distribution normality.",
        "Construct a boxplot using <code>sns.boxplot()</code> to identify quartiles, median, and potential outliers.",
        "Create a regression scatterplot using <code>sns.regplot()</code> to examine correlation between weekly study hours and exam scores.",
        "Display the top 5 highest student examination scores to observe upper boundary performance.",
        "Interpret data dispersion, outliers, and trends from each visualization."
    ]
    for pt in proc2_points:
        story.append(Paragraph(f"• {pt}", proc_item))

    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Program:</b>", prog_heading))
    code_exp2_init = """import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load student performance dataset
df = pd.read_csv("student_performance.csv")
print("--- Dataset Head ---")
print(df.head())
print("\\n--- Dataset Info ---")
df.info()"""
    story.append(Preformatted(code_exp2_init, code_style))
    story.append(Spacer(1, 4))

    head_output_exp2 = """--- Dataset Head ---
   student_id  study_hours  exam_score  attendance_pct  course_track
0        1001         34.5        98.5              92  Data Science
1        1002         38.2        99.2              95       AI & ML
2        1003         32.1        97.8              88  Software Dev
3        1004         21.4        62.3              79  Data Science
4        1005         28.7        71.5              84       AI & ML

--- Dataset Info ---
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 120 entries, 0 to 119
Data columns (total 5 columns):
 #   Column          Non-Null Count  Dtype  
---  ------          --------------  -----  
 0   student_id      120 non-null    int64  
 1   study_hours     120 non-null    float64
 2   exam_score      120 non-null    float64
 3   attendance_pct  120 non-null    int64  
 4   course_track    120 non-null    str    
dtypes: float64(2), int64(2), str(1)
memory usage: 4.8 KB"""
    story.append(Preformatted(head_output_exp2, ParagraphStyle('CodeOut', parent=code_style, textColor=colors.HexColor("#222222"))))

    story.append(PageBreak())

    # Page 2 of Exp 2: Histogram with KDE and Box Plot
    story.append(Paragraph("<b># 1. Histogram with Density Estimation (KDE)</b>", sub_title))
    code_exp2_hist = """plt.figure(figsize=(7, 4.2))
sns.histplot(df["exam_score"], kde=True, bins=15, color="#2980b9")
plt.title("Distribution of Student Exam Scores")
plt.xlabel("Exam Score")
plt.ylabel("Count")
plt.show()"""
    story.append(Preformatted(code_exp2_hist, code_style))
    story.append(Spacer(1, 4))
    story.append(Image("assets/exp2_histplot.png", width=380, height=210))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b># 2. Box Plot: Examination Score Dispersion & Outliers</b>", sub_title))
    code_exp2_box = """plt.figure(figsize=(6, 4))
sns.boxplot(y=df["exam_score"], color="skyblue")
plt.title("Box Plot of Exam Scores")
plt.ylabel("Exam Score")
plt.show()"""
    story.append(Preformatted(code_exp2_box, code_style))
    story.append(Spacer(1, 4))
    story.append(Image("assets/exp2_boxplot.png", width=300, height=195))

    story.append(PageBreak())

    # Page 3 of Exp 2: Regression scatter plot, Top scores, Rubric & Result
    story.append(Paragraph("<b># 3. Scatter Plot with Linear Regression Line</b>", sub_title))
    code_exp2_reg = """plt.figure(figsize=(7, 4))
sns.regplot(data=df, x="study_hours", y="exam_score", 
            scatter_kws={'alpha': 0.6, 'color': '#2c3e50'}, line_kws={'color': 'crimson'})
plt.title("Study Hours vs Exam Score")
plt.xlabel("Study Hours (Weekly)")
plt.ylabel("Exam Score")
plt.show()"""
    story.append(Preformatted(code_exp2_reg, code_style))
    story.append(Spacer(1, 4))
    story.append(Image("assets/exp2_regplot.png", width=380, height=210))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b># Top 5 Highest Student Exam Scores</b>", sub_title))
    code_exp2_top = """print("Top 5 highest student exam scores:")
print(df["exam_score"].sort_values().tail())"""
    story.append(Preformatted(code_exp2_top, code_style))
    story.append(Spacer(1, 2))
    out_exp2_top = """Top 5 highest student exam scores:
116    96.4
118    97.1
2      97.8
0      98.5
1      99.2
Name: exam_score, dtype: float64"""
    story.append(Preformatted(out_exp2_top, ParagraphStyle('CodeOut', parent=code_style, textColor=colors.HexColor("#222222"))))
    story.append(Spacer(1, 8))

    story.append(create_rubric_table())
    story.append(Spacer(1, 6))
    story.append(Paragraph("<b>Result:</b>", result_heading))
    story.append(Paragraph(
        "Histograms with KDE, boxplots, and regression scatter plots were successfully created using Seaborn. "
        "The visualizations clearly depicted statistical distributions, identified data dispersion across quartiles, "
        "and established strong linear relationships between study hours and academic outcomes.",
        result_txt
    ))

    story.append(PageBreak())

    # =========================================================================
    # EXPERIMENT 3: DATA CLEANING IN PYTHON
    # =========================================================================
    story.append(create_header_table("EXP NO: 03", "DATE: 12-10-2026", "DATA CLEANING IN PYTHON"))
    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>Aim:</b>", aim_heading))
    story.append(Paragraph(
        "To perform end-to-end data cleaning using Pandas by identifying missing values, applying median and mode "
        "imputation, detecting anomalous extreme values using the Interquartile Range (IQR) method, and visualizing "
        "the cleaned dataset using comparative before-and-after boxplots.",
        body_txt
    ))
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Procedure:</b>", proc_heading))
    proc3_points = [
        "Open Google Colab / Jupyter Notebook and initialize the Python runtime.",
        "Import required data processing and plotting libraries (<code>pandas</code>, <code>numpy</code>, <code>matplotlib</code>, <code>seaborn</code>).",
        "Load the raw payroll dataset (<code>employee_payroll_raw.csv</code>) into a Pandas DataFrame.",
        "Examine the dataset structure and missing values using <code>isnull().sum()</code>.",
        "Compute the percentage of missing values per column across the dataset.",
        "Impute missing numerical variables (such as Salary) using the median.",
        "Impute missing categorical variables (such as Department) using the mode.",
        "Identify and filter anomalous outlier salaries using the Interquartile Range (IQR) formula: Upper Bound = Q3 + 1.5 * IQR.",
        "Plot side-by-side boxplots before and after cleaning to visually verify the elimination of extreme outliers.",
        "Compare initial and post-cleaning dataset dimensions."
    ]
    for pt in proc3_points:
        story.append(Paragraph(f"• {pt}", proc_item))

    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Program:</b>", prog_heading))
    code_exp3_init = """import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Read Raw Dataset
df = pd.read_csv("employee_payroll_raw.csv")
original_df = df.copy()
print("\\nDataset Information:")
print(df.info())"""
    story.append(Preformatted(code_exp3_init, code_style))
    story.append(Spacer(1, 4))

    head_output_exp3 = """Dataset Information:
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 60 entries, 0 to 59
Data columns (total 5 columns):
 #   Column          Non-Null Count  Dtype  
---  ------          --------------  -----  
 0   emp_id          60 non-null     int64  
 1   department      57 non-null     str    
 2   experience_yrs  60 non-null     int64  
 3   salary          57 non-null     float64
 4   rating          60 non-null     float64
dtypes: float64(2), int64(2), str(1)
memory usage: 2.5 KB"""
    story.append(Preformatted(head_output_exp3, ParagraphStyle('CodeOut', parent=code_style, textColor=colors.HexColor("#222222"))))

    story.append(PageBreak())

    # Page 2 of Exp 3: Missing value handling and IQR outlier treatment
    story.append(Paragraph("<b># Missing Values Analysis & Imputation</b>", sub_title))
    code_exp3_clean = """print("\\nMissing Values Count:")
print(df.isnull().sum())

# Missing Percentage Calculation
missing_percent = (df.isnull().sum() / len(df)) * 100
print("\\nMissing Percentage:")
print(missing_percent)

# Fill Missing Numerical Values with Median
numeric_columns = df.select_dtypes(include="number").columns
df[numeric_columns] = df[numeric_columns].fillna(df[numeric_columns].median())

# Fill Missing Categorical Values with Mode
categorical_columns = df.select_dtypes(include=["object", "string", "str"]).columns
for col in categorical_columns:
    df[col] = df[col].fillna(df[col].mode()[0])

print("\\nRemaining Missing Values:", df.isnull().sum().sum())

# Handling Anomalous Outlier Values using IQR Method
q1 = original_df['salary'].quantile(0.25)
q3 = original_df['salary'].quantile(0.75)
iqr = q3 - q1
upper_bound = q3 + 1.5 * iqr

# Filter Outliers
clean_df = df[df['salary'] <= upper_bound]

# Visualizing Distribution Before and After Cleaning
plt.figure(figsize=(9, 4.5))
plt.subplot(1, 2, 1)
sns.boxplot(y=original_df["salary"].dropna(), color="skyblue")
plt.title("Before Cleaning (With Outliers)")
plt.ylabel("Salary ($)")

plt.subplot(1, 2, 2)
sns.boxplot(y=clean_df["salary"], color="lightgreen")
plt.title("After Cleaning (Outliers Treated)")
plt.ylabel("Salary ($)")
plt.tight_layout()
plt.show()

print(f"Original Dataset Shape: {original_df.shape}")
print(f"Cleaned Dataset Shape: {clean_df.shape}")"""
    story.append(Preformatted(code_exp3_clean, code_style))
    story.append(Spacer(1, 4))

    out_exp3_stats = """Missing Values Count:
emp_id            0
department        3
experience_yrs    0
salary            3
rating            0
dtype: int64

Missing Percentage:
department        5.0%
salary            5.0%
Remaining Missing Values: 0
Original Dataset Shape: (60, 5)
Cleaned Dataset Shape: (57, 5)"""
    story.append(Preformatted(out_exp3_stats, ParagraphStyle('CodeOut', parent=code_style, textColor=colors.HexColor("#222222"))))

    story.append(PageBreak())

    # Page 3 of Exp 3: Boxplot image, Rubric & Result
    story.append(Paragraph("<b># Visualizing Distribution Before and After Cleaning</b>", sub_title))
    story.append(Image("assets/exp3_cleaning_boxplot.png", width=440, height=220))
    story.append(Spacer(1, 14))

    story.append(create_rubric_table())
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>Result:</b>", result_heading))
    story.append(Paragraph(
        "Missing values and anomalous outlier entries were successfully identified, imputed, and filtered using Pandas. "
        "The cleaned dataset demonstrated superior data consistency, and comparative boxplots confirmed the elimination "
        "of extreme skewness caused by anomalous values.",
        result_txt
    ))

    story.append(PageBreak())

    # =========================================================================
    # EXPERIMENT 4: INTERACTIVE CHARTS WITH PLOTLY
    # =========================================================================
    story.append(create_header_table("EXP NO: 04", "DATE: 12-10-2026", "INTERACTIVE CHARTS WITH PLOTLY"))
    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>Aim:</b>", aim_heading))
    story.append(Paragraph(
        "To create dynamic, interactive web charts using Plotly Express by configuring multi-variable "
        "scatter plots with bubble size and color dimensions, time-series/product line charts, and interactive bar charts.",
        body_txt
    ))
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Procedure:</b>", proc_heading))
    proc4_points = [
        "Open Jupyter Notebook or Google Colab.",
        "Import required visualization libraries: <code>pandas</code> and <code>plotly.express</code>.",
        "Load the electronics product performance dataset (<code>tech_products_sales.csv</code>).",
        "Display the first five rows using <code>head()</code> to verify field structure.",
        "Create an interactive scatter plot using <code>px.scatter()</code> with bubble sizes scaled by Units Sold and colors mapped to Categories.",
        "Add rich metadata tooltips using the <code>hover_data</code> parameter.",
        "Create an interactive multi-line chart using <code>px.line()</code> with markers to visualize product revenue.",
        "Build an interactive bar chart using <code>px.bar()</code> displaying volume sales across individual products.",
        "Display and analyze the interactive charts using <code>fig.show()</code>."
    ]
    for pt in proc4_points:
        story.append(Paragraph(f"• {pt}", proc_item))

    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Program:</b>", prog_heading))
    code_exp4_init = """import pandas as pd
import plotly.express as px

# Load dataset
df = pd.read_csv("tech_products_sales.csv")
print(df.head())"""
    story.append(Preformatted(code_exp4_init, code_style))
    story.append(Spacer(1, 3))

    head_output_exp4 = """                   Product     Category  Units_Sold  Unit_Price  Revenue  Rating  Return_Rate
0            Smart Watch X    Wearables         450         180    81000     4.5          2.1
1  Noise-Cancel Headphones        Audio         320         240    76800     4.8          1.5
2         Wireless Earbuds        Audio         780          85    66300     4.3          3.2
3          Fitness Tracker    Wearables         520          95    49400     4.1          2.8
4            Tablet Pro 11    Computing         210         650   136500     4.7          1.1"""
    story.append(Preformatted(head_output_exp4, ParagraphStyle('CodeOut', parent=code_style, textColor=colors.HexColor("#222222"))))

    story.append(PageBreak())

    # Page 2 of Exp 4: Interactive Scatter Plot & Line Chart
    story.append(Paragraph("<b># 1. Interactive Scatter Plot: Price vs Revenue (Bubble Size = Units)</b>", sub_title))
    code_exp4_scat = """fig1 = px.scatter(
    df,
    x="Unit_Price",
    y="Revenue",
    color="Category",
    size="Units_Sold",
    hover_data=["Product", "Rating", "Return_Rate"],
    title="Product Price vs Revenue (Bubble Size = Units Sold)",
    template="plotly_white"
)
fig1.show()"""
    story.append(Preformatted(code_exp4_scat, code_style))
    story.append(Spacer(1, 4))
    story.append(Image("assets/exp4_plotly_scatter.png", width=420, height=210))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b># 2. Interactive Line Chart: Product Revenue Trajectory</b>", sub_title))
    code_exp4_line = """fig2 = px.line(
    df,
    x="Product",
    y="Revenue",
    color="Category",
    markers=True,
    hover_data=["Units_Sold", "Rating"],
    title="Revenue Distribution by Product",
    template="plotly_white"
)
fig2.show()"""
    story.append(Preformatted(code_exp4_line, code_style))
    story.append(Spacer(1, 4))
    story.append(Image("assets/exp4_plotly_line.png", width=420, height=210))

    story.append(PageBreak())

    # Page 3 of Exp 4: Interactive Bar Chart, Rubric & Result
    story.append(Paragraph("<b># 3. Interactive Bar Chart: Units Sold Across Product Catalog</b>", sub_title))
    code_exp4_bar = """fig3 = px.bar(
    df,
    x="Product",
    y="Units_Sold",
    color="Category",
    hover_data=["Unit_Price", "Revenue", "Rating"],
    title="Total Units Sold by Product",
    template="plotly_white"
)
fig3.show()"""
    story.append(Preformatted(code_exp4_bar, code_style))
    story.append(Spacer(1, 4))
    story.append(Image("assets/exp4_plotly_bar.png", width=420, height=210))
    story.append(Spacer(1, 10))

    story.append(create_rubric_table())
    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>Result:</b>", result_heading))
    story.append(Paragraph(
        "The interactive scatter plot, line chart, and bar chart were successfully created using Plotly Express. "
        "Rich hover tooltips, size encodings, and category color-filtering enabled effective exploration of pricing, "
        "sales volumes, and product catalog revenues.",
        result_txt
    ))

    story.append(PageBreak())

    # =========================================================================
    # EXPERIMENT 5: CHARTS AND DASHBOARD USING TABLEAU
    # =========================================================================
    story.append(create_header_table("EXP NO: 05", "DATE: 12-10-2026", "CHARTS AND DASHBOARD USING TABLEAU"))
    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>Aim:</b>", aim_heading))
    story.append(Paragraph(
        "To connect a multivariable retail transaction dataset (<code>e_commerce_orders.csv</code>) to Tableau, "
        "construct multiple analytical charts (horizontal bar chart, profit-discount trend, scatter plot, "
        "profit-margin count, and sales histogram), and integrate them into a synchronized interactive dashboard.",
        body_txt
    ))
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Procedure:</b>", proc_heading))
    proc5_points = [
        "Launch Tableau Desktop or Tableau Public and select Connect → Text File.",
        "Locate and connect the retail transaction dataset (<code>e_commerce_orders.csv</code>).",
        "Inspect the Data Source sheet to verify categorical dimensions (Region, Category, Ship Mode) and measures (Sales, Profit, Discount).",
        "Sheet 1: Create a horizontal bar chart displaying Total Sales by Region.",
        "Sheet 2: Create a trend line tracking Average Profit against Discount rate levels.",
        "Sheet 3: Construct a scatter plot correlating Discount vs Profit with circle marks.",
        "Sheet 4: Create a column bar chart displaying the count of records by High Profit Margin classification.",
        "Sheet 5: Build a sales distribution histogram using custom bin sizing.",
        "Assemble all individual worksheets into an interactive Dashboard with synchronized regional and categorical filters.",
        "Review layout formatting and save the workbook as a Tableau Packaged Workbook (<code>.twbx</code>)."
    ]
    for pt in proc5_points:
        story.append(Paragraph(f"• {pt}", proc_item))

    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Process:</b>", prog_heading))
    step_exp5_init = """Step 1: Connect the Dataset
• Open Tableau Desktop / Tableau Public.
• Click Connect -> Text File and open e_commerce_orders.csv (1,000 records, 8 fields).
• Verify the fields: Region, Category, Ship_Mode, Sales, Discount, Profit, High_Profit_Margin.

Step 2: Create Visual Worksheets
Chart 1 - Total Sales by Region
• Drag Region to Rows.
• Drag Sales to Columns (Aggregation: SUM).
• Select Bar Chart and apply sorting in descending order.
• Set Chart Title: "Total Sales by Region"."""
    story.append(Preformatted(step_exp5_init, code_style))
    story.append(Spacer(1, 4))
    story.append(Image("assets/exp5_tableau_chart1.png", width=360, height=185))

    story.append(PageBreak())

    # Page 2 of Exp 5: Charts 2 and 3
    story.append(Paragraph("<b>Chart 2 – Average Profit vs Discount Trend</b>", sub_title))
    step_exp5_c2 = """• Drag Discount to Columns (Discrete / Dimension).
• Drag Profit to Rows (Aggregation: AVG).
• Change Marks card to Line Chart and enable data points.
• Set Chart Title: "Average Profit vs Discount Trend"."""
    story.append(Preformatted(step_exp5_c2, code_style))
    story.append(Spacer(1, 4))
    story.append(Image("assets/exp5_tableau_chart2.png", width=360, height=185))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Chart 3 – Discount vs Profit Scatter Analysis</b>", sub_title))
    step_exp5_c3 = """• Drag Discount to Columns (Continuous measure).
• Drag Profit to Rows (Continuous measure).
• Change Marks to Circle; uncheck Analysis -> Aggregate Measures to view granular transactions.
• Drag High_Profit_Margin to Color mark.
• Set Chart Title: "Discount vs Profit Analysis"."""
    story.append(Preformatted(step_exp5_c3, code_style))
    story.append(Spacer(1, 4))
    story.append(Image("assets/exp5_tableau_chart3.png", width=360, height=185))

    story.append(PageBreak())

    # Page 3 of Exp 5: Charts 4, 5 and Dashboard view
    story.append(Paragraph("<b>Chart 4 & 5 – Volume by Margin & Sales Distribution</b>", sub_title))
    step_exp5_c45 = """Chart 4: Drag High_Profit_Margin to Columns, Drag Orders (Count) to Rows.
Chart 5: Right-click Sales -> Create Bins (Bin size: 100), drag Sales (bin) to Columns and COUNT to Rows."""
    story.append(Preformatted(step_exp5_c45, code_style))
    story.append(Spacer(1, 4))
    
    # 2 charts side by side
    t_c45 = Table([[Image("assets/exp5_tableau_chart4.png", width=245, height=140),
                    Image("assets/exp5_tableau_chart5.png", width=245, height=140)]], colWidths=[255, 255])
    t_c45.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER'), ('VALIGN', (0,0), (-1,-1), 'MIDDLE')]))
    story.append(t_c45)
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Dashboard Creation & Integration</b>", sub_title))
    step_exp5_dash = """• Click New Dashboard and set canvas size to 1000 x 700 px.
• Drag the four analytical sheets into a clean 2x2 grid layout.
• Add Interactive Filters for Region and Category; configure filters to "Apply to All Worksheets"."""
    story.append(Preformatted(step_exp5_dash, code_style))
    story.append(Spacer(1, 4))
    story.append(Image("assets/exp5_tableau_dashboard.png", width=420, height=215))

    story.append(PageBreak())

    # Page 4 of Exp 5: Rubric & Result
    story.append(Spacer(1, 20))
    story.append(create_rubric_table())
    story.append(Spacer(1, 15))
    story.append(Paragraph("<b>Result:</b>", result_heading))
    story.append(Paragraph(
        "Different analytical visualizations were successfully created using categorical, numerical, and derived variables "
        "of the retail transaction dataset in Tableau. The worksheets were combined into an interactive dashboard "
        "allowing real-time multi-dimensional analysis of regional sales, discounting patterns, and profit performance.",
        result_txt
    ))

    story.append(PageBreak())

    # =========================================================================
    # EXPERIMENT 6: POWER BI WORKSHOP
    # =========================================================================
    story.append(create_header_table("EXP NO: 06", "DATE: 12-10-2026", "POWER BI WORKSHOP"))
    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>Aim:</b>", aim_heading))
    story.append(Paragraph(
        "To import, clean, model, and visualize the Global Energy Transition dataset (<code>energy_transition_2024.csv</code>) "
        "using Power BI Desktop, creating KPI summary cards, clustered bar/column charts, scatter plots, and interactive slicers.",
        body_txt
    ))
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Short Procedure:</b>", proc_heading))
    proc6_points = [
        "Open Power BI Desktop.",
        "Import the energy transition dataset using Home → Get Data → Text/CSV (or Excel).",
        "Open Power Query Transform Data to verify column headers, data types, and check for null values.",
        "Click Close & Apply to load the prepared dataset into Power BI's data model.",
        "Create KPI Card visualizations displaying average renewable energy adoption and transition index.",
        "Build a Clustered Bar Chart comparing Renewable Energy Share (%) across evaluated nations.",
        "Construct a Clustered Column Chart illustrating CO2 Emissions Per Capita.",
        "Create a Scatter Chart examining the correlation between Renewable Share and CO2 Emissions.",
        "Add a Country Slicer to allow dynamic filtering and benchmarking.",
        "Organize all visuals into a cohesive dashboard report and save as a <code>.pbix</code> file."
    ]
    for pt in proc6_points:
        story.append(Paragraph(f"• {pt}", proc_item))

    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Process:</b>", prog_heading))
    step_exp6_text = """1. Open Power BI Desktop.
2. Click Home -> Get Data -> Text/CSV.
3. Select energy_transition_2024.csv and click Transform Data.
4. Verify data types:
   • Country: Text
   • Renewable_Share_Pct: Decimal Number / Percentage
   • CO2_Emissions_Per_Capita: Decimal Number
   • Energy_Transition_Index: Decimal Number
5. Click Close & Apply.

Visual Implementation Steps:
• Card Visual 1 - Average Renewable Share:
  Select Card visual -> Field: Renewable_Share_Pct (Aggregation: Average).
• Card Visual 2 - Average Transition Index:
  Select Card visual -> Field: Energy_Transition_Index (Aggregation: Average).
• Bar Chart - Renewable Share by Country:
  Select Clustered Bar Chart -> Y-Axis: Country, X-Axis: Renewable_Share_Pct (Sort Descending).
• Column Chart - CO2 Emissions Per Capita:
  Select Clustered Column Chart -> X-Axis: Country, Y-Axis: CO2_Emissions_Per_Capita.
• Scatter Chart - Renewable Share vs CO2 Emissions:
  Select Scatter Chart -> X-Axis: Renewable_Share_Pct, Y-Axis: CO2_Emissions_Per_Capita, Details: Country.
• Slicer Visual:
  Select Slicer -> Field: Country (Dropdown/List selection)."""
    story.append(Preformatted(step_exp6_text, code_style))

    story.append(PageBreak())

    # Page 2 of Exp 6: Dashboard visual, Rubric & Result
    story.append(Paragraph("<b>Power BI Energy Transition Dashboard Overview:</b>", sub_title))
    story.append(Image("assets/exp6_powerbi_dashboard.png", width=460, height=290))
    story.append(Spacer(1, 15))

    story.append(create_rubric_table())
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>Result:</b>", result_heading))
    story.append(Paragraph(
        "The Global Energy Transition dataset was successfully imported, cleaned in Power Query, and visualized using "
        "Power BI Desktop. The interactive dashboard, KPI cards, and cross-filtering slicers enabled intuitive "
        "exploration of renewable adoption and carbon emission metrics across countries.",
        result_txt
    ))

    story.append(PageBreak())

    # =========================================================================
    # EXPERIMENT 7: GEOSPATIAL EDA USING FOLIUM
    # =========================================================================
    story.append(create_header_table("EXP NO: 07", "DATE: 12-10-2026", "GEOSPATIAL EDA USING FOLIUM"))
    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>Aim:</b>", aim_heading))
    story.append(Paragraph(
        "To perform Geospatial Exploratory Data Analysis (EDA) and visualize global volcanic activity "
        "using Folium interactive maps, including location circle markers, magnitude-scaled bubble maps, "
        "spatial density heatmaps, and choropleth regional distributions.",
        body_txt
    ))
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Procedure:</b>", proc_heading))
    proc7_points = [
        "Open Google Colab / Jupyter Notebook and import Python libraries: <code>pandas</code>, <code>folium</code>, and <code>HeatMap</code>.",
        "Load the global active volcano dataset (<code>world_volcanoes.csv</code>).",
        "Inspect the dataset structure, validating coordinates (<code>latitude</code> and <code>longitude</code>) and explosivity index (<code>vei</code>).",
        "Drop or verify non-null coordinates suitable for geographic projection.",
        "Initialize a baseline interactive Folium map centered on coordinates [20, 10] with <code>zoom_start=2</code>.",
        "Construct a Circle Marker map with popups showing volcano name, country, and elevation.",
        "Generate a bubble hotspot map with circle radii dynamically scaled by the Volcanic Explosivity Index (VEI).",
        "Create a spatial density HeatMap to identify high-density tectonic boundary clusters.",
        "Build a choropleth/regional distribution chart visualizing activity counts across countries.",
        "Export all generated map objects as interactive HTML files."
    ]
    for pt in proc7_points:
        story.append(Paragraph(f"• {pt}", proc_item))

    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Program:</b>", prog_heading))
    code_exp7_init = """import pandas as pd
import folium
from folium.plugins import HeatMap

# Load volcanic activity dataset
df = pd.read_csv("world_volcanoes.csv")
print("Dataset Head:")
print(df.head())
print("\\nRecords available for mapping:", len(df))"""
    story.append(Preformatted(code_exp7_init, code_style))
    story.append(Spacer(1, 3))

    out_exp7_init = """Dataset Head:
               name    country  latitude  longitude  elevation  vei
0  Eyjafjallajökull    Iceland     63.63     -19.62       1666    4
1        Mount Fuji      Japan     35.36     138.73       3776    5
2    Mount Vesuvius      Italy     40.82      14.43       1281    5
3          Krakatoa  Indonesia     -6.10     105.42        813    6
4  Mount St. Helens  United States 46.20    -122.19       2549    5

Records available for mapping: 15"""
    story.append(Preformatted(out_exp7_init, ParagraphStyle('CodeOut', parent=code_style, textColor=colors.HexColor("#222222"))))

    story.append(PageBreak())

    # Page 2 of Exp 7: Map 1 (CircleMarker) and Map 2 (Bubble Map)
    story.append(Paragraph("<b># 1. Interactive Circle Marker Map</b>", sub_title))
    code_exp7_m1 = """volcano_map = folium.Map(location=[20, 10], zoom_start=2)
for _, row in df.iterrows():
    folium.CircleMarker(
        location=[row["latitude"], row["longitude"]],
        radius=6,
        popup=f"<b>{row['name']}</b><br>Elevation: {row['elevation']} m<br>Country: {row['country']}",
        tooltip=row["name"],
        color="blue",
        fill=True,
        fill_opacity=0.7
    ).add_to(volcano_map)
volcano_map.save("volcano_marker_map.html")"""
    story.append(Preformatted(code_exp7_m1, code_style))
    story.append(Spacer(1, 4))
    story.append(Image("assets/exp7_marker_map.png", width=420, height=195))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b># 2. Bubble Map (Scaled by Volcanic Explosivity Index)</b>", sub_title))
    code_exp7_m2 = """bubble_map = folium.Map(location=[20, 10], zoom_start=2)
for _, row in df.iterrows():
    folium.CircleMarker(
        location=[row["latitude"], row["longitude"]],
        radius=row["vei"] * 3,
        popup=f"<b>{row['name']}</b><br>VEI: {row['vei']}",
        tooltip=f"{row['name']} (VEI: {row['vei']})",
        color="crimson",
        fill=True,
        fill_color="red",
        fill_opacity=0.6
    ).add_to(bubble_map)
bubble_map.save("volcano_bubble_map.html")"""
    story.append(Preformatted(code_exp7_m2, code_style))
    story.append(Spacer(1, 4))
    story.append(Image("assets/exp7_bubble_map.png", width=420, height=195))

    story.append(PageBreak())

    # Page 3 of Exp 7: Map 3 (Heatmap) and Choropleth
    story.append(Paragraph("<b># 3. Density HeatMap (Tectonic Cluster Intensity)</b>", sub_title))
    code_exp7_m3 = """heatmap = folium.Map(location=[20, 10], zoom_start=2)
heat_data = [[row["latitude"], row["longitude"], row["vei"]] for _, row in df.iterrows()]
HeatMap(heat_data, radius=18, blur=12, min_opacity=0.4).add_to(heatmap)
heatmap.save("volcano_heatmap.html")"""
    story.append(Preformatted(code_exp7_m3, code_style))
    story.append(Spacer(1, 4))
    story.append(Image("assets/exp7_heatmap.png", width=420, height=195))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b># 4. Regional Distribution / Choropleth Representation</b>", sub_title))
    code_exp7_m4 = """country_counts = df['country'].value_counts().reset_index()
country_counts.columns = ['country', 'volcano_count']
# Save map objects and exports
print("All Folium maps exported successfully to HTML files!")"""
    story.append(Preformatted(code_exp7_m4, code_style))
    story.append(Spacer(1, 4))
    story.append(Image("assets/exp7_choropleth_bar.png", width=420, height=190))

    story.append(PageBreak())

    # Page 4 of Exp 7: Rubric & Result
    story.append(Spacer(1, 20))
    story.append(create_rubric_table())
    story.append(Spacer(1, 15))
    story.append(Paragraph("<b>Result:</b>", result_heading))
    story.append(Paragraph(
        "Geospatial Exploratory Data Analysis (EDA) was successfully performed using Folium. Interactive marker maps, "
        "explosivity-scaled bubble maps, spatial cluster heatmaps, and regional distributions were constructed "
        "and exported as interactive HTML documents.",
        result_txt
    ))

    story.append(PageBreak())

    # =========================================================================
    # EXPERIMENT 8: D3.JS DATA VISUALIZATION USING A BAR CHART
    # =========================================================================
    story.append(create_header_table("EXP NO: 08", "DATE: 12-10-2026", "D3.js DATA VISUALIZATION USING A BAR CHART"))
    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>Aim:</b>", aim_heading))
    story.append(Paragraph(
        "To introduce D3.js by loading CSV data via JavaScript asynchronous fetch, binding data to SVG elements, "
        "and creating an interactive web bar chart with axes, value labels, and hover effects.",
        body_txt
    ))
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Procedure:</b>", proc_heading))
    proc8_points = [
        "Create an HTML file named <code>index.html</code>.",
        "Create a CSV dataset named <code>data.csv</code> (technology domain projects).",
        "Add sample categories and project counts to the CSV file.",
        "Include the official D3.js library (v7) via CDN script tag.",
        "Define an SVG canvas container with explicit width, height, and margins.",
        "Use <code>d3.csv()</code> to asynchronously load and parse the CSV data.",
        "Convert categorical project count strings into numeric values.",
        "Establish <code>scaleBand</code> for the categorical X-axis and <code>scaleLinear</code> for the numeric Y-axis.",
        "Bind data to SVG rect elements to render bars with dynamic heights and hover color transitions.",
        "Append bottom and left axes, descriptive titles, and numerical value labels on top of each bar.",
        "Open the HTML file in a web browser using a local HTTP server and observe the visualization."
    ]
    for pt in proc8_points:
        story.append(Paragraph(f"• {pt}", proc_item))

    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Program:</b>", prog_heading))
    story.append(Paragraph("<b>i) data.csv</b>", sub_title))
    csv_table_data = [
        [Paragraph("<b>Category</b>", ParagraphStyle('TH', fontName='Helvetica-Bold', fontSize=9, alignment=1)),
         Paragraph("<b>Project_Count</b>", ParagraphStyle('TH', fontName='Helvetica-Bold', fontSize=9, alignment=1))],
        [Paragraph("Cloud Computing", ParagraphStyle('TB', fontName='Helvetica', fontSize=8.5)), Paragraph("48", ParagraphStyle('TB', fontName='Helvetica', fontSize=8.5, alignment=1))],
        [Paragraph("Data Analytics", ParagraphStyle('TB', fontName='Helvetica', fontSize=8.5)), Paragraph("62", ParagraphStyle('TB', fontName='Helvetica', fontSize=8.5, alignment=1))],
        [Paragraph("Cybersecurity", ParagraphStyle('TB', fontName='Helvetica', fontSize=8.5)), Paragraph("35", ParagraphStyle('TB', fontName='Helvetica', fontSize=8.5, alignment=1))],
        [Paragraph("Web Systems", ParagraphStyle('TB', fontName='Helvetica', fontSize=8.5)), Paragraph("74", ParagraphStyle('TB', fontName='Helvetica', fontSize=8.5, alignment=1))],
        [Paragraph("Artificial Intelligence", ParagraphStyle('TB', fontName='Helvetica', fontSize=8.5)), Paragraph("91", ParagraphStyle('TB', fontName='Helvetica', fontSize=8.5, alignment=1))]
    ]
    t_csv = Table(csv_table_data, colWidths=[240, 140])
    t_csv.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, colors.black),
        ('INNERGRID', (0,0), (-1,-1), 0.7, colors.black),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f0f0f0")),
    ]))
    story.append(t_csv)

    story.append(PageBreak())

    # Page 2 of Exp 8: index.html Code (part 1)
    story.append(Paragraph("<b>ii) index.html</b>", sub_title))
    html_code_part1 = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>D3.js Bar Chart</title>
  <!-- D3.js Version 7 -->
  <script src="https://d3js.org/d3.v7.min.js"></script>
  <style>
    body { font-family: Arial, sans-serif; text-align: center; }
    h1 { color: #2c3e50; margin-bottom: 20px; }
    .bar { fill: steelblue; transition: fill 0.2s ease; }
    .bar:hover { fill: orange; }
    .value { font-size: 13px; font-weight: bold; fill: #2c3e50; }
    .axis-label { font-size: 14px; font-weight: bold; fill: #34495e; }
  </style>
</head>
<body>
  <h1>Projects Completed by Technology Domain</h1>
  <svg width="700" height="500"></svg>
  <script>
    const svg = d3.select("svg");
    const width = 700;
    const height = 500;
    const margin = { top: 40, right: 30, bottom: 80, left: 70 };

    d3.csv("data.csv").then(function(data) {
      data.forEach(function(d) {
        d.Project_Count = +d.Project_Count;
      });

      const x = d3.scaleBand()
        .domain(data.map(d => d.Category))
        .range([margin.left, width - margin.right])
        .padding(0.3);

      const y = d3.scaleLinear()
        .domain([0, d3.max(data, d => d.Project_Count) * 1.15])
        .nice()
        .range([height - margin.bottom, margin.top]);"""
    story.append(Preformatted(html_code_part1, code_style))

    story.append(PageBreak())

    # Page 3 of Exp 8: index.html Code (part 2)
    html_code_part2 = """      // X-Axis
      svg.append("g")
        .attr("class", "axis")
        .attr("transform", `translate(0, ${height - margin.bottom})`)
        .call(d3.axisBottom(x));

      // Y-Axis
      svg.append("g")
        .attr("class", "axis")
        .attr("transform", `translate(${margin.left}, 0)`)
        .call(d3.axisLeft(y));

      // Render Bars
      svg.selectAll(".bar")
        .data(data)
        .enter()
        .append("rect")
        .attr("class", "bar")
        .attr("x", d => x(d.Category))
        .attr("y", d => y(d.Project_Count))
        .attr("width", x.bandwidth())
        .attr("height", d => (height - margin.bottom) - y(d.Project_Count));

      // Render Values on Top of Bars
      svg.selectAll(".value")
        .data(data)
        .enter()
        .append("text")
        .attr("class", "value")
        .attr("x", d => x(d.Category) + x.bandwidth() / 2)
        .attr("y", d => y(d.Project_Count) - 8)
        .attr("text-anchor", "middle")
        .text(d => d.Project_Count);

      // Axis Labels
      svg.append("text")
        .attr("class", "axis-label")
        .attr("x", width / 2)
        .attr("y", height - 20)
        .attr("text-anchor", "middle")
        .text("Technology Category");

      svg.append("text")
        .attr("class", "axis-label")
        .attr("transform", "rotate(-90)")
        .attr("x", -(height / 2))
        .attr("y", 25)
        .attr("text-anchor", "middle")
        .text("Number of Projects");
    }).catch(function(err) {
      console.log("Error loading CSV:", err);
    });
  </script>
</body>
</html>"""
    story.append(Preformatted(html_code_part2, code_style))

    story.append(PageBreak())

    # Page 4 of Exp 8: Output Chart, Rubric & Result
    story.append(Paragraph("<b>OUTPUT</b>", aim_heading))
    story.append(Spacer(1, 4))
    story.append(Image("assets/exp8_d3_barchart_output.png", width=450, height=265))
    story.append(Spacer(1, 15))

    story.append(create_rubric_table())
    story.append(Spacer(1, 12))
    story.append(Paragraph("<b>Result:</b>", result_heading))
    story.append(Paragraph(
        "A working interactive D3.js web bar chart was successfully created by loading external CSV data. "
        "The visualization accurately rendered dynamic SVG bars, numerical value labels, custom axes, and "
        "smooth hover color interactions across technological categories.",
        result_txt
    ))

    # Build the document
    doc.build(story, canvasmaker=AcademicBorderCanvas)
    print(f"Successfully generated {pdf_filename}!")

if __name__ == "__main__":
    build_pdf()
