# coding=UTF-8
import sys
import os
import warnings as w

from razdel import tokenize, sentenize

from singletonMorph import Singleton
import defines


class Analyzer:

    def __init__(self, file='', txt=''):
        # Конструктор всего класса анализатора. В качестве параметра принимает имя текстового файла с текстом
        # Также имеет обработчик слов русского языка. Обращаться к нему через член класса  --  mrph  --
        if not txt:
            if file:
                try:
                    with open(file, encoding="utf-8") as self.f:
                        self.text = self.f.read()
                except FileNotFoundError:
                    w.warn('File not found')
            else:
                raise ValueError('No arguments has been provided to the class instance')
        else:
            self.text = txt

        self.sentences = list()
        self.mrph = Singleton().get_instance()
        self.s_number = 0

    def split(self, snt=''):
        if not snt:
            if self.text:
                lst = list(sentenize(self.text))
                self.sentences = [_.text for _ in lst]
            else:
                raise KeyError
        else:
            tokens = list(tokenize(snt))
            return [_.text for _ in tokens]
        # print(self.sentences)

    def split_subsnt(self, snt):
        # Метод делит предложение на подпредложения, в кажом из которых есть сказуемое

        sub_snt = ""
        lst = list()
        for lttr in snt:
            if lttr not in defines.SPLITTERS:
                sub_snt += lttr
            else:
                if lttr == "-":
                    if (snt[str.find(snt, "-") - 1] != " ") and (snt[str.find(snt, "-") + 1] != " "):
                        sub_snt += lttr
                        continue
                tks = self.split(sub_snt)
                for wrd in tks:
                    if 'VERB' in self.mrph.parse(wrd)[0].tag:
                        lst.append(sub_snt)
                        sub_snt = ""
                        break
                    else:
                        continue
                sub_snt += lttr
        if sub_snt:
            lst.append(sub_snt)
        # print(lst)
        return lst

    def replace_snt_w_subs(self, snt, lst):
        # Заменяет предложения на подпредложения

        s_n = 0
        if lst[0] != snt:
            index = self.sentences.index(snt)
            self.sentences.remove(snt)
            for sub in lst:
                self.sentences.insert(index, sub)
                index += 1
                s_n += 1
        return s_n

    def reform_sentences(self):
        self.split()
        it = iter(self.sentences)
        for snt in it:
            s_n = self.replace_snt_w_subs(snt, self.split_subsnt(snt))
            if s_n > 0:
                for _ in range(s_n-1):
                    next(it, None)
        # print(self.sentences)
        return self.sentences

    def make_sense(self):
        # Возвращает набор подпредложений, в которых слова размечены по членам предложения

        splitted_sntses = self.reform_sentences()
        result = []
        for snt in splitted_sntses:
            result.append(self.assignment(snt))
        return result
        # self.assignment(splitted_sntses[-3])

    def if_prep(self, snt, ptr):
        # Размечает обстоятельства и дополнения, начинающиеся с предлога
        # Возвращает словарь в котором ключ - номер слова в подпредложении, значение - само слово с его характеристиками
        # и ролью в предложении

        delete_later = dict()
        delete_later.update({ptr: ['PREP']})
        number = ''
        pad = ''
        for wrd in snt[ptr+1:]:
            tag = self.mrph.parse(wrd)[0].tag
            # print(self.mrph.parse(wrd))
            if ('ADJF' in tag) or ('ADJS' in tag) or ('PRTF' in tag):
                # print(tag)
                number = tag.number
                pad = tag.case
                # delete_later.update({snt.index(wrd): [tag, defines.OPR]})
            elif 'NOUN' in tag:
                if ('sing' in number) or ('plur' in number):
                    if (tag.number != number) and (tag.case != pad):
                        for p in self.mrph.parse(wrd)[1:]:
                            if (p.tag.number == number) and (p.tag.case == pad):
                                delete_later.update({snt.index(wrd): [p.tag, defines.OBST]})
                                return delete_later
                            else:
                                continue
                    else:
                        try:
                            sub_tag = self.mrph.parse(snt[snt.index(wrd)+1])[0].tag
                            if ('NOUN' in sub_tag) and ((sub_tag.number == number) and (sub_tag.case == pad)):
                                delete_later.update({snt.index(wrd): [tag, defines.OBST]})
                                continue
                            else:
                                delete_later.update({snt.index(wrd): [tag]})
                                return delete_later
                        except KeyError:
                            pass
                        delete_later.update({snt.index(wrd): [tag]})
                        return delete_later
                else:
                    delete_later.update({snt.index(wrd): [tag, defines.OBST]})
                    return delete_later

    def find_dop_obst(self, static_snt, final_res, tokens):
        # Нахожит обстоятельства и дополнения, начинающиеся с предлога
        # Размечает слова и возвращает словарь слов дополнения/обстоятельства
        # и финальный результат в виде исходного предложения

        dop_obst = dict()
        for wrd in static_snt:
            tag = self.mrph.parse(wrd)[0].tag
            if 'PREP' in tag:
                dop_obst.update(self.if_prep(tokens, static_snt.index(wrd)))
                # print(self.if_prep(tokens, static_snt.index(wrd)))
                try:
                    sub_tag = self.mrph.parse(final_res[static_snt.index(wrd)-1][0])[0].tag
                    if ('ADJF' in sub_tag) or ('ADJS' in sub_tag):
                        # final_res[static_snt.index(wrd)-1].append([sub_tag, defines.OPR])
                        for (w, t) in dop_obst.items():
                            dop_obst[w].append(defines.OPR)
                    # elif 'VERB' in sub_tag:
                    #     for (w, t) in dop_obst.items():
                    #         dop_obst[w].append(defines.OBST)
                    else:
                        for (w, t) in dop_obst.items():
                            dop_obst[w].append(defines.OBST)
                except KeyError:
                    dop_obst[0].append(defines.OBST)

        return [dop_obst, final_res]

    def assignment(self, snt):
        # Метод занимается непосредственно разметкой членов предложения, используя методы, описанные выше

        tokens = [_.text for _ in tokenize(snt)]
        static_snt = [_.text for _ in tokenize(snt)]
        final_res = dict()
        for t in tokens:
            # try:
            #     if ('PNCT' in self.mrph.parse(t)[0]) or ('PRCL' in self.mrph.parse(t)[0]):
            #         final_res.update({tokens.index(t): [t, '']})
            #     else:
            #         final_res.update({tokens.index(t): [t, '']})
            # except AttributeError:
            final_res.update({tokens.index(t): [t, self.mrph.parse(t)[0].normal_form]})
        # print(final_res)
        reduced = self.find_dop_obst(static_snt, final_res, tokens)
        dop_obst = reduced[0]
        final_res = reduced[1]
        # print(tokens, '+++++++++++++++++')
        for (k, v) in dop_obst.items():
            # print(k)
            # print(v)
            final_res[k].append(v)
            tokens.remove(final_res[k][0])
        # print(tokens, '==================')
        for wrd in tokens:
            tag = self.mrph.parse(wrd)[0].tag
            for t in self.mrph.parse(wrd):
                # sub_tag = ''
                try:
                    sub_tag = self.mrph.parse(final_res[static_snt.index(wrd) - 1][0])[0].tag
                    # print(sub_tag)
                    if ('ADJF' in sub_tag) or ('ADJS' in sub_tag):
                        if (('sing' in sub_tag.number) or ('plur' in sub_tag.number)) \
                                and (t.tag.number == sub_tag.number)\
                                and (t.tag.case == sub_tag.case):
                            tag = t.tag
                            # print(tag)
                except KeyError:
                    try:
                        sub_tag = self.mrph.parse(final_res[static_snt.index(wrd) + 1][0])[0].tag
                        if ('ADJF' in sub_tag) or ('ADJS' in sub_tag):
                            if (('sing' in sub_tag.number) or ('plur' in sub_tag.number)) \
                                    and (sub_tag.number == tag.number)\
                                    and (t.tag.case == sub_tag.case):
                                tag = t.tag
                    except KeyError:
                        pass
            if ('NOUN' in tag) and ('nomn' not in tag.case):
                try:
                    sub_tag = self.mrph.parse(final_res[static_snt.index(wrd) + 1][0])[0].tag
                    if 'VERB' not in sub_tag:
                        final_res[static_snt.index(wrd)].append([tag, defines.DOP])
                    else:
                        final_res[static_snt.index(wrd)].append([tag, defines.OBST])
                except KeyError:
                    final_res[static_snt.index(wrd)].append([tag, defines.DOP])
                tokens.remove(wrd)
        # for (k, v) in dop_obst.items():
        #     final_res[k].append(v)
        #     tokens.remove(final_res[k][0])
        # print(final_res)
        # print(tokens, '-------------------')
        for wrd in tokens:
            info = self.mrph.parse(wrd)[0]
            if ('VERB' in info.tag) and (wrd != info.normal_form):
                final_res[static_snt.index(wrd)].append([info.tag, defines.SKAZ])
                continue
            if 'INFN' in info.tag:
                final_res[static_snt.index(wrd)].append([info.tag, defines.OBST])
                continue
            if ('NOUN' in info.tag) and (info.tag.case == 'nomn'):
                try:
                    if 'VERB' not in self.mrph.parse(final_res[static_snt.index(wrd) - 1][0])[0].tag:
                        final_res[static_snt.index(wrd)].append([info.tag, defines.POD])
                        continue
                    else:
                        final_res[static_snt.index(wrd)].append([info.tag, defines.OBST])
                        continue
                except KeyError:
                    final_res[static_snt.index(wrd)].append([info.tag, defines.POD])
                    continue
            if ('NOUN' in info.tag) and (info.tag.case != 'nomn'):
                final_res[static_snt.index(wrd)].append([info.tag, defines.DOP])
                continue
            if ('ADJS' in info.tag) or ('ADJF' in info.tag):
                final_res[static_snt.index(wrd)].append([info.tag, defines.OPR])
                continue
            if ('NPRO' in info.tag) and (info.tag.case == 'nomn'):
                final_res[static_snt.index(wrd)].append([info.tag, defines.POD])
                continue
            if 'ADVB' in info.tag:
                final_res[static_snt.index(wrd)].append([info.tag, defines.OBST])
                continue
            final_res[static_snt.index(wrd)].append([info.tag, defines.UNKN])
        # print(final_res)
        return final_res
        # print(tokens)
        # print(self.mrph.parse(final_res[1][0])[0].tag)

    def close(self):
        # Закрывает файл с текстом

        self.f.close()
