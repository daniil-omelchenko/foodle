import json

class HookEntity:
    def __init__(self, json_object):
        arr = json.loads(json_object)
        self.account = arr['account']
        self.object = arr['object']
        self.object_id = arr['object_id']
        self.action = arr['action']
        self.time = arr['time']
        self.verify = arr['verify']