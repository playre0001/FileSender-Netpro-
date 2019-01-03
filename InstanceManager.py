# -*- coding :utf-8 -*-

"""
<Japanese>
各Processorクラスのインスタンスを所持するクラス
"""

import ClientProcessor,UserManager,MessageProcessor,Server,GUIProcessor

__auther__="Daisuke Kuwahara<mail : abcexe1@gmail.com>"
__status__="Student"
__version__="1.0"
__date__="2019/01/01"

class InstanceManager():
    """
    <Japanese>
    各Processorクラスのインスタンスを所持するクラス
    """
    gp=None
    sv=None
    mp=None
    um=None
    fp=None
    cp=None
    make_first_instance=False

    def __init__(self):
        if not(InstanceManager.make_first_instance):
            #自身のstaticメンバを1度だけ初期化
            InstanceManager.gp=GUIProcessor.GUIProcessor(self)
            InstanceManager.mp=MessageProcessor.MessageProcessor(self)
            InstanceManager.um=UserManager.UserManager(self)
            InstanceManager.cp=ClientProcessor.ClientProcessor(self)
            InstanceManager.sv=Server.Server(self)

            #static menberを再度生成しないようにする
            InstanceManager.make_first_instance=True

if __name__=="__main__":
    print("this is class file. Can not use system entry-point.")