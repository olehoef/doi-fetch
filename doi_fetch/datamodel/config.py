import click

class Config:
    def __init__(self):

        self.identity = None
        self.bibSaveUrl = None
        self.autoSaveBib = False
    
    def show(self,option):
        # Return value based on option
        if option == 'identity' or option == '1':
            click.echo(f'[1] Identity: {self.identity}')
        if option == 'bib_save_url' or option == '2':
            click.echo(f'[2] Bib Save URL: {self.bibSaveUrl}')
        if option == 'auto_save_bib' or option == '3':
            click.echo(f'[3] Autosave Bib: {str(self.autoSaveBib)}')
        if option == None:
            click.secho(f'Config:', underline=True, bold=True)
            click.echo(f'[1] Identity:\t\t{self.identity}\n[2] Bib Save URL:\t{self.bibSaveUrl}\n[3] Autosave Bib:\t{str(self.autoSaveBib)}')
    
    def modify(self, option, modVal):
        if option == 'identity' or option == '1':
            self.identity = modVal
            click.echo(f'Changed Identity to {click.style(self.identity, italic=True)}.')
        elif option == 'bib_save_url' or option == '2':
            self.bibSaveUrl = modVal
            click.echo(f'Changed Bib Save URL to {click.style(self.bibSaveUrl, italic=True)}.')
        elif option == 'auto_save_bib' or option == '3':
            if modVal == 'True':
                self.autoSaveBib = True
            elif modVal == 'False':
                self.autoSaveBib = False
            click.echo(f'Changed Autosave Bib to {click.style(str(self.autoSaveBib),italic=True)}.')
        else:
            click.secho('Error: ', bold=True, fg='red', nl=False)
            click.echo('No valid config option provided.')