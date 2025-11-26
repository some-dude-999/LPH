#!/usr/bin/env python3
"""
Script to fix Spanish base words in SpanishWordsOverview.csv
"""

import csv
import re

INPUT_FILE = 'SpanishWords/SpanishWordsOverview.csv'
OUTPUT_FILE = 'SpanishWords/SpanishWordsOverview.csv'

def parse_word_array(array_str):
    """Parse a bracketed, comma-separated word array."""
    if not array_str or array_str == '[]':
        return []
    # Remove brackets and split by comma
    content = array_str.strip()[1:-1]
    if not content:
        return []
    # Split by comma, handling potential edge cases
    words = [w.strip() for w in content.split(',')]
    return words

def format_word_array(words):
    """Format words back to bracketed array string."""
    return '[' + ','.join(words) + ']'

def main():
    # Read the CSV
    rows = []
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for row in reader:
            rows.append(row)

    changes_made = []

    # Fix each pack based on pack number
    for row in rows:
        pack_num = int(row['Pack_Number'])
        pack_title = row['Pack_Title']
        base_words = parse_word_array(row['Spanish_Base_Words'])
        original_base_words = base_words.copy()

        # Pack 13: Family Members - remove "mi" prefixes from standalone words
        if pack_num == 13:
            new_base_words = []
            for word in base_words:
                # Remove "mi " prefix from family words that shouldn't have it
                if word.startswith('mi ') and word not in ['mi hija', 'mi hermano', 'mi hermana', 'mi tío', 'mi tía', 'mi primo', 'mi prima', 'mi esposo', 'mi esposa']:
                    new_base_words.append(word)
                elif word == 'mi hija':
                    new_base_words.append('hija')
                elif word == 'mi hermano':
                    new_base_words.append('hermano')
                elif word == 'mi hermana':
                    new_base_words.append('hermana')
                elif word == 'mi tío':
                    new_base_words.append('tío')
                elif word == 'mi tía':
                    new_base_words.append('tía')
                elif word == 'mi primo':
                    new_base_words.append('primo')
                elif word == 'mi prima':
                    new_base_words.append('prima')
                elif word == 'mi esposo':
                    new_base_words.append('esposo')
                elif word == 'mi esposa':
                    new_base_words.append('esposa')
                else:
                    new_base_words.append(word)
            base_words = new_base_words

        # Pack 21: Going Places - clean up to focus on the verb forms, not full phrases
        if pack_num == 21:
            base_words = ['voy', 'vas', 'va', 'vamos', 'vais', 'van', 'ir', 'ir a', 'ir de', 'ir al']

        # Pack 51: Names & Calling - fix "llamo por teléfono" to cleaner forms
        if pack_num == 51:
            base_words = ['me llamo', 'te llamas', 'se llama', 'nos llamamos', 'os llamáis', 'se llaman', 'llamar', 'llamar a', 'llamada', 'nombre']

        # Pack 74: Wearing & Carrying - fix to clean verb forms
        if pack_num == 74:
            base_words = ['llevo', 'llevas', 'lleva', 'llevamos', 'lleváis', 'llevan', 'llevar', 'traer', 'puesto', 'usar']

        # Pack 81: Banking - fix "la tarjeta de débito"
        if pack_num == 81:
            new_base_words = []
            for word in base_words:
                if word == 'la tarjeta de débito':
                    new_base_words.append('tarjeta de débito')
                else:
                    new_base_words.append(word)
            base_words = new_base_words

        # Pack 90: Sending - fix to clean verb forms
        if pack_num == 90:
            base_words = ['envío', 'envías', 'envía', 'enviamos', 'enviáis', 'envían', 'enviar', 'enviar mensajes', 'mandar', 'remitir']

        # Pack 92: Opening - fix "abren tiendas" to cleaner form
        if pack_num == 92:
            new_base_words = []
            for word in base_words:
                if word == 'abren tiendas':
                    new_base_words.append('abren')
                else:
                    new_base_words.append(word)
            base_words = new_base_words

        # Pack 93: Closing - fix "cierran tiendas" to cleaner form
        if pack_num == 93:
            new_base_words = []
            for word in base_words:
                if word == 'cierran tiendas':
                    new_base_words.append('cierran')
                else:
                    new_base_words.append(word)
            base_words = new_base_words

        # Pack 95: Relationships - fix "mi mejor amigo/amiga"
        if pack_num == 95:
            new_base_words = []
            for word in base_words:
                if word == 'mi mejor amigo':
                    new_base_words.append('mejor amigo')
                elif word == 'mi mejor amiga':
                    new_base_words.append('mejor amiga')
                else:
                    new_base_words.append(word)
            base_words = new_base_words

        # Pack 97: Writing - fix to clean verb forms
        if pack_num == 97:
            base_words = ['escribo', 'escribes', 'escribe', 'escribimos', 'escribís', 'escriben', 'escribir', 'escribir a mano', 'escritura', 'redactar']

        # Pack 99: Showing - fix to clean verb forms
        if pack_num == 99:
            base_words = ['muestro', 'muestras', 'muestra', 'mostramos', 'mostráis', 'muestran', 'mostrar', 'enseñar', 'demostrar', 'presentar']

        # Pack 110: Media & News - fix "la periodista escribe"
        if pack_num == 110:
            new_base_words = []
            for word in base_words:
                if word == 'la periodista escribe':
                    new_base_words.append('periodista')
                else:
                    new_base_words.append(word)
            base_words = new_base_words

        # Pack 116: Art & Culture - fix "la artista talentosa"
        if pack_num == 116:
            new_base_words = []
            for word in base_words:
                if word == 'la artista talentosa':
                    new_base_words.append('artista')
                else:
                    new_base_words.append(word)
            base_words = new_base_words

        # Pack 119: Religion & Faith - fix "el dios griego" to just "dios"
        if pack_num == 119:
            new_base_words = []
            for word in base_words:
                if word == 'el dios griego':
                    new_base_words.append('dios')
                else:
                    new_base_words.append(word)
            base_words = new_base_words

        # Pack 132: Touching & Playing Music - fix "toca la" to "toca"
        if pack_num == 132:
            new_base_words = []
            for word in base_words:
                if word == 'toca la':
                    new_base_words.append('toca')
                else:
                    new_base_words.append(word)
            base_words = new_base_words

        # Pack 143: Space & Universe - fix "la astronauta valiente"
        if pack_num == 143:
            new_base_words = []
            for word in base_words:
                if word == 'la astronauta valiente':
                    new_base_words.append('astronauta')
                else:
                    new_base_words.append(word)
            base_words = new_base_words

        # Pack 149: Military Terms - fix gendered examples
        if pack_num == 149:
            new_base_words = []
            for word in base_words:
                if word == 'la soldado profesional':
                    new_base_words.append('soldado')
                elif word == 'la oficial médica':
                    new_base_words.append('oficial')
                elif word == 'la general doctora':
                    new_base_words.append('general')
                else:
                    new_base_words.append(word)
            base_words = new_base_words

        # Pack 152: Literature & Books - fix "la poeta laureada"
        if pack_num == 152:
            new_base_words = []
            for word in base_words:
                if word == 'la poeta laureada':
                    new_base_words.append('poeta')
                else:
                    new_base_words.append(word)
            base_words = new_base_words

        # Pack 167: Fashion & Style - fix "la modelo famosa"
        if pack_num == 167:
            new_base_words = []
            for word in base_words:
                if word == 'la modelo famosa':
                    new_base_words.append('modelo')
                else:
                    new_base_words.append(word)
            base_words = new_base_words

        # Pack 173: Journalism Terms - fix "la periodista investigadora"
        if pack_num == 173:
            new_base_words = []
            for word in base_words:
                if word == 'la periodista investigadora':
                    new_base_words.append('periodista')
                else:
                    new_base_words.append(word)
            base_words = new_base_words

        # Pack 185: Tourism Terms - fix "la turista aventurera"
        if pack_num == 185:
            new_base_words = []
            for word in base_words:
                if word == 'la turista aventurera':
                    new_base_words.append('turista')
                else:
                    new_base_words.append(word)
            base_words = new_base_words

        # Pack 191: Economics Terms - fix "la economista brillante"
        if pack_num == 191:
            new_base_words = []
            for word in base_words:
                if word == 'la economista brillante':
                    new_base_words.append('economista')
                else:
                    new_base_words.append(word)
            base_words = new_base_words

        # Pack 194: Retail & Sales - fix "la comerciante exitosa"
        if pack_num == 194:
            new_base_words = []
            for word in base_words:
                if word == 'la comerciante exitosa':
                    new_base_words.append('comerciante')
                else:
                    new_base_words.append(word)
            base_words = new_base_words

        # Pack 203: Aviation Terms - fix "la piloto profesional"
        if pack_num == 203:
            new_base_words = []
            for word in base_words:
                if word == 'la piloto profesional':
                    new_base_words.append('piloto')
                else:
                    new_base_words.append(word)
            base_words = new_base_words

        # Pack 146: Chemistry Terms - fix "la química brillante"
        if pack_num == 146:
            new_base_words = []
            for word in base_words:
                if word == 'la química brillante':
                    new_base_words.append('química')
                else:
                    new_base_words.append(word)
            base_words = new_base_words

        # Remove duplicates while preserving order
        seen = set()
        unique_base_words = []
        for word in base_words:
            if word not in seen:
                seen.add(word)
                unique_base_words.append(word)
        base_words = unique_base_words

        # Track changes
        if base_words != original_base_words:
            changes_made.append({
                'pack': pack_num,
                'title': pack_title,
                'before': original_base_words,
                'after': base_words
            })
            row['Spanish_Base_Words'] = format_word_array(base_words)

    # Write back the CSV
    with open(OUTPUT_FILE, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    # Report changes
    print(f"\n{'='*60}")
    print("CHANGES MADE TO SPANISH BASE WORDS")
    print(f"{'='*60}\n")

    for change in changes_made:
        print(f"Pack {change['pack']}: {change['title']}")
        print(f"  Before: {change['before'][:5]}..." if len(change['before']) > 5 else f"  Before: {change['before']}")
        print(f"  After:  {change['after'][:5]}..." if len(change['after']) > 5 else f"  After:  {change['after']}")
        print()

    print(f"Total packs modified: {len(changes_made)}")

if __name__ == '__main__':
    main()
