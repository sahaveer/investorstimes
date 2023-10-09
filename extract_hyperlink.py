import clr
clr.AddReference("Microsoft.Office.Interop.Excel")
import Microsoft.Office.Interop.Excel as Excel
excel = Excel.ApplicationClass()

wb = excel.Workbooks.Open('./screener/screener.xlsx')
ws = wb.Worksheets['Sheet1']

address = ws.Cells(row, col).Hyperlinks.Item(1).Address