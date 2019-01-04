# -*- coding :utf-8 -*-

"""
<Japanese>
送信されてきたメッセージを管理するクラス
"""

__auther__="Daisuke Kuwahara<mail : abcexe1@gmail.com>"
__status__="Student"
__version__="1.1"
__date__="2019/01/04"

import os

import UserManager

from datetime import datetime

class MessageProcessor():
    """
    <Japanese>
    送信されてきたメッセージを管理するクラス
    """
    def __init__(self,instancemanager):
        self.usermessage={}
        
        #ユーザデータの格納ディレクトリが存在するかを確認
        if os.path.exists("UserMessages"):
            if os.path.isdir("UserMessages"):
                #ディレクトリ内の名称をロード
                inDirectryLists=os.listdir("UserMessages")

                #全てにアクセスを行う
                for fileName in inDirectryLists:
                    
                    #ファイルかどうかを確認
                    if os.path.isfile("UserMessages/"+fileName):
                         self.usermessage[fileName.split(".")[0]]=[]

                         #ファイルならば，ロードする
                         with open("UserMessages/"+fileName,"r") as fp:
                            for line in fp:
                                self.usermessage[fileName.split(".")[0]]+=[line]

            else:
                #ディレクトリが存在しない場合
                #新規にディレクトリを作成
                os.mkdir("UserMessages")

        else:
            #ディレクトリが存在しない場合
            #新規にディレクトリを作成
            os.mkdir("UserMessages")

    def addMessage(self,username,message):
        """
        <japanese>
        新規メッセージを格納する関数
        引数 username :送信元ユーザの名前
        引数 message :メッセージ
        """
        time=datetime.now().strftime("%Y/%m/%d %H:%M:%S")

        #変数にデータを追加
        if not username in self.usermessage:
            self.usermessage[username]=[time+","+message]
        else:
            self.usermessage[username]+=[time+","+message]

        #メッセージをログに追加
        with open("UserMessages/"+username+".msg","a") as fp:
            fp.write(time+","+message+"\n")

    def getUserMessageLog(self,user):
        """
        <Japanese>
        ユーザのメッセージ記録を取得する関数
        引数 user :メッセージ記録送信元のユーザ名
        戻り値 :存在する場合はメッセージ記録をリストで，存在しない場合None
        """
        if not user in self.usermessage:
            return []

        return self.usermessage[user]
        

if __name__=="__main__":
    print("this is class file. Can not use system entry-point.")