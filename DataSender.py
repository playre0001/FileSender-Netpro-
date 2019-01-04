# -*- coding :utf-8 -*-

"""
<Japanese>
データ送信用のスレッド
"""

__auther__="Daisuke Kuwahara<mail : abcexe1@gmail.com>"
__status__="Student"
__version__="1.0"
__date__="2019/01/01"

import threading
import socket
import os

class DataSender():
    """
    <Japanese>
    メッセージとファイルを受信するためのサーバクラス
    """
    def __init__(self,ipaddr,username,publickey,datatype,data,gp,filesize=0):
        #引数 : ファイル送信の場合には，dataに暗号化後のファイルパスを格納すること
        self.ipaddr=ipaddr
        self.username=username
        self.publickey=publickey
        self.datatype=datatype
        self.data=data
        self.gp=gp

        self.filesize=str(filesize)

    def Run(self):
        """
        <Japanese>
        self.datatypeに従って、異なったスレッドを起動する関数
        #引数 gp :GUIProcessorのインスタンス
        """

        #self.datatypeに従って、異なった関数をスレッドとして設定する
        if self.datatype=="FILE":
            th=threading.Thread(target=self.ThreadFile)
        elif self.datatype=="MESSAGE":
            th=threading.Thread(target=self.ThreadMessage)
        else:
            return None

        #スレッドの実行
        th.start()
    
    def ThreadFile(self):
        #ソケットオブジェクトの作成
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        
        #コネクションを行う
        try: s.connect((self.ipaddr,11235))
        except socket.timeout:
            #タイムアウト時の処理
            self.gp.DialogBox(str(self.ipaddr)+":11235, timeout","Err")
            return
        except socket.error:
            #その他例外発生時の処理
            import traceback
            traceback.print_exc()
            self.gp.DialogBox(str(self.ipaddr)+":11235, error","Err")
            return

        #名前の送信
        s.send(self.username.encode("utf-8"))
        a=s.recv(1024)
        
        #公開鍵の送信
        s.send(self.publickey)
        b=s.recv(1024)

        #データタイプの送信
        s.send(self.datatype.encode("utf-8"))
        c=s.recv(1024)

        #メッセージの送信
        s.send(self.filesize.encode("utf-8"))
        
        #メッセージの受信
        msg=""
        
        while not msg:
            msg=s.recv(1024).decode("utf-8")
        
        #送信要求の場合
        if msg=="SEND":
            #ファイルを開く
            with open(self.data,"rb") as fp:
                while True:
                    #1024byte毎にファイルからデータを読み出し
                    msg=fp.read(1024)

                    #EOFではないか確認(msgが空文字=EOF)
                    if not msg:
                        break
                    
                    #送信
                    s.send(msg);
                #送信終了を送信
                s.send("END".encode("utf-8"))
                
        #暗号化ファイルの削除
        os.remove(self.data)
        
        #ソケットを閉じる
        s.close()

    def ThreadMessage(self):
        #ソケットオブジェクトの作成
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        
        #コネクションを行う
        try: s.connect((self.ipaddr,11235))
        except socket.timeout:
            #タイムアウト時の処理
            self.gp.DialogBox(str(self.ipaddr)+":11235, timeout","Err")
            return
        except socket.error:
            #その他例外発生時の処理
            import traceback
            traceback.print_exc()
            self.gp.DialogBox(str(self.ipaddr)+":11235, error","Err")
            return
        
        #名前の送信
        s.send(self.username.encode("utf-8"))
        s.recv(1024)
        
        #公開鍵の送信
        s.send(self.publickey)
        s.recv(1024)
        
        #データタイプの送信
        s.send(self.datatype.encode("utf-8"))
        s.recv(1024)

        #メッセージの送信
        s.send(self.data)
        
        #ソケットを閉じる
        s.close()

if __name__=="__main__":
    print("this is class file. Can not use system entry-point.")