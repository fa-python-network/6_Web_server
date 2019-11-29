from datetime import datetime


def log(ip, name, code):
	try:
		open("file.log", "r").close()
		with open("file.log", "a") as f:
			print(f"{datetime.now().time()} to {ip} sent file({name}) with code {code}", file=f)
	except:
		with open("file.log", "w") as f:
			print(f"{datetime.now().time()} to {ip} sent file({name}) with code {code}", file=f)
