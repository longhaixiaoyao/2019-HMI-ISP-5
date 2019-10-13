import os
import sys
import speech
import webbrowser

phrase={"closeSystem":"关闭人机交互系统",
        "Music":"听音乐",
        "Moive":"看电影",
        "cmd":"cmd"
}

def callback(phr,phrase):
    if phr==phrase("closeSystem"):
        speech.say("正在关闭系统")
        speech.stoplistening
        sys.exit()
    elif phr == phrase["Music"]:
        speech.say("正在为您打开网易云音乐")
        webbrowser.open_new("http://music.163.com/")
    elif phr == phrase["Moive"]:
        speech.say("正在为您打开爱奇艺")
        webbrowser.open_new("http://www.iqiyi.com/")
    elif phr == phrase["cmd"]:
        speech.say("即将打开CMD")
        os.popen("C:\Windows\System32\cmd.exe")

while True:
    phrase =speech.input()
    speech.say("You said %s"%phrase)
    if phrase =="turn off":
        break