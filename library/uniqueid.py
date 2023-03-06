import uuid

class Uniqueid(object):
    def generate_id(self):
        return str(uuid.uuid1())