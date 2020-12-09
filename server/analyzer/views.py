from django.http import HttpResponse
import sys
import os
sys.path.append(sys.path[0].replace('server', ''))

import c_analyzer as a


def resp(request):

    try:
        return HttpResponse(a.Analyzer(os.path.join(sys.path[0].replace('server', ''), 'test.txt')).make_sense())
    except ModuleNotFoundError:
        print('cannot find')
    return 1

# Create your views here.
