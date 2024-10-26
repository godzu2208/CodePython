import pandas as pd

# Đọc file Excel
file_path = 'D:\Laptop\Công việc\papercut\weekly\print_logs.xlsx'  # Đặt đường dẫn đến file Excel của bạn ở đây
df = pd.read_excel(file_path)

# Chuyển đổi "Y" thành 1 và "N" thành 0 trong cột Grayscale
df['Grayscale'] = df['Grayscale'].apply(lambda x: 1 if x == 'Y' else 0)

# Nhân số trang in với cột Grayscale để tính tổng số trang grayscale
df['Total_grayscale_pages'] = df['Total Printed Pages'] * df['Grayscale']

# Tổng hợp số liệu theo Username và Printer Name
summary = df.groupby(['Username', 'Printer Name']).agg(
    Total_Page=pd.NamedAgg(column='Total Printed Pages', aggfunc='sum'),
    Total_simplex=pd.NamedAgg(column='Simplex Pages', aggfunc='sum'),
    Total_duplex=pd.NamedAgg(column='Duplex Pages', aggfunc='sum'),
    Total_grayscale=pd.NamedAgg(column='Total_grayscale_pages', aggfunc='sum'),
    Total_Color=pd.NamedAgg(column='Total Color Pages', aggfunc='sum'),
    Documents=pd.NamedAgg(column='Document', aggfunc='count')
).reset_index()

# Lưu kết quả vào file Excel mới
output_file = 'D:\Laptop\Công việc\papercut\weekly\summary2.xlsx'
summary.to_excel(output_file, index=False)

print("Tổng hợp số liệu in đã được lưu vào", output_file)
