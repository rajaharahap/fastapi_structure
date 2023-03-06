from library import *
import os
from library.router import app
from library.db import Db

class class__(object):
    def __init__(self):
        self.db = Db()

    def test_data(self, welcome):
        return {
            "output": "welcome to api"
        }


"""
list your path url at bottom
example /testing url
test from postman :
url/api/class__/testing
for post method and other method, check tutorial from 
https://fastapi.tiangolo.com/
"""
@app.get("/api/class__/testing")
async def get_data(welcome):
    ob_data = class__()
    return ob_data.test_data(welcome)