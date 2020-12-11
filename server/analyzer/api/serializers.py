from rest_framework import serializers
from server.analyzer.models import Words, Text


class WordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Words
        fields = ('id', 'word', 'normal_form', 'case', 'gender', 'number',
                  'pers', 'voice', 'role', 'parent_text')


class TextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text
        fields = ('id', 'text')
