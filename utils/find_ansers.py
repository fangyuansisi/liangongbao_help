import pandas as pd
import json
import re
import difflib
import os
from LgbConfig import EXCEL_QUESTION_BANK_PATH, ANSWER_QUESTION_BANK_PATH, PAPER_QUESTION_BANK_PATH, WRONG_QUESTIONS_PATH


def get_equal_rate(str1, str2):
    return difflib.SequenceMatcher(None, str1, str2).quick_ratio()


class FindAnswers:
    def __init__(self) -> None:
        self.excel_question_bank = None
        self.answer_question_bank = []
        self.paper_question_bank = []
        self.open_excel_bank()
        self.open_answer_bank()
        self.open_paper_bank()

    def open_excel_bank(self):
        self.excel_question_bank = pd.read_excel(
            EXCEL_QUESTION_BANK_PATH, sheet_name='Sheet1')
        self.excel_question_bank.columns = ['id', 'timu', 'daan', 'text']
        self.excel_question_bank = self.excel_question_bank.dropna(
            axis=0, how='any')

    def open_answer_bank(self):
        with open(ANSWER_QUESTION_BANK_PATH, 'r', encoding='utf-8') as f:
            reg_str = ".*?([\u4E00-\u9FA5]+).*?"
            for line in f:
                if line == '':
                    continue
                line = line.strip('\n').split("######")
                try:
                    tmp_timu = ''.join(re.findall(reg_str, line[0]))
                    tmp_daan = json.loads(line[1])
                except:
                    continue  # 舍弃
                self.answer_question_bank.append([tmp_timu, tmp_daan])

    def open_paper_bank(self):
        with open(PAPER_QUESTION_BANK_PATH, 'r', encoding='utf-8') as f:
            for line in f:
                if line == '':
                    continue
                line = line.strip('\n').strip('\u3000\u3000')
                self.paper_question_bank.append(line)

    def get_result(self, quesTypeStr, content, answerOptions):
        find_option, find_opt_text = self._find_excel(quesTypeStr, content, answerOptions)
        # if find_option and find_opt_text:
        #     return find_option, find_opt_text
        find_option, find_opt_text = self._find_answer(quesTypeStr, content, answerOptions)
        # if find_option and find_opt_text:
        #     return find_option, find_opt_text
        delimiter = "######"
        text = quesTypeStr + delimiter + content + delimiter + str(answerOptions)
        self.collection_wrong_questions(text)  # 没找到得题自动加入错题本
        self._find_paper(quesTypeStr, content, answerOptions)
        return [], []

    def match_question_type(self, quesTypeStr, answer_match):
        if quesTypeStr == '单选题' or quesTypeStr == '判断题':
            answer_match = [value for value in answer_match if len(value) == 1]
        elif quesTypeStr == '多选题':
            answer_match = [value for value in answer_match if len(value) > 1]
        else:
            pass

        if answer_match:
            return answer_match[0]
        else:
            return []

    def option2text(self, answer_match, answerOptions):
        tmp = []
        for v in answer_match:
            tmp.append(answerOptions[ord(v)-65])
        return tmp

    def text2option(self, answer_match, answerOptions):
        tmp = []
        tmp_dict = {}
        for i, v in enumerate(answerOptions):
            tmp_dict[v] = chr(65+i)
        for v in answer_match:
            tmp.append(tmp_dict.get(v))
        return tmp

    def get_puer_text(self, content):
        reg_str = ".*?([\u4E00-\u9FA5]+).*?"  # 提取中文,放弃特殊符号
        return re.findall(reg_str, content)

    def _find_excel(self, quesTypeStr, content, answerOptions):
        res = self.get_puer_text(content)
        puer_content_chn_reg_str = '.*'.join(res)
        answer = self.excel_question_bank[self.excel_question_bank['timu'].str.contains(
            puer_content_chn_reg_str,
            case=False,  # 是否匹配大小写
            na=True,  # 默认对空值不处理，即输出结果还是 NaN
            regex=True)]
        if answer.empty:
            return [], []
        answer_match = []
        for i, tmp in enumerate(answer.loc[:, 'timu']):
            rate = get_equal_rate(content, tmp)
            answer_match.append((rate, answer.loc[:, 'daan'].values[i]))
        answer_match.sort(key=lambda item: item[0], reverse=True)
        answer_match = [value[1].replace(' ', '')
                        for value in answer_match]  # 剔除所有空格
        answer_match = [list(value) for value in answer_match]  # 打成散列
        answer_match = self.match_question_type(quesTypeStr, answer_match)
        return answer_match, self.option2text(answer_match, answerOptions)

    def _find_answer(self, quesTypeStr, content, answerOptions):
        res = ''.join(self.get_puer_text(content))
        questions = ''
        answer_match = []
        for v in self.answer_question_bank:
            questions, answer_match = v[0], v[1]
            if res == questions:
                break
        return self.text2option(answer_match, answerOptions), answer_match

    def _find_paper(self, quesTypeStr, content, answerOptions):
        ques_list = self.get_puer_text(content)
        ques_list.sort()
        full_match = []
        full_paper_match = []
        for ques in ques_list:
            if len(ques) < 4:  # 太短的匹配无意义
                continue
            answer_full = self.excel_question_bank[self.excel_question_bank['timu'].str.contains(
                ques,
                case=False,  # 是否匹配大小写
                na=True,  # 默认对空值不处理，即输出结果还是 NaN
                regex=True)]
            if not answer_full.empty:
                stdout_rate = '', 0, 0
                rows, cols = answer_full.shape
                for i, tmp in enumerate(answer_full.loc[:, 'timu']):
                    rate = get_equal_rate(content, tmp)
                    if rate > stdout_rate[1]:
                        stdout_rate = tmp, rate, i
                t_str = ''.join(['全匹配标注:置信度:', str(round(stdout_rate[1]*100.00, 2)) + '%  ',
                      answer_full.loc[:, 'daan'].values[stdout_rate[2]],
                      "->>>>>", answer_full.loc[:,'timu'].values[stdout_rate[2]],
                      answer_full.loc[:, 'text'].values[stdout_rate[2]].replace('\n', '')])
                full_match.append([stdout_rate[1], t_str])
            stdout_rate = '', 0
            for v in self.paper_question_bank:
                if ques in v:
                    rate = get_equal_rate(content, v)
                    if rate > stdout_rate[1]:
                        stdout_rate = v, rate
                    break
            if stdout_rate[0]:
                t_str = ''.join(['文章匹配标注:置信度', str(
                    round(stdout_rate[1]*100.00, 2)) + '%  ', stdout_rate[0]])
                full_paper_match.append([stdout_rate[1], t_str])
        os.system("cls")
        print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n')
        print('采集题目:', content)
        print('采集答案:', answerOptions)
        if full_match:
            full_match.sort(key=lambda item: item[0])
            print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n')
            print(full_match[-1][-1])
        if full_paper_match:
            full_paper_match.sort(key=lambda item: item[0])
            print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n')
            print(full_paper_match[-1][-1])
            print()
            t_str = ''
            t_list = []
            for txt in answerOptions:
                if txt in full_paper_match[-1][-1]:
                    t_list.append(txt)
                    t_str += '[' + txt + ']'
            print("选项命中:->>>>>>>>>>>>", t_str, quesTypeStr, self.text2option(t_list, answerOptions))
            print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n')

    def find_jieba(self, content):
        import jieba
        topic_list = self.get_puer_text(content)
        topic_str = jieba.lcut(''.join(topic_list), cut_all=False)
        jieba_confidence = []
        for topic in topic_str:
            answer_jieba = self.excel_question_bank[self.excel_question_bank['timu'].str.contains(
            topic,
            case = False, # 是否匹配大小写
            na = True, # 默认对空值不处理，即输出结果还是 NaN
            regex=True)]
            if not answer_jieba.empty:
                stdout_rate = '', 0, 0
                for i, tmp in enumerate(answer_jieba.loc[:,'timu']):
                    rate = get_equal_rate(content, tmp)
                    if rate > stdout_rate[1]:
                        stdout_rate = tmp, rate, i
                jieba_confidence.append((topic, stdout_rate[1], answer_jieba.loc[:,'daan'].values[stdout_rate[2]], 
                            answer_jieba.loc[:,'timu'].values[stdout_rate[2]]))
        jieba_confidence.sort(key=lambda item: item[1], reverse=True)
        jieba_confidence = jieba_confidence[0]
        print('jieba标注:置信度:' + str(round(jieba_confidence[1]*100.00, 2)) +'%  ' + "  ", 
            jieba_confidence[0] + "  ",
            jieba_confidence[2] + "->>>>>"+jieba_confidence[3])

    def collection_wrong_questions(self, text):
        with open(WRONG_QUESTIONS_PATH, 'a') as f:
            f.write(text + '\n')
