# -*- coding: utf-8 -*-

import LINETCR
from LINETCR.lib.curve.ttypes import *
from multiprocessing import Pool
import time,random,sys,json,codecs,threading,glob,re,datetime,urllib2,pickle

cl = LINETCR.LINE()
cl.login(qr=True)
cl.loginResult()

kk = LINETCR.LINE()

TyfeLogged = False

with open('tval.pkl') as f:
    seeall,tadmin,banned = pickle.load(f)

print "login success"
reload(sys)
sys.setdefaultencoding('utf-8')

Amid = cl.getProfile().mid

wait = {
    'contact':False,
    'autoJoin':True,
    'autoCancel':{"on":True,"members":0},
    'leaveRoom':True,
    'timeline':True,
    'autoAdd':False,
    'message':"",
    "lang":"JP",
    "comment":"",
    "commentOn":False,
    "commentBlack":{},
    "wblack":False,
    "dblack":False,
    "clock":True,
    "cName":"",
    "blacklist":{},
    "wblacklist":False,
    "dblacklist":False,
    "protectionOn":True,
    "atjointicket":False,
    "alwayRead":False
    }

wait2 = {
    'readPoint':{},
    'readMember':{},
    'setTime':{},
    'ROM':{}
    }

setTime = {}
setTime = wait2['setTime']

dangerMessage = ["cleanse","group cleansed.","mulai",".winebot",".kickall","mayhem","kick on","makasih :d","!kickall","nuke"]

def sendMessage(to, text, contentMetadata={}, contentType=0):
    mes = Message()
    mes.to, mes.from_ = to, profile.mid
    mes.text = text
    mes.contentType, mes.contentMetadata = contentType, contentMetadata
    if to not in messageReq:
        messageReq[to] = -1
    messageReq[to] += 1

def NOTIFIED_READ_MESSAGE(op):
    try:
        if op.param1 in wait2['readPoint']:
            Name = cl.getContact(op.param2).displayName
            if Name in wait2['readMember'][op.param1]:
                pass
            else:
                wait2['readMember'][op.param1] += "\n・" + Name
                wait2['ROM'][op.param1][op.param2] = "・" + Name
        else:
            pass
    except:
        pass

def time_converter(time):
    converted_time = datetime.datetime.fromtimestamp(
        int(time)
    ).strftime('%I:%M %p')
    return converted_time


def url_builder(city_id):
    user_api = '211c77f3a8739b420fc2e039a8d94a4d'  # Obtain yours form: http://openweathermap.org/
    unit = 'metric'  # For Fahrenheit use imperial, for Celsius use metric, and the default is Kelvin.
    api = 'http://api.openweathermap.org/data/2.5/weather?id='     # Search for your city ID here: http://bulk.openweathermap.org/sample/city.list.json.gz

    full_api_url = api + str(city_id) + '&mode=json&units=' + unit + '&APPID=' + user_api
    return full_api_url


def data_fetch(full_api_url):
    url = urllib2.urlopen(full_api_url)
    output = url.read().decode('utf-8')
    raw_api_dict = json.loads(output)
    url.close()
    return raw_api_dict


def data_organizer(raw_api_dict):
    data = dict(
        city=raw_api_dict.get('name'),
        country=raw_api_dict.get('sys').get('country'),
        temp=raw_api_dict.get('main').get('temp'),
        temp_max=raw_api_dict.get('main').get('temp_max'),
        temp_min=raw_api_dict.get('main').get('temp_min'),
        humidity=raw_api_dict.get('main').get('humidity'),
        pressure=raw_api_dict.get('main').get('pressure'),
        sky=raw_api_dict['weather'][0]['main'],
        sunrise=time_converter(raw_api_dict.get('sys').get('sunrise')),
        sunset=time_converter(raw_api_dict.get('sys').get('sunset')),
        wind=raw_api_dict.get('wind').get('speed'),
        wind_deg=raw_api_dict.get('deg'),
        dt=time_converter(raw_api_dict.get('dt')),
        cloudiness=raw_api_dict.get('clouds').get('all')
    )
    return data


def data_output(to,data,prov):
    m_symbol = ' °C'
    if prov == 1:
        kk.sendText(to,"สภาพอากาศ: เชียงใหม่\nอุณหภูมิ: "+str(data['temp'])+m_symbol+"\n(มากสุด: "+str(data['temp_max'])+m_symbol+", น้อยสุด: "+str(data['temp_max'])+m_symbol+")\n\nแรงลม: "+str(data['wind'])+"\nความชื้น: "+str(data['humidity'])+"\nเมฆ: "+str(data['cloudiness'])+"%\nความดัน: "+str(data['pressure'])+"\nดวงอาทิตย์ขึ้น: "+str(data['sunrise'])+"\nดวงอาทิตย์ตก: "+str(data['sunset'])+"\n\nอัพเดทล่าสุด: "+str(data['dt']))
    elif prov == 2:
        kk.sendText(to,"สภาพอากาศ: อุบลราชธานี\nอุณหภูมิ: "+str(data['temp'])+m_symbol+"\n(มากสุด: "+str(data['temp_max'])+m_symbol+", น้อยสุด: "+str(data['temp_max'])+m_symbol+")\n\nแรงลม: "+str(data['wind'])+"\nความชื้น: "+str(data['humidity'])+"\nเมฆ: "+str(data['cloudiness'])+"%\nความดัน: "+str(data['pressure'])+"\nดวงอาทิตย์ขึ้น: "+str(data['sunrise'])+"\nดวงอาทิตย์ตก: "+str(data['sunset'])+"\n\nอัพเดทล่าสุด: "+str(data['dt']))
    elif prov == 3:
        kk.sendText(to,"สภาพอากาศ: กรุงเทพมหานคร\nอุณหภูมิ: "+str(data['temp'])+m_symbol+"\n(มากสุด: "+str(data['temp_max'])+m_symbol+", น้อยสุด: "+str(data['temp_max'])+m_symbol+")\n\nแรงลม: "+str(data['wind'])+"\nความชื้น: "+str(data['humidity'])+"\nเมฆ: "+str(data['cloudiness'])+"%\nความดัน: "+str(data['pressure'])+"\nดวงอาทิตย์ขึ้น: "+str(data['sunrise'])+"\nดวงอาทิตย์ตก: "+str(data['sunset'])+"\n\nอัพเดทล่าสุด: "+str(data['dt']))

def text_has_emoji(text):
    for character in text:
        if character in emoji.UNICODE_EMOJI:
            return True
    return False

def cloudupdate(data):
    return "เชียงใหม่ เมฆ: "+str(data['cloudiness'])+"%"

user1 = Amid
user2 = ""

Rapid1To = ""

def Rapid1Say(mtosay):
    cl.sendText(Rapid1To,mtosay)

mimic = {
    "copy":False,
    "copy2":False,
    "status":False,
    "target":{}
    }

readAlert = False

