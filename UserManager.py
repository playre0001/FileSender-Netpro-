# -*- coding :utf-8 -*-

"""
<Japanese>
送信されてきたデータの公開鍵とユーザ名を管理するクラス
"""

__auther__="Daisuke Kuwahara<mail : abcexe1@gmail.com>"
__status__="Student"
__version__="1.0"
__date__="2019/01/03"

import os

class UserManager():
    """
    <Japanese>
    送信されてきたデータの公開鍵とユーザ名を管理するクラス
    """
    def __init__(self,instancemanager):
        self.userdata={}

        #ユーザデータの格納ディレクトリが存在するかを確認
        if os.path.exists("UserDatas"):
            if os.path.isdir("UserDatas"):
                #ディレクトリ内の名称をロード
                inDirectryLists=os.listdir("UserDatas")

                #全てにアクセスを行う
                for fileName in inDirectryLists:
                    #ファイルかどうかを確認
                    if os.path.isfile("UserDatas/"+fileName):
                        #ファイルならば，ロードする
                        with open("UserDatas/"+fileName,"rb") as fp:
                            self.userdata[fileName.split(".")[0]]=fp.read()

            else:
                #ディレクトリが存在しない場合
                #新規にディレクトリを作成
                os.mkdir("UserDatas")

        else:
            #ディレクトリが存在しない場合
            #新規にディレクトリを作成
            os.mkdir("UserDatas")

    def getPublicKey(self,name,publickey):
        """
        <Japanese>
        ユーザの公開鍵を取得する関数
        引数 name :ユーザ名
        引数 publickey :検索ユーザ名と同時に送信されてきた公開鍵
        戻り値 :指定したユーザ名の公開鍵
        """
        #データベースに存在しない場合
        if not name in self.userdata:
            #新規に追加
            self.userdata[name]=publickey

            with open("UserDatas/"+name+".pem","xb") as fp:
                fp.write(publickey)

        return self.userdata[name]
        
    def getUserList(self):
        """
        <Japanese>
        ユーザー名の一覧をリストで返す関数
        戻り値 :ユーザ名のリスト
        """
        return list(self.userdata.keys())

if __name__=="__main__":
    print("this is class file. Can not use system entry-point.")