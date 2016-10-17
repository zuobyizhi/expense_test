# -*- coding: GBK -*-

from Tkinter import *
import urllib
import urllib2
#import webbrowser
import json
import threading
import sys

print sys.getdefaultencoding()
if len(sys.argv) == 1:
	reload(sys)
	sys.setdefaultencoding('gb18030')
else:
	bianma = sys.argv[1]
	reload(sys)
	sys.setdefaultencoding(bianma)
print sys.getdefaultencoding()

#Globel
hosturl='http://testxingzheng.oa.com:8972'
#hosturl='http://xingzheng.oa.com'
glocation=''
guse=''
gtype=''
ggoodcode=''
ggoodprice=''
gnote=''
gnormaltip=unicode('请扫描物品条码\n','eucgb2312_cn')
cur=0
#timer=threading.Timer(1, func)
gstate=''
gdisable=False
gerrormsg=''
macjson=[]
timer=''
gpreid=''
gremark=''

#util
def httpget(url):
	try:
		#webbrowser.open(hosturl+(url).decode('gb18030').encode('utf8'))
		s = urllib2.urlopen((hosturl+url).decode('gb18030').encode('utf8'),timeout=2).read() 
		return s.decode('utf8').encode('gb18030')
	except:
		return 'err'

def guizh(tx):
	return unicode(tx,'eucgb2312_cn')

def jparser(json):
	try:
		return json.loads(json.decode('gb18030').encode('utf8'))
	except:
		return []

#init
def initmacinfo(mj):
	if mj['RetSucceed']:
		print "连接成功"
		if mj['Succeed']:
			global guse
			global glocation
			global gnote
			glocation=mj['Message']['location']
			guse=mj['Message']['machineUse']
			gnote=mj['Message']['machineNote']
			print glocation + " " + guse
			global gdisable
			gdisable = False
		else:
			print "请求失败"
			global gdisable
			global gerrormsg
			gdisable = True
			gerrormsg = mj['Message']
	else:
		print "检查网络连接"
		global gdisable
		global gerrormsg
		gdisable = True
		gerrormsg = unicode("网络连接失败。")

macinfo=httpget('/warehouse/machine/info')
try:
	macjson=json.loads(macinfo.decode('gb18030').encode('utf8'))
	initmacinfo(macjson)
except Exception:
	print 'macjson loads err 1.'
	print sys.exc_info()
	print "检查网络连接"
	global gdisable
	global gerrormsg
	gdisable = True
	gerrormsg = unicode("网络连接失败。")

