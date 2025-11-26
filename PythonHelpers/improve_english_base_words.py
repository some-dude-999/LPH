#!/usr/bin/env python3
"""
Script to improve English_Base_Words in EnglishWordsOverview.csv
"""

import csv
import re

# Define improvements for each pack that needs changes
# Format: pack_number: new_base_words_list
IMPROVEMENTS = {
    # Pack 1: Greetings - fix incomplete words
    1: ["hello", "hi", "goodbye", "bye", "good morning", "good afternoon", "good evening", "good night", "please", "thank you", "thanks", "sorry", "excuse me", "yes", "no", "okay", "welcome", "hey", "cheers", "pardon"],

    # Pack 8: Common Expressions - title says expressions, so use actual expressions
    8: ["I don't know", "I think so", "me too", "no problem", "you're welcome", "of course", "by the way", "that's right", "come on", "hold on", "let me", "I mean", "you know", "kind of", "sort of", "what about", "how about", "no way", "for sure", "my bad"],

    # Pack 16: Question Words - focus on question words and phrases
    16: ["what", "where", "when", "why", "how", "which", "who", "whom", "whose", "how much", "how many", "how long", "how far", "how often", "how old", "what kind", "what time", "what if", "why not", "how come"],

    # Pack 31: Home & Rooms - fix incomplete room names
    31: ["home", "house", "room", "kitchen", "bedroom", "bathroom", "living room", "dining room", "garage", "basement", "attic", "yard", "garden", "door", "window", "wall", "floor", "ceiling", "stairs", "hallway"],

    # Pack 80: Phrasal Verbs 1 - use complete phrasal verbs
    80: ["wake up", "get up", "turn on", "turn off", "put on", "take off", "pick up", "put down", "look for", "give up", "go on", "come back", "get back", "work out", "find out", "figure out", "run out", "show up", "set up", "break down"],

    # Pack 81: Phrasal Verbs 2 - use complete phrasal verbs
    81: ["look up", "look after", "look forward to", "take care of", "get along", "get rid of", "keep up", "come up with", "put up with", "make up", "break up", "grow up", "bring up", "turn up", "turn down", "carry on", "hold on", "hang out", "check out", "calm down"],

    # Pack 84: Hotel - fix "front" to "front desk"
    84: ["hotel", "motel", "hostel", "resort", "reception", "lobby", "front desk", "room service", "housekeeping", "concierge", "suite", "single room", "double room", "vacancy", "amenity", "checkout", "key card", "minibar", "bellhop", "tip"],

    # Pack 88: Internet & Social Media - fix "social"
    88: ["browser", "link", "search engine", "social media", "post", "share", "comment", "follow", "unfollow", "profile", "login", "logout", "password", "notification", "upload", "stream", "viral", "hashtag", "content", "influencer"],

    # Pack 91: Life Events - replace "spirit" with something more fitting
    91: ["birth", "childhood", "teenager", "adult", "elderly", "birthday", "graduation", "engagement", "marriage", "pregnancy", "funeral", "retirement", "anniversary", "celebration", "ceremony", "tradition", "festival", "milestone", "achievement", "legacy"],

    # Pack 97: Restaurant - fix "main"
    97: ["cafe", "diner", "menu", "reservation", "waiter", "waitress", "server", "appetizer", "main course", "beverage", "bill", "check", "tip", "takeout", "delivery", "buffet", "specialty", "vegetarian", "vegan", "allergy"],

    # Pack 101: Basic Law & Rules - fix "get"
    101: ["law", "rule", "ticket", "fine", "arrest", "court", "lawyer", "complaint", "contract", "document", "permission", "illegal", "legal", "guilty", "innocent", "witness", "crime", "lawsuit", "sue", "rights"],

    # Pack 102: Government & Citizenship - fix "green" and "pay"
    102: ["government", "mayor", "council", "election", "vote", "register", "party", "policy", "citizen", "citizenship", "visa", "green card", "immigration", "border", "flag", "anthem", "law", "democracy", "freedom", "taxes"],

    # Pack 106: Common Idioms 1 - use actual idiom phrases
    106: ["piece of cake", "break the ice", "hit the nail on the head", "under the weather", "beat around the bush", "call it a day", "out of hand", "in the same boat", "miss the boat", "spill the beans", "last straw", "once in a blue moon", "on the same page", "break a leg", "cost an arm and a leg"],

    # Pack 107: Common Idioms 2 - use actual idiom phrases
    107: ["cold feet", "keep an eye on", "give a hand", "head over heels", "pain in the neck", "know by heart", "let the cat out of the bag", "kill two birds with one stone", "elephant in the room", "hold your horses", "straight from the horse's mouth", "when pigs fly", "raining cats and dogs", "bite off more than you can chew", "better late than never"],

    # Pack 108: Phrasal Verbs 3 - complete phrasal verbs
    108: ["point out", "rule out", "sort out", "turn out", "carry out", "bring about", "come across", "cut down", "cut off", "drop out", "end up", "get away", "get over", "go through", "hand in", "leave out", "let down", "look into", "pass out", "make up for"],

    # Pack 109: Phrasal Verbs 4 - complete phrasal verbs
    109: ["run into", "take over", "bring back", "call off", "fill in", "fill out", "hand out", "hang up", "kick off", "lay off", "log in", "log out", "mix up", "pay back", "pay off", "pull over", "put off", "rip off", "settle down", "sign up"],

    # Pack 110: Collocations - Make & Do - complete collocations
    110: ["make a decision", "make a mistake", "make progress", "make an effort", "make sense", "make money", "make a difference", "make sure", "make friends", "make a reservation", "do homework", "do business", "do a favor", "do your best", "do the dishes", "do research", "do exercise", "do damage", "do laundry", "do nothing"],

    # Pack 111: Collocations - Have & Take - complete collocations
    111: ["have a look", "have a break", "have a conversation", "have fun", "have lunch", "have a meeting", "have a problem", "have an effect", "have experience", "have a chance", "take a break", "take a chance", "take care of", "take notes", "take place", "take time", "take action", "take a shower", "take responsibility", "take advantage"],

    # Pack 112: Collocations - Other - complete collocations
    112: ["pay attention", "keep in mind", "come to a conclusion", "catch a cold", "catch fire", "miss the point", "break the rules", "break a promise", "break the law", "break a habit", "save time", "save money", "waste time", "spend time", "kill time", "tell the truth", "tell a lie", "tell a story", "tell the difference", "tell a joke"],

    # Pack 117: Biology - fix "food" to "food chain"
    117: ["cell", "DNA", "gene", "evolution", "species", "organism", "bacteria", "virus", "immune system", "protein", "tissue", "organ", "reproduce", "adapt", "ecosystem", "biodiversity", "extinct", "mutation", "food chain", "habitat"],

    # Pack 121: Technology Advanced - fix split compound terms
    121: ["artificial intelligence", "algorithm", "automation", "robot", "robotics", "cloud computing", "virtual reality", "machine learning", "blockchain", "cryptocurrency", "encryption", "cybersecurity", "drone", "sensor", "big data", "neural network", "software", "hardware", "startup", "app"],

    # Pack 149: Environmental Science - fix "human"
    149: ["biodiversity", "sustainability", "renewable", "nonrenewable", "deforestation", "contamination", "degradation", "conservation", "restoration", "mitigation", "adaptation", "resilience", "climate change", "carbon footprint", "greenhouse gas", "emissions", "ecological", "preservation", "carbon", "habitat"],

    # Pack 151: Advanced Idioms - actual idioms
    151: ["ball is in your court", "bite the bullet", "burn the midnight oil", "cut to the chase", "go the extra mile", "hit the ground running", "leave no stone unturned", "read between the lines", "take with a grain of salt", "think outside the box", "tip of the iceberg", "back to square one", "raise the bar", "at the end of the day", "see eye to eye"],

    # Pack 152: Business Idioms - actual idioms
    152: ["back to the drawing board", "ballpark figure", "bottom line", "corner the market", "get the ball rolling", "in the red", "in the black", "learn the ropes", "red tape", "touch base", "up in the air", "win-win situation", "ahead of the curve", "bring to the table", "move the needle"],

    # Pack 156: Question Patterns - actual question patterns
    156: ["do you want", "can I get", "would you like", "could you please", "would you mind", "do you have", "is there", "are you", "have you ever", "did you", "what do you think", "where do you", "when did you", "why do you", "how do you", "who is", "which one", "how much", "how long", "how often"],

    # Pack 157: Response Patterns - actual response patterns
    157: ["that makes sense", "I see", "got it", "sounds good", "no worries", "I understand", "good point", "fair enough", "I agree", "you're right", "I'm not sure", "let me think", "I appreciate it", "thanks for", "my pleasure", "don't mention it", "happy to help", "that works", "I'll let you know", "okay fine"],

    # Pack 159: Agreement & Disagreement patterns
    159: ["I totally agree", "I couldn't agree more", "that's exactly right", "I feel the same way", "absolutely", "I'm with you", "I'm not so sure", "I have to disagree", "I see it differently", "that's not how I see it", "I'm torn", "I can see both sides", "I agree to some extent", "let's agree to disagree", "you might be right", "I hadn't thought of that", "you've convinced me", "I suppose you're right", "sure why not", "I can't argue with that"],

    # Pack 160: Apology & Excuse Patterns - actual patterns
    160: ["I'm sorry", "my bad", "I apologize", "it was an accident", "I forgot", "please forgive me", "excuse me", "I feel terrible", "I'm late", "I didn't mean to", "it won't happen again", "let me make it up to you", "I take full responsibility", "that's my fault", "there's no excuse", "I regret", "pardon me", "I made a mistake", "we're good", "no hard feelings"],
}

def format_base_words(words_list):
    """Format words list as CSV-compatible string"""
    return '"[' + ','.join(words_list) + ']"'

def parse_base_words(base_words_str):
    """Parse the base words string from CSV"""
    # Remove surrounding quotes and brackets
    cleaned = base_words_str.strip('"').strip('[').strip(']')
    return [w.strip() for w in cleaned.split(',')]

def main():
    input_file = '/home/user/LPH/EnglishWords/EnglishWordsOverview.csv'
    output_file = '/home/user/LPH/EnglishWords/EnglishWordsOverview.csv'

    rows = []

    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows.append(header)

        for row in reader:
            pack_num = int(row[0])

            if pack_num in IMPROVEMENTS:
                # Replace the English_Base_Words column (index 3)
                new_words = IMPROVEMENTS[pack_num]
                row[3] = '[' + ','.join(new_words) + ']'
                print(f"Pack {pack_num} ({row[1]}): Updated {len(new_words)} words")

            rows.append(row)

    # Write back
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    print(f"\nUpdated {len(IMPROVEMENTS)} packs total")
    print(f"Output written to: {output_file}")

if __name__ == '__main__':
    main()
