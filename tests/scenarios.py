from sure import scenario

from plant import Node
from p4rr0t007.web import Application


def prepare_app(context):
    context.node = Node(__file__)
    context.app = Application(context.node)

    @context.app.route('/html')
    def html():
        return context.app.template_response('index.html')

    @context.app.route('/text')
    def text():
        return context.app.text_response('text')

    @context.app.route('/json')
    def json():
        return context.app.json_response({
            'name': 'p4rr0t007'
        })

    @context.app.route('/error')
    def error():
        raise IOError('emulating a 500')

    context.http = context.app.test_client()

web_scenario = scenario(prepare_app)