def getMacInfo():
	global macjson
	macinfo=httpget('/warehouse/machine/info')
	try:
		global gdisable
		global labtip
		bef = gdisable
		print macinfo
		macjson=json.loads(macinfo.decode('gb18030').encode('utf8')) #可能会抛出except
		print macjson
		initmacinfo(macjson) #其中会改写gdisable
		print "111"
		#print "" + bef + " " + gdisable
		print "222"
		if gdisable:
			print "333"
			labtip['text']=gerrormsg
			edit.config(state='disabled')
		if bef==True and gdisable==False:
			print "444"
			#labtip['text']=gerrormsg
			#labtip['text']=unicode('请扫描物品条码\n','eucgb2312_cn')
			#labtip['fg']='#333333'
			edit.config(state='normal')
			global guse
			global glocation
			global gnote
			glocation=macjson['Message']['location']
			guse=macjson['Message']['machineUse']
			gnote=macjson['Message']['machineNote']
			global labsysnote
			labsysnote['text'] = gnote

			#global gtype
			#global labtitle
			#global labctrltitle
			#global gnormaltip
			#if guse == unicode("领用", 'eucgb2312_cn'):
				#labtitle['text']=unicode("物资领用", 'eucgb2312_cn')
				#gnormaltip=unicode('刷卡后完成领用\n','eucgb2312_cn')
				#labtip['text']=gnormaltip
				#gtype='1'
				#labctrltitle['text'] = unicode('1.使用【扫码枪】读取条形码\n2.核对物品信息\n3.在【读卡器】上刷卡完成领用', 'eucgb2312_cn')
			#elif guse == unicode("固定消费", 'eucgb2312_cn'):
				##labtitle['text']=unicode("固定消费", 'eucgb2312_cn')
				#gtype='2'
				#labtitle['text']=unicode("内部消费系统", 'eucgb2312_cn')
				#gnormaltip=unicode('刷卡后完成消费\n','eucgb2312_cn')
				#labtip['text']=gnormaltip
				#getgoodinfo(macjson['Message']['machineRemark'].encode('utf8'))
				#print macjson['Message']['machineRemark']
				#labctrltitle['text'] = unicode('在【读卡器】上刷卡完成消费', 'eucgb2312_cn')
			#elif guse == unicode("固定领用", 'eucgb2312_cn'):
				#gtype='3'
				#labtitle['text']=unicode("物资领用", 'eucgb2312_cn')
				#gnormaltip=unicode('刷卡后完成领用\n','eucgb2312_cn')
				#labtip['text']=gnormaltip
				#getgoodinfo(macjson['Message']['machineRemark'].encode('utf8'))
				#print macjson['Message']['machineRemark']
				#labctrltitle['text'] = unicode('在【读卡器】上刷卡完成领用', 'eucgb2312_cn')
			#else:
				#gtype='0'
				#labtitle['text']=unicode("内部消费系统", 'eucgb2312_cn')
				#labctrltitle['text'] = unicode('1.使用【扫码枪】读取条形码\n2.核对物品信息\n3.在【读卡器】上刷卡完成消费', 'eucgb2312_cn')
				#gnormaltip=unicode('请扫描物品条码\n','eucgb2312_cn')
				#labtip['text']=gnormaltip
				#labtip['fg']='#333333'
			initUI(macjson)

		else:
			use=macjson['Message']['machineUse']
			pretype = ''
			global gtype
			if use == unicode("领用", 'eucgb2312_cn'):
				pretype='1'
			elif use == unicode("固定消费", 'eucgb2312_cn'):
				pretype='2'
			elif use == unicode("固定领用", 'eucgb2312_cn'):
				pretype='3'
			else:
				pretype='0'
			if (gtype != pretype):
				initUI(macjson)
				print "666"
			else: # 系统公告和物品信息的可能更新
				note=macjson['Message']['machineNote']
				global labsysnote
				if pretype=='2' or pretype=='3':
					global gremark
					code = macjson['Message']['machineRemark']
					if code != gremark:
						initUI(macjson)
						print "777"
					else:
						print "888"
				if note != labsysnote['text']:
					labsysnote['text'] = note
					print "999"
			print "555"
			#gdisable = True
		macinfotimerstart()
	except:
		print 'macjson loads err 2.'
		print sys.exc_info()
		global gdisable
		gdisable = True
		macinfotimerstart()
		global labtip
		global edit
		global gpreid
		gpreid = ''
		labtip['text']=unicode("网络异常，请联系助理！", 'eucgb2312_cn')
		labtip['fg']='red'
		edit.delete(0,len(edit.get()))

def macinfotimerstart():
	global gstate
	timer = threading.Timer(5*60, getMacInfo)
	timer.start()
	print "mits"

macinfotimerstart()

#GUI
root = Tk()
root.attributes("-fullscreen", True)
print "root: "+str(root['width'])+","+str(root['height'])
root.title(unicode('内部消费系统','eucgb2312_cn'))

frametop=Frame(root,height=60,width=800)
frametop.pack(side = TOP, pady=30)
frametop.pack_propagate(0)
frameleft=Frame(root,width=400,height=500)
frameleft.pack(side = LEFT, padx=150)
frameleft.pack_propagate(0)
frameright=Frame(root,width=400,height=500)
frameright.pack(side = RIGHT, padx=150)
frameright.pack_propagate(0)

labtitle = Label(frametop,text=guizh('内部消费系统'), font = ("SimSun, 36"))
labtitle.pack( side = TOP, pady=0)

