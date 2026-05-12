import os
import json
from pathlib import Path

# Get the directory where getenv.py is located
current_dir = Path(__file__).parent



def getenv():
    env = {}
    env_path = current_dir / 'env.json'  # Looks in same directory as getenv.py

    with open(env_path) as f:
        env = json.load(f)


    return env