import pyautogui
import win32gui
import pyperclip

def key_lay():
	return [
		['←','→','★','☆'],
		['トリミング','傾き','WB','グリッド'],
		['調整コピー','調整ペースト','',''],
		['Undo','Redo','Reset','機能'],
	]
def btn0():
	x=1
	pyautogui.press('left')
def btn1():
	x=2
	pyautogui.press('right')
def btn2():
	x=3
	pyautogui.hotkey('Ctrl','1')
def btn3():
	x=4
	pyautogui.hotkey('Ctrl','0')
def btn4():
	x=5
	pyautogui.press('t')
def btn5():
	x=6
	pyautogui.press('r')
def btn6():
	x=7
	pyautogui.press('w')
def btn7():
	x=8
	pyautogui.press('Alt')
	pyautogui.PAUSE = 0.2
	pyautogui.press('v')
	pyautogui.PAUSE = 0.2
	pyautogui.press('w')
	pyautogui.PAUSE = 0.2
	pyautogui.press('g')
def btn8():
	x=9
	pyautogui.press('Alt')
	pyautogui.PAUSE = 0.2
	pyautogui.press('a')
	pyautogui.PAUSE = 0.2
	pyautogui.press('c')
def btn9():
	x=10
	pyautogui.press('Alt')
	pyautogui.PAUSE = 0.2
	pyautogui.press('a')
	pyautogui.PAUSE = 0.2
	pyautogui.press('p')
def btn10():
	x=11
def btn11():
	x=12
def btn12():
	x=13
	pyautogui.hotkey('Ctrl','z')
def btn13():
	x=14
	pyautogui.hotkey('Ctrl','y')
def btn14():
	x=15
	pyautogui.hotkey('Ctrl','u')