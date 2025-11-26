#!/usr/bin/env python3
"""
Fix duplicate base words in EnglishWordsOverview.csv

Strategy:
1. For each duplicate word, determine which pack it best belongs to
2. Remove it from other packs and replace with new relevant words
3. Ensure each pack maintains 20 words
"""

import csv
import re
from collections import defaultdict

# Define which pack each duplicate word should stay in
# Format: 'word': pack_number_to_keep_it_in
WORD_ASSIGNMENTS = {
    # Words appearing in 4 packs
    'reason': 42,  # More Common Nouns - most basic usage
    'market': 43,  # Places in Town - physical place meaning
    'conflict': 128,  # International Relations - most relevant

    # Words appearing in 3 packs
    'sorry': 1,  # Greetings & Basics - most common usage
    'no': 1,  # Greetings & Basics - basic response
    'neither': 4,  # Articles & Determiners
    'fall': 11,  # Months & Seasons - the season
    'season': 11,  # Months & Seasons
    'exit': 19,  # Essential Verbs: Go & Come
    'ask': 20,  # Essential Verbs: Common Actions
    'answer': 22,  # Essential Verbs: Communication
    'spend': 23,  # Irregular Verbs 1 (spend/spent)
    'fly': 24,  # Irregular Verbs 2 (fly/flew)
    'rise': 25,  # Irregular Verbs 3 (rise/rose)
    'right': 27,  # Essential Adjectives 1 - basic meaning
    'fine': 29,  # Basic Emotions - "I'm fine"
    'without': 37,  # Prepositions of Time & Other
    'never': 38,  # Time Expressions
    'yet': 38,  # Time Expressions
    'unless': 78,  # Conjunctions
    'fact': 42,  # More Common Nouns
    'pharmacy': 43,  # Places in Town
    'pretty': 44,  # Casual & Informal English - "pretty good"
    'cabinet': 48,  # Furniture
    'lawyer': 56,  # Jobs 1
    'border': 60,  # Geography
    'bill': 69,  # Money & Banking
    'budget': 69,  # Money & Banking
    'deposit': 69,  # Money & Banking
    'interest': 69,  # Money & Banking
    'prescription': 70,  # Health
    'emergency': 70,  # Health
    'apologize': 74,  # Communication Verbs
    'refuse': 74,  # Communication Verbs
    'assume': 75,  # Mental Verbs
    'therefore': 79,  # Connectors
    'approve': 86,  # Workplace Actions
    'evaluate': 86,  # Workplace Actions
    'negotiate': 87,  # Business Communication
    'support': 89,  # Relationships
    'forgive': 89,  # Relationships
    'compromise': 90,  # Social Interactions
    'role': 98,  # Movies & TV
    'rights': 101,  # Basic Law & Rules
    'argument': 103,  # Opinions & Arguments
    'resolve': 104,  # Problems & Solutions
    'revenue': 113,  # Business Basics
    'demand': 113,  # Business Basics
    'hypothesis': 116,  # Science Basics
    'influence': 124,  # Abstract Concepts
    'mutual': 137,  # Academic Adjectives 2
    'settle': 138,  # Everyday Legal

    # Words appearing in 2 packs
    'pardon': 1,  # Greetings & Basics
    'one': 2,  # Numbers 1-20
    'second': 3,  # Numbers & Counting (ordinal)
    'once': 3,  # Numbers & Counting
    'half': 3,  # Numbers & Counting
    'double': 3,  # Numbers & Counting
    'some': 4,  # Articles & Determiners
    'enough': 5,  # Quantifiers
    'none': 5,  # Quantifiers
    'number': 5,  # Quantifiers
    'couple': 5,  # Quantifiers
    'majority': 5,  # Quantifiers
    'hold on': 8,  # Common Expressions
    'green': 9,  # Colors
    'orange': 9,  # Colors
    'may': 11,  # Months & Seasons (the month)
    'date': 11,  # Months & Seasons
    'her': 14,  # Personal Pronouns
    'who': 16,  # Question Words
    'whom': 16,  # Question Words
    'whose': 16,  # Question Words
    'which': 16,  # Question Words
    'what': 16,  # Question Words
    'whatever': 15,  # Possessives & Relatives
    'when': 16,  # Question Words
    'need': 20,  # Essential Verbs: Common Actions
    'going': 19,  # Essential Verbs: Go & Come
    'rather': 17,  # Modal Verbs
    'likely': 17,  # Modal Verbs
    'leave': 19,  # Essential Verbs: Go & Come
    'left': 46,  # Directions
    'arrive': 19,  # Essential Verbs: Go & Come
    'return': 19,  # Essential Verbs: Go & Come
    'enter': 19,  # Essential Verbs: Go & Come
    'know': 20,  # Essential Verbs: Common Actions
    'think': 20,  # Essential Verbs: Common Actions
    'like': 20,  # Essential Verbs: Common Actions
    'walk': 21,  # Essential Verbs: Daily Actions
    'run': 21,  # Essential Verbs: Daily Actions
    'ran': 21,  # Essential Verbs: Daily Actions
    'sit': 21,  # Essential Verbs: Daily Actions
    'sat': 21,  # Essential Verbs: Daily Actions
    'open': 21,  # Essential Verbs: Daily Actions
    'speak': 22,  # Essential Verbs: Communication
    'spoke': 22,  # Essential Verbs: Communication
    'show': 22,  # Essential Verbs: Communication
    'buy': 23,  # Irregular Verbs 1
    'sell': 23,  # Irregular Verbs 1
    'pay': 23,  # Irregular Verbs 1
    'drive': 23,  # Irregular Verbs 1
    'fight': 24,  # Irregular Verbs 2
    'find': 24,  # Irregular Verbs 2
    'forget': 24,  # Irregular Verbs 2
    'lose': 25,  # Irregular Verbs 3
    'lost': 46,  # Directions - "I'm lost"
    'throw': 26,  # Irregular Verbs 4
    'wear': 26,  # Irregular Verbs 4
    'win': 26,  # Irregular Verbs 4
    'understand': 26,  # Irregular Verbs 4
    'cold': 27,  # Essential Adjectives 1
    'fast': 27,  # Essential Adjectives 1
    'hard': 27,  # Essential Adjectives 1
    'clean': 28,  # Essential Adjectives 2
    'confused': 29,  # Basic Emotions
    'shy': 29,  # Basic Emotions
    'restaurant': 33,  # Drinks & Meals
    'menu': 33,  # Drinks & Meals
    'plate': 33,  # Drinks & Meals
    'cup': 33,  # Drinks & Meals
    'glass': 33,  # Drinks & Meals
    'bowl': 33,  # Drinks & Meals
    'fit': 34,  # Clothing
    'wind': 35,  # Weather
    'cool': 35,  # Weather
    'temperature': 35,  # Weather
    'degree': 35,  # Weather
    'dry': 35,  # Weather
    'next': 36,  # Prepositions of Place
    'before': 37,  # Prepositions of Time & Other
    'after': 37,  # Prepositions of Time & Other
    'until': 37,  # Prepositions of Time & Other
    'since': 37,  # Prepositions of Time & Other
    'across': 37,  # Prepositions of Time & Other
    'along': 37,  # Prepositions of Time & Other
    'toward': 37,  # Prepositions of Time & Other
    'still': 38,  # Time Expressions
    'just': 38,  # Time Expressions
    'then': 38,  # Time Expressions
    'finally': 38,  # Time Expressions
    'not': 39,  # Negatives & Limits
    'nothing': 39,  # Negatives & Limits
    'nobody': 39,  # Negatives & Limits
    'nowhere': 39,  # Negatives & Limits
    'train': 40,  # Basic Transportation
    'plane': 40,  # Basic Transportation
    'trip': 40,  # Basic Transportation
    'ticket': 40,  # Basic Transportation
    'airport': 40,  # Basic Transportation
    'station': 40,  # Basic Transportation
    'gas': 40,  # Basic Transportation
    'stuff': 41,  # Common Nouns
    'school': 41,  # Common Nouns
    'idea': 41,  # Common Nouns
    'group': 42,  # More Common Nouns
    'company': 42,  # More Common Nouns
    'question': 42,  # More Common Nouns
    'hospital': 43,  # Places in Town
    'library': 43,  # Places in Town
    'theater': 43,  # Places in Town
    'cafe': 43,  # Places in Town
    'gym': 43,  # Places in Town
    'hotel': 43,  # Places in Town
    'sure': 44,  # Casual & Informal English
    'well': 45,  # Filler Words & Reactions
    'anyway': 45,  # Filler Words & Reactions
    'actually': 45,  # Filler Words & Reactions
    'so': 45,  # Filler Words & Reactions
    'really': 45,  # Filler Words & Reactions
    'straight': 46,  # Directions
    'turn': 46,  # Directions
    'driver': 47,  # More Transportation
    'pilot': 47,  # More Transportation
    'flight': 47,  # More Transportation
    'travel': 47,  # More Transportation
    'desk': 48,  # Furniture
    'mirror': 48,  # Furniture
    'drawer': 48,  # Furniture
    'curtain': 48,  # Furniture
    'towel': 48,  # Furniture
    'microwave': 49,  # Kitchen Items
    'sink': 49,  # Kitchen Items
    'tissue': 50,  # Bathroom Items
    'organize': 51,  # Household Chores
    'fix': 51,  # Household Chores
    'replace': 51,  # Household Chores
    'onion': 52,  # More Food
    'garlic': 52,  # More Food
    'blender': 49,  # Kitchen Items
    'coach': 63,  # More Sports
    'athlete': 63,  # More Sports
    'compete': 63,  # More Sports
    'practice': 62,  # Sports
    'game': 62,  # Sports
    'score': 62,  # Sports
    'performance': 64,  # Entertainment
    'audience': 64,  # Entertainment
    'stage': 64,  # Entertainment
    'fan': 64,  # Entertainment
    'cost': 68,  # Shopping
    'price': 68,  # Shopping
    'discount': 68,  # Shopping
    'cheap': 68,  # Shopping
    'expensive': 68,  # Shopping
    'save': 69,  # Money & Banking
    'borrow': 69,  # Money & Banking
    'medicine': 70,  # Health
    'treatment': 70,  # Health
    'rest': 70,  # Health
    'injury': 70,  # Health
    'download': 71,  # Technology
    'upload': 71,  # Technology
    'search': 71,  # Technology
    'screen': 71,  # Technology
    'move': 72,  # Verbs of Motion
    'climb': 72,  # Verbs of Motion
    'jump': 72,  # Verbs of Motion
    'lift': 72,  # Verbs of Motion
    'push': 72,  # Verbs of Motion
    'pull': 72,  # Verbs of Motion
    'change': 73,  # Verbs of Change
    'become': 73,  # Verbs of Change
    'develop': 73,  # Verbs of Change
    'improve': 73,  # Verbs of Change
    'increase': 73,  # Verbs of Change
    'decrease': 73,  # Verbs of Change
    'reduce': 73,  # Verbs of Change
    'add': 73,  # Verbs of Change
    'remove': 73,  # Verbs of Change
    'create': 73,  # Verbs of Change
    'explain': 74,  # Communication Verbs
    'discuss': 74,  # Communication Verbs
    'agree': 74,  # Communication Verbs
    'disagree': 74,  # Communication Verbs
    'suggest': 74,  # Communication Verbs
    'complain': 74,  # Communication Verbs
    'promise': 74,  # Communication Verbs
    'invite': 74,  # Communication Verbs
    'accept': 74,  # Communication Verbs
    'introduce': 74,  # Communication Verbs
    'describe': 74,  # Communication Verbs
    'mention': 74,  # Communication Verbs
    'announce': 74,  # Communication Verbs
    'warn': 74,  # Communication Verbs
    'advise': 74,  # Communication Verbs
    'inform': 74,  # Communication Verbs
    'express': 74,  # Communication Verbs
    'convince': 74,  # Communication Verbs
    'believe': 75,  # Mental Verbs
    'remember': 75,  # Mental Verbs
    'realize': 75,  # Mental Verbs
    'recognize': 75,  # Mental Verbs
    'imagine': 75,  # Mental Verbs
    'wonder': 75,  # Mental Verbs
    'guess': 75,  # Mental Verbs
    'suppose': 75,  # Mental Verbs
    'expect': 75,  # Mental Verbs
    'hope': 75,  # Mental Verbs
    'wish': 75,  # Mental Verbs
    'doubt': 75,  # Mental Verbs
    'consider': 75,  # Mental Verbs
    'decide': 75,  # Mental Verbs
    'prefer': 75,  # Mental Verbs
    'quickly': 76,  # Adverbs of Manner
    'slowly': 76,  # Adverbs of Manner
    'carefully': 76,  # Adverbs of Manner
    'easily': 76,  # Adverbs of Manner
    'loudly': 76,  # Adverbs of Manner
    'quietly': 76,  # Adverbs of Manner
    'softly': 76,  # Adverbs of Manner
    'gently': 76,  # Adverbs of Manner
    'badly': 76,  # Adverbs of Manner
    'clearly': 76,  # Adverbs of Manner
    'simply': 76,  # Adverbs of Manner
    'directly': 76,  # Adverbs of Manner
    'properly': 76,  # Adverbs of Manner
    'perfectly': 76,  # Adverbs of Manner
    'correctly': 76,  # Adverbs of Manner
    'completely': 76,  # Adverbs of Manner
    'suddenly': 76,  # Adverbs of Manner
    'very': 77,  # Adverbs of Degree
    'quite': 77,  # Adverbs of Degree
    'fairly': 77,  # Adverbs of Degree
    'too': 77,  # Adverbs of Degree
    'extremely': 77,  # Adverbs of Degree
    'absolutely': 77,  # Adverbs of Degree
    'totally': 77,  # Adverbs of Degree
    'highly': 77,  # Adverbs of Degree
    'slightly': 77,  # Adverbs of Degree
    'somewhat': 77,  # Adverbs of Degree
    'almost': 77,  # Adverbs of Degree
    'nearly': 77,  # Adverbs of Degree
    'especially': 77,  # Adverbs of Degree
    'incredibly': 77,  # Adverbs of Degree
    'surprisingly': 77,  # Adverbs of Degree
    'relatively': 77,  # Adverbs of Degree
    'and': 78,  # Conjunctions
    'but': 78,  # Conjunctions
    'or': 78,  # Conjunctions
    'because': 78,  # Conjunctions
    'if': 78,  # Conjunctions
    'while': 78,  # Conjunctions
    'although': 78,  # Conjunctions
    'though': 78,  # Conjunctions
    'as': 78,  # Conjunctions
    'than': 78,  # Conjunctions
    'whether': 78,  # Conjunctions
    'whereas': 78,  # Conjunctions
    'however': 79,  # Connectors
    'also': 79,  # Connectors
    'besides': 79,  # Connectors
    'instead': 79,  # Connectors
    'otherwise': 79,  # Connectors
    'meanwhile': 79,  # Connectors
    'moreover': 79,  # Connectors
    'furthermore': 79,  # Connectors
    'nevertheless': 79,  # Connectors
    'indeed': 79,  # Connectors
    'likewise': 79,  # Connectors
    'similarly': 79,  # Connectors
    'vacation': 82,  # Travel
    'holiday': 82,  # Travel
    'tour': 82,  # Travel
    'destination': 82,  # Travel
    'passport': 82,  # Travel
    'visa': 82,  # Travel
    'luggage': 82,  # Travel
    'suitcase': 82,  # Travel
    'pack': 82,  # Travel
    'departure': 82,  # Travel (keep here, remove from Airport)
    'arrival': 82,  # Travel (keep here, remove from Airport)
    'customs': 82,  # Travel
    'tourist': 82,  # Travel
    'reservation': 82,  # Travel
    'baggage': 83,  # Airport & Flying
    'terminal': 83,  # Airport & Flying
    'boarding': 83,  # Airport & Flying
    'gate': 83,  # Airport & Flying
    'runway': 83,  # Airport & Flying
    'security': 83,  # Airport & Flying
    'delay': 83,  # Airport & Flying
    'cancel': 83,  # Airport & Flying
    'turbulence': 83,  # Airport & Flying
    'seatbelt': 83,  # Airport & Flying
    'overhead': 83,  # Airport & Flying
    'meeting': 85,  # Work & Office
    'report': 85,  # Work & Office
    'deadline': 85,  # Work & Office
    'project': 85,  # Work & Office
    'schedule': 85,  # Work & Office
    'salary': 85,  # Work & Office
    'interview': 85,  # Work & Office
    'resume': 85,  # Work & Office
    'career': 85,  # Work & Office
    'position': 85,  # Work & Office
    'hire': 86,  # Workplace Actions
    'fire': 86,  # Workplace Actions
    'resign': 86,  # Workplace Actions
    'retire': 86,  # Workplace Actions
    'apply': 86,  # Workplace Actions
    'manage': 86,  # Workplace Actions
    'coordinate': 86,  # Workplace Actions
    'assign': 86,  # Workplace Actions
    'delegate': 86,  # Workplace Actions
    'submit': 86,  # Workplace Actions
    'review': 86,  # Workplace Actions
    'complete': 86,  # Workplace Actions
    'achieve': 86,  # Workplace Actions
    'succeed': 86,  # Workplace Actions
    'fail': 86,  # Workplace Actions
    'promote': 86,  # Workplace Actions
    'trust': 89,  # Relationships
    'relationship': 89,  # Relationships
    'friendship': 89,  # Relationships
    'partner': 89,  # Relationships
    'boyfriend': 89,  # Relationships
    'girlfriend': 89,  # Relationships
    'single': 89,  # Relationships
    'married': 89,  # Relationships
    'divorced': 89,  # Relationships
    'engaged': 89,  # Relationships
    'wedding': 89,  # Relationships
    'anniversary': 89,  # Relationships
    'respect': 89,  # Relationships
    'commitment': 89,  # Relationships
    'conversation': 90,  # Social Interactions
    'chat': 90,  # Social Interactions
    'gossip': 90,  # Social Interactions
    'secret': 90,  # Social Interactions
    'betray': 90,  # Social Interactions
    'encourage': 90,  # Social Interactions
    'criticize': 90,  # Social Interactions
    'compliment': 90,  # Social Interactions
    'insult': 90,  # Social Interactions
    'reconcile': 90,  # Social Interactions
    'cooperate': 90,  # Social Interactions
    'ignore': 90,  # Social Interactions
    'interrupt': 90,  # Social Interactions
    'offend': 90,  # Social Interactions
    'defend': 90,  # Social Interactions
    'birth': 91,  # Life Events
    'childhood': 91,  # Life Events
    'teenager': 91,  # Life Events
    'adult': 91,  # Life Events
    'elderly': 91,  # Life Events
    'birthday': 91,  # Life Events
    'graduation': 91,  # Life Events
    'engagement': 91,  # Life Events
    'marriage': 91,  # Life Events
    'pregnancy': 91,  # Life Events
    'funeral': 91,  # Life Events
    'retirement': 91,  # Life Events
    'celebration': 91,  # Life Events
    'ceremony': 91,  # Life Events
    'tradition': 91,  # Life Events
    'festival': 91,  # Life Events
    'milestone': 91,  # Life Events
    'achievement': 91,  # Life Events
    'legacy': 91,  # Life Events
    'rent': 92,  # Housing
    'lease': 92,  # Housing
    'landlord': 92,  # Housing
    'tenant': 92,  # Housing
    'apartment': 92,  # Housing
    'mortgage': 92,  # Housing
    'property': 92,  # Housing
    'neighborhood': 92,  # Housing
    'utilities': 92,  # Housing
    'maintenance': 92,  # Housing
    'furnished': 92,  # Housing
    'unfurnished': 92,  # Housing
    'eviction': 92,  # Housing
    'renovate': 92,  # Housing
    'inspect': 92,  # Housing
    'heating': 92,  # Housing
    'cooling': 92,  # Housing
    'relocate': 92,  # Housing
    'pollution': 94,  # Environment
    'recycle': 94,  # Environment
    'renewable': 94,  # Environment
    'sustainable': 94,  # Environment
    'climate': 94,  # Environment
    'global': 94,  # Environment
    'energy': 94,  # Environment
    'waste': 94,  # Environment
    'wildlife': 94,  # Environment
    'conservation': 94,  # Environment
    'ecosystem': 94,  # Environment
    'carbon': 94,  # Environment
    'emissions': 94,  # Environment
    'organic': 94,  # Environment
    'solar': 94,  # Environment
    'endangered': 94,  # Environment
    'bake': 95,  # Cooking Methods
    'fry': 95,  # Cooking Methods
    'boil': 95,  # Cooking Methods
    'grill': 95,  # Cooking Methods
    'roast': 95,  # Cooking Methods
    'steam': 95,  # Cooking Methods
    'simmer': 95,  # Cooking Methods
    'broil': 95,  # Cooking Methods
    'barbecue': 95,  # Cooking Methods
    'reheat': 95,  # Cooking Methods
    'defrost': 95,  # Cooking Methods
    'marinate': 95,  # Cooking Methods
    'stir': 95,  # Cooking Methods
    'whisk': 95,  # Cooking Methods
    'blend': 95,  # Cooking Methods
    'chop': 95,  # Cooking Methods
    'slice': 95,  # Cooking Methods
    'peel': 96,  # Food Preparation
    'cut': 96,  # Food Preparation
    'dice': 96,  # Food Preparation
    'mince': 96,  # Food Preparation
    'grate': 96,  # Food Preparation
    'mash': 96,  # Food Preparation
    'mix': 96,  # Food Preparation
    'pour': 96,  # Food Preparation
    'measure': 96,  # Food Preparation
    'combine': 96,  # Food Preparation
    'spread': 96,  # Food Preparation
    'wrap': 96,  # Food Preparation
    'garnish': 96,  # Food Preparation
    'serve': 96,  # Food Preparation
    'portion': 96,  # Food Preparation
    'recipe': 96,  # Food Preparation
    'ingredient': 96,  # Food Preparation
    'preparation': 96,  # Food Preparation
    'diner': 97,  # Restaurant
    'waiter': 97,  # Restaurant
    'waitress': 97,  # Restaurant
    'server': 97,  # Restaurant
    'appetizer': 97,  # Restaurant
    'beverage': 97,  # Restaurant
    'check': 97,  # Restaurant
    'tip': 97,  # Restaurant
    'takeout': 97,  # Restaurant
    'delivery': 97,  # Restaurant
    'buffet': 97,  # Restaurant
    'specialty': 97,  # Restaurant
    'vegetarian': 97,  # Restaurant
    'vegan': 97,  # Restaurant
    'allergy': 97,  # Restaurant
    'cinema': 98,  # Movies & TV
    'series': 98,  # Movies & TV
    'episode': 98,  # Movies & TV
    'actor': 98,  # Movies & TV
    'actress': 98,  # Movies & TV
    'director': 98,  # Movies & TV
    'producer': 98,  # Movies & TV
    'scene': 98,  # Movies & TV
    'script': 98,  # Movies & TV
    'cast': 98,  # Movies & TV
    'comedy': 98,  # Movies & TV
    'drama': 98,  # Movies & TV
    'thriller': 98,  # Movies & TV
    'horror': 98,  # Movies & TV
    'documentary': 98,  # Movies & TV
    'animation': 98,  # Movies & TV
    'sequel': 98,  # Movies & TV
    'trailer': 98,  # Movies & TV
    'novel': 99,  # Books & Reading
    'fiction': 99,  # Books & Reading
    'nonfiction': 99,  # Books & Reading
    'author': 99,  # Books & Reading
    'chapter': 99,  # Books & Reading
    'page': 99,  # Books & Reading
    'cover': 99,  # Books & Reading
    'plot': 99,  # Books & Reading
    'character': 99,  # Books & Reading
    'genre': 99,  # Books & Reading
    'bookstore': 99,  # Books & Reading
    'publish': 99,  # Books & Reading
    'bestseller': 99,  # Books & Reading
    'paperback': 99,  # Books & Reading
    'hardcover': 99,  # Books & Reading
    'biography': 99,  # Books & Reading
    'memoir': 99,  # Books & Reading
    'bookmark': 99,  # Books & Reading
    'singer': 100,  # Music & Art
    'band': 100,  # Music & Art
    'album': 100,  # Music & Art
    'instrument': 100,  # Music & Art
    'guitar': 100,  # Music & Art
    'piano': 100,  # Music & Art
    'drum': 100,  # Music & Art
    'violin': 100,  # Music & Art
    'lyrics': 100,  # Music & Art
    'melody': 100,  # Music & Art
    'rhythm': 100,  # Music & Art
    'beat': 100,  # Music & Art
    'artist': 100,  # Music & Art
    'painting': 100,  # Music & Art
    'drawing': 100,  # Music & Art
    'sculpture': 100,  # Music & Art
    'gallery': 100,  # Music & Art
    'exhibition': 100,  # Music & Art
    'creative': 100,  # Music & Art
    'composer': 100,  # Music & Art
    'law': 101,  # Basic Law & Rules
    'rule': 101,  # Basic Law & Rules
    'arrest': 101,  # Basic Law & Rules
    'court': 101,  # Basic Law & Rules
    'complaint': 101,  # Basic Law & Rules
    'contract': 101,  # Basic Law & Rules
    'document': 101,  # Basic Law & Rules
    'permission': 101,  # Basic Law & Rules
    'illegal': 101,  # Basic Law & Rules
    'legal': 101,  # Basic Law & Rules
    'guilty': 101,  # Basic Law & Rules
    'innocent': 101,  # Basic Law & Rules
    'witness': 101,  # Basic Law & Rules
    'crime': 101,  # Basic Law & Rules
    'lawsuit': 101,  # Basic Law & Rules
    'sue': 101,  # Basic Law & Rules
    'government': 102,  # Government & Citizenship
    'mayor': 102,  # Government & Citizenship
    'council': 102,  # Government & Citizenship
    'election': 102,  # Government & Citizenship
    'vote': 102,  # Government & Citizenship
    'register': 102,  # Government & Citizenship
    'party': 102,  # Government & Citizenship
    'policy': 102,  # Government & Citizenship
    'citizen': 102,  # Government & Citizenship
    'citizenship': 102,  # Government & Citizenship
    'immigration': 102,  # Government & Citizenship
    'flag': 102,  # Government & Citizenship
    'anthem': 102,  # Government & Citizenship
    'democracy': 102,  # Government & Citizenship
    'freedom': 102,  # Government & Citizenship
    'taxes': 102,  # Government & Citizenship
    'opinion': 103,  # Opinions & Arguments
    'view': 103,  # Opinions & Arguments
    'perspective': 103,  # Opinions & Arguments
    'debate': 103,  # Opinions & Arguments
    'claim': 103,  # Opinions & Arguments
    'assert': 103,  # Opinions & Arguments
    'contend': 103,  # Opinions & Arguments
    'maintain': 103,  # Opinions & Arguments
    'stance': 103,  # Opinions & Arguments
    'standpoint': 103,  # Opinions & Arguments
    'issue': 104,  # Problems & Solutions
    'challenge': 104,  # Problems & Solutions
    'difficulty': 104,  # Problems & Solutions
    'obstacle': 104,  # Problems & Solutions
    'crisis': 104,  # Problems & Solutions
    'solution': 104,  # Problems & Solutions
    'solve': 104,  # Problems & Solutions
    'overcome': 104,  # Problems & Solutions
    'approach': 104,  # Problems & Solutions
    'method': 104,  # Problems & Solutions
    'strategy': 104,  # Problems & Solutions
    'alternative': 104,  # Problems & Solutions
    'option': 104,  # Problems & Solutions
    'possibility': 104,  # Problems & Solutions
    'opportunity': 104,  # Problems & Solutions
    'progress': 104,  # Problems & Solutions
    'success': 104,  # Problems & Solutions
    'failure': 104,  # Problems & Solutions
    'climb': 105,  # Describing Trends (as in "prices climb")
    'drop': 105,  # Describing Trends
    'surge': 105,  # Describing Trends
    'plunge': 105,  # Describing Trends
    'soar': 105,  # Describing Trends
    'dip': 105,  # Describing Trends
    'spike': 105,  # Describing Trends
    'level': 105,  # Describing Trends
    'plateau': 105,  # Describing Trends
    'fluctuate': 105,  # Describing Trends
    'skyrocket': 105,  # Describing Trends
    'plummet': 105,  # Describing Trends
    'stabilize': 105,  # Describing Trends
    'peak': 105,  # Describing Trends
    'triple': 105,  # Describing Trends
    'multiply': 105,  # Describing Trends
    'trade': 113,  # Business Basics
    'import': 113,  # Business Basics
    'export': 113,  # Business Basics
    'competition': 113,  # Business Basics
    'profit': 113,  # Business Basics
    'loss': 113,  # Business Basics
    'investment': 113,  # Business Basics
    'investor': 113,  # Business Basics
    'corporation': 113,  # Business Basics
    'enterprise': 113,  # Business Basics
    'industry': 113,  # Business Basics
    'sector': 113,  # Business Basics
    'consumer': 113,  # Business Basics
    'retail': 113,  # Business Basics
    'wholesale': 113,  # Business Basics
    'supply': 113,  # Business Basics
    'business': 113,  # Business Basics
    'financial': 114,  # Finance Basics
    'stock': 114,  # Finance Basics
    'bond': 114,  # Finance Basics
    'fund': 114,  # Finance Basics
    'asset': 114,  # Finance Basics
    'liability': 114,  # Finance Basics
    'equity': 114,  # Finance Basics
    'dividend': 114,  # Finance Basics
    'portfolio': 114,  # Finance Basics
    'invest': 114,  # Finance Basics
    'inflation': 114,  # Finance Basics
    'capital': 114,  # Finance Basics
    'exchange': 114,  # Finance Basics
    'rate': 114,  # Finance Basics
    'advertise': 115,  # Marketing & Sales
    'campaign': 115,  # Marketing & Sales
    'brand': 115,  # Marketing & Sales
    'logo': 115,  # Marketing & Sales
    'launch': 115,  # Marketing & Sales
    'product': 115,  # Marketing & Sales
    'service': 115,  # Marketing & Sales
    'client': 115,  # Marketing & Sales
    'competitor': 115,  # Marketing & Sales
    'survey': 115,  # Marketing & Sales
    'share': 115,  # Marketing & Sales
    'target': 115,  # Marketing & Sales
    'sponsor': 115,  # Marketing & Sales
    'sales': 115,  # Marketing & Sales
    'scientific': 116,  # Science Basics
    'experiment': 116,  # Science Basics
    'theory': 116,  # Science Basics
    'research': 116,  # Science Basics
    'discovery': 116,  # Science Basics
    'invention': 116,  # Science Basics
    'laboratory': 116,  # Science Basics
    'observe': 116,  # Science Basics
    'data': 116,  # Science Basics
    'result': 116,  # Science Basics
    'breakthrough': 116,  # Science Basics
    'phenomenon': 116,  # Science Basics
    'variable': 116,  # Science Basics
    'prove': 116,  # Science Basics
    'evidence': 116,  # Science Basics
    'study': 116,  # Science Basics
    'conclusion': 116,  # Science Basics
    'proof': 116,  # Science Basics
    'cell': 117,  # Biology Basics
    'dna': 117,  # Biology Basics
    'gene': 117,  # Biology Basics
    'evolution': 117,  # Biology Basics
    'species': 117,  # Biology Basics
    'organism': 117,  # Biology Basics
    'bacteria': 117,  # Biology Basics
    'virus': 117,  # Biology Basics
    'protein': 117,  # Biology Basics
    'organ': 117,  # Biology Basics
    'reproduce': 117,  # Biology Basics
    'adapt': 117,  # Biology Basics
    'biodiversity': 117,  # Biology Basics
    'extinct': 117,  # Biology Basics
    'mutation': 117,  # Biology Basics
    'habitat': 117,  # Biology Basics
    'reaction': 118,  # Basic Chemistry & Physics
    'element': 118,  # Basic Chemistry & Physics
    'compound': 118,  # Basic Chemistry & Physics
    'molecule': 118,  # Basic Chemistry & Physics
    'atom': 118,  # Basic Chemistry & Physics
    'force': 118,  # Basic Chemistry & Physics
    'motion': 118,  # Basic Chemistry & Physics
    'gravity': 118,  # Basic Chemistry & Physics
    'mass': 118,  # Basic Chemistry & Physics
    'velocity': 118,  # Basic Chemistry & Physics
    'wave': 118,  # Basic Chemistry & Physics
    'radiation': 118,  # Basic Chemistry & Physics
    'electricity': 118,  # Basic Chemistry & Physics
    'magnetic': 118,  # Basic Chemistry & Physics
    'particle': 118,  # Basic Chemistry & Physics
    'nuclear': 118,  # Basic Chemistry & Physics
    'formula': 118,  # Basic Chemistry & Physics
    'pressure': 118,  # Basic Chemistry & Physics
    'health': 119,  # Health & Wellness
    'healthy': 119,  # Health & Wellness
    'wellness': 119,  # Health & Wellness
    'symptom': 119,  # Health & Wellness
    'diagnosis': 119,  # Health & Wellness
    'therapy': 119,  # Health & Wellness
    'surgery': 119,  # Health & Wellness
    'chronic': 119,  # Health & Wellness
    'acute': 119,  # Health & Wellness
    'illness': 119,  # Health & Wellness
    'disease': 119,  # Health & Wellness
    'recovery': 119,  # Health & Wellness
    'immune': 119,  # Health & Wellness
    'infection': 119,  # Health & Wellness
    'medication': 119,  # Health & Wellness
    'dosage': 119,  # Health & Wellness
    'allergic': 119,  # Health & Wellness
    'condition': 119,  # Health & Wellness
    'mental': 120,  # Mental Health Basics
    'anxiety': 120,  # Mental Health Basics
    'depression': 120,  # Mental Health Basics
    'stress': 120,  # Mental Health Basics
    'therapist': 120,  # Mental Health Basics
    'counselor': 120,  # Mental Health Basics
    'psychology': 120,  # Mental Health Basics
    'disorder': 120,  # Mental Health Basics
    'trauma': 120,  # Mental Health Basics
    'panic': 120,  # Mental Health Basics
    'phobia': 120,  # Mental Health Basics
    'obsession': 120,  # Mental Health Basics
    'compulsion': 120,  # Mental Health Basics
    'mood': 120,  # Mental Health Basics
    'emotion': 120,  # Mental Health Basics
    'coping': 120,  # Mental Health Basics
    'mindfulness': 120,  # Mental Health Basics
    'meditation': 120,  # Mental Health Basics
    'burnout': 120,  # Mental Health Basics
}

