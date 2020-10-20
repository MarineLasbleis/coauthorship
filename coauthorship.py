## Header


## Extract data from Google Scholar
# Possible libraries: 
## scholarly
## gscholar ? https://github.com/venthur/gscholar Maybe too old.
## From stack exchange: suggestion to build a webscrapper that may work better: https://stackoverflow.com/questions/13200709/extract-google-scholar-results-using-python-or-r

import pandas as pd
import matplotlib.pyplot as plt


from scholarly import scholarly
import re
import networkx as nx


def add_author(author_list, author_name):
    if author_name in author_list: 
        author_list[author_name] += 1
    else: 
        author_list[author_name] = 1
    return author_list

def format_name_authors(string_author):
    """ Take a string with surname and family name, and return the first letter of surname + family name 
    
    works only if family name is 1 word
    """
    names = re.split("\s", string_author)
    family_name = names[-1]
    surname_initial = names[0]
    surname_initial = surname_initial[0]
    return surname_initial + " " + family_name 


def extract_relationships(name, citation_threshold=0, verbose=False):
    """
    Explore the Google scholar profile of someone and extract the co-authorships in the publication list.
    
    name: of the author
    citation_threshol: by default, all the publications will be listed (use 1 to have all the publications cited at least once)
    verbose: if you want more things to be printed on screen
    """
    search_query = scholarly.search_author(name)
    short_name = format_name_authors(name)
    author = next(search_query)#.fill()
    if verbose: 
        print("You are looking at the Google scholar profile of {}, from {}".format(author.name, author.affiliation))
    author = author.fill() # add info about co authors and publications
    author_list = {}
    relationships = pd.DataFrame(0, index=[short_name], columns=[short_name])
        
    # go through all the publications and create a big matrix with all the relationships (and add author names to author_list)
    for pub in author.publications:
        if float(pub.bib["cites"])>= citation_threshold:  #only the papers that have been cited at least once
            pub_complete = pub.fill()
            print(pub_complete.bib["title"])
            authors = pub_complete.bib["author"]
            authors = re.split(" and ", authors)
            single_paper = []
            for author_name in authors: 
                single_author = format_name_authors(author_name)
                author_list = add_author(author_list, single_author)
                single_paper.append(single_author)
                if single_author not in relationships.columns:
                    relationships[single_author] = 0.
                    new_line = pd.DataFrame(0, index=[single_author], columns=relationships.columns)
                    relationships = relationships.append(new_line)
            for author1 in single_paper:
                for author2 in single_paper:
                    if author1 != author2:
                        relationships[author1][author2] += 1
    return author_list, relationships


if __name__ == "__main__": 



    #print(next(scholarly.search_author('Marine Lasbleis')))

    name = 'Marine Lasbleis'
    short_name = "M Lasbleis"

    search_query = scholarly.search_author('Marine Lasbleis')
    author = next(search_query).fill()
    print(author)


    # Print the titles of the author's publications
    #print([pub.bib for pub in author.publications])

    author_list = {}



    relationships = pd.DataFrame(0, index=[short_name], columns=[short_name])
    for pub in author.publications:
        #print(pub)
        if float(pub.bib["cites"])> 0:  #only the papers that have been cited at least once
            pub_complete = pub.fill()
            print(pub_complete.bib["title"])
            authors = pub_complete.bib["author"]
            authors = re.split(" and ", authors)
            #print(authors)
            single_paper = []
            for author_name in authors: 
                single_author = format_name_authors(author_name)
                author_list = add_author(author_list, single_author)
                single_paper.append(single_author)
                if single_author not in relationships.columns:
                    relationships[single_author] = 0.
                    #print(relationships)
                    new_line = pd.DataFrame(0, index=[single_author], columns=relationships.columns)
                    relationships = relationships.append(new_line)
            for author1 in single_paper:
                for author2 in single_paper:
                    if author1 != author2:
                        relationships[author1][author2] += 1
            # add authors in columns and lines in the pandaframe relationships
            # add the relationships for each couples in the author list (if author list is longer than 1!)


    print(author_list)    
    print(relationships)

    # Which papers cited that publication?
    # print([citation.bib['title'] for citation in pub.citedby])



    ## Create a graph


    G = nx.Graph()

    for name in author_list:
        G.add_node(name, size=author_list[name])


    #add weights to edges
    edge_list = [] #test networkx
    for index, row in relationships.iterrows():
        i = 0
        for col in row:
            weight = float(col)/1.
            edge_list.append((index, relationships.columns[i], weight))
            i += 1
    updated_edge_list = [x for x in edge_list if not x[2] == 0.0]
    #remove self references
    for i in updated_edge_list:
        if i[0] == i[1]:
            updated_edge_list.remove(i)
    #reorder edge list - this was a pain
    test = nx.get_edge_attributes(G, 'weight')

    G.add_weighted_edges_from(updated_edge_list)

    updated_again_edges = []
    for i in nx.edges(G):
        for x in test.keys():
            if i[0] == x[0] and i[1] == x[1]:
                updated_again_edges.append(test[x])
                
    widths = [x*100 for x in updated_again_edges]
    print(widths)

    pos = nx.circular_layout(G) #, k=0.2, iterations=17)
    nx.draw(G, pos, with_labels=True, node_size=[author_list[k]*1 for k in author_list],  width = widths)

    plt.show()