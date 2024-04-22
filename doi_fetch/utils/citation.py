def getCitation(authors, created):
    citation = 'error'
    if len(authors) == 2:
        citation = authors[0].family + ' & ' + authors[1].family + f' ({created[0]})'
    if len(authors) >= 3: 
        citation = authors[0].family + ' et al. ' + f'({created[0]})'
    if len(authors) == 1:
        citation = authors[0].family + ' ' + f'({created[0]})'
    return citation