import re

def clean_names(raw_name):
    # remove degrees / titles
    remove_words = ["md", "m.d.", "dr.", "dr", "phd", "ph.d", "jr", "sr", "mr.", "mrs.", "ms."]
    name = raw_name.lower()

    for w in remove_words:
        name = name.replace(w, "")

    # remove extra spaces and punctuation
    name = re.sub(r"[^a-z\s]", "", name)
    name = re.sub(r"\s+", " ", name).strip()

    return name
