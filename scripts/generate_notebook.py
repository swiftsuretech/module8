import nbformat as nbf
import os

def generate_notebook():
    # file paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(current_dir)
    output_path = os.path.join(root_dir, 'Lab 3 - DPU Initial Configuration.ipynb')

    # Create a new notebook object
    nb = nbf.v4.new_notebook()
    cells = []

    # --- Header ---
    logo_md = """<img src="https://www.nvidia.com/content/dam/en-zz/Solutions/about-nvidia/logo-and-brand/01-nvidia-logo-horiz-500x200-2c50-d@2x.png" alt="NVIDIA Logo" style="width: 300px; height: auto;">"""
    cells.append(nbf.v4.new_markdown_cell(logo_md))

    sep_md = "---"
    cells.append(nbf.v4.new_markdown_cell(sep_md))

    # --- Overview ---
    overview_md = """# Lab 3: DPU Initial Configuration

## Lab Overview

### Audience
This workbook is intended for technical training students.

### Objectives
In this practice, you will:
* Install DOCA on the server
* Install BlueField Bundle on the DPU

### Prerequisites
There are no prerequisites for this lab.
"""
    cells.append(nbf.v4.new_markdown_cell(overview_md))
    cells.append(nbf.v4.new_markdown_cell(sep_md))

    # --- Setup Task ---
    setup_md = """### Configure Lab Environment
Please run the following cell to configure the lab environment for the DPU simulation.
"""
    cells.append(nbf.v4.new_markdown_cell(setup_md))
    
    setup_code = "%run scripts/lab_setup.py"
    cells.append(nbf.v4.new_code_cell(setup_code))

    cells.append(nbf.v4.new_markdown_cell(sep_md))

    # --- Practice 1 ---
    p1_md = """## Practice 1: Install DOCA and BlueField Bundle

In this practice you will install DOCA on the host and BlueField Bundle on the DPU.
"""
    cells.append(nbf.v4.new_markdown_cell(p1_md))

    # --- Task 1 ---
    t1_md = """### Task 1: Download and Install DOCA on the Server

For this exercise, the required package (`doca-host_2.9.1...`) has already been downloaded to your environment.
"""
    cells.append(nbf.v4.new_markdown_cell(t1_md))

    # Step: Root
    cells.append(nbf.v4.new_markdown_cell("#### 1.1 - Enter root mode:"))
    cells.append(nbf.v4.new_code_cell("sudo -i"))

    # Step: Uninstall
    cells.append(nbf.v4.new_markdown_cell("#### 1.2 - Uninstall the current version of DOCA:"))
    cells.append(nbf.v4.new_code_cell("for f in $( dpkg --list | grep doca | awk '{print $2}' ); do echo $f ; apt remove --purge $f -y ; done"))
    
    # Step: OFED
    cells.append(nbf.v4.new_markdown_cell("#### 1.3 - If the output is empty, clean up OFED and dependencies:"))
    cells.append(nbf.v4.new_code_cell("/usr/sbin/ofed_uninstall.sh --force"))
    
    # Step: Navigate (Critical for simulation flow)
    cells.append(nbf.v4.new_markdown_cell("#### 1.4 - Navigate to the installation directory:"))
    cells.append(nbf.v4.new_code_cell("cd /home/student/AI_Infra/module5/hands_on_1"))

    # Step: Install
    cells.append(nbf.v4.new_markdown_cell("#### 1.5 - Unpack the installation file:"))
    cells.append(nbf.v4.new_code_cell("dpkg -i doca-host_3.1.0-091000-25.07-ubuntu2204_amd64.deb"))

    # Step: Update
    cells.append(nbf.v4.new_markdown_cell("#### 1.6 - Update package manager:"))
    cells.append(nbf.v4.new_code_cell("apt update"))

    # Step: Rshim
    cells.append(nbf.v4.new_markdown_cell("#### 1.7 - Verify that rshim is installed:"))
    cells.append(nbf.v4.new_code_cell("systemctl status rshim"))

    cells.append(nbf.v4.new_markdown_cell("#### 1.8 - If rshim is not installed, install it:"))
    cells.append(nbf.v4.new_code_cell("apt install rshim"))

    cells.append(nbf.v4.new_markdown_cell("#### 1.9 - Start the rshim service:"))
    cells.append(nbf.v4.new_code_cell("sudo systemctl start rshim"))

    # Step: DOCA All
    cells.append(nbf.v4.new_markdown_cell("#### 1.10 - Install the DOCA-All package:"))
    cells.append(nbf.v4.new_code_cell("apt install -y doca-all mlnx-fw-updater"))

    # Step: Exit
    cells.append(nbf.v4.new_markdown_cell("#### 1.11 - Exit root shell:"))
    cells.append(nbf.v4.new_code_cell("exit"))

    cells.append(nbf.v4.new_markdown_cell(sep_md))

    # --- Task 2 ---
    t2_md = """### Task 2: Access the BlueField DPU

Now we will connect to the DPU console using Minicom.
"""
    cells.append(nbf.v4.new_markdown_cell(t2_md))

    # Step: Minicom Attempt 1
    cells.append(nbf.v4.new_markdown_cell("#### 2.1 - Login to the BlueField DPU using the console:"))
    cells.append(nbf.v4.new_code_cell("sudo minicom -D /dev/rshim0/console"))

    # Troubleshooting sequence (based on Excel flow)
    t2_trouble_md = """#### Troubleshooting
It seems the connection failed. Let's ensure the Rshim service is running correctly.
"""
    cells.append(nbf.v4.new_markdown_cell(t2_trouble_md))

    cells.append(nbf.v4.new_markdown_cell("#### 2.2 - Start Rshim service:"))
    cells.append(nbf.v4.new_code_cell("sudo systemctl start rshim"))

    cells.append(nbf.v4.new_markdown_cell("#### 2.3 - Retry connection:"))
    cells.append(nbf.v4.new_code_cell("sudo minicom -D /dev/rshim0/console"))

    cells.append(nbf.v4.new_markdown_cell("#### 2.4 - Check Status:"))
    cells.append(nbf.v4.new_code_cell("sudo systemctl status rshim"))

    cells.append(nbf.v4.new_markdown_cell("#### 2.5 - Restart Service (Stop/Start):"))
    cells.append(nbf.v4.new_code_cell("sudo systemctl stop rshim"))
    cells.append(nbf.v4.new_code_cell("sudo systemctl start rshim"))

    cells.append(nbf.v4.new_markdown_cell("#### 2.6 - Connect to Console (Success):"))
    cells.append(nbf.v4.new_code_cell("sudo minicom -D /dev/rshim0/console"))

    # DPU Interaction
    dpu_md = """### DPU Configuration
You are now connected to the DPU console.
"""
    cells.append(nbf.v4.new_markdown_cell(dpu_md))

    cells.append(nbf.v4.new_markdown_cell("#### 2.7 - Enter default username (ubuntu):"))
    cells.append(nbf.v4.new_code_cell("[DPU] ubuntu"))

    cells.append(nbf.v4.new_markdown_cell("#### 2.8 - Enter default password (ubuntu):"))
    cells.append(nbf.v4.new_code_cell("[DPU] (password entered)"))

    cells.append(nbf.v4.new_markdown_cell("#### 2.9 - Set new password (Nvidia_12345!):"))
    cells.append(nbf.v4.new_code_cell("[DPU] (new passwords entered)"))

    cells.append(nbf.v4.new_markdown_cell("#### 2.10 - Enter root mode on DPU:"))
    cells.append(nbf.v4.new_code_cell("[DPU] sudo -i"))

    cells.append(nbf.v4.new_markdown_cell("#### 2.11 - Check BFB version:"))
    cells.append(nbf.v4.new_code_cell("[DPU] sudo bfver"))

    # Save
    nb['cells'] = cells
    with open(output_path, 'w') as f:
        nbf.write(nb, f)

    print(f"Notebook generated successfully at: {output_path}")

if __name__ == "__main__":
    generate_notebook()
