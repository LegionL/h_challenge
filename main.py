import os
import json
from flask import Flask, jsonify
from flask_cors import CORS


def create_app(config=None):
    app = Flask(__name__)
    app.config['companies'] = 'resources/companies.json'
    app.config['people'] = 'resources/people.json'
    app.companies = None
    app.people = None
    app.people_index = {}
    CORS(app)

    def load_json_file():
        with open(app.config['companies']) as f:
            data = json.load(f)
            companies = {d['company']: d['index'] for d in data}
            app.companies = companies
        with open(app.config['people']) as f: 
            data = json.load(f)
            people = {d['index']: {'name': d['name'], 'age': d['age'], 'address': d['address'],
                                   'phone': d['phone'], 'company_id': d['company_id'],
                                   'has_died': d['has_died'], 'eyeColor': d['eyeColor'], 
                                   'friends': [fri['index'] for fri in d['friends']]} for d in data}
            app.people = people
        for k, v in app.people.items():
            app.people_index[v['company_id']] = app.people_index.get(v['company_id'], []) + [k]


    load_json_file()

    @app.route("/")
    def hello_world():
        return "Hello World"

    @app.route("/api/update")
    def update():
        load_json_file()
        return 'success'

    @app.route('/api/company/<company_name>', methods = ['GET'])
    def query_company(company_name):
        if company_name not in app.companies:
            return jsonify({'company_name':company_name, 'index': 'not found', 'employees': None})
        if app.companies[company_name] not in app.people_index:
            return jsonify({'company_name':company_name, 'index': app.companies[company_name], 'employees': None})
        employees = [app.people[e_id]['name'] for e_id in app.people_index[app.companies[company_name]]]



        return jsonify({'company_name':company_name, 'index':app.companies[company_name], 'employees': employees})


    return app


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    app = create_app()
    app.run(host="0.0.0.0", port=port)