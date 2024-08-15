# DOI-FETCH
CLI tool to manage academic references. More over doi-fetch can serve references to e.g. MS Excel, which allows you to use them as data types. 

## Installation

1. Clone repo.
2. Run `pip install .` in root directory.


## Usage 

`doi-fetch [OPTIONS] [PROJECT_NAME] COMMAND [ARGS]`

  Use 'all' to list all projects.

**Options**: 

  `-n`, `--new ` Create a new project.  

**Commands**:

  `add`     Add new Work.  
  `bib`     Export BibLaTex for all works.  
  `config`  Configure project.  
  `serve`   Start Server.  
  `show`    List all works of project or show work details.  
  `tui`     Open Textual TUI.


## Server request routes

`GET /api/works/add/<doi>` Add new reference.  
`GET /api/works/remove/<doi>` Remove a reference.  
`GET /api/works` Get all references.
