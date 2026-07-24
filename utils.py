import re

def extract_group_link(text):
    """Extract group link from text"""
    match = re.search(r'https://t\.me/\+[\w-]+', text)
    return match.group(0) if match else None

def is_flirty(text):
    """Check if message is flirty"""
    flirty_words = ['love', 'baby', 'cutie', 'handsome', 'beautiful', 'sexy', 
                    'i like you', 'miss you', 'kiss', 'hug', 'date']
    return any(word in text.lower() for word in flirty_words)

def get_greeting(gender):
    """Get gender-specific greeting"""
    if gender.lower() == "girl":
        return "🌸 Hello, I'm a girl bot"
    else:
        return "💪 Hello, I'm a boy bot"
