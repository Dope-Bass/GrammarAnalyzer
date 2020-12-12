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
        try:
            Text.create(request.data.get('text'))
            return Response('ok')
        except Exception as err:
            return Response(err)