def user1script(op):
    global TyfeLogged
    global kk
    global user2
    global readAlert
    try:
        # if op.type not in [61,60,48,25,26]:
            # print str(op)
            # print "\n\n"
        if op.type == 13:
            invitor = op.param2
            gotinvite = op.param3
            if invitor == user2 and gotinvite == user1:
                cl.acceptGroupInvitation(op.param1)
        if op.type == 19 and TyfeLogged == True:
            gotkick = op.param3
            if gotkick == user1:
                x = kk.getGroup(op.param1)
                defclose = False
                if x.preventJoinByTicket == True:
                    x.preventJoinByTicket = False
                    kk.updateGroup(x)
                    defclose = True
                ticket = kk.reissueGroupTicket(op.param1)
                cl.acceptGroupInvitationByTicket(op.param1,ticket)
                if defclose:
                    x.preventJoinByTicket = True
                    kk.updateGroup(x)
                try:
                    kk.kickoutFromGroup(op.param1,[op.param2])
                except:
                    pass
                now2 = datetime.datetime.now()
                nowT = datetime.datetime.strftime(now2,"%H")
                nowM = datetime.datetime.strftime(now2,"%M")
                nowS = datetime.datetime.strftime(now2,"%S")
                tm = "\n\n"+nowT+":"+nowM+":"+nowS
                kk.sendText(op.param1,"สมาชิกไม่ได้รับอนุญาติให้ลบผู้ใช้นี้ (｀・ω・´)"+tm)
        if op.type == 14:
                kk.leaveGroup(op.param1)
        if op.type == 55:
            if op.param1 in seeall:
                seeall[op.param1].append(op.param2)
                if readAlert == True:
                    reader = cl.getContact(op.param2)
                    if reader.attributes != 32:
                        try:
                            kk.sendText(user1,reader.displayName+"\nจากกลุ่ม "+cl.getGroup(op.param1).name+"\nอ่านแล้ว")
                        except:
                            kk.sendText(user1,reader.displayName+"\nอ่านแล้ว")
        if op.type == 26:
            if wait['alwayRead'] == True:
                msg = op.message
                if msg.toType == 0:
                    cl.sendChatChecked(msg.from_,msg.id)
                else:
                    cl.sendChatChecked(msg.to,msg.id)




        if op.type == 25:
            msg = op.message
            try:
                if msg.text.lower() == ".me":
                    msg.contentType = 13
                    msg.text = None
                    msg.contentMetadata = {'mid': user1}
                    cl.sendMessage(msg)
                elif msg.text.lower() == ".gift":
                    msg.contentType = 9
                    msg.contentMetadata={'PRDID': '',
                                        'PRDTYPE': 'THEME',
                                        'MSGTPL': '1'}
                    msg.text = None
                    cl.sendMessage(msg)
                elif ".gift " in msg.text.lower():
                    red = re.compile(re.escape('.gift '),re.IGNORECASE)
                    themeid = red.sub('',msg.text)
                    msg.contentType = 9
                    msg.contentMetadata={'PRDID': themeid,
                                        'PRDTYPE': 'THEME',
                                        'MSGTPL': '1'}
                    msg.text = None
                    cl.sendMessage(msg)
                elif msg.text.lower() == ".groupinfo":
                    if msg.toType == 2:
                        ginfo = cl.getGroup(msg.to)
                        try:
                            gCreator = ginfo.creator.displayName
                        except:
                            gCreator = "[[ERROR]]"
                        if ginfo.invitee is None:
                            sinvitee = "0"
                        else:
                            sinvitee = str(len(ginfo.invitee))
                        if ginfo.preventJoinByTicket == True:
                            u = "ปิด"
                        else:
                            u = "เปิด"
                        cl.sendText(msg.to,"ชื่อกลุ่ม: " + str(ginfo.name) + "\n\nผู้สร้าง: " + gCreator + "\nรหัสกลุ่ม (gid): " + msg.to + "\nรูปกลุ่ม:\nhttp://dl.profile.line.naver.jp/" + ginfo.pictureStatus + "\n\nสมาชิก: " + str(len(ginfo.members)) + " ท่าน\nค้างเชิญ: " + sinvitee + " ท่าน\nURL: " + u)
                elif msg.text.lower() == ".speed":
                    start = time.time()
                    cl.sendText(msg.to,"กำลังทดสอบ..")
                    elapsed_time = time.time() - start
                    cl.sendText(msg.to, "%s วินาที" % (elapsed_time))
                    # cl.sendText(msg.to,"0.000000000000 วินาที")
                elif ".say " in msg.text.lower():
                    red = re.compile(re.escape('.say '),re.IGNORECASE)
                    mts = red.sub('',msg.text)
                    mtsl = mts.split()
                    mtsTimeArg = len(mtsl) - 1
                    mtsTime = mtsl[mtsTimeArg]
                    del mtsl[mtsTimeArg]
                    mtosay = " ".join(mtsl)
                    global Rapid1To
                    Rapid1To = msg.to
                    RapidTime = mtsTime
                    rmtosay = []
                    for count in range(0,int(RapidTime)):
                        rmtosay.insert(count,mtosay)
                    p = Pool(20)
                    p.map(Rapid1Say,rmtosay)
                    p.close()
                elif msg.text.lower() == ".invitecancel":
                    if msg.toType == 2:
                        group = cl.getGroup(msg.to)
                        gMembMids = [contact.mid for contact in group.invitee]
                        cl.cancelGroupInvitation(msg.to,gMembMids)
                elif msg.text.lower() == ".id":
                    cl.sendText(msg.to,msg.to)
                elif msg.text.lower() == ".mentionall":
                    group = cl.getGroup(msg.to)
                    nama = [contact.mid for contact in group.members]
                    cb = ""
                    cb2 = ""
                    strt = int(0)
                    akh = int(0)
                    for md in nama:
                        if md != user1:
                            akh = akh + int(5)
                            cb += """{"S":"""+json.dumps(str(strt))+""","E":"""+json.dumps(str(akh))+""","M":"""+json.dumps(md)+"},"""
                            strt = strt + int(6)
                            akh = akh + 1
                            cb2 += "@nrik\n"
                    cb = (cb[:int(len(cb)-1)])
                    cb2 = cb2[:-1]
                    msg.contentType = 0
                    msg.text = cb2
                    msg.contentMetadata ={'MENTION':'{"MENTIONEES":['+cb+']}','EMTVER':'4'}
                    try:
                        cl.sendMessage(msg)
                    except Exception as error:
                        print error
                elif msg.text.lower() == ".alwayread on":
                    wait['alwayRead'] = True
                    cl.sendText(msg.to,"เปิดโหมดอ่านอัตโนมัติแล้ว")
                elif msg.text.lower() == ".alwayread off":
                    wait['alwayRead'] = False
                    cl.sendText(msg.to,"ปิดโหมดอ่านอัตโนมัติแล้ว")
                elif msg.text.lower() == ".tyfelogin":
                    if TyfeLogged == False:
                        kk.login(qr=True)
                        kk.loginResult()
                        user2 = kk.getProfile().mid
                        TyfeLogged = True
                        cl.sendText(msg.to,"ล็อคอินสำเร็จ Tyfe พร้อมใช้งานแล้ว")
                    else:
                        cl.sendText(msg.to,"Tyfe ได้ทำการล็อคอินไปแล้ว")
                elif msg.text.lower() == ".":
                    gs = []
                    try:
                        gs = cl.getGroup(msg.to).members
                    except:
                        try:
                            gs = cl.getRoom(msg.to).contacts
                        except:
                            pass
                    tlist = ""
                    for i in gs:
                        tlist = tlist+i.displayName+" "+i.mid+"\n\n"
                    if TyfeLogged == True:
                        try:
                            kk.sendText(user1,tlist)
                        except:
                            kk.new_post(tlist)
                    else:
                        cl.sendText(msg.to,"Tyfe ยังไม่ได้ล็อคอิน")
                elif msg.text.lower() == ".crash":
                    msg.contentType = 13
                    msg.text = None
                    msg.contentMetadata = {'mid': msg.to+"',"}
                    cl.sendMessage(msg)
                elif msg.text.lower() == ".help":
                    cl.sendText(msg.to,"คำสั่งทั้งหมด (พิมพ์ . ตามด้วยคำสั่ง):\n\n- help\n- tyfelogin\n- me\n- id\n- groupinfo\n- invitecancel\n- gift\n- mentionall\n- crash\n- alwayread [on/off]\n- speed\n- say [ข้อความ] [จำนวน]\n\n**คำสั่งสำหรับบัญชีนี้เท่านั้น")
            except Exception as error:
                print error




    except Exception as error:
        print error

