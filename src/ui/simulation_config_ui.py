import tkinter as tk
from tkinter import ttk
from src.core.cost_function import CostFunction

class SimulationConfigUI:
    def __init__(self, master):
        self.master = master
        self.master.title('Simulation Configuration')
        self.master.geometry('350x280')
        self.master.resizable(False, False)

        frame = ttk.Frame(master, padding="15")
        frame.pack(expand=True, fill=tk.BOTH)

        # CostFunction select
        ttk.Label(frame, text="Cost Function:").grid(row=0, column=0, sticky=tk.W, pady=8)
        self.cost_function_var = tk.StringVar()
        self.cost_function_combo = ttk.Combobox(
            frame, textvariable=self.cost_function_var, state="readonly",
            values=[cf.name for cf in CostFunction]
        )
        self.cost_function_combo.current(0)
        self.cost_function_combo.grid(row=0, column=1, pady=8, sticky=(tk.W, tk.E))

        # Dimensions
        ttk.Label(frame, text="Dimensions:").grid(row=1, column=0, sticky=tk.W, pady=8)
        self.dimensions_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.dimensions_var).grid(row=1, column=1, pady=8, sticky=(tk.W, tk.E))

        # Population size input
        ttk.Label(frame, text="Population Size:").grid(row=2, column=0, sticky=tk.W, pady=8)
        self.population_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.population_var).grid(row=2, column=1, pady=8, sticky=(tk.W, tk.E))

        # Epochs number input
        ttk.Label(frame, text="Epochs Number:").grid(row=3, column=0, sticky=tk.W, pady=8)
        self.epochs_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.epochs_var).grid(row=3, column=1, pady=8, sticky=(tk.W, tk.E))

        # Add Start button
        self._add_start_button()

    def _add_start_button(self):
        frame = self.master.children['!frame']
        start_button = ttk.Button(frame, text="Start", command=self.print_config)
        start_button.grid(row=4, column=0, columnspan=2, pady=15)

    def get_config(self):
        selected_cost_function = self.cost_function_var.get()
        population_size = self.population_var.get()
        epochs_no = self.epochs_var.get()
        dimensions = self.dimensions_var.get()
        return selected_cost_function, dimensions, population_size, epochs_no

    def print_config(self):
        selected_cost_function, dimensions, population_size, epochs_no = self.get_config()
        print("Cost Function: ", selected_cost_function)
        print("Dimensions: ", dimensions)
        print("Population Size: ", population_size)
        print("Epochs Number: ", epochs_no)
