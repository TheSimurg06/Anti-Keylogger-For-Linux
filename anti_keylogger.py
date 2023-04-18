#!/usr/bin/env python3
from ast import For, While
from asyncio import subprocess
from logging import Filter
from multiprocessing import ProcessError
import os
from re import T
import readline
from subprocess import call
import subprocess
from subprocess import Popen, PIPE
import os.path

system_process = []
system_process_backup = ["systemd-l","systemd","Xorg","acpid"]
safe_process = []
sus_process = []
sus_pidno = []
sus_pidnoi = []
sus_location = []
sus_deactive = []
sus_deactivepid = []
secim=1
processinfo = ""
lines2 = ""
event =""
event_indeks = 0
sayac = 0

#şüpheli programların lokasyonları tespit edilir.
def location(location_kontrol):
    global sus_pidnoi
    global sus_process
    global sus_location
    sus_path = ""
    sus = 0
    counter =0
    if(location_kontrol==True):
        call('sudo date >> archive.txt',shell=True)
        for pidno in sus_pidnoi:
            call('sudo readlink -v /proc/{0}/exe >> path.txt'.format(pidno),shell=True)
            call('sudo readlink -v /proc/{0}/exe >> archive.txt'.format(pidno),shell = True)
        if(os.path.exists('path.txt')):
            sus_pathdosya = open('path.txt','r+')
            sus_pathlines = sus_pathdosya.readlines()
            for a in sus_pathlines:
                sus_path +=a
            sus_pathdosya.close()

        while(sus !=-1):
            sus = sus_path.find("\n",sus+1,len(sus_path))
            if(sus ==-1):
                break
            sus_location.append(sus_path[counter:sus])
            counter = sus +1

    elif(len(sus_pidnoi) > 0 and location_kontrol==False):
        print("Şüpheli programlar\n")
        for i in sus_location:
            print(i)
    else:
        print("Şüpheli program bulunamadı")        

#klavye event'ini kullanan tüm işlemler taranır. Şüpheli ve Güvenli olmak üzere sınıflandırılır
#Bu şüpheli işlemlere karşı yapılacak opsiyonlar sunulur
def process_tara():
    global safe_process
    global sus_pidno
    global sus_process
    global processinfo
    global lines2
    global sus_deactive
    global sus_deactivepid
    global event
    processinfo =""
    lines2 = ""

    #Event dosyasını kullanan process'lere göz at
    if(os.path.exists('active_process.txt')):
        active_process = open('active_process.txt','r+')
        active_process.truncate(0)
        active_process.close()
    call('sudo lsof | grep "{0}" > active_process.txt '.format(event),shell=True)
    active_process = open('active_process.txt', 'r+')
    lines2 = active_process.readlines()

    for line2 in lines2:
        processinfo +=line2
    active_process.close()
    
    event_sayac=0
    print("")
    print("Klavyeden veri okuyan Programlar\n")

    count =0
    while(count < len(lines2)):
        kontrol(processinfo,event_sayac,count)
        count +=1
    global sus_pidnoi
    sus_pidnoi = list(map(int,sus_pidno))

    location(True)
    inp = ""
    check = [True,False]
    sus_deactive = sus_process.copy()
    sus_deactivepid = sus_pidnoi.copy()

    while(True):
        print("")
        print("Yapmak İstediğiniz İşlemin Sıra Numarasını Giriniz\n")
        print("1) Şüpheli Programları Sonlandırın")
        print("2) Detaylı Bilgi ve Seçenekler")
        print("3) Tekrar Keylogger Taraması Yap")
        print("4) Sisteme bağlı başka bir klavyeye geçiş yap.")
        print("5) Çıkış\n")
        inp = input(":")
        print("")
        if(inp == "1"):
            if(check[0]):
                check = sonlandır(check[0],check[1])
            elif(check[0]==False and check[1] == True ):
                check = sonlandır(check[0],check[1])
            elif(check[0]==False and check[1] == False and len(sus_deactive) ==0):
                print("Şüpheli uygulamalar zaten imha edildi")
                continue
        elif(inp == "2"):
            inp = detay()
            if(inp == "3"):
                continue
        elif(inp =="3"):
            safe_process = []
            sus_process =[]
            sus_pidno=[]    
            process_tara()
            break
        elif(inp =="4"):
            eventchange()
        elif(inp =="5"):
            print("-- Çıkış")
            quit()


def anamenu():
    print("")
    print("Hoşgeldiniz\n")
    while(True):
        secenek = secenekler()
        if(secenek=="1"):
            print("1) Keylogger Taramasını Başlat")
            process_tara()
        elif(secenek=="2"):
            print("2) İletişim")
            inp = iletisim()
            continue
        elif(secenek=="3"):
            print("-- Çıkış")
            quit()
            


def iletisim():
    print("")
    print("mail: onurhandursun0625@gmail.com")
    print("")
    print("1) Geri gitmek için herhangi bir tuş giriniz.")
    return input(": ")

