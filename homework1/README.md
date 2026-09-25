# Homework #1: Introduction to Python & Unit Testing
Student: Fabian A. Perez Muñoz
Course: CS4300/5300 002

## Installing Python and Virtual Environment (venv)
```bash
python3 -m venv hw1_venv --system-site-packages
source hw1_venv/bin/activate
```

## Required Packages
Recommended, install requirements.txt to comply with the packages necessary.
```bash
python -m pip install -r requirements.txt
```

```bash
python3 -m pip install pytest
python3 -m pip install sympy # Task 3
python3 -m pip install requests # Task7
```

## Running Pytests
1. Open an Integrated Terminal within folder homework1.
2. Ensure you have activated your virtual environment and that it has the proper packages installed (requirements.txt installation).

### Global Pytest
To run all pytests at once:
- Within `/homework1` run: 
`pytest`
OR 
`python -m pytest` (can add -q for 'quiet')

### Individual Pytesting
If you want to run an individual pytest: 
`python -m pytest tests/test_task2.py`

### Test Task 1 Console Output
To verify that task1.py provides the script console output:
`python src/task1.py`

