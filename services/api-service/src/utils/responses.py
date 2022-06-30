

def response(action, data, object=None, url=None, has_more=None):
    if action == 'list':
        return {
            "object": object,
            "url": url,
            "has_more": has_more,
            "data":  data
        }
    return data
