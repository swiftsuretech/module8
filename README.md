# Module 8: NVIDIA AI Infrastructure Labs

This repository contains Jupyter notebook labs for NVIDIA AI Infrastructure training.

## Lab Notebooks

- **Lab 1 - Driver Installation.ipynb** - Install NVIDIA drivers and use nvidia-smi
- **Lab 2 - Installing and Running AI Software.ipynb** - Install Container Toolkit and run PyTorch training
- **Lab 3 - DPU Initial Configuration.ipynb** - Configure BlueField DPU (simulated)

## Updating Labs

### Prerequisites
- Git access to this repository
- Brev CLI installed and authenticated (`brev login`)

### Making Changes

1. Clone the repository:
   ```bash
   git clone git@github.com:swiftsuretech/module8.git
   cd module8
   ```

2. Edit the Jupyter notebooks as needed

3. Commit and push changes:
   ```bash
   git add .
   git commit -m "Description of changes"
   git push
   ```

4. The changes will be available to students on next lab instance creation

---

## Generating Lab Access Report

The lab access report provides students with their assigned Jupyter notebook URLs and password.

### Prerequisites
- Brev CLI installed and authenticated
- Lab instances running (`brev ls` to verify)
- Python 3.8+

### Update Student List

Edit `scripts/students.csv` with the current cohort:

```csv
first_name,last_name,email
John,Smith,jsmith@example.com
Jane,Doe,jdoe@example.com
```

### Generate Report

```bash
python scripts/generate_lab_report.py
```

The report is generated at `reports/lab_access_report.html`.

### Options

```bash
# Custom password
python scripts/generate_lab_report.py -p "YourPassword123"

# Custom output location
python scripts/generate_lab_report.py -o /path/to/report.html

# Custom student list
python scripts/generate_lab_report.py -s /path/to/students.csv
```

### Workflow

1. Update `scripts/students.csv` with student names and emails
2. Ensure lab instances are running: `brev ls`
3. Refresh brev SSH config: `brev refresh`
4. Generate report: `python scripts/generate_lab_report.py`
5. Open `reports/lab_access_report.html` in browser
6. Print to PDF or share directly with students

---

## Directory Structure

```
module8/
├── Lab 1 - Driver Installation.ipynb
├── Lab 2 - Installing and Running AI Software.ipynb
├── Lab 3 - DPU Initial Configuration.ipynb
├── README.md
├── guides/                    # PDF lab guides
├── materials/                 # Training materials (train.py, test.py, etc.)
├── reports/
│   └── lab_access_report.html # Generated student access report
└── scripts/
    ├── generate_lab_report.py # Report generator
    ├── students.csv           # Student list (update per cohort)
    ├── templates/
    │   └── lab_report.html    # HTML template
    ├── fix-lab-env.sh         # Driver initialization script
    ├── timer.py               # GPU/CPU timing helper
    └── suspend_module_8_labs.sh # Stop all lab instances
```

## Managing Lab Instances

### List running instances
```bash
brev ls
```

### Stop all module 8 instances
```bash
./scripts/suspend_module_8_labs.sh
```

### Refresh SSH config (required after instance creation)
```bash
brev refresh
```
