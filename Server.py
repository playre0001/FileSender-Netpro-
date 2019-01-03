# -*- coding :utf-8 -*-

"""
<Japanese>
メッセージとファイルを受信するためのサーバクラス
"""

__auther__="Daisuke Kuwahara<mail : abcexe1@gmail.com>"
__status__="Student"
__version__="1.0"
__date__="2018/12/22"

import SocketProcessor
import socket,threading

class Server():
    """
    <Japanese>
    メッセージとファイルを受信するためのサーバクラス
    """
    def __init__(self,instancemanager):
        #インスタンスマネージャーを取得
        self.im=instancemanager

        #終了フラグのセット
        self.endFlag=False

        #SocketProcessorのインスタンスを定義
        self.sp=SocketProcessor.SocketProcessor(self.im.mp,self.im.gp,self.im.um)

        #ソケットを取得
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #ポートをバインド
        self.socket.bind(("localhost",11235))

    def Run(self):
        """
        <Japanese>
        サーバ用プロセスを起動する関数
        """
        #プロセスを軌道
        th=threading.Thread(target=self.ServerThread)
        th.start()

    def End(self):
        """
        <Japanese>
        サーバプロセスの終了を行う関数
        """
        #フラグを立てる
        self.endFlag=True

        #終了用の信号を送る
        s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("localhost",11235))
        s.send("__SYSTEM__END__FLAG__".encode("utf-8"))
        s.close()

    def ServerThread(self):
        """
        <Japanese>
        サーバ用プロセス
        """

        #最大5個までの接続を受信待ち
        self.socket.listen(5)

        #ループ
        while True:
            #終了処理
            if self.endFlag:
                break

            #処理を別スレッドに任せる
            self.sp.Run(self.socket.accept())

            

if __name__=="__main__":
    print("this is class file. Can not use system entry-point.")