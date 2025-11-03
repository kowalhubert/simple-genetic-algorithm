# Genetic Algorithm Simulation

A Python application for running genetic algorithm simulations with configurable parameters.

## Project Structure

```
p1/
├── src/                          # Main source code
│   ├── __init__.py
│   ├── core/                     # Core genetic algorithm components
│   │   ├── __init__.py
│   │   ├── cost_function.py
│   │   ├── crossing.py
│   │   ├── inversion.py
│   │   ├── mutation.py
│   │   ├── results_saver.py
│   │   ├── selection.py
│   │   ├── simulation.py
│   │   └── unit.py
│   ├── ui/                       # User interface components
│   │   ├── __init__.py
│   │   └── simulation_ui.py
│   └── config/                   # Configuration management
│       ├── __init__.py
│       ├── cost_function_config.py
│       ├── crossing_config.py
│       ├── general_config.py
│       ├── inversion_config.py
│       ├── mutation_config.py
│       ├── selection_config.py
│       └── simulation_config.py
├── main.py                       # Application entry point (launches Tkinter UI)
├── requirements.txt              # Direct dependencies (human-maintained)
├── requirements.lock.txt         # Fully pinned deps (auto-generated, optional)
└── README.md                     # This file
```

## Installation

1. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the application (launches the Tkinter UI):
```bash
python main.py
```

### Saving Results

See detailed documentation for automatic results export in `RESULTS_SAVER_USAGE.md`.

## Module Dependencies

- **src/core/**: Contains core genetic algorithm logic (chromosome, cost functions)
- **src/ui/**: Contains user interface components (tkinter-based)
- **src/config/**: Contains configuration classes and validation
- **main.py**: Application entry point with minimal dependencies

## Dependencies

- `benchmark-functions` (via PyPI) – optimization benchmark functions
- `matplotlib` – plotting in the UI
- `tkinter` – built-in Python GUI library (comes with CPython on most platforms)
