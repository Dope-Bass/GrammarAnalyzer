from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Words, Text

from django.forms.models import model_to_dict

from .converter import Defines
d = Defines()


def make_json(query):

    model_dict = model_to_dict(query)

    json_list = [
        'word',
        'normal_form',
        'speech_part',
        'case',
        'gender',
        'number',
        'pers',
        'voice',
        'role'
    ]
    def_list = {
        'word': None,
        'normal_form': None,
        'speech_part': d.speech_parts,
        'case': d.case,
        'gender': d.gender,
        'number': d.number,
        'pers': d.person,
        'voice': d.voice,
        'role': None
    }
    res = {}
    for arg in json_list:
        if not def_list[arg]:
            res[arg] = model_dict[arg]
        else:
            try:
                res[arg] = def_list[arg][model_dict[arg]]
            except KeyError:
                res[arg] = model_dict[arg]

    return res


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
        try:
            Text.create(request.data.get('text'))
            return Response('ok')
        except Exception as err:
            return Response(err)
