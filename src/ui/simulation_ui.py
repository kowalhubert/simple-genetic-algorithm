import json
from math import isnan, nan
import tkinter as tk
from tkinter import ttk
from src.config.cost_function_config import CostFunctionConfig
from src.config.general_config import GeneralConfig
from src.config.selection_config import SelectionConfig
from src.config.simulation_config import SimulationConfiguration
from src.core.cost_function import CostFunction
from src.core.selection import SelectionMethodType

class SimulationUI:
    def __init__(self, master):
        self.master = master
        self.master.title('Simulation Configuration')
        self.master.geometry('1200x580')
        self.master.resizable(False, False)

        frame = ttk.Frame(master, padding="15")
        frame.pack(expand=True, fill=tk.BOTH)

        
        # general config
        ### epochs number
        ttk.Label(frame, text="Epochs Number:").grid(row=0, column=0, sticky=tk.W, pady=8)
        self.epochs_var = tk.IntVar(value=10)
        ttk.Entry(frame, textvariable=self.epochs_var).grid(row=0, column=1, pady=8, sticky=(tk.W, tk.E))

        ### population size
        ttk.Label(frame, text="Population Size:").grid(row=0, column=2, sticky=tk.W, pady=8)
        self.population_var = tk.IntVar(value=10)
        ttk.Entry(frame, textvariable=self.population_var).grid(row=0, column=3, pady=8, sticky=(tk.W, tk.E))

        ### chromosome representation
        ttk.Label(frame, text="Chromosome Precision:").grid(row=1, column=0, sticky=tk.W, pady=8)
        self.chromosome_repr_precision_var = tk.IntVar(value=6)
        ttk.Entry(frame, textvariable=self.chromosome_repr_precision_var).grid(row=1, column=1, pady=8, sticky=(tk.W, tk.E))

        # cost function config
        ### cost function type
        ttk.Label(frame, text="Cost Function:").grid(row=2, column=0, sticky=tk.W, pady=8)
        self.cost_function_var = tk.StringVar()
        self.cost_function_map = {cf.name: cf for cf in CostFunction}
        self.cost_function_combo = ttk.Combobox(
            frame, textvariable=self.cost_function_var, state="readonly",
            values=[cf.name for cf in CostFunction]
        )
        self.cost_function_combo.current(0)
        self.cost_function_combo.grid(row=2, column=1, pady=8, sticky=(tk.W, tk.E))

        ### cost function dimensions
        ttk.Label(frame, text="Dimensions:").grid(row=2, column=2, sticky=tk.W, pady=8)
        self.dimensions_var = tk.IntVar(value=2)
        ttk.Entry(frame, textvariable=self.dimensions_var).grid(row=2, column=3, pady=8, sticky=(tk.W, tk.E))

        # selection config
        ### selection config type


        ### selection config properties
        ttk.Label(frame, text="Selection type:").grid(row=3, column=0, sticky=tk.W, pady=8)
        self.selection_function_var = tk.StringVar()
        self.selection_function_map = {cf.value: cf for cf in SelectionMethodType}
        self.selection_function_combo = ttk.Combobox(
            frame, textvariable=self.selection_function_var, state="readonly",
            values=[cf.value for cf in SelectionMethodType]
        )
        self.selection_function_combo.current(0)
        self.selection_function_combo.grid(row=3, column=1, pady=8, sticky=(tk.W, tk.E))

        ### selection percentage
        ttk.Label(frame, text="Selection percentage (%):").grid(row=3, column=2, sticky=tk.W, pady=8)
        self.selection_percentage_var = tk.IntVar(value=20)
        ttk.Entry(frame, textvariable=self.selection_percentage_var).grid(row=3, column=3, pady=8, sticky=(tk.W, tk.E))

        def on_selection_function_change(event):
            selected_type = self.selection_function_var.get()
            # You can further adjust UI/logic here when user changes the selection type
            # For example, show/hide tournament size entry if "Tournament" is selected

            # Remove old tournament size entry if exists
            if hasattr(self, 'tournament_size_label'):
                self.tournament_size_label.grid_remove()
                self.tournament_size_entry.grid_remove()
            
            if selected_type == SelectionMethodType.TOURNAMENT.value:
                # Show tournament size input
                self.tournament_size_var = tk.IntVar(value=3)
                self.tournament_size_label = ttk.Label(frame, text="Tournament Size:")
                self.tournament_size_label.grid(row=3, column=4, sticky=tk.W, pady=8)
                self.tournament_size_entry = ttk.Entry(frame, textvariable=self.tournament_size_var)
                self.tournament_size_entry.grid(row=3, column=5, pady=8, sticky=(tk.W, tk.E))

        self.selection_function_combo.bind("<<ComboboxSelected>>", on_selection_function_change)

        # Optionally, call it once initially to setup initial state
        on_selection_function_change(None)

        # Add Start button
        self._add_start_button()

    def _add_start_button(self):
        frame = self.master.children['!frame']
        start_button = ttk.Button(frame, text="Start", command=self._start_simulation)
        start_button.grid(row=5, column=0, columnspan=2, pady=15)

    def _get_config(self) -> SimulationConfiguration:
        try:
            # general config
            general_config = GeneralConfig(self.population_var.get(), self.epochs_var.get(), self.chromosome_repr_precision_var.get() )
            
            # cost function config
            cost_function_config = CostFunctionConfig(self.dimensions_var.get(), self.cost_function_map[self.cost_function_var.get()])

            # selection function config
            tournament_size = None
            if hasattr(self, 'tournament_size_label'):
                self.tournament_size_label.grid_remove()
                self.tournament_size_entry.grid_remove()
                tournament_size = self.tournament_size_var.get()

            selection_config = SelectionConfig(self.selection_function_map[self.selection_function_var.get()], self.selection_percentage_var.get(), tournament_size)
            
            # e) Implementacja krzyżowania jednopunktowego, dwupunktowego, krzyżowania
            # jednorodnego, krzyżowania ziarnistego + konfiguracja prawdopodobieństwa
            # krzyżowania.
            crossing_config = None
            
            # f) Implementacji mutacji brzegowej, jedno oraz dwupunktowej + konfiguracja
            # prawdopodobieństwa mutacji
            mutation_config = None

            # g) Implementacja operatora inwersji + konfiguracja prawdopodobieństwa jego
            # wystąpienia
            inversion_config = None

            # h) Implementacjastrategiielitarnej+konfiguracja%lubliczbyosobnikówprzechodzącej
            # do kolejnej populacji
            elite_strategy_config = None
        

            return SimulationConfiguration(
                cost_function_config,
                crossing_config,
                elite_strategy_config,
                general_config,
                inversion_config,
                mutation_config,
                selection_config
            )
        except AssertionError:
            self._display_vaidation_error()
            return

    def _display_vaidation_error(self):
        error_window = tk.Toplevel(self.master)
        error_window.title("Configuration Error")
        error_window.grab_set()
        error_label = ttk.Label(error_window, text="Invalid configuration! Please check your simulation parameters.", padding=10)
        error_label.pack(padx=20, pady=10)
        close_button = ttk.Button(error_window, text="Close", command=error_window.destroy)
        close_button.pack(pady=(0, 10))

    def _start_simulation(self):
        config = self._get_config()

        if config is None:
            return

