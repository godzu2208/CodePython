import tkinter as tk
from tkinter import scrolledtext
import subprocess

OLLAMA_PATH = r"C:\Users\Linh IT\AppData\Local\Programs\Ollama"
MODEL_NAME = "deepseek-r1:14b"

# Khởi động Ollama và Model AI tự động
def start_ollama():
    global ollama_process
    ollama_process = subprocess.Popen(
        ["cmd.exe", "/k", f"cd /d {OLLAMA_PATH} && ollama run {MODEL_NAME}"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

def send_message():
    user_input = entry.get()
    if not user_input.strip():
        return

    chat_history.insert(tk.END, f"Bạn: {user_input}\n")
    entry.delete(0, tk.END)

    try:
        # Gửi dữ liệu vào model AI
        ollama_process.stdin.write(user_input + "\n")
        ollama_process.stdin.flush()

        # Đọc phản hồi từ model AI
        ai_response = ollama_process.stdout.readline().strip()

        chat_history.insert(tk.END, f"AI: {ai_response}\n")
    except Exception as e:
        chat_history.insert(tk.END, f"Lỗi: {str(e)}\n")

# Tạo giao diện chatbox
root = tk.Tk()
root.title("Chatbox AI")

chat_history = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=20)
chat_history.pack(padx=10, pady=10)

entry = tk.Entry(root, width=40)
entry.pack(padx=10, pady=5, side=tk.LEFT)

send_button = tk.Button(root, text="Gửi", command=send_message)
send_button.pack(pady=5, side=tk.RIGHT)

# Khởi động Ollama và Model AI khi chạy chương trình
start_ollama()

root.mainloop()
