import os
import sys
import traceback
import threading
import tkinter as tk
from tkinter.filedialog import askopenfiles

from decrypt import decrypt_file, CustomException
from ctypes import windll

class StdoutRedirector(object):
    def __init__(self, text_widget):
        self.text_space = text_widget

    def write(self, string):
        self.text_space.insert('end', string)
        self.text_space.see('end')

    def flush(self):
        pass

def open_file():
    files = askopenfiles(filetypes=[
        ("PDF/CAJ", "*.pdf *.caj")])
    if not files:
        return

    threading.Thread(target=lambda: decrypt_files_background(files)).start()

def decrypt_files_background(files):
    for i in files:
        outpath = os.path.dirname(i.name) + "/output/"
        filename = os.path.basename(i.name)
        if not os.path.exists(outpath):
            os.mkdir(outpath)
        print("开始解密", filename)
        decrypt_background(i.name, outpath + filename)

def decrypt_background(src, dst):
    try:
        decrypt_file(src, dst)
        print("解密成功！解密后的文件为：", dst)
    except Exception as exc:
        if not isinstance(exc, CustomException):
            print("[Error] 解密失败，未知错误: ", str(exc))
        else:
            print("[Error] 解密失败，", str(exc))
        print("\n如果你需要帮助，请复制以下信息到GitHub ( https://github.com/301Moved/ScienceDecrypting/issues/new ) 上提交Issue")
        print("-" * 64)
        traceback.print_exc()


if __name__ == "__main__":
    windll.shcore.SetProcessDpiAwareness(1)
    root = tk.Tk()
    root.title("ScienceDecrypting")
    root.geometry("800x600")
    btn = tk.Button(root, text='选择要解密的文件', command=lambda: open_file())
    btn.pack(side=tk.TOP, pady=20)
    sb = tk.Scrollbar(root)
    LOG = tk.Text(root, yscrollcommand=sb.set)
    sb.config(command=LOG.yview)
    sb.pack(side=tk.RIGHT, fill='y')
    LOG.pack(side=tk.LEFT)

    sys.stdout = StdoutRedirector(LOG)
    sys.stderr = StdoutRedirector(LOG)
    tk.mainloop()
