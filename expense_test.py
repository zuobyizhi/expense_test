# -*- coding: GBK -*-

from Tkinter import *
import urllib
import urllib2
#import webbrowser
import json
import threading
import sys
import traceback

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
gnormaltip=unicode('��ɨ����Ʒ����\n','eucgb2312_cn')
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
		
def bconsume():
	global gtype
	return gtype == '0'
	
def breceive():
	global gtype
	return gtype == '1'
	
def bfixconsume():
	global gtype
	return gtype == '2'
	
def bfixreceive():
	global gtype
	return gtype == '3'
	
def maketype(_use):
	if _use == unicode("����", 'eucgb2312_cn'):
		return '1'
	elif _use == unicode("�̶�����", 'eucgb2312_cn'):
		return '2'
	elif _use == unicode("�̶�����", 'eucgb2312_cn'):
		return '3'
	else:
		return '0'

class GoodsRecorder:
	goods = {}
	goodsnum = 0
	goodstotal = 0.0
	def __init__(self):
		self.clear()
	def addgood(self,goodid,price=0.0):
		self.goodsnum += 1
		self.goodstotal += price
		if goodid in self.goods:
			self.goods[goodid] += 1
		else:
			self.goods[goodid] = 1
		return self
	def full(self, goodid):
		m = 2#10
		l = len(self.goods.keys())
		if m > l:
			print "f1"
			return False
		elif m == l:
			print "f2"
			print not goodid in self.goods.keys()
			return not goodid in self.goods.keys()
		else:
			print "f3"
			return True
	def getString(self):
		strg = ''
		strn = ''
		for i,g in enumerate(self.goods.keys()):
			if i == 0:
				strg = str(g)
				strn = str(self.goods[g])
			else:
				strg += "," + str(g)
				strn += "," + str(self.goods[g])
		return strg, strn
	def number(self):
		return self.goodsnum
	def clear(self):
		self.goods = {}
		self.goodsnum = 0
		self.goodstotal = 0.0
		
goodsRecorder = GoodsRecorder()

#init
def initmacinfo(mj):
	if mj['RetSucceed']:
		print "���ӳɹ�"
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
			print "����ʧ��"
			global gdisable
			global gerrormsg
			gdisable = True
			gerrormsg = mj['Message']
	else:
		print "�����������"
		global gdisable
		global gerrormsg
		gdisable = True
		gerrormsg = unicode("��������ʧ�ܡ�")

macinfo=httpget('/warehouse/machine/info')
try:
	macjson=json.loads(macinfo.decode('gb18030').encode('utf8'))
	initmacinfo(macjson)
except Exception:
	print 'macjson loads err 1.'
	print sys.exc_info()
	print "�����������"
	global gdisable
	global gerrormsg
	gdisable = True
	gerrormsg = unicode("��������ʧ�ܡ�")

def getMacInfo():
	global macjson
	macinfo=httpget('/warehouse/machine/info')
	try:
		global gdisable
		global labtip
		bef = gdisable
		print macinfo
		macjson=json.loads(macinfo.decode('gb18030').encode('utf8')) #���ܻ��׳�except
		print macjson
		initmacinfo(macjson) #���л��дgdisable
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
			#labtip['text']=unicode('��ɨ����Ʒ����\n','eucgb2312_cn')
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

			initUI(macjson)

		else:
			use=macjson['Message']['machineUse']
			pretype = ''
			global gtype
			pretype = maketype(use)
			if (gtype != pretype):
				initUI(macjson)
				print "666"
			else: # ϵͳ�������Ʒ��Ϣ�Ŀ��ܸ���
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
		labtip['text']=unicode("�����쳣������ϵ����", 'eucgb2312_cn')
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
root.title(unicode('�ڲ�����ϵͳ','eucgb2312_cn'))

frametop=Frame(root,height=60,width=800)
frametop.pack(side = TOP, pady=30)
frametop.pack_propagate(0)
frameleft=Frame(root,width=400,height=500)
frameleft.pack(side = LEFT, padx=150)
frameleft.pack_propagate(0)
frameright=Frame(root,width=400,height=500)
frameright.pack(side = RIGHT, padx=150)
frameright.pack_propagate(0)

labtitle = Label(frametop,text=guizh('�ڲ�����ϵͳ'), font = ("SimSun, 36"))
labtitle.pack( side = TOP, pady=0)

