import os
import json
import csv
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, TYPE_CHECKING

from src.config.simulation_config import SimulationConfiguration

def config_to_dict(simulation_config: SimulationConfiguration) -> Dict[str, Any]:
    """
    Convert SimulationConfiguration object to dictionary for serialization.
    
    Args:
        simulation_config: SimulationConfiguration object
        
    Returns:
        Dictionary representation of the configuration
    """
    return {
        "general_config": {
            "population_size": simulation_config.general_config.population_size,
            "epochs_no": simulation_config.general_config.epochs_no,
            "chromosome_precision": simulation_config.general_config.repr_precision
        },
        "cost_function_config": {
            "dimensions": simulation_config.cost_function_config.dimensions,
            "cost_function_name": simulation_config.cost_function_config.cost_func.__class__.__name__,
            "suggested_bounds": list(simulation_config.cost_function_config.cost_func.suggested_bounds())
        },
        "selection_config": {
            "selection_type": str(simulation_config.selection_config.selection_type),
            "selection_percentage": simulation_config.selection_config.selection_percentage,
            "is_maximization": simulation_config.selection_config.is_maxim_case,
            "tournament_size": simulation_config.selection_config.tournament_size
        },
        "crossing_config": {
            "crossing_type": str(simulation_config.crossing_config.crossing_type),
            "crossing_percentage": str(simulation_config.crossing_config.probability),
            "elite_count": simulation_config.crossing_config.elite_count,
            "grain_size": simulation_config.crossing_config.grain
        },
        "mutation_config": {
            "mutation_type": str(simulation_config.mutation_config.mutation_type),
            "probability": simulation_config.mutation_config.probability
        },
        "inversion_config": {
            "probability": simulation_config.inversion_config.probability
        }
    }


class SimulationResultsSaver:
    """
    Responsible for saving simulation results to files.
    Each simulation gets its own timestamped subfolder in /results directory.
    """
    
    def __init__(self, base_results_dir: str = "results"):
        self.base_results_dir = Path(base_results_dir)
        self.base_results_dir.mkdir(exist_ok=True)
        self.simulation_dir = None
        self._create_simulation_folder()
    
    def _create_simulation_folder(self) -> Path:
        """
        Create a unique timestamped folder for this simulation.
        Format: YYYYMMDD_HHMMSS_microseconds
        """
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d_%H%M%S_%f")
        self.simulation_dir = self.base_results_dir / timestamp
        self.simulation_dir.mkdir(exist_ok=True)
        return self.simulation_dir
    
    def save_simulation_config(self, config: Dict[str, Any], filename: str = "simulation_config.json"):
        """
        Save simulation configuration to JSON file.
        
        Args:
            config: Dictionary containing simulation configuration
            filename: Name of the configuration file
        """
        config_path = self.simulation_dir / filename
        
        # Convert any non-serializable objects to strings
        serializable_config = self._make_serializable(config)
        
        with open(config_path, 'w') as f:
            json.dump(serializable_config, f, indent=4)
    
    def save_metrics(self, best_costs: list[float], avg_costs: list[float], 
                     deviations: list[float], filename: str = "results.csv"):
        """
        Save simulation metrics to CSV file.
        Each epoch has one row with: epoch, best_cost, avg_cost, deviation
        
        Args:
            best_costs: List of best costs per epoch
            avg_costs: List of average costs per epoch
            deviations: List of standard deviations per epoch
            filename: Name of the CSV file
        """
        metrics_path = self.simulation_dir / filename
        
        with open(metrics_path, 'w', newline='') as f:
            writer = csv.writer(f)
            
            # Write header
            writer.writerow(['epoch', 'best_cost', 'avg_cost', 'deviation'])
            
            # Write data rows
            for epoch in range(len(best_costs)):
                writer.writerow([
                    epoch + 1,
                    best_costs[epoch],
                    avg_costs[epoch],
                    deviations[epoch]
                ])
    
    def save_additional_info(self, info: Dict[str, Any], filename: str = "additional_info.json"):
        """
        Save additional information (e.g., elapsed time, final best unit).
        
        Args:
            info: Dictionary with additional information
            filename: Name of the file
        """
        info_path = self.simulation_dir / filename
        
        serializable_info = self._make_serializable(info)
        
        with open(info_path, 'w') as f:
            json.dump(serializable_info, f, indent=4)
    
    def _make_serializable(self, obj: Any) -> Any:
        """
        Recursively convert non-serializable objects to serializable format.
        """
        if isinstance(obj, dict):
            return {key: self._make_serializable(value) for key, value in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [self._make_serializable(item) for item in obj]
        elif isinstance(obj, Path):
            return str(obj)
        elif hasattr(obj, '__dict__'):
            # Custom objects - convert to dict representation
            return self._make_serializable(obj.__dict__)
        else:
            # Try to return the object as-is if it's JSON serializable
            try:
                json.dumps(obj)
                return obj
            except (TypeError, ValueError):
                return str(obj)
    
    def get_simulation_dir(self) -> Path:
        """
        Get the path to the current simulation directory.
        """
        return self.simulation_dir
    
    def save_results(self, simulation, config_dict: Dict[str, Any]):
        """
        Complete save operation - saves config, metrics, and additional info.
        
        Args:
            simulation: The Simulation object
            config_dict: Configuration as dictionary
        """
        # Save configuration
        self.save_simulation_config(config_dict)
        
        # Save metrics
        self.save_metrics(
            best_costs=simulation.best_cost_history,
            avg_costs=simulation.avg_cost_history,
            deviations=simulation.std_cost_history
        )
        
        # Save additional info
        additional_info = {
            "elapsed_time": simulation.elapsed_time,
            "population_size": simulation._population_size,
            "dimensions": simulation._dimesions,
            "epochs": simulation._epochs_number,
            "final_best_cost": simulation.best_cost_history[-1] if simulation.best_cost_history else None,
            "best_unit_parameters": simulation._population[0].real_values if simulation._population else None
        }
        self.save_additional_info(additional_info)
