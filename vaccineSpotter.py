import requests
from datetime import date,datetime,timedelta
import os
import smtplib,ssl
from time import time,ctime
import yaml


class vaccineSpotter:
	def __init__(self, config_file_path, time_delay=1):
		self.config_file_path = config_file_path
		self.time_delay = time_delay
		self.cfg = self.read_config()
		self.set_params()
		self.prev_response=None
		self.telegram_info=None
		self.headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"}


	def read_config(self):
		with open(self.config_file_path, "r") as ymlfile:
			cfg = yaml.safe_load(ymlfile)
		return cfg
		
	def set_params(self):
		## params
		self.area_info = self.cfg["area_info"]
		
		## sender mail info
		if self.cfg.get("email"):
			self.email_info = self.cfg["email"]
			self.sent_from = self.email_info['sent_from']
			self.email_user = self.sent_from
			self.email_password = self.email_info['email_password']
			# receiver email details
			self.to = self.email_info['to']

		# area code
		self.__district_code = self.area_info['__district_code']
		self.__pincode = self.area_info['__pincode']

		#age limit for vaccination
		self.age_limit_info = self.cfg['age_limit']
		self.age_limit = self.age_limit_info['age_limit']

		# if self.cfg.
		if self.cfg.get('telegram') :
			self.telegram_info=self.cfg['telegram']
			self.telegram_token=self.telegram_info["token"]
			self.telegram_channel=self.telegram_info["channel"]
			self.base = "https://api.telegram.org/bot{}/".format(self.telegram_token)

	def send_email(self, result,d1):
	# turn on allow less secure apps to get email
	#  https://myaccount.google.com/lesssecureapps
	# suggest to use a backup account for this to preserve security
	
		subject = 'Vaccine slot available in your area for date {}'.format(d1)
		body = "Following vaccines centers are found \n\n Query Time : \
				 "+ctime(time())+"\n\n" + result

		email_text = f"""\
Subject: {subject}
To: {",".join(self.to)}
From: {self.sent_from}

{body}"""

		try:
			server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
			server.ehlo()
			server.login(self.email_user, self.email_password)
			server.sendmail(from_addr=self.sent_from, to_addrs=self.to, msg=email_text)
			print('Email sent!\n')
		except Exception as e:
			print('Something went wrong...')
			print (e)
		# finally:
		# 	server.quit()

	def send_telegram_msg(self,result_str):
		url = self.base + "sendMessage?chat_id=@{}&text={}".format(self.telegram_channel,result_str)
		if result_str is not None:
			response=requests.get(url,headers=self.headers)
			print("response from telegram :{}".format(response))

	def parse_json_district_code(self, result):
		output = []
		centers = result['centers']
		for center in centers:
			sessions = center['sessions']
			for session in sessions:
				if session['available_capacity'] > 0:
					res = { 'name': center['name'], 'block_name':center['block_name'],'address':center['address'],\
					'fee_type':center['fee_type'],'age_limit':session['min_age_limit'], 'vaccine_type':session['vaccine'] ,\
					 'date':session['date'],'available_capacity':session['available_capacity'] }
					if res['age_limit'] in self.age_limit:
						output.append(res)
		return output


	def parse_json_pincode(self, result):
		output = []
		sessions = result['sessions']
		if len(sessions)==0:
			return output
		for session in sessions:
			if session['available_capacity'] >= 0:
				res = { 'name': session['name'], 'block_name':session['block_name'],'address':center['address'],\
				'fee_type':center['fee_type'],'age_limit':session['min_age_limit'], 'vaccine_type':session['vaccine'] , \
				'date':session['date'],'available_capacity':session['available_capacity'] }
				if res['age_limit'] in self.age_limit:
					output.append(res)
		return output

	def call_api(self, url, headers, query_type,d1):
		response = requests.get(url, headers = headers)
		if response.status_code == 200:
			print("API call success")
			result = response.json()
			if result==self.prev_response:
				print('response is same as previous .... skipping\n')
				return
			if query_type=='district_code':
				output = self.parse_json_district_code(result)
			elif query_type =='pincode':
				output = self.parse_json_pincode(result)
			else:
				print('incorrect query type\nquery type must be either district_code or pincode\n')
				return
			if len(output) > 0:
				print("Vaccines available")
				print('\007')
				result_str = "!!!! AVAILABLE SLOTS ALERT !!!!"+ "\n\n"
				for center in output:
					result_str = result_str + "Center Name : "+center['name'] + "\n"
					result_str = result_str + "Date : "+str(center['date']) + "\n"
					result_str = result_str + "Block : "+center['block_name'] + "\n"
					result_str = result_str + "Address : "+center['address'] + "\n"
					result_str = result_str + "Fee Type : "+center['fee_type'] + "\n"
					result_str = result_str + "Available Vaccine Count : "+str(center['available_capacity']) + "\n"
					result_str = result_str + "Vaccin Type : "+ center['vaccine_type'] + "\n"
					result_str = result_str + "Age limit : "+str(center['age_limit'])+"\n"
					result_str = result_str + "\n-----------------------------------------------------\n"
				self.prev_response=result
				if self.cfg.get("email"):
					self.send_email(result_str,d1)
				if self.cfg.get('telegram') :
					self.send_telegram_msg(result_str)

			else:
				print("Vaccines not available for age limit {}\nTrying again\
				 after {} minute.....\n".format(*self.age_limit, self.time_delay))
		else:
			print("something went wrong :(\nStatus code {} \nTrying again......\
				after {} minute.....\n".format(response.status_code, self.time_delay))


	def query(self, root_url, query_type,d1):
		print(ctime(time()))
		
		# format date
		# today = date.today()
		# d1 = today.strftime("%d/%m/%Y")
		__date = str(d1).replace("/","-")


		if query_type == 'district_code':
			url = root_url + "/calendarByDistrict?district_id=" + self.__district_code + "&date="+ __date

		elif query_type =='pincode':
			url = root_url + "/findByPin?pincode=" + self.__pincode + "&date=" + __date
		else:
			print('incorrect query type\nquery type must be either district_code or pincode\n')
			return
		self.call_api(url,  self.headers, query_type,d1)


t = datetime.now()
if __name__ == '__main__':
	# setu docs say they have a rate limit of 100 requests per 5 min
	time_delay = 0.1
	query_type = 'district_code' # set it to "pincode" to query by pincode
	config_file_path = 'config.yml'
	
	print("querying by {} .....".format(query_type))
	## root url and headers
	root_url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public"

	vaccineSpotter = vaccineSpotter(config_file_path, time_delay)

	while True:
		delta = datetime.now()-t
		if delta.seconds >= time_delay * 60:
			# for i in range(6):
			try:
				d1=datetime.strftime(datetime.today() + timedelta(days = 0) , ("%d/%m/%Y"))
				print("trying to get slots for date:{}.....\n".format(d1))
				vaccineSpotter.query(root_url,query_type,d1)
				t = datetime.now()
			except Exception as e:
				print("EXCEPTION : {}".format(e))