L1 = Label(frameleft, text=unicode('系统提示','eucgb2312_cn'), font=("SimSun, 30"),anchor='w')
L1.pack( side = TOP,fill='x',pady=0)
f1=Frame(frameleft,height=3,bg='#e9e9e9')
f1.pack(side = TOP,fill='x', padx=0)
f1.pack_propagate(0)
f11=Frame(f1,height=3,width=160,bg='#00c0ff')
f11.pack(side = LEFT, padx=0)
f11.pack_propagate(0)
labtip = Label(frameleft,wraplength=380,fg='#333333',height=3, text=unicode('请扫描物品条码\n','eucgb2312_cn'), font=("SimSun, 18"),anchor='nw',justify='left')
labtip.pack( side = TOP,fill='x',pady=0,padx=0)
L2 = Label(frameleft, text=unicode('物品信息','eucgb2312_cn'), font=("SimSun, 30"),anchor='w')
L2.pack( side = TOP,fill='x',pady=0)
f2=Frame(frameleft,height=3,bg='#e9e9e9')
f2.pack(side = TOP,fill='x', padx=0)
f2.pack_propagate(0)
f21=Frame(f2,height=3,width=160,bg='#00c0ff')
f21.pack(side = LEFT, padx=0)
f21.pack_propagate(0)
labgood = Label(frameleft,fg='#333333',wraplength=380,height=3, text=unicode('\n\n\n','eucgb2312_cn'), font=("SimSun, 16"),anchor='nw',justify='left')
labgood.pack( side = TOP,fill='x',pady=0,padx=0)
#L3 = Label(frameleft, text=unicode('','eucgb2312_cn'), font=("SimSun, 40"),fg='red')
#L3.pack( side = TOP,pady=10)
L3 = Label(root, text=unicode('','eucgb2312_cn'), font=("SimSun, 40"),fg='red')
L3.place(relx=0.8,y=70)
L4 = Label(frameleft, text=unicode('条形码/工卡','eucgb2312_cn'), font=("SimSun, 30"),anchor='w')
L4.pack( side = TOP,fill='x',pady=0)
f3=Frame(frameleft,height=3,bg='#e9e9e9')
f3.pack(side = TOP,fill='x', padx=0)
f3.pack_propagate(0)
f31=Frame(f3,height=3,width=220,bg='#00c0ff')
f31.pack(side = LEFT, padx=0)
f31.pack_propagate(0)
edit = Entry(frameleft, bd =0, width=60, font=("SimSun, 22"))
edit.pack(side = TOP,pady=10)
edit.focus()

#L6= Label(frameright, text=unicode(' 温馨提示','eucgb2312_cn'),justify='left', font=("SimSun, 18"),fg='white',bg='#00c0ff',anchor='w')
#L6.pack( side = TOP,pady=0,padx=0,fill='x')
L5= Label(frameright, text=unicode(' 系统公告','eucgb2312_cn'),fg='white',bg='#00c0ff',justify='left', font=("SimSun, 22"),anchor='w')
L5.pack( side = TOP,pady=0,padx=0,fill='x')
f4=Frame(frameright,height=190,bg='white')
f4.pack(side = TOP,fill='x', padx=0)
f4.pack_propagate(0)
labsysnote = Label(f4,fg='#333333',wraplength=320,height=5,justify='left', text=unicode('\n\n\n\n\n','eucgb2312_cn'), font=("SimSun, 16"),bg='white',anchor='nw')
labsysnote.pack( side = TOP,pady=10,padx=16,fill='x')
if gnote != '':
	labsysnote['text']=gnote
L9 = Label(frameright, text=unicode('','eucgb2312_cn'), font=("SimSun, 20"),fg='red')
L9.pack( side = TOP,pady=0)
L6 = Label(frameright,compound = 'left',justify='left',fg='white',bg='#00c0ff', text=unicode(' 操作指南','eucgb2312_cn'), font=("SimSun, 22"),anchor='w')
L6.pack( side = TOP,pady=0,padx=0,fill='x')
f5=Frame(frameright,height=140,bg='white')
f5.pack(side = TOP,fill='x', padx=0)
f5.pack_propagate(0)
labctrltitle = Label(f5,bg='white',height=5,anchor='nw',justify='left',fg='#333333', text=unicode('1.使用【扫码枪】读取条形码\n2.核对物品信息\n3.在【读卡器】上刷卡完成消费','eucgb2312_cn'), font=("SimSun, 16"))
labctrltitle.pack( side = TOP,pady=10,padx=16,fill='x')

