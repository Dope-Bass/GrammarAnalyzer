from rest_framework import serializers
from server.analyzer.models import Words, Text


class WordsSerializer(serializers.ModelSerializer):

    """
    Сериализатор для удобного представления модели в виде json.
    По идее, работает только в админке сервера. Больше нигде не юзал

    """

    class Meta:
        model = Words
        fields = ('id', 'word', 'normal_form', 'case', 'gender', 'number',
                  'pers', 'voice', 'role', 'parent_text')


class TextSerializer(serializers.ModelSerializer):

    """
    Сериализатор для удобного представления модели в виде json.
    По идее, работает только в админке сервера. Больше нигде не юзал

    """

    class Meta:
        model = Text
        fields = ('id', 'text')
