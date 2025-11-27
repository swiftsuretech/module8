# Module 8 - DPU & AI Software Configuration

This repository contains the lab materials for Module 8, designed for training technical students on NVIDIA DPU administration and AI software configuration.

The environment provides a set of Jupyter Notebooks that guide students through the process of installing drivers, configuring the BlueField DPU, and running AI workloads.

## Repository Structure

- **Root**: Contains the main lab notebooks (`Lab 1`, `Lab 2`, `Lab 3`).
- **dpu simulator/**: Contains the data source for the simulated terminal environment.
- **scripts/**: Python and Shell scripts that power the simulation and environment setup.
- **guides/**: PDF documentation (`labguide.pdf`).

## Lab Overview

1. **Lab 1 - Driver Installation**: Covers the installation of DOCA host drivers and utilities on the server.
2. **Lab 2 - Installing and Running AI Software**: Focuses on deploying and executing AI workloads, comparing CPU vs. GPU performance.
3. **Lab 3 - DPU Initial Configuration**: Guides the student through the initial setup of the BlueField DPU, including installing the BlueField Bundle (BFB) and verifying connectivity.

## How the DPU Simulator Works

Because these labs often run in environments without physical access to a dedicated DPU or where re-imaging a real DPU would be time-consuming, this repository uses a **DPU Simulator**.

### The "Chat" Mechanism
The simulator functions like a scripted "chat" between the user and a virtual terminal. It is powered by two main components:

1.  **`scripts/simulator_magic.py`**: A custom IPython Magic extension. It defines the `%%doca` cell magic used in the notebooks.
2.  **`dpu simulator/doca_installation_commands.csv`**: A CSV file acting as the script.

**How it functions:**
- The CSV file contains columns for `Command` and `Output`.
- When a student runs a cell starting with `%%doca`, the simulator reads their command.
- It looks up the corresponding command in the CSV file (sequentially).
- It then "simulates" the execution by printing the pre-defined `Output` from the CSV.

This allows students to type realistic commands (like `sudo -i`, `apt install`, `minicom`) and receive realistic feedback (including errors and prompts) without actually changing the system state.

## Helper Scripts

- **`scripts/lab_setup.py`**: Automatically runs at the start of notebooks to install dependencies (pandas, openpyxl) and load the simulator magic.
- **`scripts/generate_notebook.py`**: A utility to programmatically generate/reset `Lab 3` to a known good state.
- **`scripts/timer.py`**: A helper for Lab 2 to measure and compare execution times between CPU and GPU workloads.

