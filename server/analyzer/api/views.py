import sys
import os

from django.http import HttpResponse
import c_analyzer as a

from rest_framework.views import APIView
from rest_framework.response import Response
from server.analyzer.models import Words, Text


class WordViewSet(APIView):

    def get(self, request):

        words = [data for data in Words.objects.all()]
        return Response(words)


class TextViewSet(APIView):

    @staticmethod
    def get(self, request):

        text = Text.objects.all()
        return Response(text)

    def post(self, request):
        pass


def resp(request):

    try:
        return HttpResponse(a.Analyzer(os.path.join(sys.path[0].replace('server', ''), 'test.txt')).make_sense())
    except ModuleNotFoundError:
        print('cannot find')
    return 1

# Create your views here.
