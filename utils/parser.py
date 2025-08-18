import bibtexparser
import json

# Funzione per convertire gli autori da stringa BibTeX in lista
def parse_authors(author_str):

    # Decodifica LaTeX prima di rimuovere parentesi graffe
    decoded = author_str.replace("{\\`o}", "ò")
    decoded = decoded.replace("{\\`{o}}", "ò")

    # Rimuove parentesi graffe, ritorni a capo e spazi extra
    cleaned = decoded.replace("{", "").replace("}", "").replace("\n", " ").strip()
    cleaned = " ".join(cleaned.split())
    
    # Split usando ' and ' come separatore
    raw_authors = [a.strip() for a in cleaned.split(" and ") if a.strip()]
    
    authors = []
    for a in raw_authors:
        # Se c'è una virgola, invertiamo Cognome, Nome -> Nome Cognome
        if ',' in a:
            parts = [p.strip() for p in a.split(',', 1)]
            a = f"{parts[1]} {parts[0]}"
        authors.append(a)

    return authors


def parse_title(str):
    # Decodifica LaTeX prima di rimuovere parentesi graffe
    decoded = str.replace("{\\`o}", "ò")
    decoded = decoded.replace("{\\`{o}}", "ò")

    # Rimuove parentesi graffe, ritorni a capo e spazi extra
    cleaned = decoded.replace("{", "").replace("}", "").replace("\n", " ").strip()
    cleaned = " ".join(cleaned.split())

    return cleaned

def parse_best_paper(str):
    # Controlla se l'entry ha il campo 'bestPaper'
    if str.lower() == "true":
        print(str)
        return True
    #print(f"Best paper not found in entry: {entry}")
    return False

# Funzione per convertire un entry BibTeX in dizionario
def bib_entry_to_dict(entry):
    ref = {
        "authors": parse_authors(entry.get("author", "")),
        "title": parse_title(entry.get("title", "")),
        "book": entry.get("booktitle", entry.get("journal", "")),
        "editors": parse_authors(entry.get("editor", "")) if "editor" in entry else [],
        "publisher_location": entry.get("address", ""),
        "publisher": entry.get("publisher", ""),
        "year": entry.get("year", ""),
        "pages": entry.get("pages", ""),
        "doi": entry.get("doi", ""),
        "bestPaper": parse_best_paper(entry.get("bestpaper", ""))
    }
    return ref

# Funzione per formattare il riferimento nello stile richiesto
def format_reference(ref):
    authors = ", ".join(ref["authors"][:-1]) + " and " + ref["authors"][-1] if len(ref["authors"]) > 1 else ref["authors"][0]
    editors = ", ".join(ref["editors"])
    editors_str = f"Ed. by {editors}. " if editors else ""
    return (f"{authors}. “{ref['title']}”. In: *{ref['book']}*. "
            f"{editors_str}{ref['publisher_location']}: {ref['publisher']}, {ref['year']}, "
            f"pp. {ref['pages']}. doi: {ref['doi']}.")

# Leggere il file .bib
with open("../assets/biblio.bib", encoding="utf-8") as bib_file:
    bib_database = bibtexparser.load(bib_file)

# Convertire in lista di dizionari
refs_list = [bib_entry_to_dict(entry) for entry in bib_database.entries]

# Salvare in JSON
with open("../assets/biblio.json", "w", encoding="utf-8") as json_file:
    json.dump(refs_list, json_file, indent=4, ensure_ascii=False)

