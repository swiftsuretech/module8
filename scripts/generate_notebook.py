import nbformat as nbf
import pandas as pd
import os

def generate_notebook():
    # file paths
    # This script is in 'scripts/', excel in 'dpu simulator/', output in root
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(current_dir)
    
    excel_path = os.path.join(root_dir, 'dpu simulator', 'doca_installation_commands.xlsx')
    output_path = os.path.join(root_dir, 'DOCA_Simulation.ipynb')

    # Read the Excel file
    try:
        df = pd.read_excel(excel_path)
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return

    # Create a new notebook object
    nb = nbf.v4.new_notebook()

    # Create the setup cell
    setup_code = """# Setup for DOCA Simulator
import sys
import os

# Add the scripts directory to the path explicitly
current_dir = os.getcwd()
scripts_path = os.path.join(current_dir, 'scripts')

# Force add to the BEGINNING of sys.path to ensure it takes precedence
if scripts_path not in sys.path:
    sys.path.insert(0, scripts_path)

# Manually import the module to force it into sys.modules
import simulator_magic

# Now load the extension
%reload_ext simulator_magic
"""
    cells = [nbf.v4.new_code_cell(setup_code)]

    # Iterate through the dataframe and create cells
    for idx, row in df.iterrows():
        command = row['Command']
        
        # Check for NaN command, though typically shouldn't happen based on intent
        if pd.isna(command):
            command = "# No command specified"
        
        # Construct the cell content
        # We put the index in the magic line, and the command in the body
        cell_content = f"%%doca {idx}\n{command}"
        
        cells.append(nbf.v4.new_code_cell(cell_content))

    nb['cells'] = cells

    # Write the notebook
    with open(output_path, 'w') as f:
        nbf.write(nb, f)

    print(f"Notebook generated successfully at: {output_path}")

if __name__ == "__main__":
    generate_notebook()

