import json
import re

def parse_text_to_cells(text_content):
    cells = []
    
    # Remove page headers/footers (simplified regex)
    # Remove lines that just look like page numbers or common footer text
    clean_lines = []
    for line in text_content.splitlines():
        if re.match(r'^\s*\d+\s*$', line): # Just a number (page number)
            continue
        if "Revision #" in line or "Base Command Manager Administration" in line:
            continue
        if line.strip() == "And": # Artifact from page 1
            continue
        if line.strip() == "LAB GUIDE":
             continue
        clean_lines.append(line)
        
    full_text = "\n".join(clean_lines)
    
    # Split into sections based on "Practice X:" or "Task X:" or "Prerequisites"
    # We want to capture the title as part of the section.
    # Using regex split with capturing group to keep the delimiter.
    
    # Regex for section headers
    section_pattern = r'(^Practice \d+:.*?$|^Task \d+:.*?$|^Prerequisites.*?$|^Launchpad Lab Topology.*?$|^Overview.*?$)'
    
    parts = re.split(section_pattern, full_text, flags=re.MULTILINE)
    
    current_content = []
    current_header = ""
    
    for part in parts:
        if not part.strip():
            continue
            
        if re.match(section_pattern, part.strip(), re.MULTILINE):
            # This is a header. If we have previous content, save it.
            if current_header or current_content:
                cells.append(create_cell(current_header, current_content))
            current_header = part.strip()
            current_content = []
        else:
            current_content.append(part)
            
    # Add the last section
    if current_header or current_content:
        cells.append(create_cell(current_header, current_content))
        
    return cells

def create_cell(header, content_lines):
    content_text = "".join(content_lines)
    
    # Basic cleanup
    content_text = content_text.replace('\x0c', '') # Remove form feeds
    
    # formatting the header
    md_header = ""
    if header:
        if header.startswith("Practice"):
            md_header = f"## {header}\n\n"
        elif header.startswith("Task"):
            md_header = f"### {header}\n\n"
        else:
            md_header = f"## {header}\n\n"
            
    # Attempt to detect code blocks
    # Heuristic: indented lines or lines with prompts
    # This is tricky to do perfectly with regex, so we'll do a line-by-line pass
    
    final_lines = [md_header]
    
    in_code_block = False
    code_lines = []
    
    lines = content_text.splitlines()
    for i, line in enumerate(lines):
        is_code = False
        stripped = line.strip()
        
        # Heuristics for code/output
        if line.startswith("     ") and stripped: # Indented (5 spaces from layout)
            is_code = True
        elif stripped.startswith("root@") or stripped.startswith("[bcm]") or stripped.startswith("./"):
            is_code = True
        elif stripped in ["list", "device", "cmsh", "exit", "quit"]: # Common single commands seen in text
             is_code = True
        
        # Check previous line for "Example output:"
        if i > 0 and "Example output:" in lines[i-1]:
            is_code = True
            
        if is_code:
            if not in_code_block:
                final_lines.append("```bash\n")
                in_code_block = True
            final_lines.append(line + "\n") # Keep indentation
        else:
            if in_code_block:
                final_lines.append("```\n")
                in_code_block = False
            final_lines.append(line + "\n")
            
    if in_code_block:
        final_lines.append("```\n")
        
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": final_lines
    }

def main():
    # Read the text content
    with open('bcm11_content.txt', 'r') as f:
        text_content = f.read()
        
    new_cells = parse_text_to_cells(text_content)
    
    # Load existing notebook
    with open('Lab 4 - BCM 11.ipynb', 'r') as f:
        notebook = json.load(f)
        
    # Append new cells
    notebook['cells'].extend(new_cells)
    
    # Save
    with open('Lab 4 - BCM 11.ipynb', 'w') as f:
        json.dump(notebook, f, indent=1)
        
    print(f"Appended {len(new_cells)} cells to the notebook.")

if __name__ == "__main__":
    main()

