import json
from pprint import pprint

with open('resources/companies.json') as f:
    data = json.load(f)
companies = {d['company']: d['index'] for d in data}
pprint(companies)


with open('resources/people.json') as f:
    data = json.load(f)

people = {d['index']: {'name': d['name'], 'age': d['age'], 'address': d['address'],
					   'phone': d['phone'], 'company_id': d['company_id'],
					   'has_died': d['has_died'], 'eyeColor': d['eyeColor'], 
					   'friends': [fri['index'] for fri in d['friends']]} for d in data}
pprint(people[3])

import collections
c = [v['company_id'] for k, v in people.items()]

print(set(range(0,100)) - set(c))