L1 = Label(frameleft, text=unicode('ϵͳ��ʾ','eucgb2312_cn'), font=("SimSun, 30"),anchor='w')
L1.pack( side = TOP,fill='x',pady=0)
f1=Frame(frameleft,height=3,bg='#e9e9e9')
f1.pack(side = TOP,fill='x', padx=0)
f1.pack_propagate(0)
f11=Frame(f1,height=3,width=160,bg='#00c0ff')
f11.pack(side = LEFT, padx=0)
f11.pack_propagate(0)
labtip = Label(frameleft,wraplength=380,fg='#333333',height=3, text=unicode('��ɨ����Ʒ����\n','eucgb2312_cn'), font=("SimSun, 18"),anchor='nw',justify='left')
labtip.pack( side = TOP,fill='x',pady=0,padx=0)
L2 = Label(frameleft, text=unicode('��Ʒ��Ϣ','eucgb2312_cn'), font=("SimSun, 30"),anchor='w')
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
L4 = Label(frameleft, text=unicode('������/����','eucgb2312_cn'), font=("SimSun, 30"),anchor='w')
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

#L6= Label(frameright, text=unicode(' ��ܰ��ʾ','eucgb2312_cn'),justify='left', font=("SimSun, 18"),fg='white',bg='#00c0ff',anchor='w')
#L6.pack( side = TOP,pady=0,padx=0,fill='x')
L5= Label(frameright, text=unicode(' ϵͳ����','eucgb2312_cn'),fg='white',bg='#00c0ff',justify='left', font=("SimSun, 22"),anchor='w')
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
L6 = Label(frameright,compound = 'left',justify='left',fg='white',bg='#00c0ff', text=unicode(' ����ָ��','eucgb2312_cn'), font=("SimSun, 22"),anchor='w')
L6.pack( side = TOP,pady=0,padx=0,fill='x')
f5=Frame(frameright,height=140,bg='white')
f5.pack(side = TOP,fill='x', padx=0)
f5.pack_propagate(0)
labctrltitle = Label(f5,bg='white',height=5,anchor='nw',justify='left',fg='#333333', text=unicode('1.ʹ�á�ɨ��ǹ����ȡ������\n2.�˶���Ʒ��Ϣ\n3.�ڡ�����������ˢ���������','eucgb2312_cn'), font=("SimSun, 16"))
labctrltitle.pack( side = TOP,pady=10,padx=16,fill='x')

