import sys
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--input", "-i", type = str)
parser.add_argument("--output", "-o", type = str, default = "cleanbib.bib")
parser.add_argument("--abbreviate","-a", action=argparse.BooleanOptionalAction)
parser.add_argument("--dotless", action=argparse.BooleanOptionalAction)
args = parser.parse_args()
old_bibfile = args.input
new_bibfile = args.output
abbreviate = args.abbreviate
dotless = args.dotless

with open("journalList.txt", 'r') as f:
    journalList = f.readlines()

jdict = dict()
for line in journalList:
    s = line.split(" = ")
    s[1] = s[1].replace("\n","")
    if dotless:
        s[1] = s[1].replace(".", "")
    jdict[s[0]] = s[1]
    
print("Cleaning bibliography {}\n".format(old_bibfile))

with open(old_bibfile, 'r', encoding = "utf-8") as f:
    bibtexdb = f.read()

fields_to_keep = ["author", "date", "journaltitle", "title", "doi", "number", 
                  "volume", "pages"] # fields kept for @Articles entries all other removed
fields_to_remove = ["file", "groups", "abstract", "comment", "hal_id", "hal_version"]
# fields removed for other types of entries, all other are kept
stats_entries = 0
stats_removed = 0
stats_months = 0
stats_missing_fields = 0
stats_type = dict()
stats_journal = dict()

entries = bibtexdb.split("@")
biblist = []
citedjdict = dict()
unreferenced = set()
for entry in entries[1:]:
    stats_entries+=1
    if entry[:7].lower() != "comment":
        bibdict = dict()
        i1 = entry.find("{")
        j1 = entry.find(",")
        bibdict["entrytype"] = entry[:i1]
        bibdict["keyword"] = entry[i1+1:j1]
        i = j1+1
        posegal = i+entry[i:].find("=")
        size = len(entry)
        endentry = False
        while not(endentry):
            before = entry[i:posegal]
            k = before.replace("\n", "").replace(" ","") # remove spaces and \n 
            deltaegal = entry[posegal+1:].find("=")
            if deltaegal > 0:
                nextegal = posegal+1+deltaegal
            else:
                nextegal = entry.rfind(',')
                endentry = True
            opening = posegal+1 + entry[posegal+1:].find("{")
            closing = opening + entry[opening:nextegal].rfind("}")
            v = entry[opening+1:closing]
            bibdict[k] = v
            i = closing+2
            posegal=nextegal
        # Clean if article 
        entrytype = bibdict["entrytype"].lower()
        if entrytype in stats_type.keys():
            stats_type[entrytype] += 1
        else:
            stats_type[entrytype] = 1 
        if entrytype == "article":
            if not("journaltitle" in bibdict.keys()):
                try:
                    bibdict["journaltitle"] = bibdict["journal"]
                except:
                    raise KeyError("entry {} has no journal nor journaltitle field.".format(bibdict["keyword"]))
            # check journal names 
            journal = bibdict["journaltitle"]
            try:
                journalAbb = jdict[journal]
                if not(journalAbb in citedjdict.keys()):
                    citedjdict[journalAbb] = set()
                citedjdict[journalAbb].add(journal)
                
                if abbreviate:
                    bibdict["journaltitle"] = jdict[bibdict["journaltitle"]]
            except:
                unreferenced.add(journal)
                journalAbb = journal
            
            if journalAbb in stats_journal.keys():
                stats_journal[journalAbb] += 1
            else:
                stats_journal[journalAbb] = 1
            
            
            newbibdict = dict(entrytype = "Article", keyword = bibdict["keyword"])

            for k in fields_to_keep:
                try:
                    v = bibdict[k]
                except KeyError:
                    if k != "number":
                        print("     entry {} has no {} field".format(bibdict["keyword"], k))
                        stats_missing_fields += 1
                else:
                    if k == "date":
                        vsplit = v.split("-")
                        if len(vsplit) > 1:
                            stats_months += 1
                            v = vsplit[0] # remove month
                    newbibdict[k] = v
            bibdict = newbibdict
        else:
            for k in fields_to_remove:
                if bibdict.pop(k, "") == "":
                    stats_removed += 1

        biblist.append(bibdict)

# journal statistics 
stats_journal = dict(sorted(stats_journal.items(), key = lambda item: item[1], reverse=True))
with open("stats.csv", "w") as f:
    f.write("nb.articles;journal\n")
    for k in stats_journal.keys():
        f.write("{};{}\n".format(stats_journal[k], k))
    


if unreferenced:
    print("\nUnreferenced journal names:")
    for j in unreferenced:
        print("     {}".format(j))

# Check for ambiguous names 
stats_ambiguous = 0
for j in citedjdict.keys():
    if len(citedjdict[j]) > 1:
        print("\nThere are several journal names for the abbreviation {}".format(j))
        stats_ambiguous += 1
        for jj in citedjdict[j]:
            print("     {}".format(jj))

# Sort by keyword
biblist = sorted(biblist, key = lambda entry: entry["keyword"])

newbib = ""

for item in biblist:
    entrytype, keyword = item.pop("entrytype"), item.pop("keyword")
    newbib+= "@{}{{{},\n".format(entrytype, keyword)
    for k in item.keys():
        
        newbib += "  {}".format(k) + " "*(15-len(k))
        newbib += " = {{{}}},\n".format(item[k])
    newbib+= "}\n\n"

with open(new_bibfile, "w", encoding="utf-8") as f:
    f.write(newbib)

print("\n" + "-"*30)
print("Bibliography cleaned and stored to {}".format(new_bibfile))
print("\n{} entries analyzed including:".format(stats_entries))
for t in stats_type.keys():
    print("     {} for the type {}".format(stats_type[t], t))
    

print("\n{} removed fields (for non-article entries)".format(stats_removed))

print("\nFor {} article(s):".format(stats_type["article"]))
print("     {} missing field(s)".format(stats_missing_fields))
print("     {} unreferenced journal name(s)".format(len(unreferenced)))
print("     {:.1f} % journal coverage".format(100*(1-len(unreferenced) / len(citedjdict))))
print("     {:.1f} % ambiguous journal names".format(100*(stats_ambiguous / len(citedjdict))))
print("     {} months removed from dates".format(stats_months))