#sistem tarafından güvenli olarak sınıflandırılan işlemler
def safe_file_backup():
    global system_process
    global system_process_backup
    system_process_file=""
    if(os.path.exists('system_process_file.txt')):
        system_process_file = open('system_process_file.txt','r+')
        system_process_file.truncate(0)
        system_process = []
        system_process_file.close()
    system_process_file = open('system_process_file.txt','a')
    for a in system_process_backup:
        system_process_file.write(a+"\n")
        system_process.append(a)
    system_process_file.close()

#şüpheli işlemler, klavye driver'ı ve güvenli olarak sınıflandırılan işlemler hakkında bilgi
def detay():
    global system_process
    global event
    print("")
    print("Klavye Driver'ı:",event,"\n")
    print("Eğer klavye Driver'ı değiştirdiyseniz ve eski haline almak istiyorsanız programı yeniden başlatın\n")
    print("Sistem tarafından güvenli olarak sınıflandırılan programlar\n")
    forsayac =1
    for guvenli in system_process:
    
        print(forsayac,":",guvenli)
        forsayac +=1
    print("1) Bir uygulamayı güvenli olarak etiketle")
    print("2) Güvenli uygulamaları(system_process_file.txt dosyasını) varsayılan ayarlara döndür")
    print("3) Şüpheli programların lokasyonlarını göster")
    print("4) Geri")
    detaysecim = input(":")
    if(detaysecim=="1"):
        print("Güvenli olarak etiketlemek istediğiniz uygulamanın tam adını giriniz")
        print("Büyük küçük harf duyarlıdır.\n")
        print("Vazgeçtiyseniz lütfen iptal yazınız")
        add_process = input(":")
        if(add_process != "iptal"):
            system_process_file2 = open('system_process_file.txt','a')
            system_process_file2.writelines(add_process+"\n")
            system_process_file2.close()
            system_process.append(add_process)
            print("Uygulama başarıyla güvenli olarak etiketlendi")
            detay()
        else:
            print("Herhangi bir uygulamayı güvenli olarak etiketlemediniz")
            detay()
    elif(detaysecim=="2"):
        print("Dosya başarılı olarak varsayılan ayarlara döndürüldü")
        safe_file_backup()
        detay()
    elif(detaysecim=="3"):
        location(False)

    elif(detaysecim =="4"):
        return detaysecim

#ana seçenekler
def secenekler():

    print("")
    print("Opsiyonları Sıra Numarasını Girerek Seçebilirsiniz\n")
    print("1) Keylogger Taramasını Başlat")
    print("2) İletişim")
    print("3) Çıkış\n")
    secenek = input(": ")
    return secenek

#şüpheli programları sonladırma ve silme işlemleri
def sonlandır(check,sonlandır_check):
    global sus_deactive
    global sus_deactivepid
    global sus_location
    global sus_process
    global sus_pidnoi

    if(len(sus_deactive) >0 and check):
        print("1) Hepsini sonlandır")
        print("2) Hangisinin sonlandırılacağını seçmeme izin ver")
        print("3) Geri")
        inp2 = input(":")
        if(inp2 == "1"):
            sayac = 0
            for pid in sus_deactivepid:
                call('sudo kill -9 {0} '.format(pid),shell=True)
                print(sus_deactive[sayac],"Sonlandırıldı")
                sayac +=1
            check = False
            sonlandır_check = True
            print("")
            print("Şüpheli uygulamaların hepsi sonlandırıldı\n")
            sus_deactive = []
            sus_deactivepid = []

        elif(inp2 == "2"):
            print("")
            for sayac in range(0,len(sus_deactive)):
                print(sayac,")",sus_deactive[sayac] ,":",sus_deactivepid[sayac])
                #trycath
            secim = int(input("Sonlandırmak istediğiniz programın sıra numarasını giriniz. İşlemi iptal etmek için -1 giriniz\n"))
            if(len(sus_deactive) > secim and secim >=0 ):
                pid = sus_deactivepid[secim]
                call('sudo kill -9 {0} '.format(pid),shell=True)
                print(sus_deactive[secim],"Sonlandırıldı")
                check = True
                sonlandır_check = True
                sus_deactive.pop(secim)
                sus_deactivepid.pop(secim)
            else:
                print("")
                print("Hatalı bir sıra numarası girdiniz. Uygulama sonlandırılamadı")
                return True,False
        elif(inp2 == "3"):
            return True,False
        if(sonlandır_check):
            print("Sonlandırılan şüpheli uygulamalar silinsin mi?")
            print("Dikkat! Sonlandırılmış her şüpheli uygulama silinecektir\n")    
            print("1) Evet")
            print("2) Hayır")
            inp = input(":")

            if(inp == "1"):
                del_location = ""
                index =0
                if(len(sus_deactive) < len(sus_process)):
                    for i in sus_pidnoi:
                        if(i not in sus_deactivepid):
                            index = sus_pidnoi.index(i)
                            for count in range(0,len(sus_location)):
                                if(sus_process[index] in sus_location[count]):
                                    del_location = sus_location[count]
                                    if(os.path.isfile(del_location)):
                                        os.remove(del_location)
                                        print(del_location," başarıyla silindi")
                    if(len(sus_deactive) == 0):
                        print("Silinen dosyalar hakkında bilgileri path.txt de bulabilirsiniz")
                        return False,False
                    elif(len(sus_deactive) > 0):
                        return True,True

                else:
                    print("Sonlandırılan bir uygulama bulunamadı")
                    return True,False
            elif(inp!="1"):
                print("Hayır")
                print("Sonlandırılmış şüpheli uygulamaların lokasyonlarına 'path.txt' dosyasından ulaşabilirsiniz.")              
                if(len(sus_deactive)>0):
                    return True,True
                #herşeyi silip hayıra bastıysan    
                else:
                    return False,True

    elif(check == False and sonlandır_check == True ):
        if(len(sus_deactive) == 0):
            print("Başka şüpheli program bulunamadı")
        print("Sonlandırılmış uygulamaların silinmesini ister misiniz?")
        print("1) Evet")
        print("2) Hayır")
        inp = input(":")
        print("")
        if(inp == "1"):
            for i in sus_pidnoi:
                            if(i not in sus_deactivepid):
                                index = sus_pidnoi.index(i)
                                for count in range(0,len(sus_location)):
                                    if(sus_process[index] in sus_location[count]):
                                        del_location = sus_location[count]
                                        if(os.path.isfile(del_location)):
                                            os.remove(del_location)
                                            print(del_location," başarıyla silindi")
            print("Silinen dosyalar hakkında bilgileri path.txt de bulabilirsiniz")
            return False,False
        else:
            return False,True

    else:
        print("")
        print("Şüpheli program bulunamadı\n")
        return False,False
    
