p4rr0t007
=========


installing
----------

.. code:: bash

   pip install p4rr0t007


5-minute example
----------------

create ``yourapp`` folder
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

    mkdir -p yourapp/{templates,static}
    touch yourapp/__init__.py
    touch yourapp/application.py


create an ``index.html`` template
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

    mkdir -p yourapp/{templates,static}
    cat > yourapp/templates/index.html << EOF
    <html>
        <head>
            <title>hello world</title>
        </head>
        <body>
            <h1>hello world</h1>
            <pre>{{ now }}</pre>
            <br />
            <hr />
            <br />
            <a href="{{ url_for('html') }}">html</a>
            <a href="{{ url_for('text') }}">text</a>
            <a href="{{ url_for('json') }}">json</a>
        </body>
    </html>
    EOF


create the flask app using p4rr0t007.Application
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


.. code:: python

   cat > yourapp/application.py << EOF

   import os
   from plant import Node
   from datetime import datetime
   from p4rr0t007.web import Application


   node = Node(__file__)

   server = Application(
       node,
       static_folder='~/yourapp/static'.
       template_folder='~/yourapp/templates'.
       settings_module='yourapp.config',
   )

   @server.route('/')
   def html():
       return app.template_response('index.html', {'now': datetime.utcnow().isoformat()})


   @server.route('/text')
   def text():
       return app.text_response('text')


   @server.route('/json')
   def json():
       return app.json_response({
           'name': 'p4rr0t007'
       }, code=200)


   if __name__ == '__main__':
       settings.update(
           SECRET_KEY=os.urandom(32).encode('base64').strip(),
       )
       server.run(debug=True)

   EOF
