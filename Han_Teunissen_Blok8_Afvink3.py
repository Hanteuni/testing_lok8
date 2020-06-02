from Bio import Entrez
import time


def main():
    total_list, combined_terms = read_files()
    query_files(total_list)


def read_files():
    lijst1 = []
    lijst2 = []
    lijst3 = []
    total_list = []

    query1 = open("Testbestand1")
    query2 = open("Testbestand2")
    query3 = open("Testbestand3")

    inhoud1 = query1.readlines()[:]
    inhoud2 = query2.readlines()[:]
    inhoud3 = query3.readlines()[:]
    print("test")
    for i in range(len(inhoud1)):
        try:
            inhoud1[i] = inhoud1[i].strip("\n")
            inhoud2[i] = inhoud2[i].strip("\n")
            inhoud3[i] = inhoud3[i].strip("\n")
        except:
            pass
    total_list = inhoud1 + inhoud2 + inhoud3
    print("Total list: ",total_list)
    combined_terms = add_together(inhoud1, inhoud2, inhoud3)
    return total_list, combined_terms


def query_files(total_list):
    for item in total_list:
        search(item)


def search(query):
    Entrez.email = 'smartrutger@gmail.com'
    handle = Entrez.esearch(db='pubmed',
                            sort='relevance',
                            retmax=200,
                            retmode='xml',
                            term=query)
    results = Entrez.read(handle)
    print(results)
    time.sleep(10)
    fetch_details(results)


def fetch_details(id_list):
    ids = ','.join(id_list)
    Entrez.email = 'smartrutger@gmail.com'
    handle = Entrez.efetch(db='pubmed',
                           retmode='text',
                           id=ids)
    results = Entrez.read(handle)
    return results


def add_together(inhoud1, inhoud2, inhoud3):
    combined_terms = []
    for compound in inhoud1:
        for fenotype in inhoud2:
            for molecular_effect in inhoud3:
                combined_terms.append("{} AND {} AND {}".format(compound, fenotype, molecular_effect))
    print(combined_terms)
    return combined_terms

main()