#���ӿ�
def getgoodinfo(code):
	print "getgoodinfo code: "+code
	global guse
	global glocation
	global hosturl
	print "getgoodinfo: " + (glocation) + " " + (guse)
	giurl=''
	if breceive():
		giurl=hosturl+'/warehouse/goods/barcode?use=��������,����,����Ʒ,ʳ��&code='+code+'&location='
	elif bfixconsume():
		giurl=hosturl+'/warehouse/goods/barcode?use=��������,����,ʳ��&code='+code+'&location='
	elif bfixreceive():
		giurl=hosturl+'/warehouse/goods/barcode?use=��������,����,����Ʒ,ʳ��&code='+code+'&location='
	else:
		giurl=hosturl+'/warehouse/goods/barcode?use=��������,����&code='+code+'&location='
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
			global goodsRecorder
			ggoodcode=mj['Message']['goodsID']
			ggoodprice = str(mj['Message']['goodsPrice'])
			if goodsRecorder.full(ggoodcode):
				labtip['text']=unicode("���Ѳ����������Ʒ��")
				labgood['text']=unicode("�����������10����Ʒ\n�����", 'eucgb2312_cn') + str(goodsRecorder.goodsnum) + unicode("����Ʒ	�ܼ۸�:",'eucgb2312_cn') + ggoodprice + unicode("Ԫ",'eucgb2312_cn')
			elif bconsume():
				global goodsRecorder
				goodsRecorder.addgood(ggoodcode, float(ggoodprice))
				ggoodprice = str(goodsRecorder.goodstotal)
				if goodsRecorder.goodsnum == 1:
					labgood['text']=unicode("��Ʒ����:", 'eucgb2312_cn') + mj['Message']['goodsName'] + unicode("\n�۸�:",'eucgb2312_cn') + ggoodprice + unicode("Ԫ",'eucgb2312_cn')
				else:
					labgood['text']=unicode("�����������10����Ʒ\n�����", 'eucgb2312_cn') + str(goodsRecorder.goodsnum) + unicode("����Ʒ	�ܼ۸�:",'eucgb2312_cn') + ggoodprice + unicode("Ԫ",'eucgb2312_cn')
			elif breceive():
				global goodsRecorder
				goodsRecorder.addgood(ggoodcode)
				if goodsRecorder.goodsnum == 1:
					labgood['text']=unicode("��Ʒ����:", 'eucgb2312_cn') + mj['Message']['goodsName']
				else:
					labgood['text']=unicode("�����������10����Ʒ\n�����", 'eucgb2312_cn') + str(goodsRecorder.goodsnum) + unicode("����Ʒ",'eucgb2312_cn')
			elif bfixreceive():
				labgood['text']=unicode("��Ʒ����:", 'eucgb2312_cn') + mj['Message']['goodsName']
				return
			else:
				labgood['text']=unicode("��Ʒ����:", 'eucgb2312_cn') + mj['Message']['goodsName'] + unicode("\n�۸�:",'eucgb2312_cn') + ggoodprice
				return
			# if bfixreceive() or bfixconsume():
			#	return # �̶���Ŀ��ȡ��Ʒ������
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
			global goodsRecorder
			global labtip
			if bconsume() and goodsRecorder.goodsnum>0:
				labtip['text']=mj['Message'] + unicode("\n���蹺������Ʒ�������ɨ�롣")
				labtip['fg']='#333333'
			elif breceive() and goodsRecorder.goodsnum>0:
				labtip['text']=mj['Message'] + unicode("\n������ȡ�����Ʒ�������ɨ�롣")
				labtip['fg']='#333333'
			else:
				clearAll()
				labtip['text']=mj['Message']
				labtip['fg']='red'
			show10sec()
	else:
		global labtip
		labtip['text']=unicode("��ѯ��Ʒ�ӿڴ�������ϵ����", 'eucgb2312_cn')
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
		global gpreid # ��ֹͬһ������ˢ���
		global cur
		if gpreid==id:
			print "repeat send."
			edit.delete(0,len(edit.get()))
			global labtip
			labtip['text']=unicode("�����ظ��򿨣�\n", 'eucgb2312_cn')
			labtip['fg']='red'
			return # ����϶���
		else:
			gpreid = id
	global gstate
	global goodsRecorder
	if gstate=='10' and (gtype=='0' or gtype=='1') and goodsRecorder.goodsnum==0:
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
	# data['goodsID'] = ggoodcode
	global goodsRecorder
	print "1"
	gsid, gsnum = goodsRecorder.getString()
	print "2"
	data['goodsID'] = gsid
	data['goodsNumber'] = gsnum
	print data
	#r=httpget(giurl)
	r=urllib2.urlopen(hosturl+giurl, timeout=2, data=urllib.urlencode(data)).read().decode('utf8').encode('gb18030')
	if r!='':
		print r
		edit.delete(0,len(edit.get()))
		sendjson=json.loads(r.decode('gb18030').encode('utf8'))
		if sendjson['RetSucceed'] & sendjson['Succeed']:
			if breceive() or bfixreceive():
				labtip['text']=unicode("���óɹ���\n", 'eucgb2312_cn')
			else:
				labtip['text']=unicode("���ѳɹ���\n", 'eucgb2312_cn')
			labtip['fg']='#08b439'
			show10sec()
		else:
			clearAll()
			labtip['text']=sendjson['Message']
			labtip['fg']='red'
			show10sec()
	else:
		labtip['text']=unicode("��ȡ�����ӿڴ�������ϵ����", 'eucgb2312_cn')
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

def func(): # 15�뵹��
	global gstate
	if gstate != '15':
		return
	global cur
	global L3
	L3['text']=str(cur)
	global labtip
	global goodsRecorder
	global ggoodcode
	if goodsRecorder.full(ggoodcode):
		labtip['text']=unicode("���Ѳ����������Ʒ��")
	elif breceive():
		# labtip['text']=unicode("����"+str(cur)+"����ˢ��������á�\n", 'eucgb2312_cn')
		labtip['text']=unicode("����"+str(cur)+"����ˢ��������ã�\n������ȡ�����Ʒ�������ɨ�롣", 'eucgb2312_cn')
		labtip['fg']='#333333'
	elif bconsume():
		# labtip['text']=unicode("����"+str(cur)+"����ˢ��������ѣ��������ѽ��Ϊ" + ggoodprice + "Ԫ��", 'eucgb2312_cn')
		labtip['text']=unicode("����"+str(cur)+"����ˢ��������ѣ�\n���蹺������Ʒ�������ɨ�롣", 'eucgb2312_cn')
		labtip['fg']='#333333'
	else:
		pass
	if cur==0:
		clearAll()
	else:
		cur=cur-1
		timerstart()

