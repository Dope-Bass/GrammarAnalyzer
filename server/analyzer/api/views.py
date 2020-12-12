import sys
import os

from django.http import HttpResponse
import c_analyzer as a

from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Words, Text


def make_json(query):
    return {
        'word': query.word,
        'normal_form': query.normal_form,
        'speech_part': query.speech_part,
        'case': query.case,
        'gender': query.gender,
        'number': query.number,
        'person': query.pers,
        'voice': query.voice,
        'role': query.role
    }


class WordViewSet(APIView):

    @staticmethod
    def get(request):

        words = [make_json(data) for data in Words.objects.all()]
        return Response(words)


class TextViewSet(APIView):

    @staticmethod
    def get(request):

        text = Text.objects.all()
        return Response({'text': _.text} for _ in text)

    @staticmethod
    def post(request):

        Text.create(request.data.get('text'))
        return Response('ok')


def resp(request):

    try:
        return HttpResponse(a.Analyzer(os.path.join(sys.path[0].replace('server', ''), 'test.txt')).make_sense())
    except ModuleNotFoundError:
        print('cannot find')
    return 1

# Create your views here.
