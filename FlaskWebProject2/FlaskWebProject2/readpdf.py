# Script to export tables from PDF files
# Requirements:
# Pandas (cmd --> pip install pandas)
# Java   (https://www.java.com/en/download/)
# Tabula (cmd --> pip install tabula-py)
# openpyxl (cmd --> pip install openpyxl) to export to Excel from pandas dataframe

import tabula
import pandas as pd

# Path to input PDF file
pdf_in = "C:/Temp/результаты.pdf" #Path to PDF

# pages and multiple_tables are optional attributes
# outputs df as list
PDF = tabula.read_pdf(pdf_in, pages='all', multiple_tables=True)

#View result
print ('\nTables from PDF file\n'+str(PDF))

pdf_out_csv = "C:/Temp/результаты1.csv"

tabula.convert_into (pdf_in, pdf_out_csv, pages='1')
print("Done")