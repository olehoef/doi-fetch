import csv
import os
import click


def getSJR(search_term, search_column, year):
    default_dict = {
        'sjr_score': 'N/A',
        'h_index': 'N/A'
    }

    available_years = ['2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2020'] 
    if year not in available_years:
        return default_dict
    
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sjr_file_path = os.path.join(project_root, f'sjr-data/{year}.csv')
    print("Config file path:", sjr_file_path)
    with open(sjr_file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=';')
        
        # Iterate through the rows to find the matching entry
        for row in csv_reader:
            if row[search_column][:8] == search_term:
                sjr_value = row.get('SJR', 'N/A')
                h_index_value = row.get('H index', 'N/A')
                sjr_dict = {
                    'sjr_score': sjr_value,
                    'h_index': h_index_value
                }
                return sjr_dict

    click.secho('Warning: ', fg=(255,140,0), bold=True, nl=False)
    click.echo(f"Entry with ISSN '{search_term}' not found in CSV.")
    return default_dict

