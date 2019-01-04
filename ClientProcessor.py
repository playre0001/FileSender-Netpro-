# -*- coding :utf-8 -*-

"""
<Japanese>
クライアントの情報を管理すると同時に、通信用のスレッドを起動するクラス
"""

__auther__="Daisuke Kuwahara<mail : abcexe1@gmail.com>"
__status__="Student"
__version__="1.1"
__date__="2019/01/04"

import DataSender,GUIProcessor

#os
from os.path import exists,isfile,getsize
from os import remove

#日時
from datetime import datetime

#RSA
from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

import tkinter
import tkinter.simpledialog as ts

class ClientProcessor():
    """
    <Japanese>
    クライアントの情報を管理すると同時に、通信用のスレッドを起動するクラス
    """

    def __init__(self,instancemanager):
        #InstanceManagerクラスを取得
        self.im=instancemanager

        #フィールドを初期化
        self.USERNAME=None
        self.PRIVATE_PEM=None
        self.PUBLIC_PEM=None

        #アプリケーションの設定ファイルが存在するかを確認
        if not(exists("appData.ini") and isfile("appData.ini")):
            #設定ファイルが存在しない場合
            #ユーザからユーザ名を入力してもらう
            tkinter.messagebox.showinfo(title="Information",message="アプリケーションファイルが存在しません")
            USERNAME=ts.askstring("Input Box","自身のユーザ名を入力してください")

            #何か入力されるまで待機
            while not USERNAME:
                USERNAME=ts.askstring("Input Box","自身のユーザ名を入力してください")

            #公開鍵と秘密鍵を生成
            random_func=Random.new().read
            rsa=RSA.generate(2048,random_func)                  #2048bitで鍵を生成

            PRIVATE_PEM=rsa.exportKey(format="PEM")             #秘密鍵生成
            PUBLIC_PEM=rsa.publickey().exportKey(format="PEM")  #公開鍵生成

            #ファイルに保存
            with open("appData.ini","x") as fp:
                fp.write("USERNAME="+USERNAME+"\n");
                fp.write("PUBLIC_PEM=publickey.pem\n")
                fp.write("PRIVATE_PEM=privatekey.pem\n")

            #ライブラリの都合上，公開鍵で複合ができないので，逆に保存する
            with open("publickey.pem","wb") as fp:
                fp.write(PRIVATE_PEM)
            
            with open("privatekey.pem","wb") as fp:
                fp.write(PUBLIC_PEM)

            #ユーザに通知
            tkinter.messagebox.showinfo(title="Information",message="アプリケーションファイルの作成完了")

        #アプリケーションの設定ファイルをロード
        with open("appData.ini","r") as fp:
            for line in fp:
                s=line.split("=")

                s[0]=s[0].upper()

                #設定ファイルの読み込み結果をフィールドに格納
                if s[0]=="USERNAME":
                    self.USERNAME=s[1][:len(s[1])-1]
                
                elif s[0]=="PUBLIC_PEM":
                    #"\n"を削除
                    s[1]=s[1][:len(s[1])-1]
                    with open(s[1],"rb") as fp1:
                        self.PUBLIC_PEM=fp1.read()
                
                elif s[0]=="PRIVATE_PEM":
                    #"\n"を削除
                    s[1]=s[1][:len(s[1])-1]
                    with open(s[1],"rb") as fp2:
                        self.PRIVATE_PEM=fp2.read()

        #アプリケーションファイルの例外処理
        if (self.USERNAME is None) or (self.PUBLIC_PEM is None) or (self.PRIVATE_PEM is None):
            tkinter.messagebox.showinfo(title="Information",message="アプリケーションファイルが不正です。appData.iniを削除します")
            remove("appData.ini")                               #ファイル内容が必要十分ではない場合に、ファイルを削除する
            self.__init__(instancemanager)                      #appDataが存在しない状態で再度コンストラクタを呼び出す
    
    def SendMessage(self,ipaddr,message):
        """
        <Japanese>
        メッセージを暗号化し、送信用スレッドに投げるメソッド
        引数  ipadder   :送信先のIPアドレス
        引数  message   :送信用メッセージ(String)
        """

        #引数の例外処理
        if not type(message)==str:
            message=str(message)

        #messageを秘密鍵で暗号化
        cipher=PKCS1_OAEP.new(RSA.importKey(self.PRIVATE_PEM))
        cipher_text=cipher.encrypt(message.encode("utf-8"))                     #暗号化
        
        #スレッドに渡す
        th=DataSender.DataSender(ipaddr,self.USERNAME,self.PUBLIC_PEM,"MESSAGE",cipher_text,self.im.gp)
        th.Run()

    def SendFile(self,ipaddr,filepath):
        """
        <Japanese>
        メッセージを暗号化し、送信用スレッドに投げるメソッド
        引数  ipadder   :送信先のIPアドレス
        引数  message   :送信用メッセージ(String)
        """

        #引数の例外処理
        if not(exists(filepath) and isfile(filepath)):
            tkinter.messagebox.showinfo(title="Information",message="ファイルが存在しません")
            return None                     #例外処理：ファイルが存在しない場合

        #暗号化ファイル名の作成
        cipher_filename=datetime.now().strftime("%Y_%m_%d_%H_%M_%S")+".cipfile"
        
        #暗号化の準備
        cipher=PKCS1_OAEP.new(RSA.importKey(self.PRIVATE_PEM))

        #暗号化ファイルを開く
        with open(cipher_filename,"xb") as cfp:

            #平文ファイルを開く
            with open(filepath,"rb") as fp:
                #ファイル内容の読み込みと暗号化、書き込み
                while True:
                    d=fp.read(128)
                    
                    if not d:
                        #EOFなら終了
                        break
                    
                    cipher_file_data=cipher.encrypt(d)
                    cfp.write(cipher_file_data)
                    
        
        #スレッドに渡す
        th=DataSender.DataSender(ipaddr,self.USERNAME,self.PUBLIC_PEM,"FILE",cipher_filename,self.im.gp,filesize=getsize(cipher_filename))
        th.Run()
 

if __name__=="__main__":
    print("this is class file. Can not use system entry-point.")