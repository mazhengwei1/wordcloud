# coding: utf-8
# AUTHOR: Macus
'''
通过itchat库分析微信中男女比例和年龄以及个性签名生成词云

'''

import jieba
import numpy as np
from PIL import Image
from wordcloud import WordCloud,STOPWORDS, ImageColorGenerator
import re
import time
import matplotlib.pyplot as mp
import itchat
from itchat.content import TEXT

def log_in():
    print("登录成功")

def log_out():
    print("退出成功")


def main():

    # 登录就发送给文件传输助手消息
    # itchat.send("hello world", toUserName='filehelper')

    # 自动回复对方发送的消息
    # @itchat.msg_register(TEXT)
    # def text_reply(msg):
    #     return msg.text
    # itchat.auto_login(hotReload=True, loginCallback=log_in, exitCallback=log_out)
    # itchat.run()

    # 打印发送消息人
    # @itchat.msg_register(TEXT)
    # def _(msg):
    #     print(msg.fromUserName)

    # 登录
    itchat.auto_login(hotReload=True, loginCallback=log_in, exitCallback=log_out)
    # 获取所有好友
    friends = itchat.get_friends()
    all_friend = []
    with open('friends.txt', 'a+', encoding='utf-8') as fw:
        for friend in friends:
            # print(friend)
            '''
            ['NickName', 'Sex', 'Signature', 'Province', 'City', ]
            '''
            # 改写性别
            if friend['Sex'] == 0:
                sex = '女'
            elif friend['Sex'] == 1:
                sex = '男'
            else:
                sex = '未知'
            # 改写签名中的表情
            pattern = '<span class="emoji emoji([\s\S]*?)"></span>'
            Sig = re.sub(pattern, " ", friend['Signature'])
            Sig = re.sub(r'\n', ',', Sig)
            # 如果备注名为空就是无
            rename = friend['RemarkName'] if friend['RemarkName'] else "无"
            # 添加到列表
            all_friend.append({
                "网名": friend['NickName'],
                "备注": rename,
                "性别": sex,
                "签名": Sig,
                "省份": friend['Province'],
                "城市": friend['City'],
            })
            fw.write(Sig)
    return all_friend


def create_img():
    # 1.读出个签
    text = open('friends.txt', 'r', encoding='utf-8').read()
    # 2.把个签剪开
    cut_text = jieba.cut(text)
    # print(type(cut_text))
    # print(next(cut_text))
    # print(next(cut_text))
    # 3.以空格拼接起来
    result = " ".join(cut_text)
    # print(result)
    # 4.生成词云
    stopwords = set(STOPWORDS)
    stopwords.add("贷款")
    img = np.array(Image.open("3.jpg"))
    wc = WordCloud(
        font_path='msyhbd.ttc',  # 字体路劲
        background_color='white',  # 背景颜色
        max_font_size=50,  # 字体大小
        min_font_size=10,
        mask=img,  # 背景图片
        max_words=2000,
        stopwords=stopwords,
    )
    wc.generate(result)
    img_color = ImageColorGenerator(img)
    # 5.显示图片
      # 图片保存
    mp.imshow(wc.recolor(color_func=img_color), interpolation="bilinear")
    mp.axis('off')  # 关闭坐标
    mp.figure('个签')  # 图片显示的名字
    # wc.to_file('个签2.png')
    mp.show()




if __name__ == '__main__':
    fri_list =  main()     # 获取好友信息并写入文件friends.txt
    # print(fri_list)
    # create_img()    # 个性签名词云







