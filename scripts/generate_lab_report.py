#!/usr/bin/env python3
"""
Generate HTML lab access report for NVIDIA AI Infrastructure training.

Usage:
    python generate_lab_report.py [--password PASSWORD] [--output FILE]

The script:
1. Reads student list from students.csv
2. Fetches running brev instances and their IPs
3. Matches students to instances
4. Generates an HTML report from the template
"""

import argparse
import csv
import subprocess
import sys
from datetime import datetime
from pathlib import Path


SCRIPT_DIR = Path(__file__).parent
TEMPLATE_PATH = SCRIPT_DIR / "templates" / "lab_report.html"
STUDENTS_CSV = SCRIPT_DIR / "students.csv"
DEFAULT_OUTPUT = SCRIPT_DIR.parent / "reports" / "lab_access_report.html"
DEFAULT_PASSWORD = "Ac15T4BOoEs3@gg0Eo1Lz9"
JUPYTER_PORT = 8888


def run_cmd(cmd: list[str]) -> str:
    """Run a command and return stdout."""
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout


def get_brev_instances() -> dict[str, dict]:
    """
    Get all running brev instances with their IPs.
    Returns dict of {instance_name: {ip, status, build}}
    """
    # Refresh SSH config
    print("Refreshing brev...")
    run_cmd(["brev", "refresh"])
    
    # Parse brev ls output
    output = run_cmd(["brev", "ls"])
    instances = {}
    
    for line in output.strip().split("\n"):
        # Skip header and info lines
        if not line.startswith(" lab---module-8"):
            continue
        
        parts = line.split()
        if len(parts) >= 4:
            name = parts[0]
            status = parts[1]
            build = parts[2]
            instances[name] = {
                "status": status,
                "build": build,
                "ip": None
            }
    
    # Get IPs from SSH config
    ssh_config = Path.home() / ".brev" / "ssh_config"
    if ssh_config.exists():
        current_host = None
        with open(ssh_config) as f:
            for line in f:
                line = line.strip()
                if line.startswith("Host ") and not line.endswith("-host"):
                    current_host = line.split()[1]
                elif line.startswith("Hostname ") and current_host:
                    ip = line.split()[1]
                    if current_host in instances:
                        instances[current_host]["ip"] = ip
                    current_host = None
    
    return instances


def load_students(csv_path: Path) -> list[dict]:
    """Load students from CSV file."""
    students = []
    with open(csv_path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            students.append({
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "email": row["email"],
                "full_name": f"{row['first_name']} {row['last_name']}"
            })
    return students


def match_students_to_instances(students: list[dict], instances: dict) -> list[dict]:
    """
    Match students to instances.
    Sorts both lists and pairs them in order.
    """
    sorted_students = sorted(students, key=lambda s: s["full_name"])
    sorted_instances = sorted(instances.items())
    
    assignments = []
    for i, student in enumerate(sorted_students):
        if i < len(sorted_instances):
            instance_name, instance_data = sorted_instances[i]
            ip = instance_data.get("ip")
            build = instance_data.get("build", "UNKNOWN")
            
            if ip and build == "COMPLETED":
                lab_link = f"http://{ip}:{JUPYTER_PORT}"
                status = "ready"
            elif ip:
                lab_link = f"http://{ip}:{JUPYTER_PORT}"
                status = "building"
            else:
                lab_link = None
                status = "error"
        else:
            lab_link = None
            status = "error"
        
        assignments.append({
            **student,
            "lab_link": lab_link,
            "status": status
        })
    
    return assignments


def generate_table_rows(assignments: list[dict]) -> str:
    """Generate HTML table rows."""
    rows = []
    for a in sorted(assignments, key=lambda x: x["full_name"]):
        if a["lab_link"]:
            status_class = f"status-{a['status']}"
            link_html = f'<a href="{a["lab_link"]}" target="_blank" class="{status_class}">{a["lab_link"]}</a>'
        else:
            link_html = '<span class="status-error">No instance assigned</span>'
        
        rows.append(f"""                    <tr>
                        <td>{a["full_name"]}</td>
                        <td>{a["email"]}</td>
                        <td>{link_html}</td>
                    </tr>""")
    
    return "\n".join(rows)


def generate_report(template: str, password: str, assignments: list[dict]) -> str:
    """Generate the HTML report from template."""
    table_rows = generate_table_rows(assignments)
    current_date = datetime.now().strftime("%B %Y")
    
    html = template.replace("{{DATE}}", current_date)
    html = html.replace("{{PASSWORD}}", password)
    html = html.replace("{{TABLE_ROWS}}", table_rows)
    
    return html


def main():
    parser = argparse.ArgumentParser(
        description="Generate lab access report for NVIDIA AI Infrastructure training"
    )
    parser.add_argument(
        "--password", "-p",
        default=DEFAULT_PASSWORD,
        help=f"Jupyter notebook password (default: {DEFAULT_PASSWORD})"
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"Output HTML file (default: {DEFAULT_OUTPUT})"
    )
    parser.add_argument(
        "--students", "-s",
        type=Path,
        default=STUDENTS_CSV,
        help=f"Students CSV file (default: {STUDENTS_CSV})"
    )
    args = parser.parse_args()
    
    # Validate inputs
    if not TEMPLATE_PATH.exists():
        print(f"Error: Template not found at {TEMPLATE_PATH}")
        sys.exit(1)
    
    if not args.students.exists():
        print(f"Error: Students CSV not found at {args.students}")
        sys.exit(1)
    
    # Load template
    template = TEMPLATE_PATH.read_text()
    
    # Load students
    print(f"Loading students from {args.students}...")
    students = load_students(args.students)
    print(f"  Found {len(students)} students")
    
    # Get brev instances
    print("Fetching brev instances...")
    instances = get_brev_instances()
    print(f"  Found {len(instances)} running instances")
    
    # Match students to instances
    assignments = match_students_to_instances(students, instances)
    
    ready_count = sum(1 for a in assignments if a["status"] == "ready")
    building_count = sum(1 for a in assignments if a["status"] == "building")
    error_count = sum(1 for a in assignments if a["status"] == "error")
    
    print(f"\nAssignment summary:")
    print(f"  Ready: {ready_count}")
    print(f"  Building: {building_count}")
    print(f"  Error/Unassigned: {error_count}")
    
    # Generate report
    html = generate_report(template, args.password, assignments)
    
    # Write output
    args.output.write_text(html)
    print(f"\nReport generated: {args.output}")
    print(f"Open in browser: file://{args.output.absolute()}")


if __name__ == "__main__":
    main()
