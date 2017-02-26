import json
from tests.scenarios import web_scenario


@web_scenario
def test_html(context):
    response = context.http.get('/html')
    response.status_code.should.equal(200)
    response.data.should.equal('<html><head><title>p4rr0t007</title></head><body><h1>p4rr0t007</h1></body></html>')
    response.headers.should.have.key('Content-Type').being.equal('text/html')


@web_scenario
def test_json(context):
    response = context.http.get('/json')
    response.status_code.should.equal(200)
    response.headers.should.have.key('Content-Type').being.equal('application/json')
    response.data.should.equal(json.dumps({
        "name": "p4rr0t007"
    }, indent=2))


@web_scenario
def test_text(context):
    response = context.http.get('/text')
    response.status_code.should.equal(200)
    response.headers.should.have.key('Content-Type').being.equal('text/plain')
    response.data.should.equal('text')


@web_scenario
def test_error(context):
    response = context.http.get('/error')
    response.headers.should.have.key('Content-Type').being.equal('text/html')
    response.data.should.equal('<html><head><title>server error</title></head><body><h1>server error</h1></body></html>')
    response.status_code.should.equal(500)
