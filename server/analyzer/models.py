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

    text = models.TextField(blank=False)

    @classmethod
    def create(cls, t):

        for instance in cls.objects.all():
            instance.delete()

        text = cls(text=t)

        for w in a.Analyzer(os.path.join(sys.path[0].replace('server', ''), 'test.txt')).make_sense():
            Words.create(w, text)

    def __str__(self):

        return {
            'text': self.text
        }


class Words(models.Model):

    word = models.TextField()
    normal_form = models.TextField()
    case = models.TextField(default='')

    # masc or femn or neut or ms-f as masc|femn at the same time
    gender = models.TextField(default='')

    # plur or sing
    number = models.TextField(default='')

    # 1per or 2per or 3per
    pers = models.TextField(default='')

    # actv or pssv
    voice = models.TextField(default='')

    # role in sentence
    role = models.TextField(default='')

    # binding to text that word is from
    parent_text = models.ForeignKey(Text, on_delete=models.CASCADE)

    @classmethod
    def create(cls, wrd, text):

        cls(
            word=wrd[general_defs['word']],
            normal_form=wrd[general_defs['normal_form']],
            case=wrd[general_defs['tag_list']][tag_list_defs['tag']].case,
            gender=wrd[general_defs['tag_list']][tag_list_defs['tag']].gender,
            number=wrd[general_defs['tag_list']][tag_list_defs['tag']].number,
            pers=wrd[general_defs['tag_list']][tag_list_defs['tag']].person,
            voice=wrd[general_defs['tag_list']][tag_list_defs['tag']].voice,
            role=wrd[general_defs['tag_list']][tag_list_defs['role']],
            parent_text=text
        )

    def __str__(self):

        return {
            'word': self.word,
            'normal_form': self.normal_form,
            'case': self.case,
            'gender': self.gender,
            'number': self.number,
            'person': self.pers,
            'voice': self.voice,
            'role': self.role
        }
