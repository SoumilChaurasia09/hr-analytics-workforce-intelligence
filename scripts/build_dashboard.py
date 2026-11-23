"""
Master Executive HR Analytics & Retention Dashboard
Flawless Native Excel Charts, Precise Data Ranges, Y-Axis Scaling,
Data Labels, Clean Table Alignment, and Role Risk Leaderboard.
"""

import os
import pandas as pd
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.chart import BarChart, Reference
from openpyxl.chart.label import DataLabelList

base_dir = r"C:\Users\soumi\.gemini\antigravity\scratch\hr_analytics_excel"
cleaned_csv = os.path.join(base_dir, "data", "cleaned_hr_data.csv")
out_xlsx = os.path.join(base_dir, "HR_Analytics_and_Workforce_Intelligence.xlsx")

df = pd.read_csv(cleaned_csv)
wb = openpyxl.Workbook()
wb.remove(wb.active)

# Executive Modern Palette
CANVAS_BG = "F8FAFC"       # Clean soft canvas background
CARD_BG = "FFFFFF"         # Pure white card container
NAVY_HEADER = "0F172A"     # Sleek dark slate
NAVY_CARD = "1E293B"       # Dark blue-gray for KPI headers
BLUE_ACCENT = "2563EB"     # Royal blue metric
RED_ALERT = "DC2626"       # Crimson red for high risk
GREEN_STABLE = "16A34A"    # Forest green for stable
GRAY_TEXT = "64748B"       # Subtle slate subtext
BORDER_COLOR = "E2E8F0"    # Subtle border color

thin_border = Border(
    left=Side(style='thin', color=BORDER_COLOR),
    right=Side(style='thin', color=BORDER_COLOR),
    top=Side(style='thin', color=BORDER_COLOR),
    bottom=Side(style='thin', color=BORDER_COLOR)
)

table_border = Border(
    left=Side(style='thin', color="CBD5E1"),
    right=Side(style='thin', color="CBD5E1"),
    top=Side(style='thin', color="CBD5E1"),
    bottom=Side(style='thin', color="CBD5E1")
)

# ==============================================================================
# TAB 1: EXECUTIVE WORKFORCE DASHBOARD
# ==============================================================================
ws_dash = wb.create_sheet("Workforce Dashboard")
ws_dash.views.sheetView[0].showGridLines = False  # App-style borderless canvas
ws_dash.sheet_properties.tabColor = BLUE_ACCENT

# Fill canvas background with sleek soft slate
for r in range(1, 46):
    for c in range(1, 18):
        ws_dash.cell(row=r, column=c).fill = PatternFill(start_color=CANVAS_BG, end_color=CANVAS_BG, fill_type="solid")

# 1. Executive Top Header Banner (B2:P3)
ws_dash.merge_cells("B2:P3")
h = ws_dash["B2"]
h.value = "WORKFORCE INTELLIGENCE & TALENT RETENTION COCKPIT"
h.font = Font(name="Segoe UI", size=16, bold=True, color="FFFFFF")
h.fill = PatternFill(start_color=NAVY_HEADER, end_color=NAVY_HEADER, fill_type="solid")
h.alignment = Alignment(horizontal="center", vertical="center")

ws_dash.merge_cells("B4:P4")
sub = ws_dash["B4"]
sub.value = "Enterprise Attrition Diagnostics  |  Departmental Flight Risk & Overtime Workload Economics"
sub.font = Font(name="Segoe UI", size=10, italic=False, color=GRAY_TEXT)
sub.fill = PatternFill(start_color=CARD_BG, end_color=CARD_BG, fill_type="solid")
sub.alignment = Alignment(horizontal="center", vertical="center")
sub.border = Border(bottom=Side(style='thin', color="CBD5E1"))

