#-*-coding:utf-8-*-
from aip import AipSpeech
import warnings
warnings.filterwarnings("ignore")

# 读取文件
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

""" 你的 APPID AK SK """
APP_ID = '15419230'
API_KEY = 'wBbkPr5yae1qYMAUPfW5Gt00'
SECRET_KEY = '6iXMgOx9WfqBaP3PuEfrQKOxN9mGnQ6u'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)



# 识别本地文件
# _result = client.asr(get_file_content('test.wav'), 'wav', 16000)
# print(_result['result'][0])
# print(_result)