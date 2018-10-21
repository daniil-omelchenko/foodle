from domain.serializable import Serializable


class HookObject(object):
    SPOT = 'spot'
    PRODUCT = 'product'


class HookAction(object):
    REMOVED = 'removed'
    ADDED = 'added'
    CHANGED = 'changed'


class HookUpdate(Serializable):

    def __init__(self, account, object, object_id, action, time, verify):
        # type: (str, str, str, str, str, str) -> None
        self.account = account
        self.object = object
        self.object_id = object_id
        self.action = action
        self.time = time
        self.verify = verify

    def serialize(self):
        # type: () -> dict
        return {
            'account': self.account,
            'object': self.object,
            'object_id': self.object_id,
            'action': self.action,
            'time': self.time,
            'verify': self.verify
        }

    @classmethod
    def deserialize(cls, data):
        # type: (dict) -> HookUpdate
        return HookUpdate(
            account=data['account'],
            object=data['object'],
            object_id=data['object_id'],
            action=data['action'],
            time=data['time'],
            verify=data['verify']
        )
