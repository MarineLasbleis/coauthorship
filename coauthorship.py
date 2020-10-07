## Header


## Extract data from Google Scholar
# Possible libraries: 
## scholarly
## gscholar ? https://github.com/venthur/gscholar Maybe too old.
## From stack exchange: suggestion to build a webscrapper that may work better: https://stackoverflow.com/questions/13200709/extract-google-scholar-results-using-python-or-r

from scholarly import scholarly
import re

#print(next(scholarly.search_author('Marine Lasbleis')))

search_query = scholarly.search_author('Marine Lasbleis')
author = next(search_query).fill()
#print(author)


# Print the titles of the author's publications
#print([pub.bib for pub in author.publications])


def format_name_authors(string_author):
    """ Take a string with surname and family name, and return the first letter of surname + family name 
    
    works only if family name is 1 word
    """
    names = re.split("\s", string_author)
    family_name = names[-1]
    surname_initial = names[0]
    surname_initial = surname_initial[0]
    return surname_initial + " " + family_name 

for pub in author.publications:
    pub_complete = pub.fill()
    authors = pub_complete.bib["author"]
    authors = re.split(" and ", authors)
    print(authors)
    for author_name in authors: 
        print(format_name_authors(author_name))


    
# Take a closer look at the first publication
pub = author.publications[0].fill()
print(pub.bib["author"])

# Which papers cited that publication?
# print([citation.bib['title'] for citation in pub.citedby])



## Create a graph