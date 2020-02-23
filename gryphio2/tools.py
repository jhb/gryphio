from collections.abc import Mapping

def searchkeys(obj,*args,default=None):
    for key in args:
        if isinstance(obj, Mapping):
            if key in obj:
                return obj[key]
        if hasattr(obj, key):
            return getattr(obj,key)
    return default


a = 'foo'
print(searchkeys({'blub':13},'blub',default=''))