# Replacement words for each pack when duplicates are removed
# Format: pack_number: [list of replacement words]
REPLACEMENT_WORDS = {
    4: ['few', 'many', 'much', 'several', 'little'],  # Articles & Determiners - lost 'no'
    5: ['plenty', 'lots', 'various', 'numerous', 'multiple', 'abundant'],  # Quantifiers
    14: ['oneself', 'anyone', 'someone', 'everyone', 'no one'],  # Personal Pronouns - lost 'one', 'her'
    15: ['whenever', 'wherever', 'however', 'whomever', 'whatsoever'],  # Possessives & Relatives
    17: ['have to', 'had better', 'might as well', 'would rather'],  # Modal Verbs
    24: ['write', 'wrote', 'written', 'bring', 'brought', 'tear', 'torn'],  # Irregular Verbs 2
    25: ['steal', 'stole', 'bite', 'bit', 'bitten', 'strike', 'struck'],  # Irregular Verbs 3
    26: ['write', 'wrote', 'wake', 'woke', 'woken', 'shine', 'shone'],  # Irregular Verbs 4
    28: ['fresh', 'stale', 'whole', 'broken', 'perfect'],  # Essential Adjectives 2 - lost 'open', 'clean'
    29: ['jealous', 'anxious', 'relaxed', 'hopeful', 'curious'],  # Basic Emotions
    39: ['lack', 'absent', 'missing', 'void', 'empty', 'nonexistent'],  # Negatives & Limits
    40: ['commute', 'fare', 'route', 'schedule', 'transit'],  # Basic Transportation
    41: ['matter', 'issue', 'subject', 'topic', 'detail'],  # Common Nouns
    43: ['post office', 'police station', 'fire station', 'supermarket', 'grocery store'],  # Places in Town
    44: ['chill', 'sick', 'legit', 'lame', 'hang', 'hit up'],  # Casual & Informal English
    45: ['kind of', 'you know', 'i mean', 'sort of', 'i guess'],  # Filler Words & Reactions
    46: ['forward', 'backward', 'sideways', 'upward', 'downward'],  # Directions
    47: ['commuter', 'passenger', 'route', 'fare', 'timetable'],  # More Transportation
    48: ['nightstand', 'dresser', 'armchair', 'ottoman', 'headboard'],  # Furniture
    49: ['dishwasher', 'spatula', 'ladle', 'colander', 'cutting board'],  # Kitchen Items
    50: ['lotion', 'deodorant', 'mouthwash', 'floss', 'cotton'],  # Bathroom Items
    51: ['laundry', 'sanitize', 'rinse', 'hang', 'store'],  # Household Chores
    52: ['ham', 'turkey', 'lamb', 'fish', 'sausage'],  # More Food
    53: ['cantaloupe', 'papaya', 'fig', 'date', 'persimmon'],  # Fruits
    54: ['kale', 'artichoke', 'leek', 'turnip', 'parsnip'],  # Vegetables
    56: ['dentist', 'nurse', 'builder', 'baker', 'butcher'],  # Jobs 1
    58: ['crocodile', 'gorilla', 'zebra', 'giraffe', 'hippo'],  # More Animals
    61: ['diploma', 'tuition', 'campus', 'scholarship', 'curriculum'],  # School & Education
    62: ['championship', 'tournament', 'referee', 'league', 'trophy'],  # Sports
    63: ['fitness', 'workout', 'endurance', 'stamina', 'agility'],  # More Sports
    64: ['premiere', 'blockbuster', 'review', 'rating', 'genre'],  # Entertainment
    66: ['outgoing', 'introverted', 'reserved', 'cheerful', 'moody'],  # Personality
    67: ['complexion', 'posture', 'stature', 'physique', 'features'],  # Physical Appearance
    68: ['purchase', 'browse', 'deal', 'offer', 'warranty'],  # Shopping
    70: ['fever', 'ache', 'sore', 'symptom', 'cure'],  # Health
    71: ['network', 'browser', 'server', 'virus', 'storage'],  # Technology
    72: ['march', 'step', 'sprint', 'dash', 'glide'],  # Verbs of Motion
    73: ['evolve', 'shift', 'modify', 'alter', 'transition'],  # Verbs of Change
    74: ['clarify', 'elaborate', 'confirm', 'deny', 'retract'],  # Communication Verbs
    75: ['recall', 'perceive', 'anticipate', 'suspect', 'conclude'],  # Mental Verbs
    76: ['swiftly', 'smoothly', 'roughly', 'harshly', 'firmly'],  # Adverbs of Manner
    77: ['merely', 'barely', 'hardly', 'scarcely', 'utterly'],  # Adverbs of Degree
    78: ['nor', 'provided', 'assuming', 'lest', 'hence'],  # Conjunctions
    79: ['consequently', 'subsequently', 'alternatively', 'admittedly', 'incidentally'],  # Connectors
    81: ['look after', 'look out', 'look over', 'take on', 'come along'],  # Phrasal Verbs 2
    82: ['excursion', 'journey', 'backpack', 'itinerary', 'jet lag'],  # Travel
    83: ['cockpit', 'cabin', 'aisle', 'tray table', 'carry-on'],  # Airport & Flying
    84: ['inn', 'lodge', 'guesthouse', 'check-in', 'room key'],  # Hotel
    85: ['department', 'colleague', 'supervisor', 'executive', 'intern'],  # Work & Office
    86: ['oversee', 'implement', 'supervise', 'assess', 'monitor'],  # Workplace Actions
    87: ['correspondence', 'memo', 'briefing', 'minutes', 'agenda'],  # Business Communication
    88: ['follower', 'subscriber', 'algorithm', 'engagement', 'platform'],  # Internet & Social Media
    89: ['bond', 'affection', 'loyalty', 'intimacy', 'devotion'],  # Relationships
    90: ['interact', 'mingle', 'befriend', 'socialize', 'network'],  # Social Interactions
    91: ['baptism', 'confirmation', 'memorial', 'reunion', 'homecoming'],  # Life Events
    92: ['condo', 'townhouse', 'dwelling', 'residence', 'household'],  # Housing
    93: ['anchor', 'correspondent', 'scoop', 'expose', 'tabloid'],  # News & Media
    94: ['compost', 'reuse', 'landfill', 'greenhouse', 'ozone'],  # Environment
    95: ['saute', 'braise', 'poach', 'caramelize', 'glaze'],  # Cooking Methods (was sauté)
    96: ['tenderize', 'score', 'baste', 'fold', 'knead'],  # Food Preparation
    97: ['cuisine', 'entree', 'side dish', 'gratuity', 'hostess'],  # Restaurant
    98: ['sitcom', 'spinoff', 'cameo', 'premiere', 'finale'],  # Movies & TV
    99: ['anthology', 'excerpt', 'prologue', 'epilogue', 'index'],  # Books & Reading
    100: ['orchestra', 'choir', 'concert', 'recital', 'symphony'],  # Music & Art
    101: ['verdict', 'bail', 'parole', 'sentence', 'appeal'],  # Basic Law & Rules
    102: ['legislation', 'regulation', 'amendment', 'constitution', 'ballot'],  # Government & Citizenship
    103: ['viewpoint', 'notion', 'conviction', 'assertion', 'rebuttal'],  # Opinions & Arguments
    104: ['remedy', 'workaround', 'breakthrough', 'setback', 'impasse'],  # Problems & Solutions
    105: ['trend', 'pattern', 'trajectory', 'forecast', 'projection'],  # Describing Trends
    113: ['startup', 'franchise', 'merger', 'acquisition', 'bankruptcy'],  # Business Basics
    114: ['securities', 'commodities', 'derivatives', 'hedge', 'yield'],  # Finance Basics
    115: ['branding', 'outreach', 'promotion', 'endorsement', 'testimonial'],  # Marketing & Sales
    116: ['methodology', 'analysis', 'correlation', 'causation', 'replication'],  # Science Basics
    117: ['genome', 'chromosome', 'heredity', 'genetics', 'cellular'],  # Biology Basics
    118: ['friction', 'momentum', 'acceleration', 'circuit', 'conductor'],  # Basic Chemistry & Physics
    119: ['rehabilitation', 'prognosis', 'remission', 'relapse', 'complication'],  # Health & Wellness
    120: ['resilience', 'self-care', 'awareness', 'trigger', 'flashback'],  # Mental Health Basics
    121: ['data science', 'deep learning', 'internet of things', 'augmented reality', '3D printing'],  # Technology Advanced
    122: ['annotation', 'footnote', 'appendix', 'index', 'peer review'],  # Academic Writing
    123: ['metaphysics', 'epistemology', 'aesthetics', 'dialectic', 'syllogism'],  # Philosophy & Ethics
    124: ['dimension', 'variable', 'parameter', 'criterion', 'indicator'],  # Abstract Concepts
    125: ['correlation', 'catalyst', 'catalyst', 'repercussion', 'ramification'],  # Cause & Effect
    126: ['definite', 'tentative', 'speculative', 'conclusive', 'presumptive'],  # Certainty & Probability
    127: ['solidarity', 'marginalization', 'empowerment', 'advocacy', 'grassroots'],  # Social Issues
    128: ['sovereignty', 'neutrality', 'intervention', 'mediation', 'reconciliation'],  # International Relations
    129: ['narrator', 'exposition', 'climax', 'resolution', 'subplot'],  # Literature
    130: ['renaissance', 'baroque', 'impressionism', 'abstract', 'avant-garde'],  # Art & Culture
    131: ['ascertain', 'delineate', 'discern', 'exemplify', 'expound'],  # Formal Vocabulary 1
    132: ['proliferate', 'perpetuate', 'precede', 'propagate', 'permeate'],  # Formal Vocabulary 2
    133: ['ameliorate', 'augment', 'bolster', 'buttress', 'corroborate'],  # Formal Vocabulary 3
    134: ['expedite', 'extricate', 'fabricate', 'fluctuate', 'formulate'],  # Formal Vocabulary 4
    135: ['anomaly', 'apparatus', 'benchmark', 'catalyst', 'connotation'],  # Academic Nouns
    136: ['analogous', 'commensurate', 'congruent', 'contingent', 'disparate'],  # Academic Adjectives
    137: ['nominal', 'peripheral', 'predominant', 'provisional', 'rudimentary'],  # Academic Adjectives 2
    138: ['arbitration', 'litigation', 'plaintiff', 'defendant', 'subpoena'],  # Everyday Legal
    139: ['physician', 'surgeon', 'specialist', 'paramedic', 'ward'],  # Everyday Medical
    140: ['mortgage', 'premium', 'deductible', 'beneficiary', 'compound'],  # Everyday Finance
    141: ['correlation', 'deviation', 'outlier', 'regression', 'sampling'],  # Research & Statistics
    142: ['cognition', 'conditioning', 'inhibition', 'projection', 'rationalization'],  # Psychology Basics
    143: ['assimilation', 'conformity', 'alienation', 'mobility', 'cohesion'],  # Sociology Basics
    144: ['analyze', 'distinguish', 'substantiate', 'corroborate', 'extrapolate'],  # Critical Thinking
    145: ['premise', 'inference', 'syllogism', 'proposition', 'rebuttal'],  # Debate & Argument
    146: ['arbitrator', 'facilitator', 'consensus', 'stalemate', 'ultimatum'],  # Negotiation
    147: ['sprint', 'agile', 'backlog', 'iteration', 'retrospective'],  # Project Management
    148: ['unicorn', 'incubator', 'accelerator', 'seed round', 'series a'],  # Business Advanced
    149:'depletion, degradation, reclamation, sequestration, reforestation'.split(', '),  # Environmental Science
    150: ['litotes', 'synecdoche', 'metonymy', 'anaphora', 'chiasmus'],  # Literary Devices
    151: ['the ball is in your court', 'bite the bullet', 'burn bridges', 'cut corners', 'devil\'s advocate'],  # Advanced Idioms
    152: ['a dime a dozen', 'bite the hand that feeds you', 'cross that bridge', 'down to the wire', 'face the music'],  # Business Idioms
    153: ['ergo', 'vis-a-vis', 'per se', 'ipso facto', 'de facto'],  # Formal Connectors
    154: ['ameliorate', 'bifurcate', 'coalesce', 'debilitate', 'enervate'],  # Advanced Verbs
    155: ['salient', 'cogent', 'trenchant', 'germane', 'apposite'],  # Nuanced Adjectives
    156: ['inquire', 'query', 'probe', 'interrogate', 'solicit'],  # Question Patterns
    157: ['retort', 'rebuff', 'affirm', 'corroborate', 'acquiesce'],  # Response Patterns
    158: ['negate', 'nullify', 'void', 'invalidate', 'refute'],  # Negative Patterns
    159: ['concur', 'dissent', 'acquiesce', 'ratify', 'sanction'],  # Agreement & Disagreement
    160: ['remorse', 'contrition', 'atonement', 'absolution', 'repentance'],  # Apology & Excuse Patterns
}

