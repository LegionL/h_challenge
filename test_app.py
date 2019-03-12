import pytest
import main
import json

@pytest.fixture
def app():
    app = main.create_app()
    app.debug = True
    return app

def test_hello_world(client):
    res = client.get("/")
    assert b"Hello World" in res.data

def test_query_company(client):
    res = client.get("/api/company/GEOFORM")
    res = json.loads(res.data)
    assert {'company_name': 'GEOFORM',
            'employees': ['Heidi Hudson', 'Olivia Leblanc', 'Kelley Holcomb', 'Holland Sharpe', 'Brandy James'],
            'index': 20} == res

    res = client.get("/api/company/this_is_not_a_real_company")
    res = json.loads(res.data)
    assert {'company_name': 'this_is_not_a_real_company', 'employees': None, 'index': 'not found'} == res


    res = client.get("/api/company/NETBOOK")
    res = json.loads(res.data)
    assert {'company_name': 'NETBOOK', 'employees': None, 'index': 0} == res

def test_query_friend(client):
    res = client.get("/api/friends/Carmella Lambert/Mindy Beasley")
    res = json.loads(res.data) 
    assert res == ['Decker Mckenzie']

def test_query_food(client):
    res = client.get("/api/food/Carmella Lambert")
    res = json.loads(res.data) 
    assert res == {'age': 61, 'fruits': ['orange', 'apple', 'banana', 'strawberry'], 'username': 'Carmella Lambert',
                   'vegetables': []}
