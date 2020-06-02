from Bio import Entrez
from Bio import Medline
import matplotlib.pyplot as plt
import numpy as np


def main():
    years = pubmed_get_years()
    years_clustered_by_five, y_values = year_counter(years)
    create_plot(years_clustered_by_five, y_values)


def pubmed_get_years():
    Entrez.email = 'probalyjunk@outlook.com'
    term = 'Toxine'
    years = []
    id_handle = Entrez.esearch(db='pubmed', retmax=100, term=term)
    id_result = Entrez.read(id_handle)
    ids = id_result['IdList']
    text_handle = Entrez.efetch(db='pubmed', id=ids, rettype='medline', retmode='text')
    records = Medline.parse(text_handle)
    for record in records:
        date = str(record['MHDA'])
        year, month, rest = date.split("/")
        year = int(year)
        years.append(year)
    years.sort()
    return years

def year_counter(years):
    y_values = []
    first_year = years[0]
    last_year = years[(len(years)-1)]
    years_clustered_by_five = []
    current_year = first_year
    year_counter_per_five(current_year, years_clustered_by_five, last_year, years, five_counter=-1)
    for value in years_clustered_by_five:
        y_values.append(len(value))
    return years_clustered_by_five, y_values


def year_counter_per_five(current_year, years_clustered_by_five,last_year, years, five_counter):
    templist = []
    five_counter += 1
    for year in years:
        if current_year <= year <= (current_year + 5):
            templist.append(year)
            years.remove(year)
    years_clustered_by_five.append(templist)
    current_year = current_year + 5
    if current_year <= last_year:
        return year_counter_per_five(current_year, years_clustered_by_five,last_year, years, five_counter)


def create_plot(years_clustered_by_five,y_values):
    number_of_bars = len(years_clustered_by_five)
    height_of_bars = tuple(y_values)
    arrangement = tuple(np.arange(number_of_bars))
    plt.bar(arrangement, height_of_bars)
    plt.show()


main()
