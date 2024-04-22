from doi_fetch.datamodel.project import Project
from doi_fetch.utils.crossrefRequests import requestWork
from doi_fetch.utils.rest import rest
from doi_fetch.utils.citation import getCitation
import click
import inquirer
import sys
from trogon import tui

## DOI-FETCH                                                                            
@tui()
@click.group()
@click.option('--new', '-n', is_flag=True, default=False, help='Create a new project.')
@click.argument('project_name')
@click.pass_context
def doi_fetch(ctx, new, project_name):

    # Initiating config and works bases
    project = Project(project_name)

    # Only execute if project is given
    if project != None:

        # Access existing project
        if not new:
            # Check if project exists
            try:
                project.load()
            except:
                click.secho(f'Error: ', nl=False, fg='red', bold=True)
                click.echo(f'Poject <{project}> does not exist.')
                click.ClickException('error')
            
        # Create new project
        else:
            # Create new Persitence file
            project.save()

            # Load new project
            project.load()
    
    # Add objects to pass context
    ctx.obj = {'project': project}

## ADD                                                                                      
@doi_fetch.command()
@click.argument('doi')
@click.pass_context
def add(ctx, doi):
    '''Add new Work.'''

    # Define objects from pass context
    project = ctx.obj['project']


    # Add and display work
    requestedWork = project.searchWork(doi)
    if requestedWork != None:
        click.secho('Work exists already.', fg=(255,140,0))
        requestedWork.show(short=True)
    else:
        requestedWork = requestWork(doi, project)
        if requestedWork != None: 

            project.addWork(requestedWork)
            project.save()
            requestedWork = project.searchWork(doi)
            click.secho('Work saved sucessfully!', fg='green')
            requestedWork.show(short=True)
            if project.config.autoSaveBib:
                if project.config.bibSaveUrl:
                    with open(project.config.bibSaveUrl, 'a') as bibfile:
                        biblatex = requestedWork.to_biblatex()
                        bibfile.write(biblatex + '\n')
                else:
                    click.secho('Warning: ', bold=True, fg=(255,140,0), nl=False)
                    click.echo('Could not save bib. No file provided in config.')
        else:
            print(f"work {doi} not found")

## SERVE                                                                                
@doi_fetch.command()
@click.option('--port', '-p', default=8000, help='Specify port.')
@click.pass_context
def serve(ctx, port):
    '''Start Server.'''

    project = ctx.obj['project']
    rest(project, port)

## SHOW                                                                                 
@doi_fetch.command()
@click.argument('doi', default=None, required=False)
@click.pass_context
def show(ctx,doi):
    '''List all works of project or show work details.'''

    project = ctx.obj['project']
    if doi == None:
        works_num = len(project.works)
        click.secho(f'Showing ', bold=True, fg='cyan', nl=False)
        click.secho(works_num, italic=True, bold=True, fg='cyan', nl=False)
        click.secho(' works for project ', bold=True, fg='cyan', nl=False)
        click.secho(project.name, italic=True, fg='cyan', bold=True)

        max_cit_len = 0
        for work in project.works:
            citation = getCitation(work.authors, work.created)
            cit_len = len(citation)
            if cit_len > max_cit_len:
                max_cit_len = cit_len
        
        available_works = []
        for work in project.works:     
            citation = getCitation(work.authors, work.created)
            cit_len = len(citation)
            gap_len = max_cit_len + 5 - cit_len
            display_output = citation + gap_len * ' ' + work.doi
            display_work_pair = (display_output, work)
            available_works.append(display_work_pair)
        available_works.append(('exit', None))
        choices = [
            inquirer.List(
                'work',
                message=click.style('Select for more details', italic=True, fg=(211,211,211)),
                choices=available_works,
                carousel=True
            )
        
        ]
        response = inquirer.prompt(choices)
        chosen_work = response.get('work')
        if chosen_work != None:
            click.clear()
            chosen_work.show()
        else:
            sys.exit()
    else:
        requestedWork = project.searchWork(doi)
        if requestedWork:
            requestedWork.show()
        else:
            click.secho('Error: ', bold=True, fg='red', nl=False)
            click.echo('Work not found. Please add as new.')

## CONFIG                                                                               
@doi_fetch.command()
@click.argument('option', default=None, required=False)
@click.option('--view', '-v', is_flag=True, default=False, help="View option(s).")
@click.option('--modify', '-m', help='Modify option(s).')
@click.pass_context
def config(ctx, option, view, modify):
    '''Configure project.'''

    project = ctx.obj['project']
    if view:
        project.config.show(option)
    if modify:
        project.config.modify(option, modify)
        project.save()


## BIB                                                                                  
@doi_fetch.command()
@click.pass_context
def bib(ctx):
    '''Export BibLaTex for all works.'''

    project = ctx.obj['project']

    if project.config.bibSaveUrl:
        for work in project.works:
            with open(project.config.bibSaveUrl, 'a') as bibfile:
                biblatex = work.to_biblatex()
                bibfile.write(biblatex + '\n')
        click.echo('Successfully saved all biblatex to:')
        click.echo(project.config.bibSaveUrl)
    else:
        click.secho('Warning: ', bold=True, fg=(255,140,0), nl=False)
        click.echo('Could not save bib. No file provided in config.')



