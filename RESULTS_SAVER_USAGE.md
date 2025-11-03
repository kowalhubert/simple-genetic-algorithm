# Simulation Results Saver

## Overview

The `SimulationResultsSaver` class automatically saves simulation results to organized files in the `/results` directory.

## Directory Structure

```
results/
├── YYYYMMDD_HHMMSS_microseconds/
│   ├── simulation_config.json      # Simulation configuration
│   ├── results.csv                  # Metrics per epoch
│   └── additional_info.json        # Additional information
```

## Files Generated

### 1. `simulation_config.json`
Contains the complete simulation configuration:
- General config (population size, epochs, precision)
- Cost function config (dimensions, function type, bounds)
- Selection config (type, percentage, maximization, tournament size)
- Crossing config (type, elite count, grain size)
- Mutation config (type, probability)
- Inversion config (probability)

### 2. `results.csv`
Contains metrics for each epoch with columns:
- `epoch`: Epoch number (1-based)
- `best_cost`: Best cost value in this epoch
- `avg_cost`: Average cost value in this epoch
- `deviation`: Standard deviation of costs in this epoch

### 3. `additional_info.json`
Contains runtime information:
- `elapsed_time`: Total simulation time in seconds
- `population_size`: Population size
- `dimensions`: Number of dimensions
- `epochs`: Number of epochs
- `final_best_cost`: Best cost at the end
- `best_unit_parameters`: Parameters of the best unit

## Usage

### Basic Usage

```python
from src.core.results_saver import SimulationResultsSaver, config_to_dict

# After running simulation
saver = SimulationResultsSaver()
config_dict = config_to_dict(simulation_config)
saver.save_results(simulation, config_dict)

# Get the results directory
results_dir = saver.get_simulation_dir()
print(f"Results saved to: {results_dir}")
```

### Automatic Integration

The results saver is already integrated into the UI. After each simulation completes, results are automatically saved to:

```
results/YYYYMMDD_HHMMSS_microseconds/
```

## Timestamp Format

The timestamp format is `YYYYMMDD_HHMMSS_microseconds` to ensure uniqueness:
- Example: `20231215_143025_123456`
- Format: `2023-12-15 14:30:25.123456`

This ensures that:
1. Each simulation gets a unique folder
2. Folders are sorted chronologically
3. No collisions occur

## Example Results

### `simulation_config.json`:
```json
{
    "general_config": {
        "population_size": 100,
        "epochs_no": 50,
        "chromosome_precision": 6
    },
    "cost_function_config": {
        "dimensions": 2,
        "cost_function_name": "Rastrigin",
        "suggested_bounds": [[-5.12, -5.12], [5.12, 5.12]]
    },
    ...
}
```

### `results.csv`:
```csv
epoch,best_cost,avg_cost,deviation
1,123.45,234.56,67.89
2,120.30,232.45,65.32
3,118.20,229.87,63.15
...
```

### `additional_info.json`:
```json
{
    "elapsed_time": 12.34,
    "population_size": 100,
    "dimensions": 2,
    "epochs": 50,
    "final_best_cost": 45.67,
    "best_unit_parameters": [1.23, -0.45]
}
```