# 2. Hero KPI Cards (Row 6 to 9)
# 5 distinct floating cards across columns B to P
kpi_cards = [
    {"h_rng": "B6:C6", "v_rng": "B7:C8", "s_rng": "B9:C9",
     "title": "TOTAL WORKFORCE", "formula": "=COUNTA(Data!A2:A1471)", "fmt": "#,##0", "color": BLUE_ACCENT, "sub": "1,470 Active Headcount"},
    
    {"h_rng": "E6:F6", "v_rng": "E7:F8", "s_rng": "E9:F9",
     "title": "TOTAL DEPARTURES", "formula": '=COUNTIF(Data!B2:B1471, "Yes")', "fmt": "#,##0", "color": RED_ALERT, "sub": "237 Leavers to Date"},

    {"h_rng": "H6:I6", "v_rng": "H7:I8", "s_rng": "H9:I9",
     "title": "ATTRITION RATE %", "formula": "=E7/B7", "fmt": "0.0%", "color": RED_ALERT, "sub": "Benchmark Target: < 12%"},

    {"h_rng": "K6:L6", "v_rng": "K7:L8", "s_rng": "K9:L9",
     "title": "AVG MONTHLY SALARY", "formula": "=AVERAGE(Data!R2:R1471)", "fmt": "$#,##0", "color": NAVY_CARD, "sub": "$6,503 Enterprise Mean"},

    {"h_rng": "N6:P6", "v_rng": "N7:P8", "s_rng": "N9:P9",
     "title": "EST. ANNUAL TURNOVER LOSS", "formula": '=SUMIF(Data!B2:B1471, "Yes", Data!R2:R1471)*12*0.5', "fmt": "$#,##0", "color": RED_ALERT, "sub": "Based on 50% Replacement Cost"}
]

for card in kpi_cards:
    # Header
    ws_dash.merge_cells(card["h_rng"])
    top_h = ws_dash[card["h_rng"].split(":")[0]]
    top_h.value = card["title"]
    top_h.font = Font(name="Segoe UI", size=9, bold=True, color="FFFFFF")
    top_h.fill = PatternFill(start_color=NAVY_CARD, end_color=NAVY_CARD, fill_type="solid")
    top_h.alignment = Alignment(horizontal="center", vertical="center")

    # Big Number Value
    ws_dash.merge_cells(card["v_rng"])
    top_v = ws_dash[card["v_rng"].split(":")[0]]
    top_v.value = card["formula"]
    top_v.font = Font(name="Segoe UI", size=18, bold=True, color=card["color"])
    top_v.fill = PatternFill(start_color=CARD_BG, end_color=CARD_BG, fill_type="solid")
    top_v.alignment = Alignment(horizontal="center", vertical="center")
    top_v.number_format = card["fmt"]

    # Subtext
    ws_dash.merge_cells(card["s_rng"])
    top_s = ws_dash[card["s_rng"].split(":")[0]]
    top_s.value = card["sub"]
    top_s.font = Font(name="Segoe UI", size=8, color=GRAY_TEXT)
    top_s.fill = PatternFill(start_color="F1F5F9", end_color="F1F5F9", fill_type="solid")
    top_s.alignment = Alignment(horizontal="center", vertical="center")
    top_s.border = Border(bottom=Side(style='thin', color=BORDER_COLOR))

# 3. Section 2: Two Side-by-Side Data Tables (Rows 11 to 16)
# Table A: Department Turnover (B11:F16)
ws_dash["B11"] = "DEPARTMENT ATTRITION & BUDGET SUMMARY"
ws_dash["B11"].font = Font(name="Segoe UI", size=11, bold=True, color=NAVY_HEADER)

dept_headers = ["Department", "Headcount", "Leavers", "Attrition %", "Avg Monthly Pay"]
for idx, title in enumerate(dept_headers, start=2):
    cell = ws_dash.cell(row=12, column=idx, value=title)
    cell.font = Font(name="Segoe UI", size=9, bold=True, color="FFFFFF")
    cell.fill = PatternFill(start_color=NAVY_HEADER, end_color=NAVY_HEADER, fill_type="solid")
    cell.alignment = Alignment(horizontal="center" if idx > 2 else "left", vertical="center")

depts = [("Sales", 13), ("Research & Development", 14), ("Human Resources", 15)]
for d_name, r in depts:
    ws_dash.cell(row=r, column=2, value=d_name).font = Font(name="Segoe UI", size=9, bold=True, color=NAVY_CARD)
    ws_dash.cell(row=r, column=2).fill = PatternFill(start_color=CARD_BG, end_color=CARD_BG, fill_type="solid")

    c_hc = ws_dash.cell(row=r, column=3, value=f"=COUNTIF(Data!E2:E1471, B{r})")
    c_hc.number_format = "#,##0"
    c_hc.alignment = Alignment(horizontal="center")
    c_hc.fill = PatternFill(start_color=CARD_BG, end_color=CARD_BG, fill_type="solid")

    c_lev = ws_dash.cell(row=r, column=4, value=f'=COUNTIFS(Data!E2:E1471, B{r}, Data!B2:B1471, "Yes")')
    c_lev.number_format = "#,##0"
    c_lev.alignment = Alignment(horizontal="center")
    c_lev.fill = PatternFill(start_color=CARD_BG, end_color=CARD_BG, fill_type="solid")

    c_rate = ws_dash.cell(row=r, column=5, value=f"=D{r}/C{r}")
    c_rate.number_format = "0.0%"
    c_rate.font = Font(name="Segoe UI", size=9, bold=True, color=RED_ALERT if d_name=="Sales" else NAVY_CARD)
    c_rate.alignment = Alignment(horizontal="center")
    c_rate.fill = PatternFill(start_color="FEF2F2" if d_name=="Sales" else CARD_BG, end_color="FEF2F2" if d_name=="Sales" else CARD_BG, fill_type="solid")

    c_pay = ws_dash.cell(row=r, column=6, value=f"=AVERAGEIF(Data!E2:E1471, B{r}, Data!R2:R1471)")
    c_pay.number_format = "$#,##0"
    c_pay.alignment = Alignment(horizontal="right")
    c_pay.fill = PatternFill(start_color=CARD_BG, end_color=CARD_BG, fill_type="solid")

    for c_i in range(2, 7):
        ws_dash.cell(row=r, column=c_i).border = table_border

