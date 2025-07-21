import spacy

nlp = spacy.load("en_core_web_sm")
ruler = nlp.add_pipe("entity_ruler", before="ner")

# Products
product_keywords = [
    'milk', 'eggs', 'yogurt', 'greek yogurt', 'cheese', 'butter', 'shampoo',
    'conditioner', 'soap', 'body wash', 'face wash', 'lotion', 'bread', 'bagels',
    'snacks', 'cookies', 'chips', 'canned vegetables', 'toothpaste', 'toothbrush',
    'mouthwash', 'floss', 'detergent', 'dish soap'
]

product_patterns = [
    {"label": "Product", "pattern": [{"LOWER": word} for word in item.split()]}
    for item in product_keywords
]

# Aisles + Entrance
aisle_patterns = [
    {"label": "Aisle", "pattern": [{"TEXT": {"REGEX": "^[A-Za-z]\\d{1,4}$"}}]},
    {"label": "Aisle", "pattern": [{"TEXT": {"REGEX": "^[A-Za-z]$"}}, {"IS_DIGIT": True}]},
    {"label": "Entrance", "pattern": [{"LOWER": "entrance"}]}
]

ruler.add_patterns(aisle_patterns + product_patterns)

# Role keyword sets
source_keywords = {"from", "at", "starting", "start", "in"}
destination_keywords = {"to", "buy", "need", "get", "go", "towards", "into", "find", "reach"}

def extract_entities(text):
    doc = nlp(text)
    entities = []

    for ent in doc.ents:
        if ent.label_ not in {"Product", "Aisle", "Entrance"}:
            continue

        entity_text = ent.text.strip().upper() if ent.label_ == "Aisle" else ent.text.lower()

        # Check 3 tokens before to infer role
        context = [doc[i].text.lower() for i in range(max(0, ent.start - 3), ent.start)]
        role = None
        if any(word in source_keywords for word in context):
            role = "Source"
        elif any(word in destination_keywords for word in context):
            role = "Destination"

        entities.append({
            "text": entity_text,
            "label": ent.label_,
            "role": role
        })

    return entities

