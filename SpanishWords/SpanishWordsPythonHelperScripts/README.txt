SPANISH WORDS PYTHON HELPER SCRIPTS
====================================

This folder contains utility scripts for maintaining and validating
the Spanish Words translation packs.

SCRIPTS:
--------

1. check_divisible_by_3.py
   - Purpose: Validates that all word pack arrays have counts divisible by 3
   - Reason: Each base word should have exactly 3 example instances
   - Usage: python3 check_divisible_by_3.py
   - Output: Lists any packs with word counts not divisible by 3

2. examine_pack_structure.py  
   - Purpose: Displays the structure of a specific pack with grouping markers
   - Reason: Helps identify which base words are missing examples or have too many
   - Usage: python3 examine_pack_structure.py <pack_number>
   - Example: python3 examine_pack_structure.py 208
   - Output: Shows all words with markers every 3rd word

3. verify_word_counts.py
   - Purpose: Verifies Word_Count column matches actual array lengths
   - Reason: Ensures overview CSV metadata is accurate
   - Usage: python3 verify_word_counts.py
   - Output: Lists any mismatches between stated and actual counts

4. verify_csv_matches_overview.py
   - Purpose: Verifies SpanishWords*.csv files match their overview arrays
   - Reason: Ensures CSV files contain the exact words specified in overview
   - Usage: python3 verify_csv_matches_overview.py
   - Output: Lists any packs where CSV doesn't match overview

VALIDATION RULES:
-----------------

1. Each base word must have exactly 3 example instances
2. Word_Count must equal the actual number of words in the array
3. Word_Count must be divisible by 3
4. CSV files must contain exact words from overview arrays
5. All translations must follow format rules (see 000 SPANISH TRANSLATION FORMAT RULES.txt)

MAINTENANCE:
------------

Run all scripts after making changes to ensure data integrity.
