from math import isnan, nan
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from src.config.cost_function_config import CostFunctionConfig
from src.config.crossing_config import CrossingConfig
from src.config.general_config import GeneralConfig
from src.config.inversion_config import InversionConfig
from src.config.mutation_config import MutationConfig
from src.config.selection_config import SelectionConfig
from src.config.simulation_config import SimulationConfiguration
from src.core.cost_function import CostFunction
from src.core.crossing import CrossingMethodType
from src.core.mutation import MutationMethodType
from src.core.selection import SelectionMethodType
from src.core.simulation import Simulation
from src.core.unit import UnitFactory

class SimulationUI:
    __EPOCHS_NUMBER_DEFAULT = 10
    __POPULATION_SIZE_DEFAULT = 10
    __CHROMOSOME_PRECISION_DEFAULT = 6
    
    __COST_FUNCTION_TYPE_DEFAULT = CostFunction.RASTRIGIN.name
    __COST_FUNCTION_DIMENSIONS_DEFAULT = 2
    
    __SELECTION_TYPE_DEFAULT = SelectionMethodType.BEST.value
    __SELECTION_PERCENTAGE_DEFAULT = 50
    
    __CROSSING_FUNC_TYPE_DEFAULT = CrossingMethodType.SINGLE_POINT.value
    __CROSSING_PERCENTAGE_DEFAULT = 80
    __CROSSING_GRAIN_SIZE_DEFAULT = 3
    
    __MUTATION_TYPE_DEFAULT = MutationMethodType.SINGLE_POINT.value
    __MUTATION_PROBABILITY_DEFAULT = 30

    __INVERSION_PROBABILITY = 30

    __ELITE_STRATEGY_UNIT_COUNT = 1

    def __init__(self, master):
        self.master = master
        self.master.title('Simulation Configuration')
        self.master.geometry('1200x580')
        self.master.resizable(False, False)

        self._setup_ui()

    def _setup_ui(self):
        frame = ttk.Frame(self.master, padding="15")
        frame.pack(expand=True, fill=tk.BOTH)
        
        # general config
        self._setup_general_config(frame)

        # cost function config
        self._setup_cost_func_config(frame)

        # selection config
        self._setup_selection_config(frame)
    
        # crossing config
        self._setup_crossing_config(frame)

        # mutation config
        self._setup_mutation_config(frame)

        # inversion config
        self._setup_inversion_config(frame)

        # elite strategy config
        self._setup_elite_strategy_config(frame)

        # Add Start button
        self._add_start_button(frame)

    def _setup_general_config(self, frame):
        # general config
        ### epochs number
        ttk.Label(frame, text="Epochs Number:").grid(row=0, column=0, sticky=tk.W, pady=8)
        self.epochs_var = tk.IntVar(value=self.__EPOCHS_NUMBER_DEFAULT)
        ttk.Entry(frame, textvariable=self.epochs_var).grid(row=0, column=1, pady=8, sticky=(tk.W, tk.E))

        ### population size
        ttk.Label(frame, text="Population Size:").grid(row=0, column=2, sticky=tk.W, pady=8)
        self.population_var = tk.IntVar(value=self.__POPULATION_SIZE_DEFAULT)
        ttk.Entry(frame, textvariable=self.population_var).grid(row=0, column=3, pady=8, sticky=(tk.W, tk.E))

        ### chromosome representation
        ttk.Label(frame, text="Chromosome Precision:").grid(row=1, column=0, sticky=tk.W, pady=8)
        self.chromosome_repr_precision_var = tk.IntVar(value=self.__CHROMOSOME_PRECISION_DEFAULT)
        ttk.Entry(frame, textvariable=self.chromosome_repr_precision_var).grid(row=1, column=1, pady=8, sticky=(tk.W, tk.E))

    def _setup_cost_func_config(self, frame):
        ### cost function type
        ttk.Label(frame, text="Cost Function:").grid(row=2, column=0, sticky=tk.W, pady=8)
        self.cost_function_var = tk.StringVar(value=self.__COST_FUNCTION_TYPE_DEFAULT)
        self.cost_function_map = {cf.name: cf for cf in CostFunction}
        self.cost_function_combo = ttk.Combobox(
            frame, textvariable=self.cost_function_var, state="readonly",
            values=[cf.name for cf in CostFunction]
        )
        self.cost_function_combo.current(0)
        self.cost_function_combo.grid(row=2, column=1, pady=8, sticky=(tk.W, tk.E))

        ### cost function dimensions
        ttk.Label(frame, text="Dimensions:").grid(row=2, column=2, sticky=tk.W, pady=8)
        self.dimensions_var = tk.IntVar(value=self.__COST_FUNCTION_DIMENSIONS_DEFAULT)
        ttk.Entry(frame, textvariable=self.dimensions_var).grid(row=2, column=3, pady=8, sticky=(tk.W, tk.E))

    def _setup_selection_config(self, frame):
        ### selection config type
        ttk.Label(frame, text="Selection type:").grid(row=3, column=0, sticky=tk.W, pady=8)
        self.selection_function_var = tk.StringVar(value=self.__SELECTION_TYPE_DEFAULT)
        self.selection_function_map = {cf.value: cf for cf in SelectionMethodType}
        self.selection_function_combo = ttk.Combobox(
            frame, textvariable=self.selection_function_var, state="readonly",
            values=[cf.value for cf in SelectionMethodType]
        )
        self.selection_function_combo.grid(row=3, column=1, pady=8, sticky=(tk.W, tk.E))

        ### selection percentage
        ttk.Label(frame, text="Selection percentage (%):").grid(row=3, column=2, sticky=tk.W, pady=8)
        self.selection_percentage_var = tk.IntVar(value=self.__SELECTION_PERCENTAGE_DEFAULT)
        ttk.Entry(frame, textvariable=self.selection_percentage_var).grid(row=3, column=3, pady=8, sticky=(tk.W, tk.E))

        def on_selection_function_change(event):
            selected_type = self.selection_function_var.get()
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
        on_selection_function_change(None)

    def _setup_crossing_config(self, frame):
        ### crossing function type
        ttk.Label(frame, text="Crossing type:").grid(row=4, column=0, sticky=tk.W, pady=8)
        self.crossing_function_var = tk.StringVar(value=self.__CROSSING_FUNC_TYPE_DEFAULT)
        self.crossing_function_map = {cf.value: cf for cf in CrossingMethodType}
        self.crossing_function_combo = ttk.Combobox(
            frame, textvariable=self.crossing_function_var, state="readonly",
            values=[cf.value for cf in CrossingMethodType]
        )
        self.crossing_function_combo.grid(row=4, column=1, pady=8, sticky=(tk.W, tk.E))

        ### crossing percentage
        ttk.Label(frame, text="Crossing percentage (%):").grid(row=4, column=2, sticky=tk.W, pady=8)
        self.crossing_percentage_var = tk.IntVar(value=self.__CROSSING_PERCENTAGE_DEFAULT)
        ttk.Entry(frame, textvariable=self.crossing_percentage_var).grid(row=4, column=3, pady=8, sticky=(tk.W, tk.E))

        def on_crossing_function_change(event):
            selected_type = self.crossing_function_var.get()

            if hasattr(self, 'crossing_grain_label'):
                self.crossing_grain_label.destroy()
                self.crossing_grain_entry.destroy()

            if selected_type == CrossingMethodType.GRAIN.value:
                self.crossing_grain_var = tk.IntVar(value=self.__CROSSING_GRAIN_SIZE_DEFAULT)
                self.crossing_grain_label = ttk.Label(frame, text="Grain:")
                self.crossing_grain_label.grid(row=4, column=2, sticky=tk.W, pady=8)
                self.crossing_grain_entry = ttk.Entry(frame, textvariable=self.crossing_grain_var)
                self.crossing_grain_entry.grid(row=4, column=3, pady=8, sticky=(tk.W, tk.E))

        self.crossing_function_combo.bind("<<ComboboxSelected>>", on_crossing_function_change)

        on_crossing_function_change(None)

    def _setup_mutation_config(self, frame):
        # Mutation type selection
        ttk.Label(frame, text="Mutation type:").grid(row=5, column=0, sticky=tk.W, pady=8)
        self.mutation_function_var = tk.StringVar(value=self.__MUTATION_TYPE_DEFAULT)
        self.mutation_function_map = {m.value: m for m in MutationMethodType}
        self.mutation_function_combo = ttk.Combobox(
            frame, 
            textvariable=self.mutation_function_var, 
            state="readonly",
            values=[m.value for m in MutationMethodType]
        )
        self.mutation_function_combo.grid(row=5, column=1, pady=8, sticky=(tk.W, tk.E))

        # Mutation probability
        ttk.Label(frame, text="Mutation probability [%]:").grid(row=5, column=2, sticky=tk.W, pady=8)
        self.mutation_probability_var = tk.IntVar(value=self.__MUTATION_PROBABILITY_DEFAULT)
        ttk.Entry(frame, textvariable=self.mutation_probability_var).grid(row=5, column=3, pady=8, sticky=(tk.W, tk.E))
        
    def _setup_inversion_config(self, frame):
        # Inversion probability
        ttk.Label(frame, text="Inversion probability [%]:").grid(row=6, column=0, sticky=tk.W, pady=8)
        self.inversion_probability_var = tk.IntVar(value=self.__INVERSION_PROBABILITY)
        ttk.Entry(frame, textvariable=self.inversion_probability_var).grid(row=6, column=1, pady=8, sticky=(tk.W, tk.E))

    def _setup_elite_strategy_config(self, frame):
        # Elite count input field next to inversion probability
        ttk.Label(frame, text="Elite count:").grid(row=6, column=2, sticky=tk.W, pady=8)
        self.elite_count_var = tk.IntVar(value=self.__ELITE_STRATEGY_UNIT_COUNT)
        ttk.Entry(frame, textvariable=self.elite_count_var).grid(row=6, column=3, pady=8, sticky=(tk.W, tk.E))

    def _add_start_button(self, frame):
        # Remove any existing button if needed (optional, in current layout only one created).

        # Add a spacer row to push the button to the bottom.
        frame.grid_rowconfigure(99, weight=1)  # Make row 99 expandable, leaves room above the button.

        start_button = ttk.Button(frame, text="Start", command=self._start_simulation)
        # Set sticky to 's' (south) and 'ew' to center horizontally and pin to the bottom row.
        start_button.grid(row=100, column=0, columnspan=4, pady=15, sticky='sew')

    def _get_config(self) -> SimulationConfiguration:
        try:
            # to move upper (UI)
            is_maxim_case = False
            
            # general config
            general_config = GeneralConfig(self.population_var.get(), self.epochs_var.get(), self.chromosome_repr_precision_var.get() )
            
            # cost function config
            cost_function_config = CostFunctionConfig(self.dimensions_var.get(), self.cost_function_map[self.cost_function_var.get()])

            # unit factory
            suggested_bounds = cost_function_config.cost_func.suggested_bounds()

            lower_bound, upper_bound = suggested_bounds[0][0], suggested_bounds[1][0]
            unit_factory = UnitFactory(lower_bound, upper_bound, 6)

            # selection function config
            tournament_size = None
            if hasattr(self, 'tournament_size_label'):
                self.tournament_size_label.grid_remove()
                self.tournament_size_entry.grid_remove()
                tournament_size = self.tournament_size_var.get()

            selection_config = SelectionConfig(self.selection_function_map[self.selection_function_var.get()], self.selection_percentage_var.get(), is_maxim_case, tournament_size)

            # crossing config
            grain = None
            if hasattr(self, 'crossing_grain_label'):
               grain = self.crossing_grain_var.get()
        
            crossing_config = CrossingConfig(self.crossing_function_map[self.crossing_function_var.get()], self.crossing_percentage_var.get(), unit_factory, self.elite_count_var.get(), grain=grain)

            # mutation config
            mutation_config = MutationConfig(unit_factory, self.mutation_function_map[self.mutation_function_var.get()], self.mutation_probability_var.get())

            # inversion config
            inversion_config = InversionConfig(unit_factory, self.inversion_probability_var.get())

            return SimulationConfiguration(
                unit_factory,
                cost_function_config,
                crossing_config,
                general_config,
                inversion_config,
                mutation_config,
                selection_config
            )
        except AssertionError:
            self._display_vaidation_error()
            return

    def _reset_variables(self):        
        # general config
        self.epochs_var.set(self.__EPOCHS_NUMBER_DEFAULT)
        self.population_var.set(self.__POPULATION_SIZE_DEFAULT)
        self.chromosome_repr_precision_var.set(self.__CHROMOSOME_PRECISION_DEFAULT)
        
        # cost config
        self.cost_function_var.set(self.__COST_FUNCTION_TYPE_DEFAULT)
        self.dimensions_var.set(self.__COST_FUNCTION_DIMENSIONS_DEFAULT)
        if hasattr(self, 'tournament_size_label'):
            self.tournament_size_label.grid_remove()
            self.tournament_size_entry.grid_remove()

        # selection config
        self.selection_function_var.set(self.__SELECTION_TYPE_DEFAULT)
        self.selection_percentage_var.set(self.__SELECTION_PERCENTAGE_DEFAULT)

        # crossing config
        self.crossing_function_var.set(self.__CROSSING_FUNC_TYPE_DEFAULT)
        if hasattr(self, 'crossing_grain_label'):
            self.crossing_grain_label.grid_remove()
            self.crossing_grain_entry.grid_remove()
        self.crossing_percentage_var.set(self.__CROSSING_PERCENTAGE_DEFAULT)

        # mutation config
        self.mutation_function_var.set(self.__MUTATION_TYPE_DEFAULT)
        self.mutation_probability_var.set(self.__MUTATION_PROBABILITY_DEFAULT)

        # inversion config
        self.inversion_probability_var.set(self.__INVERSION_PROBABILITY)

        # elite config
        self.elite_count_var.set(self.__ELITE_STRATEGY_UNIT_COUNT)

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
            self._reset_variables()
            return

        # create simulation
        self._open_loading_window()

        simulation = Simulation(config)
        simulation.start()

        self._close_loading_window()
        self._switch_to_results_page(simulation)

    def _open_loading_window(self):
        loading_window = tk.Toplevel(self.master)
        loading_window.title("Simulation Running")
        loading_window.geometry("300x100")
        loading_window.grab_set()
        loading_label = ttk.Label(loading_window, text="Simulation is running...", anchor='center', font=("Arial", 14))
        loading_label.place(relx=0.5, rely=0.5, anchor='center')
        loading_window.update()
        self.loading_window = loading_window

    def _close_loading_window(self):
        self.loading_window.destroy()

    def _switch_to_results_page(self, simulation: Simulation):
        self._clear_page()
        self._draw_charts(simulation)

        elapsed_time_sec = simulation.elapsed_time
        self.elapsed_label = ttk.Label(
            self.master,
            text=f"Simulation run time: {elapsed_time_sec:.2f} seconds",
            font=("Arial", 14)
        )
        self.elapsed_label.pack(pady=(10, 5))

    def _draw_charts(self, simulation: Simulation):
        # Prepare data
        epochs = list(range(len(simulation.best_cost_history)))
        best_cost = simulation.best_cost_history
        avg_cost = simulation.avg_cost_history
        std_cost = simulation.std_cost_history

        # Create a new matplotlib figure with two subplots
        fig, axs = plt.subplots(3, 1, figsize=(8, 6))
        fig.suptitle('Simulation Results')

        # Plot Best Cost History
        axs[0].plot(epochs, best_cost, label='Best Cost', color='blue')
        axs[0].set_title('Best Cost per Epoch')
        axs[0].set_xlabel('Epoch')
        axs[0].set_ylabel('Best Cost')
        axs[0].legend()
        axs[0].grid(True)

        # Plot Average Cost History
        axs[1].plot(epochs, avg_cost, label='Average Cost', color='green')
        axs[1].set_title('Average Cost per Epoch')
        axs[1].set_xlabel('Epoch')
        axs[1].set_ylabel('Average Cost')
        axs[1].legend()
        axs[1].grid(True)

        # Plot Standard Deviation of Cost History
        axs[2].plot(epochs, std_cost, label='Standard Deviation', color='red')
        axs[2].set_title('Standard Deviation of Cost per Epoch')
        axs[2].set_xlabel('Epoch')
        axs[2].set_ylabel('Standard Deviation')
        axs[2].legend()
        axs[2].grid(True)

        plt.tight_layout(rect=[0, 0, 1, 0.96])
        plt.show()

    def _clear_page(self):
        for widget in self.master.winfo_children():
            widget.destroy()