# -*- coding :utf-8 -*-

"""
<Japanese>
アプリケーションのエントリポイント
"""

__auther__="Daisuke Kuwahara<mail : abcexe1@gmail.com>"
__status__="Student"
__version__="1.0"
__date__="2019/01/03"

if __name__=="__main__":
    import InstanceManager,GUIProcessor,Server

    #インスタンスマネージャーを生成
    im=InstanceManager.InstanceManager()

    #サーバを起動
    im.sv.Run()

    #クライアントシステムを起動
    im.gp.ClientGUI()

    #終了待ち
    im.sv.End()
    im.gp.End()

