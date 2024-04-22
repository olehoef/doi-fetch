from flask import Flask
from urllib.parse import unquote
import json
from doi_fetch.utils.crossrefRequests import requestWork

def rest(project, port):
    app = Flask(__name__)
    print("Flask app is running...")

    @app.route('/api/works/add/<path:encoded_doi>', methods=['GET'])
    def add(encoded_doi):
        doi = unquote(encoded_doi)
        print(f"Received DOI: {doi}")
        requestedWork = project.searchWork(doi)
        if requestedWork != None:
            response = {"message": f"work {doi} exists already"}
        else:
            requestedWork = requestWork(doi, project)
            
            if requestedWork != None:
                project.addWork(requestedWork)
                project.save()
                response = {"message": f"work {doi} successfully added"}
            else:
                response = {"message": f"work {doi} not found"}
        return response

    @app.route('/api/works/remove/<path:encoded_doi>', methods=['GET'])
    def remove(encoded_doi):
        doi = unquote(encoded_doi)
        print(f"Received DOI: {doi}")
        deletedWork = project.removeWork(doi)
        if deletedWork == None:
            response = {"message": "work doesn't exist"}
        else:
            project.save()
            response = {"message": f"work {deletedWork.doi} successfully removed"}
        return response

    @app.route('/api/works', methods=['GET'])
    def getAllWorks():
        
        
        response = project.respond()
        
        return json.dumps(response)
    
    app.run(debug=False, port=port)

