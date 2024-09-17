import tkinter as tk
import sys


def on_button_click_1():
    """按钮1被点击时调用的函数"""
    print("game.go")
    import game

def on_button_click_2():
    """按钮2被点击时调用的函数"""
    sys.exit()

# 创建主窗口
root = tk.Tk()
root.geometry("400x300")
root.title("Flight simulation")
#image_label = tk.Label(root, image=)
#image_label.pack()

# 创建第一个按钮
button1 = tk.Button(root, text="go", command=on_button_click_1)
button1.pack(pady=10)  # pady用于设置按钮之间的垂直间距

# 创建第二个按钮
button2 = tk.Button(root, text="quit", command=on_button_click_2)
button2.pack(pady=10)  # 也可以使用padx设置水平间距

# 进入主事件循环
root.mainloop()
