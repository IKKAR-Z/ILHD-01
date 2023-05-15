import ctypes
import time
import PySimpleGUI as sg
import tkinter as tk
from tkinter import filedialog

from importlib import import_module
from importlib import reload

def setting_load():
	typ = [('設定ファイル', '*.py')]
	dir = r'C:'
	fle = filedialog.askopenfilename(filetypes = typ, initialdir = dir)
	f = fle.split('/')
	mdl=f[-1].replace('.py','')
	return mdl

def gui_open(cap):
    col1=[
        [sg.Text(cap[0][0],justification='center',expand_x=False,expand_y=True,size=(10,1),pad=0,key='-L0-')],
        [sg.Text(cap[1][0],justification='center',expand_x=False,expand_y=True,size=(10,1),pad=0,key='-L4-')],
        [sg.Text(cap[2][0],justification='center',expand_x=False,expand_y=True,size=(10,1),pad=0,key='-L8-')],
        [sg.Text(cap[3][0],justification='center',expand_x=False,expand_y=True,size=(10,1),pad=0,key='-L12-')],
    ]

    col2=[
        [sg.Text(cap[0][1],justification='center',expand_x=False,expand_y=True,size=(10,1),pad=0,key='-L1-')],
        [sg.Text(cap[1][1],justification='center',expand_x=False,expand_y=True,size=(10,1),pad=0,key='-L5-')],
        [sg.Text(cap[2][1],justification='center',expand_x=False,expand_y=True,size=(10,1),pad=0,key='-L9-')],
        [sg.Text(cap[3][1],justification='center',expand_x=False,expand_y=True,size=(10,1),pad=0,key='-L13-')],
    ]

    col3=[
        [sg.Text(cap[0][2],justification='center',expand_x=False,expand_y=True,size=(10,1),pad=0,key='-L2-')],
        [sg.Text(cap[1][2],justification='center',expand_x=False,expand_y=True,size=(10,1),pad=0,key='-L6-')],
        [sg.Text(cap[2][2],justification='center',expand_x=False,expand_y=True,size=(10,1),pad=0,key='-L10-')],
        [sg.Text(cap[3][2],justification='center',expand_x=False,expand_y=True,size=(10,1),pad=0,key='-L14-')],
    ]

    col4=[
        [sg.Text(cap[0][3],justification='center',expand_x=False,expand_y=True,size=(10,1),pad=0,key='-L3-')],
        [sg.Text(cap[1][3],justification='center',expand_x=False,expand_y=True,size=(10,1),pad=0,key='-L7-')],
        [sg.Text(cap[2][3],justification='center',expand_x=False,expand_y=True,size=(10,1),pad=0,key='-L11-')],
        [sg.Text(cap[3][3],justification='center',expand_x=False,expand_y=True,size=(10,1),pad=0,key='-L15-')],
    ]

    layout=[[sg.Column(col1),sg.Column(col2),sg.Column(col3),sg.Column(col4)]]
    return sg.Window('ボタンステータス',layout,no_titlebar=True,keep_on_top=True,grab_anywhere=True,alpha_channel=0.75)
    
# ルートウィンドウ作成
root = tk.Tk()
# ルートウィンドウの非表示
root.withdraw()

keylist=setting_load()
kl = import_module(keylist)
caption=kl.key_lay()

b_list=[17,18,20,24,33,34,36,40,65,66,68,72,129,130,132,136]
sg.theme('Dark')

window = gui_open(caption)

#ポートの設定
dll = ctypes.CDLL(r'.\ftd2xx64.dll')
handle = ctypes.c_void_p()
res = dll.FT_Open(0, ctypes.pointer(handle))
#res = dll.FT_SetChars(handle, 0xd, 1, 0, 0)
res = dll.FT_SetTimeouts(handle,500,500)
res=dll.FT_SetBaudRate(handle, 921600)
res=dll.FT_SetBitMode(handle, 0x00, 1)

config=0
btpress=False
buff = ctypes.c_long()
btnflg=[False]*16

while True:
    event, values = window.read(timeout=10,timeout_key='-timeout-')
    if event == sg.WIN_CLOSED:#窓を閉じたときの処理
        break
	#ポートのビットを取得してbuffに代入
    res=dll.FT_GetBitMode(handle,ctypes.pointer(buff))
    chk=buff.value in b_list
    if chk:
        #押した時
        btpress=True
        idx=b_list.index(buff.value)
        window['-L'+str(idx)+'-'].update(background_color='blue')
        if idx==15:
            config+=1
            window['-L15-'].update(value=caption[3][3]+'('+str(config)+')')
        else:    
            try:
                btnflg[idx]=kl.btn(idx)
                time.sleep(0.3)
            except:
                aaaa=True
    elif buff.value ==0 and btpress:
        #押して離した時
        if config>=40:
            break
        elif config>=1 and config<10:
            keylist=setting_load()
            if keylist !='':
                del kl
                kl = import_module(keylist)
                reload( kl )
                caption=kl.key_lay()
                k=0
                for i in caption:
                    for j in i:
                        window['-L'+str(k)+'-'].update(value=j,background_color='grey25')
                        k=k+1
        config=0
        window['-L15-'].update(value=caption[3][3])
        for i,x in enumerate(btnflg):
            if x:
                window['-L'+str(i)+'-'].update(background_color='red')
            else:
                window['-L'+str(i)+'-'].update(background_color='grey25')
        btpress=False
    time.sleep(0.0333)

res = dll.FT_Close(handle)
window.close()
