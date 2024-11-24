import spacy

def extract_keywords(caption):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(caption)
    return [token.text for token in doc if token.pos_ in ['NOUN', 'ADJ', 'PROPN']]
