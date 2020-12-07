from os import system, name
from time import sleep
from datetime import date
from datetime import datetime
import numpy as np
import pandas as pd

custCatalog = []
custMultiplier = []
custTotal = 0
custCash = 0

def clear(): 
	if name == 'nt': 
		_ = system('cls')

def inputCustomerCatalog():
	openCatalog = pd.read_excel("dataBarang.xlsx")
	print("======================================================")
	print("                     LIST BARANG                      ")
	print("======================================================")
	print(openCatalog)
	print("======================================================")
	print("   INPUT KODE DAN JUMLAH BARANG (X UNTUK MENGAKHIRI)  ")
	print("======================================================")

	i=1
	while True:
		print(f"KODE BARANG {i}: ", end="")
		itemCode = input()
		if(itemCode=="X"): break

		openCatalog = pd.read_excel("dataBarang.xlsx")
		exists=itemCode in openCatalog.values

		openCatalog = openCatalog.set_index('kodeBarang')
		itemPrice = openCatalog['hargaBarang']
		itemNames = openCatalog['namaBarang']

		if (exists):
			print("JUMLAH BARANG: ", end="")
			itemAmount=0

			while True:
				try:
					itemAmount=int(input())
					if(itemAmount<=0):
						print("INVALID INPUT")
						print("JUMLAH BARANG: ", end="")
						continue
					break
				except:
					print("INVALID INPUT")
					print("JUMLAH BARANG: ", end="")
					continue

			print("{:<25s} {:>4d}x {:>10d} per pcs"
			.format(itemNames[itemCode], itemAmount, itemPrice[itemCode]))
			print("\n")

			custCatalog.append(itemCode)
			custMultiplier.append(itemAmount)
			i+=1
		else:
			print("KODE INVALID")
			continue

	clear()
	openCatalog = pd.read_excel("dataBarang.xlsx")
	print("======================================================")
	print("                     LIST BARANG                      ")
	print("======================================================")
	print(openCatalog)
	print("======================================================")
	print("                  KATALOG PELANGGAN:                  ")
	print("======================================================")

	openCatalog = openCatalog.set_index('kodeBarang')
	itemPrice = openCatalog['hargaBarang']
	itemNames = openCatalog['namaBarang']

	print("{:<25s} {:>8s}x {:>15s} per pcs".format("BARANG", "JUMLAH", "HARGA"))

	for i in range(len(custCatalog)):
		print("{:<25s} {:>8d}x {:>15d}"
			.format(itemNames[custCatalog[i]], custMultiplier[i], itemPrice[custCatalog[i]]))
	print("Konfirmasi? (YES/NO)")

	isConfirmCat = input()
	while not((isConfirmCat == "YES") or (isConfirmCat == "NO")):
		print("INPUT INVALID. Konfirmasi? (YES/NO) ", end="")
		isConfirmCat = input()

	if(isConfirmCat=="YES"): return True
	else: return False

def priceTotallings():
	openCatalog = pd.read_excel("dataBarang.xlsx")

	layouting = '='*60
	print(layouting)
	print("{:>38s}{:<25s}".format("KATALOG PELANGGAN", " "))
	print(layouting)

	openCatalog = openCatalog.set_index('kodeBarang')
	itemPrice = openCatalog['hargaBarang']
	itemNames = openCatalog['namaBarang']

	print("{:<25s} {:>8s}x {:>15s} per pcs".format("BARANG", "JUMLAH", "HARGA"))
	for i in range(len(custCatalog)):
		print("{:<25s} {:>8d}x {:>15d}"
			.format(itemNames[custCatalog[i]], custMultiplier[i], itemPrice[custCatalog[i]]))

	priceSum=0
	for i in range(len(custCatalog)):
		priceSum+=custMultiplier[i]*itemPrice[custCatalog[i]]
	print(f"\nJumlah uang tunai yang harus dibayar: {priceSum}")
	return priceSum

def calculateDenom(number):
	temp = number

	denom = [0 for i in range(10)]
	pecahan = (100000, 50000, 20000, 10000, 5000, 
				2000, 1000, 500, 200, 100)

	for i in range(10):
		denom[i] = int(temp/pecahan[i])
		temp -= denom[i]*pecahan[i]

	if(temp==0):
		print("\nDENOMINASI PECAHAN KEMBALIAN:")

		for i in range(10):
			print("{:<10d} rupiah: {:>5} buah".format(pecahan[i], denom[i]))
		print()
	else:
		for i in range(10):
			print(f"{pecahan[i]} rupiah: {denom[i]} buah")

		print(f"SISA: {temp} rupiah\n")

