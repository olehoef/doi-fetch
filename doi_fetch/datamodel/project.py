from doi_fetch.datamodel.work import Work
from doi_fetch.datamodel.author import Author
from doi_fetch.utils.crossrefRequests import requestJournal
from doi_fetch.datamodel.config import Config
import json
from doi_fetch.utils.sjr import getSJR
import os


class Project:
    def __init__(self, name):
        self.name = name
        filename = f'persistence/{self.name}.json'
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.persistence_file_path = os.path.join(project_root, filename)
        self.works = []
        self.config = Config()

    def addWork(self, data):

        author_list = data.get('message', {}).get('author', [])
        issn = data.get('message', {}).get('ISSN', [])
        event = data.get('message', {}).get('event', {}).get('name', {})
        type = data.get('message', {}).get('type')
        if issn != []:
            journal_data = requestJournal(issn[0], self)
            if journal_data != None:
                journal = journal_data.get('message', {}).get('title', '')
            else:
                journal = 'Error: Journal not found.'
        elif event != '':
            journal = event
        else:
            journal = 'Error: Journal not found.'

        if type == 'journal-article':
            sjr_dict = getSJR(issn[0].replace('-', ''), 'Issn', '2022')
        elif type == 'proceedings-article':
            sjr_dict = getSJR(journal, 'Title', journal[:4])
        else:
            sjr_dict = {
                'sjr_score': 'N/A',
                'h_index': 'N/A'
            }
        
        #print(formatted_data)
        work_data = Work(
            title=data.get('message', {}).get('title', [])[0],
            doi=data.get('message', {}).get('DOI', ''),
            type=data.get('message', {}).get('type'),
            page=data.get('message', {}).get('page', ''),
            publisher=data.get('message', {}).get('publisher'),
            volume=data.get('message', {}).get('volume',''),
            url=data.get('message', {}).get('URL'),
            issue=data.get('message', {}).get('issue',''),
            created=data.get('message', {}).get('created', {}).get('date-parts',[])[0], # returns [year, month, date]
            authors=[Author(given=author.get('given', ''), family=author.get('family', '')) for author in author_list],
            journal=journal,
            sjr_score=sjr_dict['sjr_score'],
            h_index=sjr_dict['h_index']
        )
        self.works.append(work_data)

    def removeWork(self, doi):
        index_to_remove = next((index for index, work in enumerate(self.works) if work.doi.lower() == doi.lower()), None)

        if index_to_remove is not None:
            removed_work = self.works.pop(index_to_remove)
            return removed_work
        else:
            print(f"No work with DOI {doi} found.")
            return None

    def save(self):
        with open(self.persistence_file_path, 'w') as file:

            #* Works
            works_data = []
            for work in self.works:
                works_data.append({
                    'doi': work.doi,
                    'type': work.type,
                    'created': work.created,
                    'page': work.page,
                    'title': work.title,
                    'volume': work.volume,
                    'authors': [{'given': author.given, 'family': author.family} for author in work.authors],
                    'url': work.url,
                    'publisher': work.publisher,
                    'issue': work.issue,
                    'journal': work.journal,
                    'sjr_score': work.sjr_score,
                    'h_index': work.h_index
                })
            
            #* Config
            config_data = {"identity": self.config.identity,
                    "bib_save_url": self.config.bibSaveUrl,
                    "auto_save_bib": self.config.autoSaveBib}
            
            #* Writre to file
            json.dump({"works": works_data, "config": config_data}, file)


    def load(self):

        with open(self.persistence_file_path, 'r') as file:

            #* Read from file
            data = json.load(file)

            #* Works
            self.works = []
            for work_data in data.get('works', []):
                authors = [Author(given=author['given'], family=author['family']) for author in work_data['authors']]
                work = Work(
                    doi=work_data['doi'],
                    type=work_data['type'],
                    created=work_data['created'],
                    page=work_data['page'],
                    title=work_data['title'],
                    volume=work_data['volume'],
                    authors=authors,
                    url=work_data['url'],
                    publisher=work_data['publisher'],
                    issue=work_data['issue'],
                    journal=work_data['journal'],
                    sjr_score=work_data['sjr_score'],
                    h_index=work_data['h_index']
                )
                self.works.append(work)
            
            #* Config
            config_data = data.get("config", {})
            self.config.identity = config_data.get("identity", '')
            self.config.bibSaveUrl = config_data.get("bib_save_url", '')
            self.config.autoSaveBib = config_data.get("auto_save_bib", '')

    
    def respond(self):
        responds= []
        for work in self.works:
            authors = '' 
            for author in work.authors:
                if author == work.authors[-1]:
                    authors += author.family
                else:
                    authors += author.family + ', '

            citation = getCitation(work.authors, work.created)
            workObject = {
                "doi": work.doi,
                "yearCreated": work.created[0],
                "page": work.page,
                "heading": work.title,
                "volume": work.volume,
                "url": work.url,
                "publisher": work.publisher,
                "journal": work.journal,
                "authors": authors,
                "citation": citation,
                "sjr_score": work.sjr_score,
                "h_index": work.h_index
            }
            responds.append(workObject)
        return responds
    
    def searchWork(self, doi):
        doi = doi.lower()
        for work in self.works:
            if work.doi.lower() == doi:
                return work
        return None

    

def getCitation(authors, created):
    citation = 'error'
    if len(authors) == 2:
        citation = authors[0].family + ' & ' + authors[1].family + f' ({created[0]})'
    if len(authors) >= 3: 
        citation = authors[0].family + ' et al. ' + f'({created[0]})'
    if len(authors) == 1:
        citation = authors[0].family + ' ' + f'({created[0]})'
    return citation