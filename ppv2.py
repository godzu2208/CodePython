import pandas as pd

file_path = 'D:\Laptop\Công việc\papercut\weekly\print_logs.xlsx'  # Đặt đường dẫn đến file Excel của bạn ở đây
df = pd.read_excel(file_path)

# Lọc những lần in file grayscale
grayscale_prints = df[df['Grayscale'] == 'Y']

# Lọc các cột cần thiết
filtered_columns = ['Username', 'Printer Name', 'Total Printed Pages', 'Duplex Pages', 'Simplex Pages', 'Total Color Pages', 'Document']
grayscale_filtered = grayscale_prints[filtered_columns]

# Lưu kết quả vào file Excel mới
output_file = 'D:\Laptop\Công việc\papercut\weekly\summary1.xlsx'
grayscale_filtered.to_excel(output_file, index=False)

print("Dữ liệu in file grayscale đã được lọc và lưu vào", output_file)
