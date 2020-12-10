from django.db import models


class Text(models.Model):

    text = models.TextField(blank=False)

    def __str__(self):

        return self.text


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
