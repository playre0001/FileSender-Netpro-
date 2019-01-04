# -*- coding :utf-8 -*-

"""
<Japanese>
GUIの表示を管理するクラス
"""

__auther__="Daisuke Kuwahara<mail : abcexe1@gmail.com>"
__status__="Student"
__version__="1.1"
__date__="2019/01/04"

import MessageProcessor,ClientProcessor,UserManager,InstanceManager

import tkinter

import tkinter.messagebox as tkmsg
import tkinter.simpledialog as ts

from time import sleep

class GUIProcessor():
    """
    <Japanese>
    GUIの表示を管理するクラス.
    version 1.0以前では、CUIによる表示になっている
    """
    def __init__(self,instancemanager):
        #InstanceManagerクラスを取得
        self.im=instancemanager

        #thinterクラスを用意
        self.tkroot=tkinter.Tk()
        
        #GUIの構成
        self.tkroot.title("File Sender")            #タイトルを用意
        self.tkroot.geometry("400x300+100+100")     #window size = 400 x 300, window locate = (100,100)
        
        #フォームの生成
        self.listboxForm=tkinter.Frame(master=self.tkroot)
        self.listboxForm.pack(side=tkinter.TOP)

        self.bottomForm=tkinter.Frame(master=self.tkroot)
        self.bottomForm.pack(side=tkinter.BOTTOM)

        self.entryForm=tkinter.Frame(master=self.bottomForm)
        self.entryForm.pack(side=tkinter.LEFT)

        self.buttonForm=tkinter.Frame(master=self.bottomForm)
        self.buttonForm.pack(side=tkinter.RIGHT)

        self.entry1Form=tkinter.Frame(master=self.entryForm)
        self.entry1Form.pack(side=tkinter.TOP)

        self.entry2Form=tkinter.Frame(master=self.entryForm)
        self.entry2Form.pack(side=tkinter.TOP)

        self.entry3Form=tkinter.Frame(master=self.entryForm)
        self.entry3Form.pack(side=tkinter.TOP)

        #リストボックスの生成
        self.listbox1=tkinter.Listbox(self.listboxForm,selectmode=tkinter.SINGLE,height=13)
        
        #スクロール可能にする
        self.listbox1.xview()
        self.listbox1.yview()

        self.listbox2=tkinter.Listbox(self.listboxForm,selectmode=tkinter.SINGLE,width=40,height=13)

        #スクロール可能にする
        self.listbox2.xview()
        self.listbox2.yview()

        #ボタンの生成
        self.button1=tkinter.Button(master=self.buttonForm,text="メッセージ送信",command=self.sendMessage)
        self.button1.pack()
        
        self.button2=tkinter.Button(master=self.buttonForm,text="ファイル送信",command=self.sendFile)
        self.button2.pack()

        #入力フォームの生成
        self.entry1Text = tkinter.Label(self.entry1Form, text="IP address")
        self.entry1Text.pack(side=tkinter.LEFT)
        self.entry1 = tkinter.Entry(self.entry1Form, bd=1)
        self.entry1.pack(side=tkinter.RIGHT)
        
        self.entry2Text = tkinter.Label(self.entry2Form, text="Message")
        self.entry2Text.pack(side=tkinter.LEFT)
        self.entry2 = tkinter.Entry(self.entry2Form, bd=1)
        self.entry2.pack(side=tkinter.RIGHT)

        self.entry3Text = tkinter.Label(self.entry3Form, text="FilePath")
        self.entry3Text.pack(side=tkinter.LEFT)
        self.entry3 = tkinter.Entry(self.entry3Form, bd=1)
        self.entry3.pack(side=tkinter.RIGHT)

        #フラグの初期化
        self.dialog_yes=False   #yesボタンのみのdialog boxの表示フラグ
        self.dialog_yesno=False #yes, noボタンのdialog boxの表示フラグ
        self.dialog_err=False   #yesボタンのみのerror表示用dialog boxの表示フラグ
        self.dialog_input=False #入力フォームのdialog box表示フラグ
        
        self.dialog_end=False   #Dialogに返答があったかどうかのフラグ

        #その他初期化
        self.dialog_message=None
        self.dialog_return=None
        self.currentId=0        #current Userのlistbox上のID

    def ClientGUI(self):
        """
        <Japanese>
        ClientGUIを表示する関数
        """
        #ユーザデータの一覧を取得
        users=self.im.um.getUserList()

        #カレントユーザを設定
        if not users==[]:
            #ユーザが1人以上存在する場合
            currentUser=users[0]

            #カレントユーザのメッセージログを取得
            messageLog=self.im.mp.getUserMessageLog(currentUser)
        else:
            currentUser=""
            messageLog={}

        #ユーザデータ一覧をリストに追加
        for i in range(0,len(users)):
            self.listbox1.insert(i,users[i])

        self.listbox1.pack(side=tkinter.LEFT)

        #カレントユーザのメッセージを読み込み
        msgs=self.im.mp.getUserMessageLog(currentUser)

        #メッセージをリストに追加
        for i in range(0,len(msgs)):
            self.listbox2.insert(i,msgs[i])

        #カレントユーザーをアクティブ化する
        self.listbox2.activate(1)

        self.listbox2.pack(side=tkinter.RIGHT)

        #時間枚のイベントを作成
        self.TimeEvent()

        #GUIの表示
        self.tkroot.mainloop()


    def DialogBox(self,message,type):
        """
        <Japanese>
        message引数に格納された内容を、ダイアログボックスに表示する関数
        引数    message     :表示する内容
        引数    type        :ダイアログボックスの種類
        """

        #引数の例外処理
        if message is None:
            return None

        #ダイアログボックスを表示
        if str(type).lower()=="yes":
            #DialogBox用のデータを格納
            self.dialog_message=message

            #DialogBoxの表示フラグを立てる
            self.dialog_yes=True

            #DialogBoxに返答があるまで待機
            while not self.dialog_end:
                pass
            
            return "Yes"

        elif str(type).lower()=="yesno":
            #DialogBox用のデータを格納
            self.dialog_message=message

            #DialogBoxの表示フラグを立てる
            self.dialog_yesno=True

            #DialogBoxに返答があるまで待機
            while not self.dialog_end:
                pass

            if self.dialog_return:
                return "Yes"
            else:
                return "No"

            self.dialog_return=None

        elif str(type).lower()=="err":
            #DialogBox用のデータを格納
            self.dialog_message=message

            #DialogBoxの表示フラグを立てる
            self.dialog_err=True

            #DialogBoxに返答があるまで待機
            while not self.dialog_end:
                pass
            
            return "Yes"

        return ""

    def InputForm(self,message):
        """
        <Japanese>
        messageに格納された内容をユーザにダイアログボックスとして表示し、その結果を入力フォームで取得する
        引数    message     :表示する内容
        """
        #DialogBox用のデータを格納
        self.dialog_message=message

        #DialogBoxの表示フラグを立てる
        self.dialog_input=True

        #DialogBoxに返答があるまで待機
        while not self.dialog_return:
            pass

        userIn=self.dialog_return
        self.dialog_return=None

        return userIn
        
    def TimeEvent(self):
        """
        一定時間ごとに動作するTkinterイベント
        """
        #DialogBoxの表示
        if self.dialog_yes:
            tkmsg.showinfo(title="Information",message=self.dialog_message)
            self.dialog_message=None
            self.dialog_yes=False
            self.dialog_end=True

        elif self.dialog_yesno:
            self.dialog_return=tkmsg.askyesno(title="Information",message=self.dialog_message)
            self.dialog_message=None
            self.dialog_yesno=False
            self.dialog_end=True

        elif self.dialog_err:
            tkmsg.showerror(title="Error",message=self.dialog_message)
            self.dialog_message=None
            self.dialog_err=False
            self.dialog_end=True

        elif self.dialog_input:
            while not self.dialog_return:
                self.dialog_return=ts.askstring("Input Box",self.dialog_message)

            self.dialog_message=None
            self.dialog_input=False
            self.dialog_end=True

        #ユーザの更新
        users=self.im.um.getUserList()

        if not len(users)==self.listbox1.size(): #ユーザ一覧の長さが表示しているものと違う場合
            for i in range(0,len(users)-self.listbox1.size()):
                self.listbox1.insert(self.listbox1.size()+i,users[self.listbox1.size()+i])

        #カレントユーザ変更の処理
        if not 1==self.listbox1.selection_includes(self.currentId):
            keep=self.currentId
            
            #カレントユーザーが変更されている場合
            for i in range(0,self.listbox1.size()):
                #現在のカレントユーザを検索
                if 1==self.listbox1.selection_includes(i):
                    #カレントユーザのIDを更新
                    self.currentId=i
                    break

            if not keep==self.currentId:
                #リスト自体がアクティブになっている場合

                #現在のメッセージを削除
                self.listbox2.delete(0,tkinter.END)
                
                #メッセージをロード
                msgs=self.im.mp.getUserMessageLog(self.listbox1.get(self.currentId))

                #メッセージを追加
                for i in range(0,len(msgs)):
                    self.listbox2.insert(i,msgs[i])

        #メッセージの更新処理
        msgs=self.im.mp.getUserMessageLog(self.listbox1.get(self.currentId))

        if not len(msgs)==self.listbox2.size(): #メッセージの長さが表示しているものと違う場合
            for i in range(0,len(msgs)-self.listbox2.size()):
                self.listbox2.insert(self.listbox2.size()+i,msgs[self.listbox2.size()+i])

        #再度自分を呼び出す
        self.tkroot.after(500,self.TimeEvent)   #500msごとに関数を呼び出し


    def sendMessage(self):
        """
        <Japanese>
        メッセージ送信ボタンの処理
        """
        #関数を呼び出し
        self.im.cp.SendMessage(self.entry1.get(),self.entry2.get())

        #メッセージの入力フォームをクリア
        self.entry2.delete(0,tkinter.END)

    def sendFile(self):
        """
        <Japanese>
        ファイル送信ボタンの処理
        """
        #関数を呼び出し
        self.im.cp.SendFile(self.entry1.get(),self.entry3.get())

        #メッセージの入力フォームをクリア
        self.entry3.delete(0,tkinter.END)

    def End(self):
        """
        <Japanese>
        DialogBoxの終了待ちを解除する関数
        """
        while not self.dialog_end:
            self.dialog_end=True

if __name__=="__main__":
    print("this is class file. Can not use system entry-point.")