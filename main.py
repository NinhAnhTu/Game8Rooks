import tkinter as tk    
from gui import RookGUI

def main():
    root = tk.Tk()
    app = RookGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()