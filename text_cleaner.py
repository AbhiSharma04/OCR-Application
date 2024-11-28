import re
from spellchecker import SpellChecker

def clean_and_format_text(raw_text):
    """
    Cleans and formats extracted text for improved readability.
    """

    if not raw_text or not isinstance(raw_text, str):  # Handle None, empty, or non-string input
        return ""

    spell = SpellChecker()

    # Correct typos, preserving non-alphabetic characters
    words = raw_text.split()
    corrected_words = [
        spell.correction(word) if word.isalpha() and word not in spell else word 
        for word in words
    ]
    cleaned_text = " ".join(corrected_words)

    # Remove repeated consecutive words (case-insensitive)
    cleaned_text = re.sub(r'\b(\w+)( \1\b)+', r'\1', cleaned_text, flags=re.IGNORECASE)

    # Define headers or questions to separate into paragraphs
    questions = [
        "State the universal law of gravitation.",
        "What do you mean by free fall?",
        "What do you mean by acceleration due to gravity?",
        "If the moon attracts the earth; why does the Earth not move towards the moon?"
    ]
    for question in questions:
        # Ensure proper paragraph formatting around each header/question
        cleaned_text = re.sub(
            rf'({re.escape(question)})', r'\n\n\1\n\n', cleaned_text, flags=re.IGNORECASE
        )

    # Add line breaks after bullet points and periods
    cleaned_text = cleaned_text.replace("•", "\n•")  # Handle bullet points
    cleaned_text = re.sub(r'(?<!\d)\. ', ".\n", cleaned_text)  # Avoid breaking decimals like 9.8

    # Normalize spaces and handle artifacts
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()

    # Ensure extra line breaks for better readability
    cleaned_text = re.sub(r'(\n\s*)+', '\n', cleaned_text)  # Collapse multiple line breaks
    cleaned_text = cleaned_text.strip()

    return cleaned_text