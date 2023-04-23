import ctypes
import time
import keyboard
import PySimpleGUI as sg
import tkinter as tk
from tkinter import filedialog

import pyautogui
import win32gui
import pyperclip

def setting_load():
	typ = [('設定ファイル', '*.py')]
	dir = r'C:'
	fle = filedialog.askopenfilename(filetypes = typ, initialdir = dir)
	f = fle.split('/')
	mdl=f[-1].replace('.py','')
	return mdl

# ルートウィンドウ作成
root = tk.Tk()
# ルートウィンドウの非表示
root.withdraw()

keylist=setting_load()
exec('import '+keylist + ' as kl')
caption=kl.key_lay()


b_list=[17,18,20,24,33,34,36,40,65,66,68,72,129,130,132,136]
sg.theme('Dark')
layout=[[sg.Table(caption,headings=['A','B','C','D'],select_mode=sg.TABLE_SELECT_MODE_NONE,num_rows=4, def_col_width=10, auto_size_columns=False,justification='center', vertical_scroll_only=True,hide_vertical_scroll=True, key='-button_st-')]]
window = sg.Window('ボタンステータス',layout,no_titlebar=True,keep_on_top=True,grab_anywhere=True,alpha_channel=0.6)


#ポートの設定
dll = ctypes.CDLL(r'.\ftd2xx64.dll')
handle = ctypes.c_void_p()
res = dll.FT_Open(0, ctypes.pointer(handle))
#res = dll.FT_SetChars(handle, 0xd, 1, 0, 0)
res = dll.FT_SetTimeouts(handle,500,500)
res=dll.FT_SetBaudRate(handle, 921600)
res=dll.FT_SetBitMode(handle, 0x00, 1)

config=0
q=0

buff = ctypes.c_long()

while True:
	event, values = window.read(timeout=10,timeout_key='-timeout-')
	if event == sg.WIN_CLOSED:#窓を閉じたときの処理
		break
	#ポートのビットを取得してbuffに代入
	res=dll.FT_GetBitMode(handle,ctypes.pointer(buff))

	for i in b_list:
		if b_list[15]==buff.value:
			config+=1
			caption[3][3]=caption[3][3]+'('+str(config)+')'
			break
		elif i==buff.value:
			btndef='kl.btn'+str(b_list.index(i))+'()'
			try:
				exec(btndef)
			caption[b_list.index(i)//4][b_list.index(i)%4]="＊"+caption[b_list.index(i)//4][b_list.index(i)%4]
			break
		else:
			if config>=20:
				q=1
				break
			elif config>=1 and config<5:
				del kl
				keylist=setting_load()
				exec('import '+keylist + ' as kl')
			config=0
	if q==1:
		q=0
		break
	window['-button_st-'].update(caption)
	caption=kl.key_lay()
	time.sleep(0.1)

res = dll.FT_Close(handle)
window.close()