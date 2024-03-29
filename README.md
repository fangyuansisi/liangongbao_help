# liangongbao_help

## 功能
- #####  支持使用接口答题
- #####  使用接口重连功能
- #####  支持浏览器自动化答题
- #####  *支持OCR识别手机题目手动答题*
- #####  多题库匹配
- #####  Excel题库
- #####  TXT题库
- #####  安全法文章匹配提醒机制
- #####  支持题目匹配失败时手动作答
- #####  错题汇总共同交流

## 未来展望
- #####  增加详细日志记录
- #####  增加异常处理机制
- #####  增加cookie处理
- #####  邮件通知
- #####  docker定时运行等
- #####  增加单元测试，MOCK接口等


# run
```shell
学习交流为主，其他勿扰
按需更改 LgbConfig.py 配置即可
正常情况下，是不需要手动输入答案的，一直有新的running跳动，每题默认延迟2-5s
需要手动答题的时候，只需要输入正确选项'A,B,C,D'，输入不在选项中时会提示重新输入,输入为空同理
用答过题的账号尝试可视化登录，也挺好玩~

pip install -r requirements.txt
python main.py

```
# 题库找不到答案，手动输入例子如图
![image](手动输入例子.png)


# usage
```shell

  usage: main.py [-h] [-i] [-v] [-a]

  链工宝让平凡的人懂得安全生产

  optional arguments:
    -h, --help            show this help message and exit
    -i, --interface_call  使用接口POST/GET运行
    -v, --visualization   使用浏览器可视化运行
    -a, --adb_ocr         使用ADB工具连接手机运行
```


# 有任何问题，可加Q群交流: 644738320
## 学习交流如有侵权请联系我删除