Rapid2To = ""

def Rapid2Say(mtosay):
    kk.sendText(Rapid2To,mtosay)

class BFGenerator(object):
    """Takes a string and generates a brainfuck code that, when run,
       prints the original string to the brainfuck interpreter standard
       output"""
      
    def text_to_brainfuck(self, data):
        """Converts a string into a BF program. Returns the BF code"""
        glyphs = len(set([c for c in data]))
        number_of_bins = max(max([ord(c) for c in data]) // glyphs,1)
        # Create an array that emulates the BF memory array as if the
        # code we are generating was being executed. Initialize the
        # array by creating as many elements as different glyphs in
        # the original string. Then each "bin" gets an initial value
        # which is determined by the actual message.
        # FIXME: I can see how this can become a problem for languages
        # that don't use a phonetic alphabet, such as Chinese.
        bins = [(i + 1) * number_of_bins for i in range(glyphs)]
        code="+" * number_of_bins + "["
        code+="".join([">"+("+"*(i+1)) for i in range(1,glyphs)])
        code+="<"*(glyphs-1) + "-]"
        code+="+" * number_of_bins
        # For each character in the original message, find the position
        # that holds the value closest to the character's ordinal, then
        # generate the BF code to move the memory pointer to that memory
        # position, get the value of that memory position to be equal
        # to the ordinal of the character and print it (i.e. print the
        # character).
        current_bin=0
        for char in data:
            new_bin=[abs(ord(char)-b)
                     for b in bins].index(min([abs(ord(char)-b)
                                               for b in bins]))
            appending_character=""
            if new_bin-current_bin>0:
                appending_character=">"
            else:
                appending_character="<"
            code+=appending_character * abs(new_bin-current_bin)
            if ord(char)-bins[new_bin]>0:
                appending_character="+"
            else:
                appending_character="-"
            code+=(appending_character * abs( ord(char)-bins[new_bin])) +"."
            current_bin=new_bin
            bins[new_bin]=ord(char)
        return code

def run(src):
    c = [0] * 30000
    p = 0
    loop = []
    rv = []
    ts = list(src)
    l = len(ts)
    i = 0;
    while i < l:
        t = ts[i]
        if t == ">": p += 1
        elif t == "<": p -= 1
        elif t == "+": c[p] += 1
        elif t == "-": c[p] -= 1
        elif t == ".": rv.append(chr(c[p]))
        elif t == ",": pass
        elif t == "[":
            if c[p] == 0:
                while ts[i] != "]": i += 1
                loop.pop()
            else:
                loop.append(i - 1)
        elif t == "]": i = loop[-1]
        i += 1

    return "".join(rv)

lmimic = ""
kickLockList = open("prevkick.dat","r").read().split('\n')

groupParam = ""

def kickBan(targ):
    kk.kickoutFromGroup(groupParam,[targ])

def user2script(op):
    global readAlert
    global kickLockList
    global banned
    global tadmin
    global groupParam
    try:
        # if op.type not in [61,60,55,48,26]:
            # print str(op)
            # print "\n\n"
        if op.type == 13:
            invitor = op.param2
            gotinvite = op.param3
            if invitor == user1 and gotinvite == user2:
                kk.acceptGroupInvitation(op.param1)
        if op.type == 17:
            if op.param1 in banned and op.param2 in banned[op.param1]:
                kk.kickoutFromGroup(op.param1,[op.param2])
                now2 = datetime.datetime.now()
                nowT = datetime.datetime.strftime(now2,"%H")
                nowM = datetime.datetime.strftime(now2,"%M")
                nowS = datetime.datetime.strftime(now2,"%S")
                tm = "\n\n"+nowT+":"+nowM+":"+nowS
                kk.sendText(op.param1,"สมาชิกที่ถูกแบนไม่ได้รับอนุญาตให้เข้าร่วมกลุ่ม （´・ω・｀）"+tm)
        if op.type == 19:
            gotkick = op.param3
            if op.param1 in kickLockList:
                if gotkick not in [user1,user2] and op.param2 not in [user1,user2] and kk.getContact(op.param2).attributes != 32:
                    try:
                        kk.kickoutFromGroup(op.param1,[op.param2])
                        now2 = datetime.datetime.now()
                        nowT = datetime.datetime.strftime(now2,"%H")
                        nowM = datetime.datetime.strftime(now2,"%M")
                        nowS = datetime.datetime.strftime(now2,"%S")
                        tm = "\n\n"+nowT+":"+nowM+":"+nowS
                        kk.sendText(op.param1,"สมาชิกไม่ได้รับอนุญาติให้ลบผู้ใช้นี้ (｀・ω・´)"+tm)
                    except:
                        try:
                            cl.kickoutFromGroup(op.param1,[op.param2])
                        except:
                            pass
            if gotkick == user2:
                x = cl.getGroup(op.param1)
                defclose = False
                if x.preventJoinByTicket == True:
                    x.preventJoinByTicket = False
                    cl.updateGroup(x)
                    defclose = True
                ticket = cl.reissueGroupTicket(op.param1)
                kk.acceptGroupInvitationByTicket(op.param1,ticket)
                if defclose:
                    x.preventJoinByTicket = True
                    cl.updateGroup(x)
                try:
                    kk.kickoutFromGroup(op.param1,[op.param2])
                except:
                    pass
                now2 = datetime.datetime.now()
                nowT = datetime.datetime.strftime(now2,"%H")
                nowM = datetime.datetime.strftime(now2,"%M")
                nowS = datetime.datetime.strftime(now2,"%S")
                tm = "\n\n"+nowT+":"+nowM+":"+nowS
                kk.sendText(op.param1,"สมาชิกไม่ได้รับอนุญาติให้ลบผู้ใช้นี้ (｀・ω・´)"+tm)
        if op.type == 25:
            msg = op.message
            if msg.text.lower() == "scanning":
                kk.sendText(user1,msg.to)
        if op.type == 26:
            msg = op.message
            if "tyfe:say " in msg.text.lower():
                if msg.from_ == user1:
                    red = re.compile(re.escape('tyfe:say '),re.IGNORECASE)
                    mts = red.sub('',msg.text)
                    mtsl = mts.split()
                    mtsTimeArg = len(mtsl) - 1
                    mtsTime = mtsl[mtsTimeArg]
                    del mtsl[mtsTimeArg]
                    mtosay = " ".join(mtsl)
                    global Rapid2To
                    if msg.toType != 0:
                        Rapid2To = msg.to
                    else:
                        Rapid2To = msg.from_
                    RapidTime = mtsTime
                    rmtosay = []
                    for count in range(0,int(RapidTime)):
                        rmtosay.insert(count,mtosay)
                    p = Pool(20)
                    p.map(Rapid2Say,rmtosay)
                    p.close()
                else:
                    if msg.toType == 2:
                        x = kk.getGroup(msg.to)
                        kk.sendText(msg.to,"ชื่อ: "+cl.getContact(msg.from_).displayName+"\n\nคุณไม่มีสิทธิ์ใช้คำสั่งนี้ มีเพียงผู้เดียวเท่านั้นที่ได้รับอำนาจในการใช้คำสั่งนี้")
            elif "tyfe:post " in msg.text.lower():
                if msg.from_ == user1:
                    red = re.compile(re.escape('tyfe:post '),re.IGNORECASE)
                    ttp = red.sub('',msg.text)
                    kk.new_post(str(ttp))
                    kk.sendText(msg.to,"โพสต์ข้อความแล้ว\nข้อความที่โพสต์: "+str(ttp))
                else:
                    now2 = datetime.datetime.now()
                    nowT = datetime.datetime.strftime(now2,"%H")
                    nowM = datetime.datetime.strftime(now2,"%M")
                    nowS = datetime.datetime.strftime(now2,"%S")
                    tm = "\n\n"+nowT+":"+nowM+":"+nowS
                    kk.sendText(msg.to,"ข้อผิดพลาด: คุณไม่มีสิทธิ์ใช้คำสั่งนี้ (｀・ω・´)"+tm)
            elif msg.text.lower() == "tyfe:weather:chiangmai":
                if msg.toType != 0:
                    data_output(msg.to,data_organizer(data_fetch(url_builder(1153670))),1)
                else:
                    data_output(msg.from_,data_organizer(data_fetch(url_builder(1153670))),1)
            elif msg.text.lower() == "tyfe:weather:ubonratchathani":
                if msg.toType != 0:
                    data_output(msg.to,data_organizer(data_fetch(url_builder(1605245))),2)
                else:
                    data_output(msg.from_,data_organizer(data_fetch(url_builder(1605245))),2)
            elif msg.text.lower() == "tyfe:weather:bangkok":
                if msg.toType != 0:
                    data_output(msg.to,data_organizer(data_fetch(url_builder(1609350))),3)
                else:
                    data_output(msg.from_,data_organizer(data_fetch(url_builder(1609350))),3)
            elif msg.text.lower() in ["tyfe:weather","tyfe:weather:"]:
                if msg.toType != 0:
                    kk.sendText(msg.to,"Tyfe weather\nสภาพอากาศในแต่ละจังหวัด\n\n- chiangmai\n- ubonratchathani\n- bangkok\n\nพิมพ์ \"tyfe:weather:[ชื่อจังหวัด]\" เพื่อดูข้อมูลสภาพอากาศ")
                else:
                    kk.sendText(msg.from_,"Tyfe weather\nสภาพอากาศในแต่ละจังหวัด\n\n- chiangmai\n- ubonratchathani\n- bangkok\n\nพิมพ์ \"tyfe:weather:[ชื่อจังหวัด]\" เพื่อดูข้อมูลสภาพอากาศ")
            elif any(word in msg.text.lower() for word in ["ขอ open","ขอopen","ขอไฟล์ open","ขอไฟล์open"]):
                if msg.toType == 0:
                    kk.sendText(msg.from_,"OpenVPN จากเซิฟ LONELY BAT (กรุงเทพฯ)\n[True เท่านั้น] ราคา 50 ทรู\n\nมีจำนวนจำกัด กดเลย:\nhttp://lonelybat.inth.red/openvpn/")
                else:
                    kk.sendText(msg.to,"OpenVPN จากเซิฟ LONELY BAT (กรุงเทพฯ)\n[True เท่านั้น] ราคา 50 ทรู\n\nมีจำนวนจำกัด กดเลย:\nhttp://lonelybat.inth.red/openvpn/")
            elif msg.text.lower() == "tyfe:freeopenvpn":
                text_file = open("freeopenvpn.txt", "r")
                openvpnmessage = text_file.read()
                text_file.close()
                if openvpnmessage == "#":
                    if msg.toType == 0:
                        kk.sendText(msg.from_,"ขออภัย\nขณะนี้ LONELY BAT ยังไม่มีไฟล์ OpenVPN แจกฟรี\nกรุณาตรวจสอบอีกครั้งในภายหลัง")
                    else:
                        kk.sendText(msg.to,"ขออภัย\nขณะนี้ LONELY BAT ยังไม่มีไฟล์ OpenVPN แจกฟรี\nกรุณาตรวจสอบอีกครั้งในภายหลัง")
                else:
                    if msg.toType == 0:
                        kk.sendText(msg.from_,openvpnmessage)
                    else:
                        kk.sendText(msg.to,openvpnmessage)
            elif "tyfe:brainfuck:gen " in msg.text.lower():
                red = re.compile(re.escape('tyfe:brainfuck:gen '),re.IGNORECASE)
                bf = red.sub('',msg.text)
                bfg=BFGenerator()
                if msg.toType == 0:
                    kk.sendText(msg.from_,bfg.text_to_brainfuck(bf))
                else:
                    kk.sendText(msg.to,bfg.text_to_brainfuck(bf))
            elif "tyfe:brainfuck:int " in msg.text.lower():
                red = re.compile(re.escape('tyfe:brainfuck:int '),re.IGNORECASE)
                bf = red.sub('',msg.text)
                if msg.toType == 0:
                    kk.sendText(msg.from_,run(bf))
                else:
                    kk.sendText(msg.to,run(bf))
            elif msg.text.lower() == "tyfe:mimic on":
                if msg.from_ == user1:
                    mimic["status"] = True
                    kk.sendText(msg.to,"เริ่มการล้อเลียน")
                else:
                    kk.sendText(msg.to,"คุณไม่มีสิทธิ์ใช้คำสั่งนี้")
            elif msg.text.lower() == "tyfe:mimic off":
                if msg.from_ == user1:
                    mimic["status"] = False
                    kk.sendText(msg.to,"ยกเลิกการล้อเลียน")
                else:
                    kk.sendText(msg.to,"คุณไม่มีสิทธิ์ใช้คำสั่งนี้")
            elif "tyfe:mimic " in msg.text.lower():
                if msg.from_ in user1:
                    red = re.compile(re.escape('tyfe:mimic '),re.IGNORECASE)
                    target0 = red.sub('',msg.text)
                    target1 = target0.lstrip()
                    target2 = target1.replace("@","")
                    target3 = target2.rstrip()
                    _name = target3
                    gInfo = cl.getGroup(msg.to)
                    targets = []
                    targets.insert(0,"0")
                    print _name
                    print ""
                    for a in gInfo.members:
                        if _name == a.displayName:
                	        targets[0] = a.mid
                    if targets[0] == "0":
                        kk.sendText(msg.to,"ไม่พบรายชื่อ")
                    else:
                        for target in targets:
                            try:
                                global lmimic
                                if lmimic != "":
                                    del mimic["target"][lmimic]
                                lmimic = target
                                mimic["target"][target] = True
                                kk.sendText(msg.to,"สำเร็จแล้ว")
                            except Exception as error:
                                print error
                                kk.sendText(msg.to,"ข้อผิดพลาดที่ไม่รู้จัก")
                else:
                    kk.sendText(msg.to,"คุณไม่มีสิทธิ์ใช้คำสั่งนี้")
            elif msg.text.lower() == "tyfe:mentionall":
                group = kk.getGroup(msg.to)
                nama = [contact.mid for contact in group.members]
                cb = ""
                cb2 = ""
                strt = int(0)
                akh = int(0)
                for md in nama:
                    if md != user2:
                        akh = akh + int(5)
                        cb += """{"S":"""+json.dumps(str(strt))+""","E":"""+json.dumps(str(akh))+""","M":"""+json.dumps(md)+"},"""
                        strt = strt + int(6)
                        akh = akh + 1
                        cb2 += "@nrik\n"
                cb = (cb[:int(len(cb)-1)])
                cb2 = cb2[:-1]
                msg.contentType = 0
                msg.text = cb2
                msg.contentMetadata ={'MENTION':'{"MENTIONEES":['+cb+']}','EMTVER':'4'}
                try:
                    kk.sendMessage(msg)
                except Exception as error:
                    print error
            elif msg.text.lower() == "tyfe:reader":
                mem = []
                try:
                    mem = kk.getGroup(msg.to).members
                except:
                    try:
                        mem = kk.getRoom(msg.to).contacts
                    except:
                        pass
                if msg.from_ == user1 or msg.from_ in tadmin and msg.to in tadmin[msg.from_]:
                    if msg.to in seeall:
                        thas = [i.mid for i in mem if i.attributes == 32]
                        if seeall[msg.to] != []:
                            text = "บัญชีที่อ่านข้อความ:\n"
                            got = False
                            for targ in mem:
                                if targ.mid in seeall[msg.to] and targ.mid not in thas and targ.mid != msg.from_:
                                    text = text+"- "+targ.displayName+"\n"
                                    got = True
                            text = text[:-1]
                            if got == True:
                                kk.sendText(msg.to,text)
                            else:
                                kk.sendText(msg.to,"บัญชีที่อ่านข้อความ:\n[[ไม่มี]]")
                        else:
                            kk.sendText(msg.to,"บัญชีที่อ่านข้อความ:\n[[ไม่มี]]")
                    else:
                        now2 = datetime.datetime.now()
                        nowT = datetime.datetime.strftime(now2,"%H")
                        nowM = datetime.datetime.strftime(now2,"%M")
                        nowS = datetime.datetime.strftime(now2,"%S")
                        tm = "\n\n"+nowT+":"+nowM+":"+nowS
                        kk.sendText(msg.to,"ข้อผิดพลาด: คุณยังไม่ได้ส่งข้อความก่อนหน้านี้ (｀・ω・´)"+tm)
                else:
                    now2 = datetime.datetime.now()
                    nowT = datetime.datetime.strftime(now2,"%H")
                    nowM = datetime.datetime.strftime(now2,"%M")
                    nowS = datetime.datetime.strftime(now2,"%S")
                    tm = "\n\n"+nowT+":"+nowM+":"+nowS
                    kk.sendText(msg.to,"ข้อผิดพลาด: คุณไม่มีสิทธิ์ใช้คำสั่งนี้ (｀・ω・´)"+tm)
            elif msg.text.lower() == "tyfe:reader:log on":
                if msg.from_ == user1:
                    readAlert = True
                    now2 = datetime.datetime.now()
                    nowT = datetime.datetime.strftime(now2,"%H")
                    nowM = datetime.datetime.strftime(now2,"%M")
                    nowS = datetime.datetime.strftime(now2,"%S")
                    tm = "\n\n"+nowT+":"+nowM+":"+nowS
                    kk.sendText(msg.to,"เปิดโหมดแจ้งคนอ่าน (Realtime) แล้ว (｀・ω・´)"+tm)
                else:
                    now2 = datetime.datetime.now()
                    nowT = datetime.datetime.strftime(now2,"%H")
                    nowM = datetime.datetime.strftime(now2,"%M")
                    nowS = datetime.datetime.strftime(now2,"%S")
                    tm = "\n\n"+nowT+":"+nowM+":"+nowS
                    kk.sendText(msg.to,"ข้อผิดพลาด: คุณไม่มีสิทธิ์ใช้คำสั่งนี้ (｀・ω・´)"+tm)
            elif msg.text.lower() == "tyfe:reader:log off":
                if msg.from_ == user1:
                    readAlert = False
                    now2 = datetime.datetime.now()
                    nowT = datetime.datetime.strftime(now2,"%H")
                    nowM = datetime.datetime.strftime(now2,"%M")
                    nowS = datetime.datetime.strftime(now2,"%S")
                    tm = "\n\n"+nowT+":"+nowM+":"+nowS
                    kk.sendText(msg.to,"ปิดโหมดแจ้งคนอ่าน (Realtime) แล้ว (｀・ω・´)"+tm)
                else:
                    now2 = datetime.datetime.now()
                    nowT = datetime.datetime.strftime(now2,"%H")
                    nowM = datetime.datetime.strftime(now2,"%M")
                    nowS = datetime.datetime.strftime(now2,"%S")
                    tm = "\n\n"+nowT+":"+nowM+":"+nowS
                    kk.sendText(msg.to,"ข้อผิดพลาด: คุณไม่มีสิทธิ์ใช้คำสั่งนี้ (｀・ω・´)"+tm)
            elif msg.text.lower() == "tyfe:preventkick:on":
                if msg.from_ == user1:
                    f = open("prevkick.dat","r+")
                    if msg.to not in f.read().split('\n'):
                        f.write(msg.to+"\n")
                        kickLockList = open("prevkick.dat","r").read().split('\n')
                        f.close()
                        now2 = datetime.datetime.now()
                        nowT = datetime.datetime.strftime(now2,"%H")
                        nowM = datetime.datetime.strftime(now2,"%M")
                        nowS = datetime.datetime.strftime(now2,"%S")
                        tm = "\n\n"+nowT+":"+nowM+":"+nowS
                        kk.sendText(msg.to,"เปิดโหมดห้ามลบแล้ว (｀・ω・´)"+tm)
                        f = open("prevkick.dat","r")
                        lines = f.read().split('\n')
                        f.close
                        f = open("prevkick.dat","w")
                        for line in lines:
                            if line != "":
                                f.write(line+"\n")
                        f.close()
                        kickLockList = open("prevkick.dat","r").read().split('\n')
                    else:
                        now2 = datetime.datetime.now()
                        nowT = datetime.datetime.strftime(now2,"%H")
                        nowM = datetime.datetime.strftime(now2,"%M")
                        nowS = datetime.datetime.strftime(now2,"%S")
                        tm = "\n\n"+nowT+":"+nowM+":"+nowS
                        kk.sendText(msg.to,"โหมดห้ามลบถูกเปิดอยู่แล้ว (｀・ω・´)"+tm)
                        f.close()
                else:
                    now2 = datetime.datetime.now()
                    nowT = datetime.datetime.strftime(now2,"%H")
                    nowM = datetime.datetime.strftime(now2,"%M")
                    nowS = datetime.datetime.strftime(now2,"%S")
                    tm = "\n\n"+nowT+":"+nowM+":"+nowS
                    kk.sendText(msg.to,"คุณไม่มีสิทธิ์ใช้คำสั่งนี้ (｀・ω・´)"+tm)
            elif msg.text.lower() == "tyfe:preventkick:off":
                if msg.from_ == user1:
                    f = open("prevkick.dat","r")
                    lines = f.read().split('\n')
                    f.close
                    f = open("prevkick.dat","w")
                    if msg.to in lines:
                        for line in lines:
                            if line not in [msg.to,"\n"]:
                                f.write(line+"\n")
                        now2 = datetime.datetime.now()
                        nowT = datetime.datetime.strftime(now2,"%H")
                        nowM = datetime.datetime.strftime(now2,"%M")
                        nowS = datetime.datetime.strftime(now2,"%S")
                        tm = "\n\n"+nowT+":"+nowM+":"+nowS
                        kk.sendText(msg.to,"ปิดโหมดห้ามลบแล้ว (｀・ω・´)"+tm)
                    else:
                        now2 = datetime.datetime.now()
                        nowT = datetime.datetime.strftime(now2,"%H")
                        nowM = datetime.datetime.strftime(now2,"%M")
                        nowS = datetime.datetime.strftime(now2,"%S")
                        tm = "\n\n"+nowT+":"+nowM+":"+nowS
                        kk.sendText(msg.to,"โหมดห้ามลบถูกปิดอยู่แล้ว (｀・ω・´)"+tm)
                    f.close()
                    kickLockList = open("prevkick.dat","r").read().split('\n')
                else:
                    now2 = datetime.datetime.now()
                    nowT = datetime.datetime.strftime(now2,"%H")
                    nowM = datetime.datetime.strftime(now2,"%M")
                    nowS = datetime.datetime.strftime(now2,"%S")
                    tm = "\n\n"+nowT+":"+nowM+":"+nowS
                    kk.sendText(msg.to,"คุณไม่มีสิทธิ์ใช้คำสั่งนี้ (｀・ω・´)"+tm)
            elif msg.text.lower() == "tyfe:halt":
                if msg.from_ == user1:
                    if msg.toType != 0:
                        kk.leaveGroup(msg.to)
            elif msg.text.lower() == "tyfe:setreadpoint":
                if msg.from_ == user1 or msg.from_ in tadmin and msg.to in tadmin[msg.from_]:
                    if msg.toType != 0:
                        cl.sendText(msg.to,"สำเร็จแล้ว")
                    else:
                        now2 = datetime.datetime.now()
                        nowT = datetime.datetime.strftime(now2,"%H")
                        nowM = datetime.datetime.strftime(now2,"%M")
                        nowS = datetime.datetime.strftime(now2,"%S")
                        tm = "\n\n"+nowT+":"+nowM+":"+nowS
                        kk.sendText(msg.from_,"กรุณาใช้คำสั่งในกลุ่ม (｀・ω・´)"+tm)
                else:
                    if msg.toType != 0:
                        now2 = datetime.datetime.now()
                        nowT = datetime.datetime.strftime(now2,"%H")
                        nowM = datetime.datetime.strftime(now2,"%M")
                        nowS = datetime.datetime.strftime(now2,"%S")
                        tm = "\n\n"+nowT+":"+nowM+":"+nowS
                        kk.sendText(msg.to,"คุณไม่มีสิทธิ์ใช้คำสั่งนี้ (｀・ω・´)"+tm)
            elif "tyfe:ban " in msg.text.lower():
                if msg.from_ in user1:
                    if msg.toType == 2:
                        red = re.compile(re.escape('tyfe:ban '),re.IGNORECASE)
                        namel = red.sub('',msg.text)
                        namel = namel.lstrip()
                        print namel
                        namel = namel.replace(" @","$spliter$")
                        print namel
                        namel = namel.replace("@","")
                        print namel
                        namel = namel.rstrip()
                        namel = namel.split("$spliter$")
                        print namel
                        gmem = cl.getGroup(msg.to).members
                        found = False
                        tmpl = []
                        if msg.to in banned:
                            tmpl = banned[msg.to]
                        banned[msg.to] = []
                        for targ in gmem:
                            if targ.displayName in namel:
                                found = True
                                if targ.mid not in tmpl and targ.mid not in [user1,user2]:
                                    banned[msg.to].append(targ.mid)
                        if tmpl != []:
                            for oldtarg in tmpl:
                                banned[msg.to].append(oldtarg)
                        if found == False:
                            now2 = datetime.datetime.now()
                            nowT = datetime.datetime.strftime(now2,"%H")
                            nowM = datetime.datetime.strftime(now2,"%M")
                            nowS = datetime.datetime.strftime(now2,"%S")
                            tm = "\n\n"+nowT+":"+nowM+":"+nowS
                            kk.sendText(msg.to,"ไม่พบรายชื่อ (｀・ω・´)"+tm)
                        else:
                            now2 = datetime.datetime.now()
                            nowT = datetime.datetime.strftime(now2,"%H")
                            nowM = datetime.datetime.strftime(now2,"%M")
                            nowS = datetime.datetime.strftime(now2,"%S")
                            tm = "\n\n"+nowT+":"+nowM+":"+nowS
                            kk.sendText(msg.to,"สำเร็จแล้ว (｀・ω・´)"+tm)
                else:
                    if msg.toType != 0:
                        now2 = datetime.datetime.now()
                        nowT = datetime.datetime.strftime(now2,"%H")
                        nowM = datetime.datetime.strftime(now2,"%M")
                        nowS = datetime.datetime.strftime(now2,"%S")
                        tm = "\n\n"+nowT+":"+nowM+":"+nowS
                        kk.sendText(msg.to,"คุณไม่มีสิทธิ์ใช้คำสั่งนี้ (｀・ω・´)"+tm)
            elif "tyfe:unban " in msg.text.lower():
                if msg.from_ in user1:
                    if msg.toType == 2:
                        red = re.compile(re.escape('tyfe:unban '),re.IGNORECASE)
                        namel = red.sub('',msg.text)
                        namel = namel.lstrip()
                        namel = namel.replace("@","")
                        namel = namel.rstrip()
                        namel = namel.split(" ")
                        gmem = cl.getGroup(msg.to).members
                        found = False
                        if msg.to in banned:
                            for targ in gmem:
                                if targ.displayName in namel:
                                    found = True
                                    if targ.mid in banned[msg.to]:
                                        banned[msg.to].remove(targ.mid)
                        if found == False:
                            now2 = datetime.datetime.now()
                            nowT = datetime.datetime.strftime(now2,"%H")
                            nowM = datetime.datetime.strftime(now2,"%M")
                            nowS = datetime.datetime.strftime(now2,"%S")
                            tm = "\n\n"+nowT+":"+nowM+":"+nowS
                            kk.sendText(msg.to,"ไม่พบรายชื่อ (｀・ω・´)"+tm)
                        else:
                            now2 = datetime.datetime.now()
                            nowT = datetime.datetime.strftime(now2,"%H")
                            nowM = datetime.datetime.strftime(now2,"%M")
                            nowS = datetime.datetime.strftime(now2,"%S")
                            tm = "\n\n"+nowT+":"+nowM+":"+nowS
                            kk.sendText(msg.to,"สำเร็จแล้ว (｀・ω・´)"+tm)
                else:
                    if msg.toType != 0:
                        now2 = datetime.datetime.now()
                        nowT = datetime.datetime.strftime(now2,"%H")
                        nowM = datetime.datetime.strftime(now2,"%M")
                        nowS = datetime.datetime.strftime(now2,"%S")
                        tm = "\n\n"+nowT+":"+nowM+":"+nowS
                        kk.sendText(msg.to,"คุณไม่มีสิทธิ์ใช้คำสั่งนี้ (｀・ω・´)"+tm)
            elif msg.text.lower() == "tyfe:unbanall":
                if msg.from_ == user1:
                    try:
                        banned.pop(msg.to)
                        now2 = datetime.datetime.now()
                        nowT = datetime.datetime.strftime(now2,"%H")
                        nowM = datetime.datetime.strftime(now2,"%M")
                        nowS = datetime.datetime.strftime(now2,"%S")
                        tm = "\n\n"+nowT+":"+nowM+":"+nowS
                        kk.sendText(msg.to,"ปลดแบนสมาชิกทั้งหมดสำหรับกลุ่มนี้เรียบร้อยแล้ว (｀・ω・´)"+tm)
                    except:
                        now2 = datetime.datetime.now()
                        nowT = datetime.datetime.strftime(now2,"%H")
                        nowM = datetime.datetime.strftime(now2,"%M")
                        nowS = datetime.datetime.strftime(now2,"%S")
                        tm = "\n\n"+nowT+":"+nowM+":"+nowS
                        kk.sendText(msg.to,"ไม่มีสมาชิกถูกแบนสำหรับกลุ่มนี้ (｀・ω・´)"+tm)
                else:
                    now2 = datetime.datetime.now()
                    nowT = datetime.datetime.strftime(now2,"%H")
                    nowM = datetime.datetime.strftime(now2,"%M")
                    nowS = datetime.datetime.strftime(now2,"%S")
                    tm = "\n\n"+nowT+":"+nowM+":"+nowS
                    kk.sendText(msg.to,"คุณไม่มีสิทธิ์ใช้คำสั่งนี้ (｀・ω・´)"+tm)
            elif msg.text.lower() == "tyfe:banlist":
                if msg.from_ == user1:
                    if msg.to in banned and banned[msg.to] != []:
                        kk.sendText(msg.to,"กำลังดึงข้อมูลบัญชี กรุณารอสักครู่")
                        text = "รายชื่อบัญชีที่ถูกแบนสำหรับกลุ่มนี้:\n"
                        for targ in banned[msg.to]:
                            text = text + "- " + cl.getContact(targ).displayName + "\n"
                        text = text[:-1]
                        kk.sendText(msg.to,text)
                    else:
                        now2 = datetime.datetime.now()
                        nowT = datetime.datetime.strftime(now2,"%H")
                        nowM = datetime.datetime.strftime(now2,"%M")
                        nowS = datetime.datetime.strftime(now2,"%S")
                        tm = "\n\n"+nowT+":"+nowM+":"+nowS
                        kk.sendText(msg.to,"ไม่มีสมาชิกถูกแบนสำหรับกลุ่มนี้ (｀・ω・´)"+tm)
                else:
                    now2 = datetime.datetime.now()
                    nowT = datetime.datetime.strftime(now2,"%H")
                    nowM = datetime.datetime.strftime(now2,"%M")
                    nowS = datetime.datetime.strftime(now2,"%S")
                    tm = "\n\n"+nowT+":"+nowM+":"+nowS
                    kk.sendText(msg.to,"คุณไม่มีสิทธิ์ใช้คำสั่งนี้ (｀・ω・´)"+tm)
            elif msg.text.lower() == "tyfe:kickban":
                if msg.from_ == user1:
                    if msg.to in banned and banned[msg.to] != []:
                        gmem = kk.getGroup(msg.to).members
                        groupParam = msg.to
                        targets = []
                        for targ in gmem:
                            if targ.mid in banned[msg.to]:
                                targets.append(targ.mid)
                        p = Pool(len(targets))
                        try:
                            p.map(kickBan,targets)
                        except:
                            pass
                        p.close()
                        now2 = datetime.datetime.now()
                        nowT = datetime.datetime.strftime(now2,"%H")
                        nowM = datetime.datetime.strftime(now2,"%M")
                        nowS = datetime.datetime.strftime(now2,"%S")
                        tm = "\n\n"+nowT+":"+nowM+":"+nowS
                        kk.sendText(msg.to,"สำเร็จแล้ว (｀・ω・´)"+tm)
                    else:
                        now2 = datetime.datetime.now()
                        nowT = datetime.datetime.strftime(now2,"%H")
                        nowM = datetime.datetime.strftime(now2,"%M")
                        nowS = datetime.datetime.strftime(now2,"%S")
                        tm = "\n\n"+nowT+":"+nowM+":"+nowS
                        kk.sendText(msg.to,"ไม่มีสมาชิกถูกแบนสำหรับกลุ่มนี้ (｀・ω・´)"+tm)
                else:
                    now2 = datetime.datetime.now()
                    nowT = datetime.datetime.strftime(now2,"%H")
                    nowM = datetime.datetime.strftime(now2,"%M")
                    nowS = datetime.datetime.strftime(now2,"%S")
                    tm = "\n\n"+nowT+":"+nowM+":"+nowS
                    kk.sendText(msg.to,"คุณไม่มีสิทธิ์ใช้คำสั่งนี้ (｀・ω・´)"+tm)
            elif msg.text.lower() in dangerMessage:
                try:
                    if msg.toType == 2:
                        kk.kickoutFromGroup(msg.to,[msg.from_])
                        now2 = datetime.datetime.now()
                        nowT = datetime.datetime.strftime(now2,"%H")
                        nowM = datetime.datetime.strftime(now2,"%M")
                        nowS = datetime.datetime.strftime(now2,"%S")
                        tm = "\n\n"+nowT+":"+nowM+":"+nowS
                        kk.sendText(msg.to,"ตรวจพบคำสั่งของบอทลบกลุ่ม จำเป็นต้องนำออกเพื่อความปลอดภัยของสมาชิก (｀・ω・´)"+tm)
                except:
                    pass
            elif msg.from_ in mimic["target"] and mimic["status"] == True and mimic["target"][msg.from_] == True:
                text = msg.text
                if text is not None:
                    kk.sendText(msg.to,text)
                else:
                    if msg.contentType == 7:
                        msg.contentType = 7
                        msg.text = None
                        msg.contentMetadata = {
                                              "STKID": "501",
                                              "STKPKGID": "2",
                                              "STKVER": "100" }
                        kk.sendMessage(msg)
                    elif msg.contentType == 13:
                        msg.contentType = 13
                        msg.contentMetadata = {'mid': msg.contentMetadata["mid"]}
                        kk.sendMessage(msg)
            if msg.from_ == user1:
                seeall[msg.to] = []
    except Exception as error:
        print error

def nameUpdate():
    while True:
        try:
            if wait["clock"] == True:
                now2 = datetime.datetime.now()
                nowT = datetime.datetime.strftime(now2,"%H")
                nowM = datetime.datetime.strftime(now2,"%M")
                nowT = int(nowT)
                nowM = int(nowM)
                hr = int(nowT)
                cloud = cloudupdate(data_organizer(data_fetch(url_builder(1153670))))
                profile = cl.getProfile()
                if hr >= 22:
                    if nowM == 59:
                        if nowT == 23:
                            profile.statusMessage = "(00:00) "+cloud
                        else:
                            profile.statusMessage = "("+str(int(nowT)+1)+":00) "+cloud
                    else:
                        if nowM < 9:
                            profile.statusMessage = "("+str(nowT)+":0"+str(int(nowM)+1)+") "+cloud
                        else:
                            profile.statusMessage = "("+str(nowT)+":"+str(int(nowM)+1)+") "+cloud
                elif hr >= 20:
                    if nowM == 59:
                        if nowT >= 21:
                            profile.statusMessage = "("+str(int(nowT)+1)+":00) "+cloud
                        else:
                            profile.statusMessage = "("+str(int(nowT)+1)+":00) "+cloud
                    else:
                        if nowM < 9:
                            profile.statusMessage = "("+str(nowT)+":0"+str(int(nowM)+1)+") "+cloud
                        else:
                            profile.statusMessage = "("+str(nowT)+":"+str(int(nowM)+1)+") "+cloud
                elif hr >= 19:
                    if nowM == 59:
                        if nowT >= 19:
                            profile.statusMessage = "("+str(int(nowT)+1)+":00) "+cloud
                        else:
                            profile.statusMessage = "("+str(int(nowT)+1)+":00) "+cloud
                    else:
                        if nowM < 9:
                            profile.statusMessage = "("+str(nowT)+":0"+str(int(nowM)+1)+") "+cloud
                        else:
                            profile.statusMessage = "("+str(nowT)+":"+str(int(nowM)+1)+") "+cloud
                elif hr >= 7:
                    if nowM == 59:
                        if nowT >= 18:
                            profile.statusMessage = "("+str(int(nowT)+1)+":00) "+cloud
                        else:
                            if nowT < 9:
                                profile.statusMessage = "(0"+str(int(nowT)+1)+":00) "+cloud
                            else:
                                profile.statusMessage = "("+str(int(nowT)+1)+":00) "+cloud
                    else:
                        if nowM < 9:
                            if nowT < 10:
                                profile.statusMessage = "(0"+str(nowT)+":0"+str(int(nowM)+1)+") "+cloud
                            else:
                                profile.statusMessage = "("+str(nowT)+":0"+str(int(nowM)+1)+") "+cloud
                        else:
                            if nowT < 10:
                                profile.statusMessage = "(0"+str(nowT)+":"+str(int(nowM)+1)+") "+cloud
                            else:
                                profile.statusMessage = "("+str(nowT)+":"+str(int(nowM)+1)+") "+cloud
                elif hr >= 5:
                    if nowM == 59:
                        if nowT >= 6:
                            profile.statusMessage = "(0"+str(int(nowT)+1)+":00) "+cloud
                        else:
                            profile.statusMessage = "(0"+str(int(nowT)+1)+":00) "+cloud
                    else:
                        if nowM < 9:
                            profile.statusMessage = "(0"+str(nowT)+":0"+str(int(nowM)+1)+") "+cloud
                        else:
                            profile.statusMessage = "(0"+str(nowT)+":"+str(int(nowM)+1)+") "+cloud
                elif hr >= 3:
                    if nowM == 59:
                        if nowT >= 4:
                            profile.statusMessage = "(0"+str(int(nowT)+1)+":00) "+cloud
                        else:
                            profile.statusMessage = "(0"+str(int(nowT)+1)+":00) "+cloud
                    else:
                        if nowM < 9:
                            profile.statusMessage = "(0"+str(nowT)+":0"+str(int(nowM)+1)+") "+cloud
                        else:
                            profile.statusMessage = "(0"+str(nowT)+":"+str(int(nowM)+1)+") "+cloud
                elif hr >= 1:
                    if nowM == 59:
                        if nowT >= 2:
                            profile.statusMessage = "(0"+str(int(nowT)+1)+":00) "+cloud
                        else:
                            profile.statusMessage = "(0"+str(int(nowT)+1)+":00) "+cloud
                    else:
                        if nowM < 9:
                            profile.statusMessage = "(0"+str(nowT)+":0"+str(int(nowM)+1)+") "+cloud
                        else:
                            profile.statusMessage = "(0"+str(nowT)+":"+str(int(nowM)+1)+") "+cloud
                else:
                    if nowM == 59:
                        if nowT >= 0:
                            profile.statusMessage = "(0"+str(int(nowT)+1)+":00) "+cloud
                        else:
                            profile.statusMessage = "(0"+str(int(nowT)+1)+":00) "+cloud
                    else:
                        if nowM < 9:
                            profile.statusMessage = "(0"+str(nowT)+":0"+str(int(nowM)+1)+") "+cloud
                        else:
                            profile.statusMessage = "(0"+str(nowT)+":"+str(int(nowM)+1)+") "+cloud
                cl.updateProfile(profile)
            time.sleep(120)
        except:
            pass
thread2 = threading.Thread(target=nameUpdate)
thread2.daemon = True
thread2.start()

try:
    while True:
        try:
            Opss = cl.fetchOps(cl.Poll.rev, 5)
        except EOFError:
            raise Exception("It might be wrong revision\n" + str(cl.Poll.rev))
        for Op in Opss:
            if (Op.type != OpType.END_OF_OPERATION):
                cl.Poll.rev = max(cl.Poll.rev, Op.revision)
                user1script(Op)

        if TyfeLogged == True:
            try:
                Ops = kk.fetchOps(kk.Poll.rev, 5)
            except EOFError:
                raise Exception("It might be wrong revision\n" + str(kk.Poll.rev))
            for Op in Ops:
                if (Op.type != OpType.END_OF_OPERATION):
                    kk.Poll.rev = max(kk.Poll.rev, Op.revision)
                    user2script(Op)
except:
    with open('tval.pkl', 'w') as f:
        pickle.dump([seeall,tadmin,banned], f)
    print ""
