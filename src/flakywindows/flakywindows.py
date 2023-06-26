import pydivert
import subprocess
import socket
import time
from time import sleep
import random
import sys
import threading
import multiprocessing

sys.tracebacklimit=0
hostname = socket.gethostname()
ip = str(socket.gethostbyname(hostname))

SWITCH_PROFILE="wi-fi"
MOBILE_DATA="wi-fi"
PING_DNS="8.8.8.8"
interrupted = False

profiles = {
    "3g":[768,1600,150,0],
    "3gfast":[768,1600,75,0],
    "3gslow":[400,400,200,0],
    "2g":[256,280,400,0],
     "cable":[1000,5000,14,0],
    "dsl":[384,1500,14,0],
    "4g":[9000,9000,85,0],
    "lte":[12000,12000,35,0],
    "wi-fi":[15,30],
    "edge":[200,240,35,0],    
    "stop":[0,0,1000,0],
    "nospeed":[1000000,1000000,200,0]
    }

class FlakyWindows:
    def __init__(self, p=MOBILE_DATA):
        self.p=p
        # self.inrate=profiles.get(p)[1]
        # self.outrate=profiles.get(p)[0]        
        #print(self.download)

    def drop(self, probability):
        probability = int(probability)/100
        try:
            subprocess.run("netsh advfirewall firewall add rule name=\"DROP\" dir=out action=block remoteip="+PING_DNS)

            while True:
                if random.random() < probability:
                    print("Enabled")
                    subprocess.run("netsh advfirewall firewall set rule name=\"DROP\" new enable=yes")
                else:
                    print("Disabled")
                    subprocess.run("netsh advfirewall firewall set rule name=\"DROP\" new enable=no")
            
                sleep(0.5)

        except KeyboardInterrupt:
            subprocess.run("netsh advfirewall firewall delete rule name=\"DROP\"")        

    def throttleOutbound(self, rate):
       
        try:
            subprocess.call('powershell.exe New-NetQosPolicy -Name "test" -IPSrcPrefix ' + ip + ' -NetworkProfile All  -ThrottleRateActionBitsPerSecond ' + rate +'MB' , shell= True)

            while True:
                continue
                #print("Throttled")
        except KeyboardInterrupt:
            subprocess.Popen('powershell.exe Remove-NetQosPolicy -Name "test" -Confirm:$false', shell= True)
            print("Deleted")   


    def throttleInbound(self, rate):
        rate=int(rate)
        with pydivert.WinDivert("inbound and tcp.PayloadLength > 0") as w:
            start_time = time.time()
            byte_count = 0

            for packet in w:
                payload_length = len(packet.tcp.payload)
                byte_count += payload_length
                elapsed_time = time.time() - start_time

                if elapsed_time > 1.0:
                    current_rate = (byte_count * 8)/ (elapsed_time * 800005)   
                    if current_rate > rate:
                        delay = ((byte_count * 8) / (rate * 800005)) - elapsed_time
                        if delay > 0:
                            time.sleep(delay)

                    start_time = time.time()
                    byte_count = 0

                w.send(packet)    

    def jitter_new(self, val):
        
        #val=(int(val)/100)
        val= (100-int(val))/100

        try:
            subprocess.run("netsh advfirewall firewall add rule name=\"JITTER\" protocol = icmpv4 dir=out action = block")
            while True:
                if random.random() < val:
                    print("Enabled")
                    subprocess.run("netsh advfirewall firewall set rule name=\"JITTER\" new enable=yes")
                else:
                    print("Disabled")
                    subprocess.run("netsh advfirewall firewall set rule name=\"JITTER\" new enable=no")
            
                sleep(0.5)
        except KeyboardInterrupt:
            subprocess.run("netsh advfirewall firewall delete rule name=\"JITTER\"")        

    def randomBandwidth(self,limit):

    
        val1 = random.randint(0, int(limit))
        val2 = int(limit) - val1
        
        try:
            subprocess.run('powershell.exe New-NetQosPolicy -Name "test1" -IPSrcPrefix ' + ip + ' -MinBandwidthWeightAction ' + str(val1), shell= True)
            subprocess.run('powershell.exe New-NetQosPolicy -Name "test2" -IPSrcPrefix ' + ip + ' -MinBandwidthWeightAction ' + str(val2), shell= True)

            while True:
                pass
                #print()

        except KeyboardInterrupt:
            subprocess.Popen('powershell.exe Remove-NetQosPolicy -Name "test1" -WarningAction SilentlyContinue -Confirm:$false', shell= True)
            subprocess.Popen('powershell.exe Remove-NetQosPolicy -Name "test2" -WarningAction SilentlyContinue -Confirm:$false', shell= True)
            print("Deleted both of them") 

    def randomBandwidth(self,limit):
        rate = random.randint(15,80)
        limit = int(limit)
        val1 = random.randint(0, limit)
        val2 = limit - val1

        try:
            subprocess.run('powershell.exe New-NetQosPolicy -Name "test1" -IPSrcPrefix ' + ip + ' -MinBandwidthWeightAction ' + str(val1), shell=True)
            subprocess.run('powershell.exe New-NetQosPolicy -Name "test2" -IPSrcPrefix ' + ip + ' -MinBandwidthWeightAction ' + str(val2), shell=True)
            print('Inbound rate: '+ str(rate) + 'MBPS')

            with pydivert.WinDivert("inbound and tcp.PayloadLength > 0") as w:
                start_time = time.time()
                byte_count = 0

                for packet in w:
                    payload_length = len(packet.tcp.payload)
                    byte_count += payload_length
                    elapsed_time = time.time() - start_time

                    if elapsed_time > 1.0:
                        current_rate = (byte_count * 8) / (elapsed_time * 800005)
                        if current_rate > rate:
                            delay = ((byte_count * 8) / (rate * 800005)) - elapsed_time
                            if delay > 0:
                                time.sleep(delay)

                        start_time = time.time()
                        byte_count = 0

                    w.send(packet)

        except KeyboardInterrupt:
            subprocess.Popen('powershell.exe Remove-NetQosPolicy -Name "test1" -Confirm:$false', shell=True)
            subprocess.Popen('powershell.exe Remove-NetQosPolicy -Name "test2" -Confirm:$false', shell=True)
            print("Deleted both of them")        
    
    def interrupt_thread(self,time):
        if(time <= 0):
            return
        sleep(time)
        global interrupted
        interrupted = True

    def throttleOutboundtry(self,rate):
        subprocess.call('powershell.exe New-NetQosPolicy -Name "test" -IPSrcPrefix ' + ip + ' -NetworkProfile All  -ThrottleRateActionBitsPerSecond ' + str(rate) +'MB' , shell= True)

    def throttleOutboundtest(self,rate):
            subprocess.call('powershell.exe Set-NetQosPolicy -Name "test" -ThrottleRateActionBitsPerSecond ' + str(rate) +'MB' , shell= True)
            while True:
                continue

    def throtteOutboundreal(self, outrate):
        try:
            self.throttleOutboundtry(outrate)
            sleep(50)
            self.throttleOutboundtest(30)
        except KeyboardInterrupt:
            subprocess.Popen('powershell.exe Remove-NetQosPolicy -Name "test" -Confirm:$false', shell= True)

    def droptry(self,probability, time=0):
        global interrupted
        subprocess.run("netsh advfirewall firewall add rule name=\"DROP\" dir=out action=block remoteip="+PING_DNS)
        
        probability = int(probability)/100  

        threading.Thread(target=self.interrupt_thread, args=(time,), name='interrupt_thread', daemon=True).start()
        while not interrupted:
            if random.random() < probability:
                print("Enabled")
                subprocess.run("netsh advfirewall firewall set rule name=\"DROP\" new enable=yes")
            else:
                print("Disabled")
                subprocess.run("netsh advfirewall firewall set rule name=\"DROP\" new enable=no")
        interrupted = False  

    def dropreal(self, droprate):
        try:
            self.droptry(droprate, 2)
            print("Changing drop")
            # time.sleep(2)
            self.droptry(random.randint(80,90))

        except KeyboardInterrupt:
            subprocess.run("netsh advfirewall firewall delete rule name=\"DROP\"")

    def jittertry(self,val, time=0):
        global interrupted
        val = (100 - int(val)) / 100

        #val= (100-int(val))/100
        subprocess.run("netsh advfirewall firewall add rule name=\"JITTER\" protocol = icmpv4 dir=out action = block")
        threading.Thread(target=self.interrupt_thread, args=(time,), name='interrupt_thread', daemon=True).start()

        while not interrupted:
            if random.random() < val:
                print("Enabled")
                subprocess.run("netsh advfirewall firewall set rule name=\"JITTER\" new enable=yes")
            else:
                print("Disabled")
                subprocess.run("netsh advfirewall firewall set rule name=\"JITTER\" new enable=no")
        interrupted = False
                
    def jitterreal(self, jitterrate):
        try:
            self.jittertry(jitterrate,2)
            print("Changing jitter")
            self.jittertry(random.randint(60,80))
                
        except KeyboardInterrupt:
                subprocess.run("netsh advfirewall firewall delete rule name=\"JITTER\"")        

    def throttleInboundtry(self,rate):
        rate = int(rate)

        def update_rate():
            nonlocal rate
            time.sleep(20)  
            new_rate = random.randint(80,100)
            print(f"Updating rate to: {new_rate} bits per second")
            rate = new_rate

        threading.Thread(target=update_rate, daemon=True).start()

        with pydivert.WinDivert("inbound and tcp.PayloadLength > 0") as w:
            start_time = time.time()
            byte_count = 0

            for packet in w:
                payload_length = len(packet.tcp.payload)
                byte_count += payload_length
                elapsed_time = time.time() - start_time

                if elapsed_time > 1.0:
                    current_rate = (byte_count * 8) / (elapsed_time * 800005)
                    if current_rate > rate:
                        delay = ((byte_count * 8) / (rate * 800005)) - elapsed_time
                        if delay > 0:
                            time.sleep(delay)

                    start_time = time.time()
                    byte_count = 0

                w.send(packet)

    def throttleInboundreal(self, inrate):
        self.throttleInboundtry(inrate)

    def real(self, inrate, outrate, droprate, jitterrate):
            drop_process = multiprocessing.Process(target=self.dropreal, args=(droprate,))
            throttleOut_process = multiprocessing.Process(target=self.throtteOutboundreal, args=(outrate,))
            jitter_process=multiprocessing.Process(target=self.jitterreal, args=(jitterrate,))
            throttleIn_process=multiprocessing.Process(target=self.throttleInboundreal, args=(inrate,))

            try:
                drop_process.start()
                throttleOut_process.start()
                jitter_process.start()
                throttleIn_process.start()
                drop_process.join()
                throttleOut_process.join()
                jitter_process.join()
                throttleIn_process.join()
            except KeyboardInterrupt:
                drop_process.terminate()
                throttleOut_process.terminate()
                jitter_process.terminate()
                throttleIn_process.terminate()
                drop_process.join()
                throttleOut_process.join()
                jitter_process.join()
                throttleIn_process.join()

    
f = FlakyWindows()
#f.real()
#f.throttleInbound(30)
#f.drop(50)
#f.throttleOutbound('10')
#f.jitter()
#f.jitter_new('10')
#f.randomBandwidth(100)
#f.real()



      
