from ui import ExpenseAnalyzerApp
import ttkbootstrap as ttk

if __name__ == "__main__":
    root = ttk.Window(themename="cosmo")
    app = ExpenseAnalyzerApp(root)
    root.mainloop()