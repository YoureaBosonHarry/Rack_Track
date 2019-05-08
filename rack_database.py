import json
import os
import xlrd

path = os.path.join(os.getcwd(), "Rack_Storage.xlsx")

wb = xlrd.open_workbook(path)
ws = wb.sheet_by_index(2)
rows = ws.nrows
cols = ws.ncols

row1 = {f"{i}1{j}": {} for i in list(["A", "B", "C", "D", "E", "F"]) for j in range(1,3)}
row2 = {f"{i}2{j}": {} for i in list(["A", "B", "C", "D", "E", "F"]) for j in range(1,7)}
row3 = {f"{i}3{j}": {} for i in list(["A", "B", "C", "D", "E", "F"]) for j in range(1,3)}
row4 = {f"{i}4{j}": {} for i in list(["A", "B", "C", "D", "E", "F"]) for j in range(1,2)}
row5 = {f"{i}5{j}": {} for i in list(["A", "B", "C", "D", "E", "F"]) for j in range(1,5)}
row6 = {f"{i}6{j}": {} for i in list(["A", "B", "C", "D", "E", "F"]) for j in range(1,7)}
row7 = {f"{i}7{j}": {} for i in list(["A", "B", "C", "D", "E", "F"]) for j in range(1,9)}
data = dict(row1, **row2, **row3, **row4, **row5, **row6, **row7)

filled_shelves = [[ws.cell(i, 1).value.split(" "), i] for i in range(2, rows) if ws.cell(i, 2).value != ""]
no_row = [ws.cell(i, 1).value.split(" ") for i in range(2, rows) if ws.cell(i, 2).value != ""]
strings = sorted(set([" ". join(i) for i in no_row]))
sorted_str = [i.split(" ") for i in strings]
current_count = {i: 1 for i in strings}

for i in filled_shelves:
    if i[0][0] in data:
        data[i[0][0]][f"box_{i[0][1]}"] = {}

for i in filled_shelves:
    if i[0][0] in data:
        key = " ".join(i[0])
        for j in range(2, cols):
            try:
                data[i[0][0]][f"box_{i[0][1]}"][f"Item_Group_{current_count[key]}"].append(ws.cell(i[1], j).value)
            except KeyError:
                data[i[0][0]][f"box_{i[0][1]}"][f"Item_Group_{current_count[key]}"] = [ws.cell(i[1], j).value]
        current_count[key] += 1
with open(os.path.join(os.getcwd(), "racks.json"), 'w+') as f:
    json.dump(data, f, indent=4)
