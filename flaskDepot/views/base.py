from flaskDepot import app
from flaskDepot.models import *
from flask import request, redirect, url_for, render_template
from flask_wtf import Form
from wtforms import HiddenField
from urlparse import urlparse, urljoin


def get_redirect_target():
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return target


def is_safe_url(target):
    if target == '':
        return False
    if target[0] == '/':
        return True
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc


class RedirectForm(Form):
    next = HiddenField()

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        if not self.next.data:
            self.next.data = get_redirect_target() or ''

    def redirect(self, endpoint='index', url=None, **values):
        if is_safe_url(self.next.data):
            return redirect(self.next.data)
        target = get_redirect_target() or url
        return redirect(target or url_for(endpoint, **values), code=303)