import pandas as pd
import matplotlib.pyplot as plt
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

def df2pdf(df, output_file):
    # 創建 PDF 文件
    pdf_filename = output_file
    pdf = SimpleDocTemplate(pdf_filename, pagesize=letter)
    data = [df.columns[:,].values.astype(str)] + df.values.tolist()

    # # 計算列寬
    # num_cols = len(df.columns)
    # col_widths = [100] * num_cols  # 初始化列寬，這裡假設每列寬度為100
    # 創建表格
    t = Table(data)

    # 添加表格樣式
    t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 2),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black),
                        ('FONTSIZE', (0, 0), (-1, -1), 4)]))
    # 將表格添加到 PDF 文件
    pdf.build([t])

    print(f"PDF file saved as {pdf_filename}")
    return