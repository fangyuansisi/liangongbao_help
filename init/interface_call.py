import json
import time
import random

from config.url_conf import URLS
from utils.http_utils import HTTPClient
from LgbConfig import MIN_TIME, MAX_TIME
from utils.find_ansers import FindAnswers


class InterfaceCall:
    def __init__(self) -> None:
        self.user = ""
        self.passwd = ""
        self.http_client = HTTPClient()
        self.find_answers = FindAnswers()
        self.result_dict = None

    def login(self):
        token_data = {"userName": self.user, "password": self.passwd}
        token_dict = self.http_client.send(URLS['login'], token_data)
        status = token_dict.get("status")
        if status == 20000:
            self.http_client.token = token_dict.get("data").get("token")
            self.http_client.memberId = token_dict.get("data").get("memberId")
            print("登录成功")
        else:
            print(token_dict)

    def start(self) -> bool:
        self.result_dict = self.http_client.send(URLS['start'], {})
        print(self.result_dict)
        msg = self.result_dict.get("result").get("msg")
        code = self.result_dict.get("result").get("code")
        if msg == "每天只能挑战一次哦~" and code == 9:
            print("每天只能挑战一次哦~")
            return False
        return True

    def judge_finish(self) -> bool:
        data = self.result_dict.get("data")
        if data:
            ques = data.get("ques")
            if not ques:
                print("<------恭喜您，满分！！！------>")
            else:
                return False
        else:
            print(self.result_dict)
            print("======账号答题结束======")
        return True

    def answer(self):
        while not self.judge_finish():
            quesid_, answer_ = self.get_correct_answer()
            data = {"quesId": "%s" % quesid_, "answerOptions": answer_}
            self.result_dict = self.http_client.send(
                URLS['answer'], data=json.dumps(data))
            time.sleep(random.randint(MIN_TIME, MAX_TIME))

    def get_correct_answer(self):
        quesid_ = ""
        answer_ = []

        if self.judge_finish():
            return quesid_, answer_

        ques = self.result_dict.get("data").get("ques")
        quesid_ = ques.get("quesId")
        quesTypeStr = ques.get("quesTypeStr")
        content = ques.get("content")
        answerOptions = ques.get("options")
        _, answer_ = self.find_answers.get_result(quesTypeStr, content, answerOptions)
        print("running:", quesid_, quesTypeStr, content, answerOptions, answer_)
        if all([quesid_, answer_]):
            return quesid_, answer_
        else:
            retry_flag = True
            while retry_flag:
                retry_flag = False
                t_str = input("没有找到答案>>>>>>>>>>>>手动输入答案:").upper()
                for v in t_str:
                    if ord(v)-64 > len(answerOptions):
                        retry_flag = True
            return quesid_, self.find_answers.option2text(list(t_str), answerOptions)

    def task(self):
        self.login()
        if self.start():
            self.answer()
        self.http_client.del_cookies()
        self.http_client.ranf_ua()
        time.sleep(random.randint(MIN_TIME, MAX_TIME))

    def main(self, user, passwd):
        self.user = user
        self.passwd = passwd
        self.task()
