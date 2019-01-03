#-*- coding :utf-8 -*-

"""
<Japanese>
ソケット処理用のクラス
"""

__auther__="Daisuke Kuwahara<mail : abcexe1@gmail.com>"
__status__="Student"
__version__="1.0"
__date__="2019/01/03"

import GUIProcessor,MessageProcessor,UserManager

import threading
import socket

import os

from datetime import datetime

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

class SocketProcessor():
    """
    <Japanese>
    ソケット処理用のクラス
    """

    def __init__(self,messageProcessor,gpuProcessor,userManager):
        self.mp=messageProcessor
        self.gp=gpuProcessor
        self.um=userManager
    
    def Run(self,acceptData):
        """
        <Japanese>
        SocketThreadを開始するプロセス
        引数 acceptData :socket.acceptをそのまま渡して
        """
        #スレッドの開始
        threading.Thread(target=self.SocketThread,args=acceptData).start()


    def SocketThread(self,s,addr):
        """
        <Japanese>
        クライアントとの接続ソケットを処理する関数
        引数 s :ソケット
        引数 addr :クライアントのアドレス
        """
        #ユーザ名の受信
        username=s.recv(4096).decode("utf-8")
        s.send("OK".encode("utf-8"))

        #終了用シグナルの場合，何もせずにスレッド終了
        if username=="__SYSTEM__END__FLAG__":
            return

        #公開鍵の受信
        publicKey=s.recv(4096)
        s.send("OK".encode("utf-8"))

        #データタイプの受信
        datatype=s.recv(4096).decode("utf-8")
        s.send("OK".encode("utf-8"))

        #データの受信
        chiper_data=s.recv(4096)

        #データタイプの確認
        if datatype=="FILE":
            #ファイルデータの場合
            #データサイズをデコード
            data=chiper_data.decode("utf-8")
            
            #受信するかをユーザに尋ねる
            if "Yes"==self.gp.DialogBox(data+"[bytes]のファイルを受信しますか?","YesNo"):
                #受信記録を保存
                self.mp.addMessage(username,data+"[bytes]のファイルを受信")
                
                #送信要求
                s.send("SEND".encode("utf-8"))
                
                #復号化の準備
                cipher=PKCS1_OAEP.new(RSA.importKey(publicKey))

                #ディレクトリの存在確認と作成
                if os.path.exists("DownloadFiles"):
                   if not os.path.isdir("DownloadFiles"):
                       #新規にディレクトリを作成
                       os.mkdir("DownloadFiles")
                else:
                    #新規にディレクトリを作成
                    os.mkdir("DownloadFiles")

                #ダウンロードファイルを開く
                with open("DownloadFiles/"+username+"_"+datetime.now().strftime("%Y_%m_%d_%H_%M_%S")+".dl","wb") as fp:
                    while True:
                        #256bytesずつファイルを受信
                        msg=s.recv(256)

                        #もし，終了信号ならループを抜ける
                        if msg.decode("utf-8","ignore")=="END":
                            break

                        #復号したデータをファイルに書き込む  256byte以外の長さで複合はできない
                        fp.write(cipher.decrypt(msg))

                #ダウンロード完了通知
                self.gp.DialogBox("受信完了","Yes")

            #ソケットを閉じる
            s.close()


        elif datatype=="MESSAGE":
            #ソケットを閉じる
            s.close()

            if not publicKey==self.um.getPublicKey(username,publicKey):
                #ユーザの公開鍵が一致していない場合
                #ユーザにその旨を提示
                if "No"==self.gp.DialogBox(username+"から送信されたデータの公開鍵が一致しません．受信しますか?","YesNo"):
                    return

            #メッセージの複合
            cipher=PKCS1_OAEP.new(RSA.importKey(publicKey))
            
            message=cipher.decrypt(chiper_data).decode("utf-8")
                
            #message関数に処理を渡す
            self.mp.addMessage(username,message)

            #通知の要請
            self.gp.DialogBox("<受信> "+username+":"+message,"Yes")

if __name__=="__main__":
    print("this is class file. Can not use system entry-point.")