#连接口
def getgoodinfo(code):
	print "getgoodinfo code: "+code
	global guse
	global glocation
	global hosturl
	print "getgoodinfo: " + (glocation) + " " + (guse)
	giurl=''
	global gtype
	if gtype == '1':
		giurl=hosturl+'/warehouse/goods/barcode?use=正常销售,促销,非卖品,食堂&code='+code+'&location='
	elif gtype == '2':
		giurl=hosturl+'/warehouse/goods/barcode?use=正常销售,促销,食堂&code='+code+'&location='
	elif gtype == '3':
		giurl=hosturl+'/warehouse/goods/barcode?use=正常销售,促销,非卖品,食堂&code='+code+'&location='
	else:
		giurl=hosturl+'/warehouse/goods/barcode?use=正常销售,促销&code='+code+'&location='
	r = urllib.urlopen(giurl.decode('gb18030').encode('utf8')+glocation.encode('utf8')).read().decode('utf8').encode('gb18030')
	print giurl.decode('gb18030').encode('utf8')+glocation.encode('utf8')
	print r
	if r!='':
		print r
		global edit
		edit.delete(0,len(edit.get()))
		mj =json.loads(r.decode('gb18030').encode('utf8'))
		if mj['RetSucceed'] & mj['Succeed']:
			clearAll()
			global timer
			if timer != '':
				timer.cancel()
			global ggoodcode
			global ggoodprice
			global gtype
			ggoodcode=mj['Message']['goodsID']
			if gtype == '0':
				labgood['text']=unicode("物品名称:", 'eucgb2312_cn') + mj['Message']['goodsName'] + unicode("\n价格:",'eucgb2312_cn') + str(mj['Message']['goodsPrice'])
			elif gtype=='1':
				labgood['text']=unicode("物品名称:", 'eucgb2312_cn') + mj['Message']['goodsName']
			elif gtype=='3':
				labgood['text']=unicode("物品名称:", 'eucgb2312_cn') + mj['Message']['goodsName']
			else:
				labgood['text']=unicode("物品名称:", 'eucgb2312_cn') + mj['Message']['goodsName'] + unicode("\n价格:",'eucgb2312_cn') + str(mj['Message']['goodsPrice'])
			ggoodprice = str(mj['Message']['goodsPrice'])
			global gtype
			if gtype == '2':
				print "gtype = 2"
				return
			if gtype == '3':
				print "gtype = 3"
				return
			global cur
			global gstate
			if gstate=='15':
				cur=15
				return
			gstate = '15'
			cur=15
			#timerstart()
			func()
		else:
			clearAll()
			global labtip
			labtip['text']=mj['Message']
			labtip['fg']='red'
			global gtype
			show10sec()
	else:
		global labtip
		labtip['text']=unicode("查询物品接口错误，请联系助理！", 'eucgb2312_cn')
		labtip['fg']='red'
		global edit
		edit.delete(0,len(edit.get()))
		show10sec()
		print 'err'

