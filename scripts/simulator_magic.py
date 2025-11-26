import pandas as pd
import os
from IPython.core.magic import (Magics, magics_class, cell_magic)
from IPython.display import display, HTML

@magics_class
class DocaSimulator(Magics):
    def __init__(self, shell):
        super(DocaSimulator, self).__init__(shell)
        # Load the data when the extension is loaded
        # The excel file is located in 'dpu simulator/doca_installation_commands.xlsx' relative to project root
        # We assume this script is in 'scripts/' and the excel is in 'dpu simulator/'
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Go up one level to root, then into dpu simulator
        root_dir = os.path.dirname(current_dir)
        excel_path = os.path.join(root_dir, 'dpu simulator', 'doca_installation_commands.xlsx')
        try:
            self.df = pd.read_excel(excel_path)
        except Exception as e:
            print(f"Error loading excel file: {e}")
            self.df = pd.DataFrame()

    @cell_magic
    def doca(self, line, cell):
        """
        Simulates the output of a command.
        Usage: %%doca <row_index>
        """
        try:
            idx = int(line.strip())
            if 0 <= idx < len(self.df):
                output = self.df.iloc[idx]['Output']
                
                # Handle NaN or empty output
                if pd.isna(output):
                    output = ""
                
                # Print exact output
                print(output)
            else:
                print(f"Error: Index {idx} out of bounds.")
        except ValueError:
            print(f"Error: Invalid index '{line}'.")
        except Exception as e:
            print(f"Error executing simulation: {e}")

def load_ipython_extension(ipython):
    ipython.register_magics(DocaSimulator)