def read_overview():
    """Read the CSV file and return list of pack dictionaries."""
    packs = []
    with open('EnglishWords/EnglishWordsOverview.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            pack_num = int(row['Pack_Number'])
            title = row['Pack_Title']
            act = row['Difficulty_Act']
            words_str = row['English_Base_Words']
            words = []
            if words_str.startswith('[') and words_str.endswith(']'):
                words_str = words_str[1:-1]
                words = [w.strip() for w in words_str.split(',')]
            packs.append({
                'number': pack_num,
                'title': title,
                'act': act,
                'words': words
            })
    return packs

def find_duplicates(packs):
    """Find all words appearing in multiple packs."""
    word_to_packs = defaultdict(list)
    for pack in packs:
        for word in pack['words']:
            word_lower = word.lower().strip()
            word_to_packs[word_lower].append(pack['number'])
    return {word: pack_nums for word, pack_nums in word_to_packs.items() if len(pack_nums) > 1}

def fix_duplicates(packs, duplicates):
    """Remove duplicates from wrong packs and add replacement words."""
    changes = []

    for pack in packs:
        pack_num = pack['number']
        original_words = pack['words'][:]
        new_words = []
        removed_words = []

        for word in pack['words']:
            word_lower = word.lower().strip()
            if word_lower in duplicates:
                # Check if this pack should keep the word
                assigned_pack = WORD_ASSIGNMENTS.get(word_lower)
                if assigned_pack == pack_num:
                    new_words.append(word)
                else:
                    removed_words.append(word)
            else:
                new_words.append(word)

        # Add replacement words if needed
        if removed_words and pack_num in REPLACEMENT_WORDS:
            replacements = REPLACEMENT_WORDS[pack_num]
            if isinstance(replacements, str):
                replacements = [r.strip() for r in replacements.split(',')]

            # Get existing words to avoid adding duplicates
            existing = set(w.lower() for w in new_words)
            for repl in replacements:
                if len(new_words) >= 20:
                    break
                if repl.lower() not in existing:
                    new_words.append(repl)
                    existing.add(repl.lower())

        if removed_words:
            changes.append({
                'pack': pack_num,
                'title': pack['title'],
                'removed': removed_words,
                'added': new_words[len(original_words) - len(removed_words):] if len(new_words) > len(original_words) - len(removed_words) else []
            })

        pack['words'] = new_words

    return packs, changes

def write_overview(packs):
    """Write the fixed packs back to CSV."""
    with open('EnglishWords/EnglishWordsOverview.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Pack_Number', 'Pack_Title', 'Difficulty_Act', 'English_Base_Words'])
        for pack in packs:
            words_str = '[' + ','.join(pack['words']) + ']'
            writer.writerow([pack['number'], pack['title'], pack['act'], words_str])

def main():
    print("Reading EnglishWordsOverview.csv...")
    packs = read_overview()
    print(f"Loaded {len(packs)} packs")

    print("\nFinding duplicates...")
    duplicates = find_duplicates(packs)
    print(f"Found {len(duplicates)} duplicate words")

    print("\nFixing duplicates...")
    packs, changes = fix_duplicates(packs, duplicates)

    print("\nChanges made:")
    for change in changes[:20]:  # Show first 20
        print(f"  Pack {change['pack']} ({change['title']}):")
        print(f"    Removed: {', '.join(change['removed'])}")
        if change['added']:
            print(f"    Added: {', '.join(change['added'])}")

    if len(changes) > 20:
        print(f"  ... and {len(changes) - 20} more packs modified")

    print("\nWriting fixed CSV...")
    write_overview(packs)
    print("Done!")

    # Verify
    print("\nVerifying...")
    packs = read_overview()
    duplicates = find_duplicates(packs)
    if duplicates:
        print(f"WARNING: Still have {len(duplicates)} duplicates!")
        for word, pack_nums in list(duplicates.items())[:10]:
            print(f"  '{word}' in packs: {pack_nums}")
    else:
        print("SUCCESS: No more duplicates!")

if __name__ == '__main__':
    main()