def dealsend(id):
	global ggoodcode
	global edit
	if ggoodcode == '':
		print "goodsID empty."
		edit.delete(0,len(edit.get()))
		return
	global gtype
	if True: #gtype=='2':
		global gpreid # 阻止同一个人误刷多次
		global cur
		if gpreid==id:
			print "repeat send."
			edit.delete(0,len(edit.get()))
			global labtip
			labtip['text']=unicode("请勿重复打卡！\n", 'eucgb2312_cn')
			labtip['fg']='red'
			return
		else:
			gpreid = id
	global gstate
	if gstate=='10' and (gtype=='0' or gtype=='1'):
		print "repeat send."
		edit.delete(0,len(edit.get()))
		clearAll()
		return
	giurl='/warehouse/record'
	global guse
	global hosturl
	global labtip
	data = {}
	data['recordType'] = guse.encode('utf8')
	data['userCardID'] = id
	data['goodsID'] = ggoodcode
	print data
	#r=httpget(giurl)
	r=urllib2.urlopen(hosturl+giurl, timeout=2, data=urllib.urlencode(data)).read().decode('utf8').encode('gb18030')
	if r!='':
		print r
		edit.delete(0,len(edit.get()))
		sendjson=json.loads(r.decode('gb18030').encode('utf8'))
		if sendjson['RetSucceed'] & sendjson['Succeed']:
			global gtype
			if gtype == '1':
				labtip['text']=unicode("领用成功！\n", 'eucgb2312_cn')
			elif gtype == '3':
				labtip['text']=unicode("领用成功！\n", 'eucgb2312_cn')
			else:
				labtip['text']=unicode("消费成功！\n", 'eucgb2312_cn')
			labtip['fg']='#08b439'
			show10sec()
		else:
			clearAll()
			labtip['text']=sendjson['Message']
			labtip['fg']='red'
			show10sec()
	else:
		labtip['text']=unicode("获取工卡接口错误，请联系助理！", 'eucgb2312_cn')
		labtip['fg']='red'
		edit.delete(0,len(edit.get()))
		show10sec()
		print 'err'

def show10sec():
	global timer
	if timer != '':
		timer.cancel()
	global cur
	cur=10
	global gstate
	gstate = '10'
	#timerstart()
	func2()

def func():
	global gstate
	if gstate != '15':
		return
	global cur
	global L3
	L3['text']=str(cur)
	global labtip
	global gtype
	if gtype == '1':
		labtip['text']=unicode("请在"+str(cur)+"秒内刷卡完成领用。\n", 'eucgb2312_cn')
		labtip['fg']='#333333'
	elif gtype == '0':
		labtip['text']=unicode("请在"+str(cur)+"秒内刷卡完成消费，本次消费金额为" + ggoodprice + "元。", 'eucgb2312_cn')
		labtip['fg']='#333333'
	else:
		pass
	if cur==0:
		clearAll()
		pass
	else:
		cur=cur-1
		timerstart()

def func2():
	global gstate
	if gstate != '10':
		return
	global cur
	global L3
	L3['text']=str(cur)
	if cur==0:
		clearAll()
		pass
	else:
		cur=cur-1
		timerstart()

def timerstart():
	global gstate
	global timer
	timer = threading.Timer(1, func)
	if gstate == '10':
		timer = threading.Timer(1, func2)
	timer.start()

def clearAll():
	global ggoodcode
	global gnormaltip
	global gtype
	global gstate
	global labtip
	global gpreid
	gpreid = ''
	#labtip['text']=unicode('请扫描物品条码','eucgb2312_cn')
	labtip['text']=gnormaltip
	labtip['fg']='#333333'
	L3['text']=''
	gstate=''
	if gtype == '0':
		labgood['text']=unicode("\n\n\n", 'eucgb2312_cn')
		ggoodcode=''
	if gtype == '1':
		labgood['text']=unicode("\n\n\n", 'eucgb2312_cn')
		ggoodcode=''

def worker(*arg):
	#edit.delete(0,len(edit.get()))
	global edit
	tx=edit.get().strip()
	print "code: "+tx
	#giurl=hosturl+'/warehouse/goods/barcode?use=正常销售&code=4895058311125&location=广州'
	#print '\n'+giurl+'\n'
	#webbrowser.open(giurl)
	#print urllib.urlopen(giurl.decode('gb18030').encode('utf8')).read().decode('utf8').encode('gb18030')

	if edit['state'] == 'disabled':
		return

	try:
		if len(tx) == 10:
			dealsend(tx)
		else:
			getgoodinfo(tx)
	except:
		global labtip
		#global edit
		global gpreid
		gpreid = ''
		labtip['text']=unicode("网络异常，请联系助理！", 'eucgb2312_cn')
		labtip['fg']='red'
		edit.delete(0,len(edit.get()))
		global gdisable
		gdisable = True

if guse == unicode("领用", 'eucgb2312_cn'):
	labtitle['text']=unicode("物资领用", 'eucgb2312_cn')
	gtype='1'
	labctrltitle['text'] = unicode('1.使用【扫码枪】读取条形码\n2.核对物品信息\n3.在【读卡器】上刷卡完成领用', 'eucgb2312_cn')
	gnormaltip=unicode('刷卡后完成领用\n','eucgb2312_cn')
	labtip['text']=gnormaltip