#klavyeyi kullanan program şüpheli mi güvenli mi tespit edilir
def kontrol(processinfo,eventsayac,count):
    global safe_process
    global sus_pidno
    global sus_process
    global lines2
    satır = []

    satır2 = lines2[count]
    satır2 = " ".join(satır2.split())
    
    satır.append(satır2.split(" "))
    processname = satır[0][0]
    pidno = satır[0][1]

    #process güvenli mi şüpheli mi tespit etme
    ifkontrol = True
    if(processname not in safe_process and processname not in sus_process):
        for system in system_process:
            system = str(system)
            system = system.strip(' \n')
            if(processname.find(system) !=-1):
                print(system + " - güvenli")
                ifkontrol = False
                safe_process.append(system)
                print("")
                break
        if(ifkontrol):
            print(processname , "- Şüpheli -- " , "Pid Number:", pidno )
            sus_process.append(processname)
            sus_pidno.append(pidno)
            print("")

    return eventsayac


#Sisteme bağlı diğer klavyelerin eventini bulma
def eventchange():
    global event_indeks
    global event
    global sayac
    print("Mevcut klavye Event Handler: ",event)
    print("1) Değiştir")
    print("Başka bir veri girerseniz iptal olarak varsayılacaktır")
    inp = input(":")
    print("")
    if(inp =="1"):
        control = True
        if(sayac !=-1):
            event = ""
        while(sayac != -1):
            
            sayac = info.find("Keyboard",event_indeks+4,len(info))
            if(sayac ==-1):
                sayac = info.find("keyboard",event_indeks+4,len(info))

            if(sayac !=-1 and control):
                event_indeks = info.find("event",sayac,len(info))
                for event2 in range(0,7):
                    event += info[event_indeks + event2]
                event = event.strip(" ")
                print("Sisteme bağlı diğer klavyeye geçildi")
                print("Yeni event handler: ",event)
                control = False
            else:
                return
        if(sayac ==-1):
            control = False
            print("Başka bir event handler bulunmamaktadır.")
            print("Event Handler: ",event)
            return
    else:
        print("İptal")
        return


#güvenli olarak etiketlenen sistem programları
if(os.path.exists('system_process_file.txt')):
    system_process_file = open('system_process_file.txt','r')
    systemlines = system_process_file.readlines()
    for systemline in systemlines:
        system_process.append(systemline)    
    system_process_file.close()
else:
    safe_file_backup()

#input devices
call('cat /proc/bus/input/devices > deviceinfo.txt', shell=True)

deviceinfo = open('deviceinfo.txt', 'r')
lines = deviceinfo.readlines()
info = ""
for line in lines:
    info +=line
deviceinfo.close()

if(os.path.exists('path.txt')):
    active_process = open('path.txt','r+')
    active_process.truncate(0)
    active_process.close()

#keyboard kaçıncı event tespit etme
sayac = info.find("keyboard")
if(sayac == -1):
    sayac = info.find("Keyboard")

if(sayac !=-1):
    event_indeks = info.find("event",sayac,len(info))
    for event2 in range(0,7):
        event += info[event_indeks + event2]
event = event.strip(" ")

anamenu()




