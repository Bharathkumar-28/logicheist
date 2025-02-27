from textblob import TextBlob

def simplify_text(text):
    blob = TextBlob(text)
    simplified_text = blob.correct()  # Fixes spelling & simplifies words
    return str(simplified_text)