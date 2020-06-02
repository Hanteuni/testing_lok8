from Bio import Entrez, Medline


BIG_BOY_NUMBER = 0          # most amount of hits from a combination
MOST_HITS_TERM = ""         # the term associate with the most hits


def main():
    bacteria_list, compound_list, disease_list = file_reader()
    query_list_maker(bacteria_list, compound_list, disease_list)
    infomration_extract()


def file_reader():
    bacteria_list = []
    compound_list = []
    disease_list = []
    bacteria_file = open('Testbestand1', 'r')
    compound_file = open('Testbestand2', 'r')
    disease_file = open('Testbestand3', 'r')
    bacteria_list = file_filter(bacteria_file, bacteria_list)
    compound_list = file_filter(compound_file, compound_list)
    disease_list = file_filter(disease_file, disease_list)
    return bacteria_list, compound_list, disease_list


def file_filter(file, list):
    file = file.readlines()
    for line in file:
        line = line.strip().lower()     # Filters the data to prevent redunancy
        amount_hits = esearch(line)
        if amount_hits != 0:
            list.append(line)
    return list


def esearch(term):
    global BIG_BOY_NUMBER
    global MOST_HITS_TERM
    Entrez.email = 'probalyjunk@outlook.com'
    id_handle = Entrez.esearch(db='pubmed', retmax=10, term=term)   # search the terms on pubmed
    id_result = Entrez.read(id_handle)      # gives the result direct from the pubmed page
    ids = id_result['IdList']               # gives all of the id correlated to atricles about the terms
    amount_hits = len(ids)                  # amount of artictles corralated to the term
    if BIG_BOY_NUMBER < amount_hits:        # checks if the number still equeals the most hit term
        BIG_BOY_NUMBER = amount_hits        # otherwise it'll replace the number
        MOST_HITS_TERM = term               # and the term
    return amount_hits


def query_list_maker(bacteria_list, compound_list, disease_list):
    total_list = []
    duo_list = []
    duo_bad_list = []
    for bacteria in bacteria_list:
        for compound in compound_list:
            for disease in disease_list:
                # makes a list of all the possible combinations that consist of three words
                total_list.append("{} AND {} AND {}".format(bacteria, compound, disease))
    # makes a list of all the possible combinations that consist of two words
    duo_list_maker(bacteria_list, compound_list, duo_list,duo_bad_list)
    duo_list_maker(bacteria_list, disease_list, duo_list,duo_bad_list)
    duo_list_maker(compound_list, disease_list, duo_list,duo_bad_list)
    try:
        for term in total_list:
            for bad_term in duo_bad_list:
                if bad_term in term:
                    total_list.remove(term)     # removing terms didn't give a result earlier on
    except ValueError:
        pass
    total_list.append(duo_list)             # adding the all the two terms combinations
    return total_list


def duo_list_maker(list_1, list_2, duolist, duo_bad_list):
    for item_1 in list_1:
        for item_2 in list_2:
            term = "{} AND {}".format(item_1, item_2)  # all the possible combinations of two lists
            amount_hits = esearch(term)
            if amount_hits != 0:
                duolist.append(term)       # the two terms return 1 or more result
            else:
                duo_bad_list.append(term)  # if the two terms don't retieve a hit it's marked as a "bad term"


def infomration_extract():
    Entrez.email = 'probalyjunk@outlook.com'
    id_handle = Entrez.esearch(db='pubmed', retmax=10, term=MOST_HITS_TERM)
    id_result = Entrez.read(id_handle)
    ids = id_result['IdList']
    text_handle = Entrez.efetch(db='pubmed', id=ids, rettype='medline', retmode='text')
    records = Medline.parse(text_handle)
    try:
        for record in records:
            print("===============================================================")
            print("The abstract of an article of the most prominent combination: ",record['AB']\
                  ,"\nWhich was written by: ",record['AU']\
                  ,"\n===============================================================")
    except KeyError:
        pass


main()