import tkinter as tk
from tkinter import Frame, Text, Scrollbar
import sys
import time
import threading

class RedirectText:
    def __init__(self, widget):
        self.widget = widget

    def write(self, text):
        self.widget.insert(tk.END, text)
        self.widget.see(tk.END)

    def flush(self):
        pass

def center_window(root, width_ratio=3/4, height_ratio=1):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    width = int(screen_width * width_ratio)
    height = screen_height

    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    root.geometry(f"{width}x{height}+{x}+{y}")

def create_window():
    root = tk.Tk()
    root.title("成语接龙游戏")

    # 设置窗口大小和位置
    center_window(root)

    # 创建上下等分的框架
    top_frame = Frame(root, bg='white')
    bottom_frame = Frame(root, bg='white')

    top_frame.pack(side='top', fill='both', expand=True)
    bottom_frame.pack(side='bottom', fill='both', expand=True)

    # 在下侧框架中添加Text和Scrollbar小部件
    text_area = Text(bottom_frame, wrap='word')
    text_area.pack(side='left', fill='both', expand=True)

    scrollbar = Scrollbar(bottom_frame, command=text_area.yview)
    scrollbar.pack(side='right', fill='y')

    text_area.config(yscrollcommand=scrollbar.set)

    # 重定向stdout到Text小部件
    sys.stdout = RedirectText(text_area)

    # 创建并启动一个线程，用于测试输出
    def test_output():
        for i in range(100):
            print(f"这是第 {i + 1} 秒")
            time.sleep(0.5)

    threading.Thread(target=test_output).start()

    # 运行主循环
    root.mainloop()

if __name__ == "__main__":
    create_window()
