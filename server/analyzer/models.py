import os
import sys

from django.db import models

import c_analyzer as a

general_defs = {
    'word': 0,
    'normal_form': 1,
    'tag_list': 2
}

tag_list_defs = {
    'tag': 0,
    'role': 1
}


class Text(models.Model):

    """
    Модель для базы с текстом. Обозначает набор полей в каждой строке таблицы

    """

    text = models.TextField(blank=False)

    @classmethod
    def create(cls, t):
        """
        Метод, который создает поле в таблице текста. Также анализирует текст и создает поля в таблице слов

        :param t: текст
        :return: void
        """

        # При записи нового текста старый удаляется.
        # С ним трутся все слвоа из таблицы слов, которые с этим текстом связаны по внешнему ключу

        for instance in cls.objects.all():
            instance.delete()

        text = cls(text=t)
        text.save()
        for dictionary in a.Analyzer(txt=t).make_sense():
            for index in dictionary.keys():
                print(dictionary[index])
                Words.create(dictionary[index], text)

    def __str__(self):

        return {
            'text': self.text
        }


class Words(models.Model):

    """
    Модель для базы со словами. Обозначает набор полей в каждой строке таблицы

    """

    word = models.TextField()
    normal_form = models.TextField()

    # NOUN or VERB or ADJF or PREP and so on
    speech_part = models.TextField(default=None, null=True)

    case = models.TextField(default=None, null=True)

    # masc or femn or neut or ms-f as masc|femn at the same time
    gender = models.TextField(default=None, null=True)

    # plur or sing
    number = models.TextField(default=None, null=True)

    # 1per or 2per or 3per
    pers = models.TextField(default=None, null=True)

    # actv or pssv
    voice = models.TextField(default=None, null=True)

    # role in sentence
    role = models.TextField(default=None)

    # binding to text that word is from
    parent_text = models.ForeignKey(Text, on_delete=models.CASCADE)

    @classmethod
    def create(cls, wrd, text):

        """
        Создает строку в таблице слов

        :param wrd: слово (как оно выглядит см README)
        :param text: указатель на строку в таблице текста, с которой связаны слова
        :return: void
        """

        if not isinstance(wrd[general_defs['tag_list']][tag_list_defs['tag']], str):

            instance = cls(
                word=wrd[general_defs['word']],
                normal_form=wrd[general_defs['normal_form']],
                speech_part=wrd[general_defs['tag_list']][tag_list_defs['tag']].POS,
                case=wrd[general_defs['tag_list']][tag_list_defs['tag']].case,
                gender=wrd[general_defs['tag_list']][tag_list_defs['tag']].gender,
                number=wrd[general_defs['tag_list']][tag_list_defs['tag']].number,
                pers=wrd[general_defs['tag_list']][tag_list_defs['tag']].person,
                voice=wrd[general_defs['tag_list']][tag_list_defs['tag']].voice,
                role=wrd[general_defs['tag_list']][tag_list_defs['role']],
                parent_text=text
            )
            instance.save()
        else:
            instance = cls(
                word=wrd[general_defs['word']],
                normal_form=wrd[general_defs['normal_form']],
                role=wrd[general_defs['tag_list']][tag_list_defs['role']],
                parent_text=text
            )
            instance.save()

    def __str__(self):

        return {
            'word': self.word,
            'normal_form': self.normal_form,
            'speech_part': self.speech_part,
            'case': self.case,
            'gender': self.gender,
            'number': self.number,
            'person': self.pers,
            'voice': self.voice,
            'role': self.role
        }