def inputCustCash(cash):
	layouting = '='*60

	global custCash

	print("Input uang tunai pelanggan: (-1 UNTUK MENGAKHIRI) ", end="")
	custCash = int(input())

	if(custCash==-1):
		return 0

	print(layouting)

	cashBack = custCash - cash

	while(cashBack<0):
		print("UANG TIDAK CUKUP.\nInput uang tunai pelanggan: ", end="")
		custCash = int(input())

		if(custCash==-1):
			return 0

		cashBack = custCash - cash

	if(cashBack==0):
		print("Uang pas.\n")
		print("\n", layouting)
		return 1
	elif(cashBack>=0): 
		calculateDenom(cashBack)
		print(layouting)
		return 1

def printReceipt():
	clear()
	openCatalog = pd.read_excel("dataBarang.xlsx")
	openCatalog = openCatalog.set_index('kodeBarang')
	itemPrice = openCatalog['hargaBarang']
	itemNames = openCatalog['namaBarang']
	layouting = '='*80

	fileData = open("dataToko.txt", "r")
	dataLines = fileData.readlines()
	fileData.close()

	today = date.today()
	now = datetime.now()
	dateToday = today.strftime("%b-%d-%Y")
	timeToday = now.strftime("%H-%M-%S")

	struk = open(f"STRUK {dateToday} {timeToday}.txt", 'w')
	print(f"{layouting}\n")
	struk.write(f"{layouting}\n")

	for line in dataLines:
		length = len(line)
		approxPlace = int((80-length)/2)
		outLine = "\n" + " "*approxPlace + line
		print(outLine)
		struk.write(outLine)

	print(f"\n{layouting}\n")
	struk.write(f"\n{layouting}\n")

	outLine = "{:<25s} {:>8s}x {:>20s} {:>20s}".format("BARANG", "JUMLAH", "HARGA", "TOTAL")
	print(f"\n{outLine}\n")
	struk.write(f"\n{outLine}\n")

	for i in range(len(custCatalog)):
		outLine = "{:<25s} {:>8d}x {:>20d} {:>20d}".format(itemNames[custCatalog[i]], 
		custMultiplier[i], itemPrice[custCatalog[i]], 
		custMultiplier[i]*itemPrice[custCatalog[i]])
		print(f"{outLine}\n")
		struk.write(f"{outLine}\n")

	print(f"\n{layouting}\n")
	struk.write(f"\n{layouting}\n")

	global custTotal
	global custCash

	outLine = "{:<40s} {:>36d}".format("JUMLAH HARGA:", custTotal)
	print(f"{outLine}\n")
	struk.write(f"{outLine}\n")

	outLine = "{:<40s} {:>36d}".format("TUNAI:", custCash)
	print(f"{outLine}\n")
	struk.write(f"{outLine}\n")

	outLine = "{:<40s} {:>36d}".format("KEMBALIAN:", custTotal-custCash)
	print(f"{outLine}\n")
	struk.write(f"{outLine}\n")

	print(f"\n{layouting}\n")
	struk.write(f"\n{layouting}\n")

	dateReceipt = today.strftime("%b-%d-%Y")
	timeReceipt = now.strftime("%H:%M:%S")

	outLine = "{:<40s} {:>36s}".format("TANGGAL:", dateReceipt)
	print(f"{outLine}\n")
	struk.write(f"{outLine}\n")

	outLine = "{:<40s} {:>36s}".format("JAM:", timeReceipt)
	print(f"{outLine}\n")
	struk.write(f"{outLine}\n")
	struk.close()

def main(args):


	print("Nyalakan mesin kasir? (YES/NO) ", end="")
	isActivate = input()

	while not((isActivate == "YES") or (isActivate == "NO")):
		clear()
		print("INPUT INVALID. Nyalakan mesin kasir? (YES/NO) ", end="")
		isActivate = input()
	if(isActivate=="NO"):
		exit()

	clear()
	print("Masukkan identitas dan password.")
	print("ID: ", end="")
	identityName = input()
	print("Password: ", end="")
	pwName = input()

	while (identityName != "admin") or (pwName != "admin"):
		clear()
		print("ID dan Password tidak valid. Coba lagi.", end="\n")
		print("ID: ", end="")
		identityName = input()
		print("Password: ", end="")
		pwName = input()

	global custTotal
	global custCash
	while True:
		clear()
		isConfirm = inputCustomerCatalog()

		if(isConfirm):
			clear()
			total = priceTotallings()
			custTotal = total
			isValid = inputCustCash(total)

			if(isValid==1):
				print("\n(INPUTKAN SESUATU UNTUK MENAMPILKAN RESI)")
				dump = input()
				printReceipt()
		
		print("\n(INPUTKAN SESUATU UNTUK MENGAKHIRI)")
		a = input()

		custCatalog.clear()
		custMultiplier.clear()
		custCash = 0
		custTotal = 0
		clear()

		print("Registrasi baru? (YES/NO) ")
		isNewCustomer = input()

		while not((isNewCustomer == "YES") or (isNewCustomer == "NO")):
			clear()
			print("INPUT INVALID. Registrasi baru? (YES/NO) ", end="")
			isNewCustomer = input()
		if (isNewCustomer=="NO"): break
	return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
