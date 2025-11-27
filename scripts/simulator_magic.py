import pandas as pd
import os
from IPython.core.magic import (Magics, magics_class, cell_magic)

# Global reference to the active simulator instance
_active_simulator = None

@magics_class
class DocaSimulator(Magics):
    def __init__(self, shell):
        super(DocaSimulator, self).__init__(shell)
        global _active_simulator
        _active_simulator = self
        
        self.current_index = 0
        
        # Load the data
        current_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.dirname(current_dir)
        excel_path = os.path.join(root_dir, 'dpu simulator', 'doca_installation_commands.csv')
        try:
            self.df = pd.read_csv(excel_path)
            # Normalize commands for comparison (strip whitespace)
            if 'Command' in self.df.columns:
                self.df['Command_Clean'] = self.df['Command'].astype(str).str.strip()
        except Exception as e:
            print(f"Error loading csv file: {e}")
            self.df = pd.DataFrame()

    @cell_magic
    def doca(self, line, cell):
        """
        Simulates the output of a command.
        Usage: 
          %%doca 
          <command>
        """
        try:
            # Check if line argument is an explicit index
            if line and line.strip().isdigit():
                idx = int(line.strip())
                self._print_output(idx)
                self.current_index = idx + 1
                return

            # Otherwise, match command content
            command_to_run = cell.strip()
            
            # Search for the command starting from current_index
            # We look for the *next* occurrence of this command
            subset = self.df.iloc[self.current_index:]
            match = subset[subset['Command_Clean'] == command_to_run]
            
            if match.empty:
                # If not found forward, try from beginning (wrap around)
                subset_all = self.df
                match_all = subset_all[subset_all['Command_Clean'] == command_to_run]
                
                if match_all.empty:
                    print(f"Simulation Error: Command not found in scenario:\n{command_to_run}")
                    return
                else:
                    # Found earlier in the script, jump there
                    idx = match_all.index[0]
            else:
                # Found in future
                idx = match.index[0]
            
            # Execute and advance
            self._print_output(idx)
            self.current_index = idx + 1

        except Exception as e:
            print(f"Error executing simulation: {e}")

    def _print_output(self, idx):
        if 0 <= idx < len(self.df):
            output = self.df.iloc[idx]['Output']
            if pd.isna(output):
                output = ""
            # Print exact output
            if output:
                print(output)
        else:
            print(f"Error: Index {idx} out of bounds.")

    def is_known_command(self, lines):
        """Check if the cell content matches a known command."""
        if self.df.empty:
            return False
            
        # Reconstruct the cell content from lines (input_transformer gives list of strings with newlines)
        content = "".join(lines).strip()
        
        # Check if this exact command exists in the Excel file
        return content in self.df['Command_Clean'].values

# Input Transformer Function
def doca_input_transformer(lines):
    """
    Automatically prepends %%doca to cells that match known simulation commands.
    """
    global _active_simulator
    if _active_simulator and _active_simulator.is_known_command(lines):
        # If the command is known, inject the magic
        return ['%%doca\n'] + lines
    return lines

def load_ipython_extension(ipython):
    # Register the magic class
    ipython.register_magics(DocaSimulator)
    
    # Register the input transformer to handle "magic-less" commands
    ipython.input_transformers_cleanup.append(doca_input_transformer)
