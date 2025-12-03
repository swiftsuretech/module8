import pandas as pd
import os

def convert_csv():
    current_dir = os.getcwd()
    file_path = os.path.join(current_dir, 'dpu simulator', 'doca_installation_commands.csv')
    
    # Read the pipe-separated CSV
    df = pd.read_csv(file_path, sep='|')
    
    # Remove the first column (index)
    if len(df.columns) > 0:
        df = df.iloc[:, 1:]
    
    # Write back as comma-separated CSV, with quoting
    df.to_csv(file_path, index=False, quoting=1) # quoting=1 is csv.QUOTE_ALL

if __name__ == "__main__":
    convert_csv()

