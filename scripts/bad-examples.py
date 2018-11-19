import xml.etree.ElementTree as ET
from nltk.metrics import edit_distance
tree = ET.parse('wn31.xml')

synsets = {}

for entry in tree.findall(".//LexicalEntry"):
    lemma = entry.find("Lemma").attrib["writtenForm"]
    if lemma.endswith(")"):
        lemma = lemma[:-3]
    lemmas = [lemma]
    for form in entry.findall("Form"):
        lemmas.append(form.attrib["writtenForm"])
    for sense in entry.findall("Sense"):
        synset = sense.attrib["synset"]
        if synset not in synsets:
            synsets[synset] = lemmas
        else:
            synsets[synset].extend(lemmas)

def is_likely_in(example, lemma):
    return edit_distance(example, lemma) - len(example) + len(lemma) - 2 < 0

def escape_csv(line):
    return line.replace("\"","\"\"")

for synset in tree.findall(".//Synset"):
    synset_id = synset.attrib["id"]
    for example in synset.findall("Example"):
        if not any(is_likely_in(example.text, lemma) for lemma in synsets[synset_id]):
            print("%s,\"%s\",\"%s\",,," % (synset_id,escape_csv(example.text),escape_csv(", ".join(synsets[synset_id]))))
print("ID,Example,Synset Members,Not a problem,New Member,New Definition")
