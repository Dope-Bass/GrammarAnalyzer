class Defines:

    def __init__(self):

        self.speech_parts = {
            'NOUN': 'имя существительное',
            'ADJF': 'полное прилагательное',
            'ADJS': 'краткое прилагательное',
            'COMP': 'компаратив',
            'VERB': 'глагол',
            'INFN': 'инфинитив',
            'PRTF': 'полное причастие',
            'PRTS': 'краткое причастие',
            'GRND': 'деепричастие',
            'NUMR': 'числительное',
            'ADVB': 'наречие',
            'NPRO': 'местоимение',
            'PRED': 'предикатив',
            'PREP': 'предлог',
            'CONJ': 'союз',
            'PRCL': 'частица',
            'INTJ': 'междометие',
            None  : 'знак препинания'
        }

        self.gender = {
            'masc': 'мужской род',
            'femn': 'женский род',
            'neut': 'средний род',
            'ms-f': 'смешанный род'
        }

        self.number = {
            'sing': 'единственное число',
            'plur': 'множественное число'
        }

        self.case = {
            'nomn': 'именительный падеж',
            'gent': 'родительный падеж',
            'datv': 'дательный падеж',
            'accs': 'винительный падеж',
            'ablt': 'творительный падеж',
            'loct': 'предложный падеж',
            'voct': 'звательный падеж'
        }

        self.person = {
            '1per': 'первое лицо',
            '2per': 'второе лицо',
            '3per': 'третье лицо'
        }

        self.voice = {
            'actv': 'действительный залог',
            'pssv': 'страдательный залог'
        }