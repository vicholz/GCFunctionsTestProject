import requests
import json

def main(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    request_json = request.get_json()
    if request.args and 'wake' in request.args and 'url' in request.args:
        r = wake(request.args.get('url'),request.args.get('wake'))
        print(r)
        return r
    elif request.args and 'url' in request.args:
        r = wake(request.args.get('url'),"ALL")
        print(r)
        return r
    else:
        return f'Wake CSV list and/or URL not specified. Nothing to do.'

def wake(url, wakedata):
    wakelist = wakedata.split(",")
    data = getdata(url)
    for w in wakelist:
        for d in data:
            if w == "ALL":
                data[d]["wake"] = true
            elif w.upper() == data[d] or w.upper() == data[d]["mac"]:
                data[d]["wake"] = true
                
    r = requests.post(url, data=json.dumps(data))
    return r.text
    
def getdata(url):
    r = requests.get(url, verify=False, timeout=60).json()
    return r