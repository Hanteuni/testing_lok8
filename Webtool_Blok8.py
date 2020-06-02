import tkinter as tk
from Bio import Entrez, Medline


def main():
    # query = create_gui()
    query = "Toxine"
    ids = esearch(query)
    get_information(ids)



def create_gui():
    window = tk.Tk()
    entry = tk.Entry(width=50)
    entry.pack()
    query = entry.get()
    print(query)
    window.mainloop()
    return query


def esearch(term):
    Entrez.email = 'probalyjunk@outlook.com'
    id_handle = Entrez.esearch(db='pubmed', retmax=10, term=term)   # search the terms on pubmed
    id_result = Entrez.read(id_handle)      # gives the result direct from the pubmed page
    ids = id_result['IdList']               # gives all of the id correlated to atricles about the terms
    amount_hits = len(ids)                  # amount of artictles corralated to the term
    if amount_hits > 0:
        return ids
    else:
        return "your query is wrong"


def get_information(ids):
    database = "pubmed"
    records_list = []
    columns_list = []
    text_handle = Entrez.efetch(db=database, id=ids, rettype='medline', retmode='text')
    records = Medline.parse(text_handle)
    print("Aantal publicaties: ", len(ids))
    headers = ["Title", "Abstract", "Database", "Date", "Author"]
    columns_list.append(headers)
    try:
        for record in records:
            # print("Titel: ", record['TI'])
            # print("Abstract: ", record['AB'])
            # print("Database: ", database)
            # print("Datum: ",record['MHDA'])
            # print("Auteur: ", record['AU'])
            result = [record['TI'], record['AB'], database, record['MHDA'], record['AU']]
            records_list.append(result)
    except KeyError:
        pass
    for header in headers:
        print(header)


main()