# Department Total Row (Row 16)
ws_dash.cell(row=16, column=2, value="Enterprise Total").font = Font(name="Segoe UI", size=9, bold=True, color=NAVY_HEADER)
ws_dash.cell(row=16, column=3, value="=SUM(C13:C15)").number_format = "#,##0"
ws_dash.cell(row=16, column=4, value="=SUM(D13:D15)").number_format = "#,##0"
ws_dash.cell(row=16, column=5, value="=D16/C16").number_format = "0.0%"
ws_dash.cell(row=16, column=6, value="=AVERAGE(Data!R2:R1471)").number_format = "$#,##0"
for c_i in range(2, 7):
    c = ws_dash.cell(row=16, column=c_i)
    c.font = Font(name="Segoe UI", size=9, bold=True)
    c.fill = PatternFill(start_color="E2E8F0", end_color="E2E8F0", fill_type="solid")
    c.border = Border(top=Side(style='thin', color=NAVY_HEADER), bottom=Side(style='double', color=NAVY_HEADER))

# Table B: Overtime Work Impact (H11:L16) - Strictly Aligned on Rows 12 to 16
ws_dash["H11"] = "OVERTIME WORKLOAD VS FLIGHT RISK"
ws_dash["H11"].font = Font(name="Segoe UI", size=11, bold=True, color=NAVY_HEADER)

ot_headers = ["OverTime Status", "Headcount", "Leavers", "Attrition %", "Avg Monthly Pay"]
for idx, title in enumerate(ot_headers, start=8):
    cell = ws_dash.cell(row=12, column=idx, value=title)
    cell.font = Font(name="Segoe UI", size=9, bold=True, color="FFFFFF")
    cell.fill = PatternFill(start_color=NAVY_CARD, end_color=NAVY_CARD, fill_type="solid")
    cell.alignment = Alignment(horizontal="center" if idx > 8 else "left", vertical="center")

ot_rows = [("No", "Standard Hours (No OT)", 13), ("Yes", "Overtime Required (OT)", 14)]
for ot_val, ot_lbl, r in ot_rows:
    ws_dash.cell(row=r, column=8, value=ot_lbl).font = Font(name="Segoe UI", size=9, bold=True, color=NAVY_CARD)
    ws_dash.cell(row=r, column=8).fill = PatternFill(start_color=CARD_BG, end_color=CARD_BG, fill_type="solid")

    c_hc = ws_dash.cell(row=r, column=9, value=f'=COUNTIF(Data!U2:U1471, "{ot_val}")')
    c_hc.number_format = "#,##0"
    c_hc.alignment = Alignment(horizontal="center")
    c_hc.fill = PatternFill(start_color=CARD_BG, end_color=CARD_BG, fill_type="solid")

    c_lev = ws_dash.cell(row=r, column=10, value=f'=COUNTIFS(Data!U2:U1471, "{ot_val}", Data!B2:B1471, "Yes")')
    c_lev.number_format = "#,##0"
    c_lev.alignment = Alignment(horizontal="center")
    c_lev.fill = PatternFill(start_color=CARD_BG, end_color=CARD_BG, fill_type="solid")

    c_rate = ws_dash.cell(row=r, column=11, value=f"=J{r}/I{r}")
    c_rate.number_format = "0.0%"
    c_rate.font = Font(name="Segoe UI", size=9, bold=True, color=RED_ALERT if ot_val=="Yes" else GREEN_STABLE)
    c_rate.alignment = Alignment(horizontal="center")
    c_rate.fill = PatternFill(start_color="FEF2F2" if ot_val=="Yes" else CARD_BG, end_color="FEF2F2" if ot_val=="Yes" else CARD_BG, fill_type="solid")

    c_pay = ws_dash.cell(row=r, column=12, value=f'=AVERAGEIF(Data!U2:U1471, "{ot_val}", Data!R2:R1471)')
    c_pay.number_format = "$#,##0"
    c_pay.alignment = Alignment(horizontal="right")
    c_pay.fill = PatternFill(start_color=CARD_BG, end_color=CARD_BG, fill_type="solid")

    for c_i in range(8, 13):
        ws_dash.cell(row=r, column=c_i).border = table_border

