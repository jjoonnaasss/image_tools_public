import tkinter as tk

from src.values import dimensions_help as dh
from src.values import scrollbar_width as sb_width

color_title = "#BFC9CA"
color_text = "#EAEDED"


class ScrollableFrame(tk.Frame):
    def __init__(self, container, width, height, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        print(width, height)

        self.canvas = tk.Canvas(self, width=width-sb_width-5, height=height-5)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview, width=sb_width)
        self.content_frame = tk.Frame(self.canvas)

        self.content_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.canvas.create_window((0, 0), window=self.content_frame, anchor="nw")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.content_frame.bind('<Enter>', self._bind_to_mousewheel)
        self.content_frame.bind('<Leave>', self._unbind_from_mousewheel)

    def _bind_to_mousewheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_from_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


class Collapsible(tk.Frame):
    def __init__(self, parent, title, text):
        tk.Frame.__init__(self, parent)
        self.configure(width=dh[0])
        self.grid_columnconfigure(0, minsize=dh[0])

        self.var = tk.IntVar()
        self.var.set(0)

        self.collapse_button = tk.Checkbutton(self, text=title, command=self.collapse_toggle,
                                              variable=self.var, bg=color_title, relief=tk.RIDGE)
        self.collapse_button.grid(row=0, column=0, padx=5, pady=5, sticky="W")

        self.text_frame = tk.Frame(self, borderwidth=1)
        self.text = tk.Message(self.text_frame, text=text, width=dh[0]-45, bg=color_text, relief=tk.RIDGE)
        self.text.grid(row=0, column=0)

    def collapse_toggle(self):
        if self.var.get():
            self.text_frame.grid(row=1, column=0)
        else:
            self.text_frame.grid_forget()


class RadioGroup(tk.Frame):
    def __init__(self, parent, rows, cols, color, start_val=0):
        tk.Frame.__init__(self, parent)

        self.var = tk.IntVar()
        self.var.set(start_val)

        for r in range(rows):
            for c in range(cols):
                val = r * rows + c
                tk.Radiobutton(self, variable=self.var, value=val, bg=color).grid(row=r, column=c)

    def get_value(self):
        return self.var.get()