elif guse == unicode("固定消费", 'eucgb2312_cn'):
	#labtitle['text']=unicode("固定消费", 'eucgb2312_cn')
	gtype='2'
	gnormaltip=unicode('刷卡后完成消费\n','eucgb2312_cn')
	labtip['text']=gnormaltip
	getgoodinfo(macjson['Message']['machineRemark'].encode('utf8'))
	print macjson['Message']['machineRemark']
	gremark = macjson['Message']['machineRemark']
	labctrltitle['text'] = unicode('在【读卡器】上刷卡完成消费', 'eucgb2312_cn')
elif guse == unicode("固定领用", 'eucgb2312_cn'):
	gtype='3'
	labtitle['text']=unicode("物资领用", 'eucgb2312_cn')
	gnormaltip=unicode('刷卡后完成领用\n','eucgb2312_cn')
	labtip['text']=gnormaltip
	getgoodinfo(macjson['Message']['machineRemark'].encode('utf8'))
	print macjson['Message']['machineRemark']
	gremark = macjson['Message']['machineRemark']
	labctrltitle['text'] = unicode('在【读卡器】上刷卡完成领用', 'eucgb2312_cn')
else:
	gtype='0'
	gnormaltip=unicode('请扫描物品条码\n','eucgb2312_cn')

def initUI(macjson):
	global gtype
	global labtip
	global labtitle
	global labctrltitle
	global gnormaltip
	global labsysnote
	if guse == unicode("领用", 'eucgb2312_cn'):
		labtitle['text']=unicode("物资领用", 'eucgb2312_cn')
		gnormaltip=unicode('刷卡后完成领用\n','eucgb2312_cn')
		labtip['text']=gnormaltip
		gtype='1'
		labctrltitle['text'] = unicode('1.使用【扫码枪】读取条形码\n2.核对物品信息\n3.在【读卡器】上刷卡完成领用', 'eucgb2312_cn')
		labsysnote['text'] = gnote
	elif guse == unicode("固定消费", 'eucgb2312_cn'):
		#labtitle['text']=unicode("固定消费", 'eucgb2312_cn')
		gtype='2'
		labtitle['text']=unicode("内部消费系统", 'eucgb2312_cn')
		gnormaltip=unicode('刷卡后完成消费\n','eucgb2312_cn')
		labtip['text']=gnormaltip
		getgoodinfo(macjson['Message']['machineRemark'].encode('utf8'))
		print macjson['Message']['machineRemark']
		global gremark
		gremark = macjson['Message']['machineRemark']
		labctrltitle['text'] = unicode('在【读卡器】上刷卡完成消费', 'eucgb2312_cn')
		labsysnote['text'] = gnote
	elif guse == unicode("固定领用", 'eucgb2312_cn'):
		gtype='3'
		labtitle['text']=unicode("物资领用", 'eucgb2312_cn')
		gnormaltip=unicode('刷卡后完成领用\n','eucgb2312_cn')
		labtip['text']=gnormaltip
		getgoodinfo(macjson['Message']['machineRemark'].encode('utf8'))
		print macjson['Message']['machineRemark']
		global gremark
		gremark = macjson['Message']['machineRemark']
		labctrltitle['text'] = unicode('在【读卡器】上刷卡完成领用', 'eucgb2312_cn')
		labsysnote['text'] = gnote
	else:
		gtype='0'
		labtitle['text']=unicode("内部消费系统", 'eucgb2312_cn')
		labctrltitle['text'] = unicode('1.使用【扫码枪】读取条形码\n2.核对物品信息\n3.在【读卡器】上刷卡完成消费', 'eucgb2312_cn')
		gnormaltip=unicode('请扫描物品条码\n','eucgb2312_cn')
		labtip['text']=gnormaltip
		labtip['fg']='#333333'
		labsysnote['text'] = gnote

if gdisable:
	labtip['text']=gerrormsg
	edit.config(state='disabled')

root.bind('<Return>',worker)
root.mainloop()