def func2(): # 10�뵹��
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
	global gstate
	global labtip
	global gpreid
	gpreid = ''
	#labtip['text']=unicode('��ɨ����Ʒ����','eucgb2312_cn')
	labtip['text']=gnormaltip
	labtip['fg']='#333333'
	L3['text']=''
	gstate=''
	if bconsume() or breceive():
		labgood['text']=unicode("\n\n\n", 'eucgb2312_cn')
		ggoodcode=''
		if cur==0:
			global goodsRecorder
			goodsRecorder.clear()

def worker(*arg):
	#edit.delete(0,len(edit.get()))
	global edit
	tx=edit.get().strip()
	print "code: "+tx
	#giurl=hosturl+'/warehouse/goods/barcode?use=��������&code=4895058311125&location=����'
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
		labtip['text']=unicode("�����쳣������ϵ����", 'eucgb2312_cn')
		labtip['fg']='red'
		edit.delete(0,len(edit.get()))
		global gdisable
		gdisable = True
		traceback.print_exc()

def initUI(macjson):
	global gtype
	global labtip
	global labgood
	global labtitle
	global labctrltitle
	global gnormaltip
	global labsysnote
	if guse == unicode("����", 'eucgb2312_cn'):
		labtitle['text']=unicode("��������", 'eucgb2312_cn')
		gnormaltip=unicode('ˢ�����������\n','eucgb2312_cn')
		labtip['text']=gnormaltip
		gtype='1'
		labctrltitle['text'] = unicode('1.ʹ�á�ɨ��ǹ����ȡ������\n2.�˶���Ʒ��Ϣ\n3.�ڡ�����������ˢ���������', 'eucgb2312_cn')
		labsysnote['text'] = gnote
		labgood['text']=unicode("\n\n\n", 'eucgb2312_cn')
	elif guse == unicode("�̶�����", 'eucgb2312_cn'):
		#labtitle['text']=unicode("�̶�����", 'eucgb2312_cn')
		gtype='2'
		labtitle['text']=unicode("�ڲ�����ϵͳ", 'eucgb2312_cn')
		gnormaltip=unicode('ˢ�����������\n','eucgb2312_cn')
		labtip['text']=gnormaltip
		getgoodinfo(macjson['Message']['machineRemark'].encode('utf8'))
		print macjson['Message']['machineRemark']
		global gremark
		gremark = macjson['Message']['machineRemark']
		labctrltitle['text'] = unicode('�ڡ�����������ˢ���������', 'eucgb2312_cn')
		labsysnote['text'] = gnote
	elif guse == unicode("�̶�����", 'eucgb2312_cn'):
		gtype='3'
		labtitle['text']=unicode("��������", 'eucgb2312_cn')
		gnormaltip=unicode('ˢ�����������\n','eucgb2312_cn')
		labtip['text']=gnormaltip
		getgoodinfo(macjson['Message']['machineRemark'].encode('utf8'))
		print macjson['Message']['machineRemark']
		global gremark
		gremark = macjson['Message']['machineRemark']
		labctrltitle['text'] = unicode('�ڡ�����������ˢ���������', 'eucgb2312_cn')
		labsysnote['text'] = gnote
	else:
		gtype='0'
		labtitle['text']=unicode("�ڲ�����ϵͳ", 'eucgb2312_cn')
		labctrltitle['text'] = unicode('1.ʹ�á�ɨ��ǹ����ȡ������\n2.�˶���Ʒ��Ϣ\n3.�ڡ�����������ˢ���������', 'eucgb2312_cn')
		gnormaltip=unicode('��ɨ����Ʒ����\n','eucgb2312_cn')
		labtip['text']=gnormaltip
		labtip['fg']='#333333'
		labsysnote['text'] = gnote
		labgood['text']=unicode("\n\n\n", 'eucgb2312_cn')

initUI(macjson)

if gdisable:
	labtip['text']=gerrormsg
	edit.config(state='disabled')

root.bind('<Return>',worker)
root.mainloop()
