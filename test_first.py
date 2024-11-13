p = int(input("masukkan panjang :"))
l = int(input("masukan lebar :"))
t = int(input("masukkan tinggi :"))
r = int(input("masukan jari jari :"))

import math
def volumeBalok(panjang, lebar, tinggi):
    vol = panjang * lebar * tinggi
    return vol

def volumeKerucut(jari_jari, tinggi):
    vol = math.pi * math.pow(jari_jari,2) * ((1/3) * tinggi)
    return vol

def main():
    print(__name__)
    vol_kerucut = volumeKerucut(r,t)
    print("Volume Kerucut : ", vol_kerucut)
    print("---------------------")
    volBalok = volumeBalok(p,l,t)
    print("Volume Balok : ", volBalok)

if __name__ == "__main__":
    main()