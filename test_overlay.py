import tkinter as tk

def main():
    root = tk.Tk()
    root.overrideredirect(True)                     # No borders
    root.attributes("-topmost", True)               # Always on top
    root.geometry("300x100+50+50")                  # Width x Height + X + Y
    root.configure(bg="white")                      # Background

    # OPTIONAL — comment this out if invisible
    # root.attributes("-transparentcolor", "white")

    label = tk.Label(root, text="🟠 ORANGE\nScore: 10", font=("Arial", 24, "bold"), fg="black", bg="white")
    label.pack()

    print("✅ Tkinter window is running")
    root.mainloop()

if __name__ == "__main__":
    main()
