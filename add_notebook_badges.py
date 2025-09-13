#!/usr/bin/env python3
"""Add Colab and Binder badges to Jupyter notebooks."""

import json
import os
from pathlib import Path

def add_badges_to_notebook(notebook_path):
    """Add Colab and Binder badges to a Jupyter notebook."""
    
    # Load the notebook
    with open(notebook_path, 'r') as f:
        notebook = json.load(f)
    
    # Get the relative path for the badge URL
    repo_url = "https://github.com/kennedym-ds/semiconductor_sim"
    notebook_name = os.path.basename(notebook_path)
    notebook_url = f"{repo_url}/blob/main/examples/{notebook_name}"
    colab_url = f"https://colab.research.google.com/github/kennedym-ds/semiconductor_sim/blob/main/examples/{notebook_name}"
    binder_url = f"https://mybinder.org/v2/gh/kennedym-ds/semiconductor_sim/main?filepath=examples/{notebook_name}"
    
    # Create the badge cell content
    badge_content = f"""# {notebook_name.replace('_', ' ').replace('.ipynb', '').title()}

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)]({colab_url})
[![Binder](https://mybinder.org/badge_logo.svg)]({binder_url})

---

*Interactive semiconductor device simulation using SemiconductorSim*"""
    
    # Create a new markdown cell with badges
    badge_cell = {
        "cell_type": "markdown",
        "metadata": {},
        "source": badge_content.split('\n')
    }
    
    # Check if the first cell is already a markdown cell with badges
    if (notebook['cells'] and 
        notebook['cells'][0]['cell_type'] == 'markdown' and
        any('colab-badge' in str(line) for line in notebook['cells'][0].get('source', []))):
        # Update existing badge cell
        notebook['cells'][0] = badge_cell
    else:
        # Insert at the beginning
        notebook['cells'].insert(0, badge_cell)
    
    # Save the updated notebook
    with open(notebook_path, 'w') as f:
        json.dump(notebook, f, indent=1)
    
    print(f"Added badges to {notebook_name}")

def main():
    """Add badges to all notebooks in the examples directory."""
    examples_dir = Path('examples')
    
    for notebook_path in examples_dir.glob('*.ipynb'):
        add_badges_to_notebook(notebook_path)

if __name__ == '__main__':
    main()