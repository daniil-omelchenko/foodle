class Serializable(object):
    def serialize(self):
        return {}

    def deserialize(self, data):
        return Serializable()
