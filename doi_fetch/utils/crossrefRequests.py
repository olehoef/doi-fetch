import requests
import click

def requestWork(doi, project):
    if project.config.identity:
        url = f'https://api.crossref.org/works/{doi}?mailto:{project.config.identity}'

        # Make a GET request
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()

            return data
        else:
            # Print an error message if the request was not successful
            print(f"Error: {response.status_code} - {response.text}")
            return None
    else:
        click.secho('Error: ', bold=True, fg='red', nl=False)
        click.echo('Please provide an identity.')
        return None


def requestJournal(issn, project):
    
    if project.config.identity:
        url = f'https://api.crossref.org/journals/{issn}?mailto:{project.config.identity}'
        # Make a GET request
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            
            return data
        else:
            # Print an error message if the request was not successful
            print(f"Error: {response.status_code} - {response.text}")
            return None
    else:
        click.secho('Error: ', bold=True, fg='red', nl=False)
        click.echo('Please provide an identity.')