# Overtime Delta / Multiplier Row (Row 15)
ws_dash.cell(row=15, column=8, value="Overtime Risk Multiplier").font = Font(name="Segoe UI", size=9, bold=True, color=RED_ALERT)
ws_dash.cell(row=15, column=9, value="--").alignment = Alignment(horizontal="center")
ws_dash.cell(row=15, column=10, value="--").alignment = Alignment(horizontal="center")
ws_dash.cell(row=15, column=11, value="=K14/K13").number_format = '0.0"x Risk"'
ws_dash.cell(row=15, column=11).font = Font(name="Segoe UI", size=9, bold=True, color=RED_ALERT)
ws_dash.cell(row=15, column=11).alignment = Alignment(horizontal="center")
ws_dash.cell(row=15, column=12, value="=L14-L13").number_format = '+$#,##0;-$#,##0;"$0"'
ws_dash.cell(row=15, column=12).alignment = Alignment(horizontal="right")
for c_i in range(8, 13):
    c = ws_dash.cell(row=15, column=c_i)
    c.fill = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid")
    c.border = Border(top=Side(style='thin', color=NAVY_HEADER), bottom=Side(style='thin', color=NAVY_HEADER))

# Empty padding row on Row 16 for OT table
for c_i in range(8, 13):
    ws_dash.cell(row=16, column=c_i).fill = PatternFill(start_color=CANVAS_BG, end_color=CANVAS_BG, fill_type="solid")

# 4. Flawless Native Excel Column Charts (Rows 18 to 33)
# Chart 1: Department Attrition Column Chart (B18:F32)
chart1 = BarChart()
chart1.type = "col"
chart1.title = "Attrition Rate by Department (%)"
chart1.y_axis.title = "Attrition %"
chart1.y_axis.number_format = '0%'
chart1.y_axis.scaling.min = 0.0
chart1.y_axis.scaling.max = 0.28   # 28% ceiling so bars are tall and readable
chart1.legend = None              # No redundant legend

data1 = Reference(ws_dash, min_col=5, min_row=12, max_row=15)
cats1 = Reference(ws_dash, min_col=2, min_row=13, max_row=15)
chart1.add_data(data1, titles_from_data=True)
chart1.set_categories(cats1)

chart1.dataLabels = DataLabelList()
chart1.dataLabels.showVal = True   # Clean percentage values directly above bars!

chart1.width = 13.5
chart1.height = 7.5
ws_dash.add_chart(chart1, "B18")

# Chart 2: OverTime Comparison Column Chart (H18:L32)
chart2 = BarChart()
chart2.type = "col"
chart2.title = "Turnover Propensity: Standard vs Overtime"
chart2.y_axis.title = "Attrition %"
chart2.y_axis.number_format = '0%'
chart2.y_axis.scaling.min = 0.0
chart2.y_axis.scaling.max = 0.40   # 40% ceiling
chart2.legend = None

data2 = Reference(ws_dash, min_col=11, min_row=12, max_row=14)
cats2 = Reference(ws_dash, min_col=8, min_row=13, max_row=14)
chart2.add_data(data2, titles_from_data=True)
chart2.set_categories(cats2)

chart2.dataLabels = DataLabelList()
chart2.dataLabels.showVal = True   # Clean percentage labels directly above bars!

chart2.width = 13.5
chart2.height = 7.5
ws_dash.add_chart(chart2, "H18")

# 5. Section 3: Job Role High-Risk Leaderboard (N11:P28)
# Gives the dashboard that complete, rich enterprise feel on the right side!
ws_dash["N11"] = "TOP FLIGHT RISK ROLES"
ws_dash["N11"].font = Font(name="Segoe UI", size=11, bold=True, color=NAVY_HEADER)

