import tkinter as tk
from src.ui.simulation_ui import SimulationUI

if __name__ == "__main__":
    root = tk.Tk()
    app_ui = SimulationUI(root)
    root.mainloop()
