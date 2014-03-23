import json
import collections
from subprocess import call


def convert(data):
    if isinstance(data, basestring):
        return str(data)
    elif isinstance(data, collections.Mapping):
        return dict(map(convert, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert, data))
    else:
        return data



f = open('data.json', 'r')
d = json.load(f)

for i in range(0, len(d)):

    try:
        date_fix = (d[i]['EVENT START DATE'].split(" "))[0].split('/')
        d[i]['EVENT START DATE'] = date_fix[2] + "-" + date_fix[1]+ "-" + date_fix[0]

        request = "curl -XPOST \'http://localhost:9200/cdd/disasters/\' -d \'" \
                  + str(convert(d[i])).replace('\'', '\"') + "\'"

        print request
        exit(0)
        # call(request, shell=True)
    except Exception:

        print "\n\nfailed on : " + str(i)

