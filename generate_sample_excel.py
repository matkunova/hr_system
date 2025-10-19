from openpyxl import Workbook

wb = Workbook()
ws = wb.active
ws.title = "Workers"

headers = ["first_name", "last_name", "email", "position"]
ws.append(headers)

sample_data = [
    ["Анна", "Сидорова", "anna@example.com", "HR-менеджер"],
    ["Борис", "Кузнецов", "boris@test.org", "Аналитик"],
    ["Вера", "Иванова", "vera@company.com", "Дизайнер"]
]

for row in sample_data:
    ws.append(row)

filename = "sample_import.xlsx"
wb.save(filename)
print(f"Файл '{filename}' успешно создан!")
