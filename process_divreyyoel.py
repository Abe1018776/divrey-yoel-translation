"""
Script to process divreyyoelpesach.txt:
1. Remove all standalone numbers (like 11, 22, 33, 44)
2. Keep only numbers that are part of \"DVAR TORAH X\" patterns
"""

import re

def process_file(input_file, output_file):
    processed_lines = 0
    removed_numbers = 0
    
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            original_line = line
            
            # First, handle DVAR TORAH pattern
            dvar_torah_match = re.search(r'(DVAR TORAH \d+)', line, re.IGNORECASE)
            
            if dvar_torah_match:
                # Extract the DVAR TORAH pattern
                dvar_torah = dvar_torah_match.group(1)
                
                # Remove the DVAR TORAH pattern from the line temporarily
                line_without_dvar = line.replace(dvar_torah, "")
                
                # Remove all digits from the remainder of the line
                line_without_dvar_and_numbers = re.sub(r'\d+', '', line_without_dvar)
                
                # Put back the DVAR TORAH pattern
                line = dvar_torah + line_without_dvar_and_numbers
            else:
                # For lines without DVAR TORAH, remove all digits
                line = re.sub(r'\d+', '', line)
            
            # Count removed numbers
            if original_line != line:
                removed_numbers += len(re.findall(r'\d+', original_line)) - len(re.findall(r'\d+', line))
            
            outfile.write(line)
            processed_lines += 1
    
    return processed_lines, removed_numbers

if __name__ == "__main__":
    input_file = "divreyyoelpesach.txt"
    output_file = "divreyyoelpesach_processed.txt"
    
    total_lines, total_numbers_removed = process_file(input_file, output_file)
    print(f"Processing complete. Processed {total_lines} lines.")
    print(f"Removed {total_numbers_removed} standalone numbers.")
    print(f"Preserved only numbers in 'DVAR TORAH X' patterns.")
    print(f"Processed file saved as: {output_file}")
