# coding=UTF-8

from razdel import tokenize, sentenize

from singletonMorph import Singleton
import defines


class Analyzer:

    def __init__(self, file):

        self.f = open(file, encoding="utf-8")
        self.text = self.f.read()
        self.sentences = list()

        self.mrph = Singleton().get_instance()

        self.s_number = 0

        self.doc = ""

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
        # print(snt)
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
        splitted_sntses = self.reform_sentences()
        # for snt in splitted_sntses:
        #     self.assignment(snt)
        self.assignment(splitted_sntses[14])

    def if_prep(self, snt, ptr):
        delete_later = dict()
        delete_later.update({ptr: ['PREP']})
        number = ''
        pad = ''
        for wrd in snt[ptr+1:]:
            tag = self.mrph.parse(wrd)[0].tag
            # print(self.mrph.parse(wrd))
            if ('ADJF' in tag) or ('ADJS' in tag) or ('PRTF' in tag):
                print(tag)
                number = tag.number
                pad = tag.case
                delete_later.update({snt.index(wrd): [tag, 'определение']})
            elif 'NOUN' in tag:
                if ('sing' in number) or ('plur' in number):
                    if (tag.number != number) and (tag.case != pad):
                        for p in self.mrph.parse(wrd)[1:]:
                            if (p.tag.number == number) and (p.tag.case == pad):
                                delete_later.update({snt.index(wrd): [p.tag]})
                                return delete_later
                            else:
                                continue
                    else:
                        try:
                            sub_tag = self.mrph.parse(snt[snt.index(wrd)+1])[0].tag
                            if ('NOUN' in sub_tag) and ((sub_tag.number == number) and (sub_tag.case == pad)):
                                delete_later.update({snt.index(wrd): [tag]})
                                continue
                            else:
                                delete_later.update({snt.index(wrd): [tag]})
                                return delete_later
                        except KeyError:
                            pass
                        delete_later.update({snt.index(wrd): [tag]})
                        return delete_later
                else:
                    delete_later.update({snt.index(wrd): [tag]})
                    return delete_later

    def assignment(self, snt):
        tokens = [_.text for _ in tokenize(snt)]
        static_snt = [_.text for _ in tokenize(snt)]
        final_res = dict()
        for t in tokens:
            final_res.update({tokens.index(t): [t]})
        print(final_res)
        dop_obst = dict()
        for wrd in static_snt:
            tag = self.mrph.parse(wrd)[0].tag
            if 'PREP' in tag:
                dop_obst.update(self.if_prep(tokens, static_snt.index(wrd)))
                # print(self.if_prep(tokens, static_snt.index(wrd)))
                try:
                    sub_tag = self.mrph.parse(final_res[static_snt.index(wrd)-1][0])[0].tag
                    if ('ADJF' in sub_tag) or ('ADJS' in sub_tag):
                        final_res[static_snt.index(wrd)-1].append([sub_tag, "определение"])
                        for (w, t) in dop_obst.items():
                            dop_obst[w].append("определение")
                    elif 'VERB' in sub_tag:
                        for (w, t) in dop_obst.items():
                            dop_obst[w].append("обстоятельство")
                except KeyError:
                    pass
        for (k, v) in dop_obst.items():
            print(k)
            print(v)
            final_res[k].append(v)
            tokens.remove(final_res[k][0])
        print(tokens)
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
                            print(tag)
                except KeyError:
                    sub_tag = self.mrph.parse(final_res[static_snt.index(wrd) + 1][0])[0].tag
                    if ('ADJF' in sub_tag) or ('ADJS' in sub_tag):
                        if (('sing' in sub_tag.number) or ('plur' in sub_tag.number)) \
                                and (sub_tag.number == tag.number)\
                                and (t.tag.case == sub_tag.case):
                            tag = t.tag
            if ('NOUN' in tag) and ('nomn' not in tag.case):
                final_res[static_snt.index(wrd)].append([tag, 'дополнение'])
        print(final_res)
        print(tokens)
        print(self.mrph.parse(final_res[1][0])[0].tag)

    def close(self):
        self.f.close()
