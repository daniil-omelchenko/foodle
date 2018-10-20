class Serializable(object):

    def serialize(self):
        # type: () -> dict
        return {}

    @classmethod
    def deserialize(cls, data):
        # type: (dict) -> Serializable
        return Serializable()
