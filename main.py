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
    app.company_people_index = {}
    app.people_name_index = {}
    app.fruit = ['apple', 'banana', 'orange', 'strawberry']
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
                                   'favouriteFood': d['favouriteFood'],
                                   'friends': [fri['index'] for fri in d['friends']]} for d in data}
            app.people = people
        for k, v in app.people.items():
            app.company_people_index[v['company_id']] = app.company_people_index.get(v['company_id'], []) + [k]
            app.people_name_index[v['name']] = k


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
        if app.companies[company_name] not in app.company_people_index:
            return jsonify({'company_name':company_name, 'index': app.companies[company_name], 'employees': None})
        employees = [app.people[e_id]['name'] for e_id in app.company_people_index[app.companies[company_name]]]
        return jsonify({'company_name':company_name, 'index':app.companies[company_name], 'employees': employees})

    @app.route('/api/friends/<p1_name>/<p2_name>', methods = ['GET'])
    def query_friends(p1_name, p2_name): 
        if p1_name == p2_name:
            return jsonify({'msg': 'thats the same person'})
        if p1_name not in app.people_name_index:
            return jsonify({'msg': 'cannot find %s'.format(p1_name)})
        if p2_name not in app.people_name_index:
            return jsonify({'msg': 'cannot find %s'.format(p2_name)})

        p1_id = app.people_name_index[p1_name]
        p2_id = app.people_name_index[p2_name]

        friends = list(set(app.people[p1_id]['friends']).intersection(set(app.people[p2_id]['friends'])))
        res = [app.people[f]['name'] for f in friends if app.people[f]['has_died'] == False and app.people[f]['eyeColor'].lower() == 'brown']
        return jsonify(res)
 
    @app.route('/api/food/<p_name>', methods = ['Get'])
    def query_food(p_name):
        if p_name not in app.people_name_index:
            return jsonify({'msg': 'cannot find %s'.format(p1_name)})
        pid = app.people_name_index[p_name]
        food = app.people[pid]['favouriteFood']
        fruits = []
        vegetables = []
        for f in food:
            if f in app.fruit:
                fruits.append(f)
            else:
                vegetables.append(f)
        return jsonify({'username': app.people[pid]['name'], 'age': app.people[pid]['age'],
                        'fruits': fruits, 'vegetables': vegetables})

    return app


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    app = create_app()
    app.run(host="0.0.0.0", port=port)