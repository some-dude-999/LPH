import csv
import os

# Change to SpanishWords directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.join(script_dir, '..'))

INPUT_FILE = 'SpanishWordsOverview.csv'
OUTPUT_FILE = 'SpanishWordsOverview.csv' # Overwrite in place

print(f"Migrating columns in {INPUT_FILE}...")

rows = []
with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    
    # Verify old columns exist
    if 'auto_word_count' not in reader.fieldnames:
        print("Error: 'auto_word_count' column not found. Migration might have already run.")
        exit(1)

    for row in reader:
        # Extract existing data
        pack_num = row['Pack_Number']
        title = row['Pack_Title']
        act = row['Difficulty_Act']
        words_str = row['Spanish_Words']
        manual_base = int(row['manual_base_word_count'])
        
        # Calculate new values
        # Parse array to get actual count
        start = words_str.find('[')
        end = words_str.find(']')
        words_list = words_str[start+1:end].split(',')
        # Filter empty strings in case of empty array
        words_list = [w for w in words_list if w.strip()]
        
        actual_count = len(words_list)
        expected_count = manual_base * 3
        
        # Create new row structure
        new_row = {
            'Pack_Number': pack_num,
            'Pack_Title': title,
            'Difficulty_Act': act,
            'Spanish_Words': words_str,
            'manual_base_word_count': manual_base,
            'total_words_expected': expected_count,
            'total_words_actual': actual_count
        }
        rows.append(new_row)

# Define new fieldnames
fieldnames = [
    'Pack_Number', 
    'Pack_Title', 
    'Difficulty_Act', 
    'Spanish_Words', 
    'manual_base_word_count', 
    'total_words_expected', 
    'total_words_actual'
]

# Write back to CSV
with open(OUTPUT_FILE, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print("Migration complete!")
print(f"Updated {len(rows)} rows.")
print(f"New columns: {', '.join(fieldnames)}")
