# -*- coding: utf-8 -*-

import os

import json
import hashlib
import logging
import traceback

import htmlmin

from flask import Flask, Response, request, render_template, url_for
from flask.ext.session import Session


from p4rr0t007 import settings
from p4rr0t007.lib.core import xor


def full_url_for(*args, **kw):
    return "/".join([
        settings.BASE_URL.rstrip('/'),
        url_for(*args, **kw).lstrip('/'),
    ])


class Application(Flask):
    def __init__(self, app_node, static_folder=None, template_folder=None, settings_module='p4rr0t007.settings'):
        super(Application, self).__init__(
            __name__,
            static_folder=static_folder or app_node.dir.join('static/dist'),
            template_folder=template_folder or app_node.dir.join('templates')
        )
        self.config.from_object(settings_module)
        self.app_node = app_node
        self.sesh = Session(self)
        self.secret_key = self.config['SECRET_KEY']

    def json_handle_weird(self, obj):
        logging.warning("failed to serialize %s", obj)
        return bytes(obj)

    def json_response(self, data, code=200, headers={}):
        headers = headers.copy()
        headers['Content-Type'] = 'application/json'
        payload = json.dumps(data, indent=2, default=self.json_handle_weird)
        return Response(payload, status=code, headers=headers)

    def template_response(self, name, context=None, content_type='text/html', code=200, minify=True):
        context = context or {}
        context['full_url_for'] = full_url_for
        context['seed'] = xor(
            hashlib.sha512("".join((repr(request.headers), repr(request.url), repr(request.method), repr(request.cookies)))).digest(),
            os.urandom(128),
        ).encode('hex')[27:60]

        utf8 = render_template(name, **context)
        if minify:
            mini = htmlmin.minify(utf8, remove_comments=True, remove_empty_space=True, remove_all_empty_space=True, reduce_boolean_attributes=True, remove_optional_attribute_quotes=True)
        else:
            mini = utf8

        return Response(mini, headers={
            'Content-Type': content_type,
            'Content-Encoding': 'UTF-8',
        }, status=code)

    def text_response(self, data, code=200, headers={}):
        return Response(data, status=code, headers={
            'Content-Type': 'text/plain'
        })

    def get_json_request(self):
        try:
            data = json.loads(request.data)
        except ValueError:
            logging.exception(
                "Trying to parse json body in the %s to %s",
                request.method, request.url,
            )
            data = {}

        return data

    def handle_exception(self, e):
        # tb = traceback.format_exc(e)
        logging.exception('failed to handle {} {}'.format(request.method, request.url))
        return self.template_response('500.html', code=500)
