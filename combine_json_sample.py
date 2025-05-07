import json
import re

def extract_id_number(id_str):
    """Extract the numeric part from an ID string like 'EN123' or 'HE123'"""
    # Remove 'EN' or 'HE' prefix and convert to integer
    if id_str.startswith('EN'):
        return int(id_str[2:])
    elif id_str.startswith('HE'):
        return int(id_str[2:])
    return None

def combine_json_files_sample(english_file, hebrew_file, output_file, sample_size=5):
    # Read the English file
    with open(english_file, 'r', encoding='utf-8') as f:
        english_content = f.read()
    
    # Read the Hebrew file
    with open(hebrew_file, 'r', encoding='utf-8') as f:
        hebrew_content = f.read()
    
    # Fix the JSON format (add surrounding array and fix missing commas)
    english_content = '[' + english_content.replace('}\n  {', '},\n  {') + ']'
    hebrew_content = '[' + hebrew_content.replace('}\n  {', '},\n  {') + ']'
    
    try:
        # Parse the JSON
        english_data = json.loads(english_content)
        hebrew_data = json.loads(hebrew_content)
        
        print(f"Successfully parsed JSON. English entries: {len(english_data)}, Hebrew entries: {len(hebrew_data)}")
        
        # Print a few sample IDs to verify
        print("Sample English IDs:", [item.get('id', 'No ID') for item in english_data[:3]])
        print("Sample Hebrew IDs:", [item.get('id', 'No ID') for item in hebrew_data[:3]])
        
        # Create dictionaries for easier lookup
        english_dict = {}
        hebrew_dict = {}
        
        for item in english_data:
            if 'id' in item:
                num = extract_id_number(item['id'])
                if num is not None:
                    english_dict[num] = item
        
        for item in hebrew_data:
            if 'id' in item:
                num = extract_id_number(item['id'])
                if num is not None:
                    hebrew_dict[num] = item
        
        print(f"Extracted ID numbers - English: {len(english_dict)}, Hebrew: {len(hebrew_dict)}")
    
        # Get common IDs that exist in both files
        common_ids = sorted(set(english_dict.keys()) & set(hebrew_dict.keys()))
        print(f"Common IDs found: {len(common_ids)}")
        
        if len(common_ids) > 0:
            print("First few common IDs:", common_ids[:5])
        
        # Limit to sample size
        sample_ids = common_ids[:sample_size]
        
        # Create combined data with pairs
        combined_data = []
        
        for id_num in sample_ids:
            hebrew_item = hebrew_dict.get(id_num, {})
            english_item = english_dict.get(id_num, {})
            
            # Add the pair as a single entry
            combined_item = {
                "id": str(id_num),
                "hebrew": hebrew_item.get('text', ''),
                "english": english_item.get('text', '')
            }
            
            combined_data.append(combined_item)
        
        # Write the combined data to the output file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(combined_data, f, ensure_ascii=False, indent=2)
        
        print(f"Sample combined data written to {output_file}")
        print(f"Sample size: {len(combined_data)} paragraph pairs")
    
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        print("First 100 characters of English content:", english_content[:100])
        print("First 100 characters of Hebrew content:", hebrew_content[:100])

if __name__ == "__main__":
    english_file = "translated/divreyyoelpesach_processed_english.json"
    hebrew_file = "translated/divreyyoelpesach_processed_hebrew.json"
    output_file = "translated/divreyyoelpesach_sample_combined.json"
    
    combine_json_files_sample(english_file, hebrew_file, output_file, sample_size=5)
