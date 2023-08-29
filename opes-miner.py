# imports
import pandas as pd
import time

# variables
paths = []
i=-1
allowedDuplicates = ["PERSON","","N/A"]

manualMapping = {
    "id":"N/A",
    "created_at":"N/A",
    "updated_at":"N/A",
    "deleted_at":"N/A",
    "created_by":"N/A",
    "updated_by":"N/A",
    "inv_no":"Identifikatorer, lokala",
    "section_or_side":"N/A",
    "material":"Fysisk beskrivning>Material (short)",
    "connections":"Relaterade poster i Alvin (bruk en annen ID)",
    "acquisition":"Anmärkningar>Förvärv",
    "title_or_type":"Titel / alternativ titel (Problematisk felt...)",
    "size":"Fysisk beskrivning>Storlek",
    "provenance":"Anmärkningar>Proveniens (har mulighet for separat bildepost, men...???)",
    "language":"Språk (evt språknotat)",
    "lines":"Övrig fysisk beskrivning>Layout",
    "palaeographic description":"Handskriftsbeskrivning>Skrift",
    "author":"Person [aut] (Behøver autoritetspost, hvilket kan være umulig å gjøre med noen form for presisjon)",
    "content":"Abstract/beskrivning",
    "people":"Person [asn] (Associated name - behøver igjen autoritetspost, som kan være veldig utfordrende)",
    "places":"Ämnesord>Plats (eller Geografiskt - passer ikke helt altså...)",
    "origin":"Tillkomstinformation>Plats/ort",
    "state_of_preservation":"Övrig fysisk beskrivning>Tillstånd",
    "items":"Fysisk beskrivning>Omfång",
    "publ_side":"Abstract/beskrivning?",
    "genre":"Ämnesord>Genre/form ('Literary' eksisterer ikke feks)",
    "fullsizefront_r1":"RECTO IMAGE 1",
    "fullsizeback_r1":"RECTO IMAGE 2",
    "translation":"Transkription",
    "bibliography":"Anmärkningar>Bibliografi (beskrives i, har ikke bibliografi)",
    "negative_in_copenhagen":"N/A",
    "date_cataloged":"Övriga år/datum>Inventeringsdatum",
    "extent_genre":"BLANDING AV GENRE, FYSISK BESKRIVELSE",
    "language_code":"Språk",
    "date1":"N/A",
    "date2":"N/A",
    "date":"Tillkomstinformation>År/datum (FUNGERER IKKE: UNDERFELT FOR ÅR/MÅNED/DAG. FUNGERER SOM VISAS SOM.)",
    "title_statement":"BESKRIVER OGSÅ ?? GENRE",
    "material_long":"material",
    "subjects":"Ämnesord>Allmänt",
    "public":"META",
    "p_oslo_vol":"???????????",
    "p_oslo_nr":"?????",
    "internal_comments":"Anmärkningar>Intern",
    "conservation_notes":"Anmärkningar>Konserveringshistorik",
    "acquisition_year":"Övriga år/datum>Förvärvsdatum",
    "trismegistos_url":"Externa länkar>Se även1",
    "papyri_dclp_url":"Externa länkar>Se även2",
}


# functions
def nameVariable(path,header):
    if path.upper() in allowedDuplicates:
        print(f"Multiple instance of {path.upper()} is permitted")
        paths.append(str(path).upper())
    elif path.upper() not in paths:
        paths.append(str(path).upper())
    else:
        if header in manualMapping:
            if manualMapping[header].upper() == path.upper():
                paths.append(str(path).upper())
            else:
                time.sleep(100/1000)
                if path.upper() not in paths:
                    paths.append(str(path).upper())
                else:
                    path = input(f"{path.upper()} is already in use. Enter a unique mapping value or N/A if uncertain.\n")
                    nameVariable(path,header)
        else:
            time.sleep(100/1000)
            path = input(f"{path.upper()} is already in use. Enter a unique mapping value or N/A if uncertain.\n")
            if path.upper() not in paths:
                paths.append(str(path).upper())
            else:
                nameVariable(path,header)

# read csv
df = pd.read_csv("opes.csv", encoding="utf-8")
df = df.fillna("N/A")
print(f"Registered {len(df.columns)} columns by {len(df)} rows")

# execute mapping protocol
for header in df.columns:
    i+=1
    print(f"--------------{header} ({i}/{len(df.columns)-1})--------------")
    if df[header][i] == "N/A":
        tog_found = 0
        for x in range(len(df)):
            if df[header][x] != "N/A":
                print(f"First non-N/A example: {df[header][x]}")
                tog_found = 1
                break
            else:
                if tog_found == 0:
                    if x >= len(df)-1:
                        print("WARNING: unable to match non-N/A value for header!")
                        break
    else:
        print(f"First non-N/A example: {df[header][i]}")
    time.sleep(150/1000)
    if header in manualMapping:
        path = input(f"{header} already mapped to {manualMapping[header]}.\nEnter Y or YES to confirm, OR enter a new unique value, OR N/A.\n")
        if path.upper() == "Y" or path.upper() == "YES" or path == "":
            path = manualMapping[header]
            print(f"Confirmed {header} to {path}.")
    else:
        path = input('Enter Alvin equivalent. Enter N/A if uncertain.\n')
    nameVariable(path,header)
    
# print output
print(df.columns)
print(paths)
paths