from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Words, Text

from django.forms.models import model_to_dict

from .converter import Defines
d = Defines()


def make_json(query):

    """
    Конвертирует полученные данные из анализатора в удобный человеку формат

    :param query: данные из базы, полученные из запроса к модели
    :return: json с понятными обозначениями (см README)
    """

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

    """
    Класс, который определяет доступные запросы к странице
    
    """

    @staticmethod
    def get(request):
        """
        Возвращает список json объектов 
        
        :param request: 
        :return: см README
        """

        words = [make_json(data) for data in Words.objects.all()]
        return Response(words)


class TextViewSet(APIView):
    
    """
    Класс, который определяет доступные запросы к странице

    """

    @staticmethod
    def get(request):

        """
        Возвращает json объект с текстом

        :param request: 
        :return: json текст
        """

        text = Text.objects.all()
        return Response({'text': _.text} for _ in text)

    @staticmethod
    def post(request):
        """
        Записывает json объект с текстом в базу

        :param request: json текст
        :return: ОК/error message
        """

        # По идее, должен возвращать ОК, если записалось норм, и ошибку бзе падения, если что-то пошло не так,
        # но, видимо, если ошибка слишком глубоко, то он ее не ловит и все равно падает.
        # Влом сейчас отлавливать эти исключения, надо сам анализатор править, чтобы он не работал, как говно)
        
        try:
            Text.create(request.data.get('text'))
            return Response('ok')
        except Exception as err:
            return Response(err)
