# lgb登录账号
ACCOUNT = [
    {'USER': '', 'PWD': ''},
    # {'USER': '', 'PWD': ''},
]

# Excel 题库
EXCEL_QUESTION_BANK_PATH = r'x.xls'

# TXT 题库
ANSWER_QUESTION_BANK_PATH = r'x.txt'

# 文章 题库
PAPER_QUESTION_BANK_PATH = r'x.txt'

# 错题收集本
WRONG_QUESTIONS_PATH = r'wrong_questions.txt'

# 不自动安装chrome请设置这个参数
# CHROME_CHROME_PATH = r'.wdm\drivers\chromedriver\win32\x.x.x\chromedriver.exe'
CHROME_CHROME_PATH = None
CHROME_TIMEOUT = 15

# adb devices 命令得到的手机序列号
ADB_DEVICE_SERIAL = "xxxxxxxx"

# 保护官网请求频率，设置随机请求时间
# 最大间隔请求时间
MAX_TIME = 6
# 最小间隔请求时间
MIN_TIME = 3

# 软件版本
RE_VERSION = '0.0.001'
