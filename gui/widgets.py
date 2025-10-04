import tkinter as tk
from tkinter import filedialog, scrolledtext

class LabeledText(tk.Frame):
    def __init__(self, master, label, **kw):
        super().__init__(master, **kw)
        tk.Label(self, text=label).pack(anchor="w")
        self.text = tk.Text(self, height=4, width=60)
        self.text.pack(fill="x", expand=True)

    def get(self):
        return self.text.get("1.0", "end").strip()

class FilePicker(tk.Frame):
    def __init__(self, master, label, filetypes, **kw):
        super().__init__(master, **kw)
        tk.Label(self, text=label).pack(anchor="w")
        
        row = tk.Frame(self)
        row.pack(fill="x", expand=True)
        
        self.var = tk.StringVar()
        tk.Entry(row, textvariable=self.var).pack(side="left", expand=True, fill="x")
        tk.Button(row, text="Browse", command=self.pick).pack(side="left")
        
        self.filetypes = filetypes

    def pick(self):
        path = filedialog.askopenfilename(filetypes=self.filetypes)
        if path:
            self.var.set(path)

    def get(self):
        return self.var.get()

class OutputBox(scrolledtext.ScrolledText):
    def __init__(self, master, **kw):
        super().__init__(master, height=12, width=70, state="disabled", **kw)

    def write(self, text: str):
        self.config(state="normal")
        self.insert("end", text + "\n")
        self.config(state="disabled")
        self.see("end")
