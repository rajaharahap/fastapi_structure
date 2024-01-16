import base64

from library import *
import os
from library.router import app
from library.db import Db
from pydantic import BaseModel


class item_post(BaseModel):
    x: str
    y: str
class class__(object):
    def __init__(self):
        self.db = Db()

    async def test_get(self, welcome):
        return {
            "output": "welcome to api"
        }
    async def test_post(self, x, y):
        print(x)
        print(y)
        return {
            "code":0,
            "status": "success"
        }
    async def upload_image(self, image:str):
        # data = json.loads(data_absen)
        img_data = base64.b64decode(image)

        pathFile = os.path.abspath(__file__).replace('modules/f_xxx/xxxx.py', '') + f"assets/file_xxx/name_image.jpg"
        with open(pathFile, 'wb+') as f:
            f.write(img_data)
        f.close()
        return {
            "code": 0,
            "status": "success"
        }


"""
list your path url at bottom
example /testing url
test from postman :
url/api/class__/testing
for post method and other method, check tutorial from 
https://fastapi.tiangolo.com/
"""


"=========================================="
"get excample"
@app.get("/api/module__/class__/testing")
async def test_get(welcome):
    ob_data = class__()
    return await ob_data.test_get(welcome)

"post excample"
@app.post("/api/module__/class__/testing_2")
async def submit_(item:item_post):
    ob_data = class__()
    return await ob_data.test_post(item.x, item.y)

"=========================================="

""" fill the api  in this bottom """
