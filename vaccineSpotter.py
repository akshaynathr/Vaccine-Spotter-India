import requests
from datetime import date,datetime
import os
import smtplib
from time import time,ctime
import yaml


class vaccineSpotter:
	def __init__(self, config_file_path):
		self.config_file_path = config_file_path
		self.cfg = self.read_config()
		self.set_params()

		## root url and headers
		self.root_url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public"
		self.headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"}

	# read config file
	def read_config(self):
		with open(self.config_file_path, "r") as ymlfile:
			cfg = yaml.safe_load(ymlfile)
		return cfg
		
	def set_params(self):
		## params
		self.email_info = self.cfg["email"]
		self.area_info = self.cfg["area_info"]
		self.age_limit_info = self.cfg["age_limit"]
		self.query_info = self.cfg["query_info"]
		
		## sender mail info
		self.sent_from = self.email_info['sent_from']
		self.email_user = self.sent_from
		self.email_password = self.email_info['email_password']

		# receiver email details
		self.to = self.email_info['to']

		# area code
		self.__district_code = self.area_info['__district_code']
		self.__pincode = self.area_info['__pincode']

		#age limit for vaccination
		self.age_limit = self.age_limit_info['age_limit']

		# query type and time delay for querying the cowin site
		self.query_type = self.query_info['query_type']
		self.wait_time = self.query_info['wait_time']


	def send_email(self, res):
	# turn on allow less secure apps to get email
	#  https://myaccount.google.com/lesssecureapps
	# suggest to use a backup account for this to preserve security
	
		subject = 'Vaccine slot available in your area'
		body = "Following vaccines centers are found \n\n Query Time :  "+ctime(time())+"\n\n" + res
		email_text = """\
From: %s
To: %s 
Subject: %s
%s
""" % (self.sent_from, ", ".join(self.to), subject, body)
		print(email_text)

		try:
			server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
			server.ehlo()
			server.login(self.email_user, self.email_password)
			server.sendmail(self.sent_from, self.to, email_text)
			server.close()

			print('Email sent!')
		except Exception as e:
			print('Something went wrong while sending the email...')
			print (e)


	def parse_json_district_code(self, result):
		"""
			parse json pbtained from the CoWIN API using district code
		"""
		output = []
		centers = result['centers']
		for center in centers:
			sessions = center['sessions']
			for session in sessions:
				if session['available_capacity'] > 0:
					res = { 'name': center['name'], 'block_name':center['block_name'],\
					'age_limit':session['min_age_limit'], 'vaccine_type':session['vaccine'] ,\
					 'date':session['date'],'available_capacity':session['available_capacity'] }
					if res['age_limit'] in self.age_limit:
						output.append(res)
		return output


	def parse_json_pincode(self, result):
		"""
			parse json pbtained from the CoWIN API using pincode
		"""
		output = []
		sessions = result['sessions']
		if len(sessions)==0:
			return output
		for session in sessions:
			if session['available_capacity'] >= 0:
				res = { 'name': session['name'], 'block_name':session['block_name'], \
				'age_limit':session['min_age_limit'], 'vaccine_type':session['vaccine'] , \
				'date':session['date'],'available_capacity':session['available_capacity'] }
				if res['age_limit'] in self.age_limit:
					output.append(res)
		return output

	def call_api(self, url, headers, query_type):
		"""
			call CoWIN API and exteact vaccination centre details
		"""

		response = requests.get(url, headers = headers)
		if response.status_code == 200:
			print("API call success")
			result = response.json()
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
				result_str = ""
				for center in output:
					result_str = result_str + center['name'] + "\n"
					result_str = result_str + "block:"+center['block_name'] + "\n"
					result_str = result_str + "vaccine count:"+str(center['available_capacity']) + "\n"
					result_str = result_str + "vaccine type:"+ center['vaccine_type'] + "\n"
					result_str = result_str + center['date'] + "\n"
					result_str = result_str + "age_limit:"+str(center['age_limit'])+"\n"
					result_str = result_str + "-----------------------------------------------------\n"
				self.send_email(result_str)
				print("\nTrying again after {} minutes.....\n".format(self.wait_time))

			else:
				print("Vaccines not available for age limit {}\nTrying again...\
					after {} minutes.....\n".format(*self.age_limit, self.wait_time))
		else:
			print("something went wrong :(\nStatus code {} \nTrying again...\
				after {} minutes.....\n".format(response.status_code, self.wait_time))


	def query(self, root_url, headers, query_type):
		"""
			requests the CoWIN site for vaccination availability depending on the query_type
		"""

		print(ctime(time()))
		
		# format date
		today = date.today()
		d1 = today.strftime("%d/%m/%Y")
		__date = str(d1).replace("/","-")

		# check for query type
		if query_type == 'district_code':
			url = root_url + "/calendarByDistrict?district_id=" + self.__district_code + "&date="+ __date

		elif query_type =='pincode':
			url = root_url + "/findByPin?pincode=" + self.__pincode + "&date=" + __date
		else:
			print('incorrect query type\nquery type must be either district_code or pincode\n')
			return
		self.call_api(url,  headers, query_type)
		return

	def main(self):
		"""main function for querying the CoWIN site"""
		curr_t = datetime.now()
		print("querying by {} .....".format(self.query_type))
				
		# query the CoWIN site
		self.query(self.root_url, self.headers, self.query_type)

		## query the cowin site after every time_delay minutes
		while True:
			delta = datetime.now() - curr_t
			if delta.seconds >= self.wait_time * 60:
				self.query(self.root_url, self.headers, self.query_type)
				curr_t = datetime.now()

if __name__ == '__main__':

	# config file path
	config_file_path = 'config.yml'
	vaccineSpotter = vaccineSpotter(config_file_path)
	vaccineSpotter.main()
