
import flakynetworksimulator.flakynetwork as f
import subprocess
import os


fn = f.FlakyNetwork()











from multiprocessing import Process
from time import sleep

a = 10


def main():
    with open(os.getcwd() + "test.log",'w') as outfile:
        subprocess.run("iperf3 -s",shell=True, stdout=outfile,stderr=subprocess.STDOUT)
        sleep(60)

def client():
    with open(os.getcwd() + "client.log",'w') as outfile:
        subprocess.run("iperf3 -c 127.0.0.1 -t 50 -J > output.json",shell=True, stdout=outfile,stderr=subprocess.STDOUT)
        print("client side complete")


def run():
    p1 = Process(target=main)
    p2 = Process(target=client)
    p3 = Process(target=fn.test,args=[4])

    p1.start()
    p3.start()
    p2.start()

if __name__=='__main__':
 
    run()