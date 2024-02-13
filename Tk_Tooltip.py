import tkinter as tk
class ToolTip:
    def __init__(self, widget, text, delay=800):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.id = None
        self.delay = delay
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hide_tooltip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.delay, self.show_tooltip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def show_tooltip(self):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        label = tk.Label(self.tooltip, text=self.text, background="#ffffe0", relief="groove", borderwidth=1)
        label.pack(ipadx=1)

    def hide_tooltip(self):
        tooltip = self.tooltip
        self.tooltip = None
        if tooltip:
            tooltip.destroy()