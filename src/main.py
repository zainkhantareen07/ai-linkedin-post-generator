import os
import sys

# Forces Python to look inside the current directory for modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import run_app

if __name__ == "__main__":
    run_app()