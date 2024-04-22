import json
import click

class Work:
    def __init__(self, doi, created, title, authors, type, page, volume, url, publisher, issue, journal, sjr_score, h_index):
        self.doi = doi
        self.type = type
        self.created = created
        self.page = page
        self.title = title
        self.volume = volume
        self.authors = authors
        self.url = url
        self.publisher = publisher
        self.issue = issue
        self.journal = journal
        self.sjr_score = sjr_score
        self.h_index = h_index
    
    #! Depreciated
    def printWork(self):
        return json.dumps({
            'doi': self.doi,
            'type': self.type,
            'created': self.created,
            'page': self.page,
            'title': self.title,
            'volume': self.volume,
            'authors': [{'given': author.given, 'family': author.family} for author in self.authors],
            'url': self.url,
            'publisher': self.publisher,
            'issue': self.issue,
            'journal': self.journal,
            'sjr_score': self.sjr_score
  
        }, indent=2)
    
    def show(self, short=False):
        citation = getCitation(self.authors, self.created)
        if short:
            click.echo(f'{citation}\t{self.doi}')
        else:
            click.secho('DOI:\t\t', bold=True, nl=False)
            click.echo(self.doi)
            click.secho('Citation:\t', bold=True, nl=False)
            click.echo(citation)
            click.secho('Title:\t\t', bold=True, nl=False)
            click.echo(self.title)
            click.secho('Created:\t', bold=True, nl=False)
            click.echo(f'{self.created[0]}-{self.created[1]}-{self.created[2]}')
            click.secho('Type:\t\t', bold=True, nl=False)
            click.echo(self.type)
            click.secho('Journal:\t', bold=True, nl=False)
            click.echo(self.journal)
            click.secho('Publisher:\t', bold=True, nl=False)
            click.echo(self.publisher)

    
    def to_biblatex(self):
        authors_str = ''
        for author in self.authors:
            output_str = f'given-i={author.given[0]}, given={author.given}, family={author.family}'
            if author != self.authors[-1]:
                output_str += ' and '
            authors_str += output_str
        for i, part in enumerate(self.created):
            self.created[i] = str(part)
            if len(self.created[i]) == 1:
                self.created[i] = '0' + self.created[i]
        date = f'{self.created[0]}-{self.created[1]}-{self.created[2]}'
        return f"@article{{{self.authors[0].family.replace(' ', '-').lower()}-{self.created[0]},\n" \
               f"    author = {{{authors_str}}},\n" \
               f"    title = {{{self.title}}},\n" \
               f"    date = {{{date}}},\n" \
               f"    doi = {{{self.doi}}}, \n" \
               f"    journalTitle = {{{self.journal}}},\n" \
               f"    number = {{{self.issue}}}, \n"\
               f"    pages = {{{self.page.replace('-', '--')}}}, \n" \
               f"    url = {{{self.url}}},\n" \
               f"    volume = {{{self.volume}}}, \n" \
               f"}}"

def getCitation(authors, created):
    citation = 'error'
    if len(authors) == 2:
        citation = authors[0].family + ' & ' + authors[1].family + f' ({created[0]})'
    if len(authors) >= 3: 
        citation = authors[0].family + ' et al. ' + f'({created[0]})'
    if len(authors) == 1:
        citation = authors[0].family + ' ' + f'({created[0]})'
    return citation