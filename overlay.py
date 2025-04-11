import tkinter as tk
from config import OVERLAY_POSITION, OVERLAY_SIZE

class Overlay:
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-disabled", True)  # 🛡 Prevent stealing focus
        # self.root.attributes("-transparentcolor", "white")  # Optional for transparency
        self.root.configure(bg="white")

        width, height = OVERLAY_SIZE
        x, y = OVERLAY_POSITION
        self.root.geometry(f"{width}x{height}+{x}+{y}")

        self.label = tk.Label(
            self.root,
            text="",
            font=("Arial", 24, "bold"),
            fg="black",
            bg="white"
        )
        self.label.pack()

        self.text = ""
        self.running = True

    def update_text(self, color_text, score):
        self.text = f"{color_text}\nScore: {score}"
        self.label.config(text=self.text)

    def start(self):
        self.root.after(100, self._update_loop)
        self.root.mainloop()

    def _update_loop(self):
        if self.running:
            self.label.config(text=self.text)
            self.root.after(100, self._update_loop)

    def close(self):
        self.running = False
        self.root.destroy()
