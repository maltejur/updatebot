#!/usr/bin/env python3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import json
import requests

from apis.apikey import BUGZILLA_URL, APIKEY


def sq(s):
    return '[' + s + ']'


def kw(s):
    return sq('3pl-' + s)


def fileBug(product, component, summary, description):
    data = {
        'version': "unspecified",
        'op_sys': "unspecified",

        'product': product,
        'component': component,
        'type': "enhancement",
        'summary': summary,
        'description': description,
        'whiteboard': kw('filed'),
        'cc': ['tom@mozilla.com']
    }

    r = requests.post(BUGZILLA_URL + "bug?api_key=" + APIKEY, json=data)
    j = json.loads(r.text)
    if 'id' in j:
        return j['id']

    raise Exception(j)


def commentOnBug(bugID, comment):
    data = {
        'comment': comment
    }

    r = requests.post(
        BUGZILLA_URL + "bug/" + str(bugID) + "/comment?api_key=" + APIKEY,
        json=data
    )
    j = json.loads(r.text)
    if 'id' in j:
        return j['id']

    raise Exception(j)