role_hdrs = ["Job Title", "Dept", "Attrition %"]
for idx, h_t in enumerate(role_hdrs, start=14):
    c = ws_dash.cell(row=12, column=idx, value=h_t)
    c.font = Font(name="Segoe UI", size=9, bold=True, color="FFFFFF")
    c.fill = PatternFill(start_color=NAVY_CARD, end_color=NAVY_CARD, fill_type="solid")
    c.alignment = Alignment(horizontal="center" if idx == 16 else "left", vertical="center")

top_roles = [
    ("Sales Representative", "Sales", "39.8%", 13),
    ("Laboratory Technician", "R&D", "23.9%", 14),
    ("Human Resources", "HR", "23.1%", 15),
    ("Sales Executive", "Sales", "17.5%", 16),
    ("Research Scientist", "R&D", "16.1%", 17),
    ("Manufacturing Director", "R&D", "6.9%", 18),
    ("Healthcare Rep", "R&D", "6.9%", 19),
    ("Manager", "R&D", "5.6%", 20),
    ("Research Director", "R&D", "2.5%", 21)
]

for r_title, r_dept, r_rate, row_n in top_roles:
    c1 = ws_dash.cell(row=row_n, column=14, value=r_title)
    c1.font = Font(name="Segoe UI", size=9, bold=True if "Sales Rep" in r_title or "Lab" in r_title else False)
    c1.fill = PatternFill(start_color=CARD_BG, end_color=CARD_BG, fill_type="solid")
    c1.border = thin_border

    c2 = ws_dash.cell(row=row_n, column=15, value=r_dept)
    c2.font = Font(name="Segoe UI", size=9, color=GRAY_TEXT)
    c2.fill = PatternFill(start_color=CARD_BG, end_color=CARD_BG, fill_type="solid")
    c2.border = thin_border

    c3 = ws_dash.cell(row=row_n, column=16, value=r_rate)
    c3.font = Font(name="Segoe UI", size=9, bold=True, color=RED_ALERT if float(r_rate.replace("%","")) >= 20 else (GREEN_STABLE if float(r_rate.replace("%","")) < 10 else NAVY_CARD))
    c3.fill = PatternFill(start_color="FEF2F2" if float(r_rate.replace("%","")) >= 20 else CARD_BG, end_color="FEF2F2" if float(r_rate.replace("%","")) >= 20 else CARD_BG, fill_type="solid")
    c3.alignment = Alignment(horizontal="center")
    c3.border = thin_border

# Column Dimensions
col_widths = {
    'A': 3, 'B': 24, 'C': 12, 'D': 12, 'E': 14, 'F': 16,
    'G': 3, 'H': 23, 'I': 12, 'J': 12, 'K': 14, 'L': 16,
    'M': 3, 'N': 22, 'O': 10, 'P': 13
}
for col, w in col_widths.items():
    ws_dash.column_dimensions[col].width = w

# ==============================================================================
# TAB 2: DATA TAB
# ==============================================================================
ws_data = wb.create_sheet("Data")
ws_data.views.sheetView[0].showGridLines = True
ws_data.sheet_properties.tabColor = "475569"

cols = list(df.columns)
for c_idx, c_name in enumerate(cols, start=1):
    c = ws_data.cell(row=1, column=c_idx, value=c_name)
    c.font = Font(name="Segoe UI", size=10, bold=True, color="FFFFFF")
    c.fill = PatternFill(start_color=NAVY_HEADER, end_color=NAVY_HEADER, fill_type="solid")
    c.alignment = Alignment(horizontal="center", vertical="center")

for r_idx, row in enumerate(df.itertuples(index=False), start=2):
    for c_idx, val in enumerate(row, start=1):
        c = ws_data.cell(row=r_idx, column=c_idx, value=val)
        c.font = Font(name="Segoe UI", size=9)
        if r_idx % 2 == 0:
            c.fill = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")
        col_name = cols[c_idx - 1]
        if "Income" in col_name or "Rate" in col_name:
            c.number_format = "$#,##0"
        elif col_name == "Attrition":
            if val == "Yes":
                c.fill = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid")
                c.font = Font(name="Segoe UI", size=9, bold=True, color=RED_ALERT)

ws_data.freeze_panes = "A2"
ws_data.auto_filter.ref = f"A1:{get_column_letter(len(cols))}{len(df)+1}"
for c_idx, c_name in enumerate(cols, start=1):
    ws_data.column_dimensions[get_column_letter(c_idx)].width = max(len(c_name) + 3, 12)

wb.save(out_xlsx)
print(f"Master Executive Dashboard successfully generated: {out_xlsx}")
