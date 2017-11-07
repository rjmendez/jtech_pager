#!/usr/bin/env python
 
import sys
from rflib import *
from string import maketrans
import bitstring

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''
 
keyLen = 0
baudRate = 512
try:
    frequency = int(sys.argv[1])
except:
    print("Specify frequency. '457600000'")

#low_freq = 457000000
#high_freq = 458000000
deviation = 4500.0
 
def int2binstr8(__count):
    return "{:08b}".format(__count)
 
def makeManchester(__astr):
    astr = ''
    for x in __astr:
        if (x == '0'):
            astr += '01'
        else:
            astr += '10'
    return astr
   
def ConfigureD(d):
    d.setMdmModulation(MOD_2FSK)
    d.setFreq(frequency)
    d.setMdmDRate(baudRate)
    d.setMaxPower()
    d.setMdmSyncMode(0)
    d.setMdmDeviatn(deviation)
   
    print bcolors.OKGREEN + "[+] Radio Config:"
    print bcolors.OKGREEN + "    [+] ---------------------------------"
    print bcolors.OKGREEN + "    [+] MDMModulation: MOD_2FSK"
    print bcolors.OKGREEN + "    [+] Frequency: ",frequency
    print bcolors.OKGREEN + "    [+] Packet Length:",keyLen
    print bcolors.OKGREEN + "    [+] Baud Rate:",baudRate
    print bcolors.OKGREEN + "    [+] ---------------------------------" + bcolors.ENDC
   
#-------------------------------------------------------------------
#RAW bitstream that we are sending
message = "110000011001011011110101000100111111110110001111000111011000110000101011001100110011001101010011110000101011101100011111001101"
preamble = "10101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010"
pad1 = "1"
sync1 = "10000011001011011110101000100111"
pad2 = "111"
pager_notlost = "1101100011110001110110001100001010110011" #CAP code 79984
pager_all = "1101100011110000111011111010010001010111" #CAP code 79992
#payload1 = "001100110011"
payload1 = "0011"
payload2 = "0011"
payload3 = "0011"


 
#-------------------------------------------------------------------

pagernumber = raw_input("Page all (1)\nPage 'I'm not lost!'(2)\nSelect: ")
if pagernumber == "1":
    pager = pager_all
if pagernumber == "2":
    pager = pager_notlost

print("Pager bin (inverted for transmit)" + pager.translate(maketrans("10","01")))
print("Pager hex (inverted for transmit)" + hex(int(pager.translate(maketrans("10","01")),2)))

d = RfCat()
'''
for i in xrange(low_freq, high_freq, 12500):
    print("Transmitting " + str(i) + "Hz")
    frequency = i
    ConfigureD(d)
    astr = preamble + pad1 + sync1 + pad2 + pager + payload1 + payload2 + payload3
    print("Sending freq " + str(frequency) + "\n")
    mstr = astr
    bstr = bitstring.BitArray(bin=mstr).tobytes()
    bstrLength = len(bstr)
    d.makePktFLEN(bstrLength)
    d.RFxmit(bstr)
    d.setModeIDLE()
    #time.sleep(5)
'''
ConfigureD(d)
astr = preamble + pad1 + sync1 + pad2 + pager + payload1 + payload2 + payload3
print("Sending " + bcolors.WARNING + hex(int(pager.translate(maketrans("10","01")),2)) + bcolors.HEADER + hex(int(payload1.translate(maketrans("10","01")),2)) + bcolors.FAIL + hex(int(payload2.translate(maketrans("10","01")),2)) + bcolors.OKBLUE + hex(int(payload3.translate(maketrans("10","01")),2)) + bcolors.ENDC + "\n")
mstr = astr   
#Pack the bytes
bstr = bitstring.BitArray(bin=mstr).tobytes()
bstrLength = len(bstr)
d.makePktFLEN(bstrLength)
d.RFxmit(bstr)
d.setModeIDLE()
time.sleep(0.1)
sys.stdout.write("\n[+]Done.\n")

d.cleanup()