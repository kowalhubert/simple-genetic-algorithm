import tkinter as tk
from src.ui.simulation_config_ui import SimulationConfigUI

if __name__ == "__main__":
    root = tk.Tk()
    app_ui = SimulationConfigUI(root)
    root.mainloop()
