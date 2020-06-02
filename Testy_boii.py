from Bio import Entrez, Medline
import calendar
import datetime
from time import strptime

def main():
    get_ids()


def get_ids():
    records_list = []
    counter = 0
    term = "disability"
    database = "Pubmed"
    date_ymdh = "01/01/2018"
    Entrez.email = 'probalyjunk@outlook.com'
    id_handle = Entrez.esearch(db=database, retmax=100, term=term)  # search the terms on pubmed
    id_result = Entrez.read(id_handle)  # gives the result direct from the pubmed page
    ids = id_result['IdList']  # gives all of the id correlated to atricles about the terms
    print(ids)
    amount_hits = len(ids)  # amount of artictles corralated to the term
    if amount_hits > 0:
        text_handle = Entrez.efetch(db=database, id=ids, rettype='medline', retmode='text')
        records = Medline.parse(text_handle)
        number_of_publications = len(ids)
        try:
            for record in records:
                result = [record['TI'], record['AB'], database, record['DP'], record['AU'], record['LID'], ids[counter]]
                records_list.append(result)
        except KeyError:
            pass

        records_list.append(result)
    # print(records_list[0][7])
    sort_records(records_list)
    # filter_records(filter_options)


def sort_records(records_list):
    try:
        for record in records_list:
            date_ymd = str(record[3])
            date_year, date_month, date_day = date_ymd.split(" ")
            date_month = strptime(date_month, "%b").tm_mon
            print(date_month)
            date_ymd = datetime.date(int(date_year), date_month, int(date_day))
            record[3] = date_ymd
    except ValueError:
        print("AAAAAAAAAAAAAAAAAAHHHHHHHHHHH")
        date_year = date_ymd
        date_month = 1
        date_day = 1
        date_ymd = datetime.date(int(date_year), date_month, int(date_day))
        record[3] = date_ymd
        pass
    for record2 in records_list:
        print(record2[3])

def filter_records(filter_options):
    pass

main()