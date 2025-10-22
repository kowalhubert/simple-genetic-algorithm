# Genetic Algorithm Simulation

A Python application for running genetic algorithm simulations with configurable parameters.

## Project Structure

```
p1/
├── src/                          # Main source code
│   ├── __init__.py
│   ├── core/                     # Core genetic algorithm components
│   │   ├── __init__.py
│   │   ├── chromosome.py         # Chromosome representation
│   │   └── cost_function.py      # Cost function definitions
│   ├── ui/                       # User interface components
│   │   ├── __init__.py
│   │   └── simulation_config_ui.py  # Configuration UI
│   └── config/                   # Configuration management
│       ├── __init__.py
│       └── simulation_config.py # Simulation configuration classes
├── main.py                       # Application entry point
├── requirements.txt              # Python dependencies
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

Run the application:
```bash
python main.py
```

## Module Dependencies

- **src/core/**: Contains core genetic algorithm logic (chromosome, cost functions)
- **src/ui/**: Contains user interface components (tkinter-based)
- **src/config/**: Contains configuration classes and validation
- **main.py**: Application entry point with minimal dependencies

## Dependencies

- `benchmark-functions`: For optimization benchmark functions
- `tkinter`: Built-in Python GUI library
