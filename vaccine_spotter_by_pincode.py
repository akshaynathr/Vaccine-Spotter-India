import requests
from datetime import date,datetime
import os
import smtplib
from time import time,ctime
import yaml

## get params
with open("config.yml", "r") as ymlfile:
    cfg = yaml.safe_load(ymlfile)

email_info = cfg["email"]
area_info = cfg["area_info"]


sent_from = email_info['sent_from']
email_password = email_info['email_password']


# receiver email details
to = email_info['to']

# area code
__pincode = area_info['__pincode']

## call api after every five minutes
minutes = 5

today = date.today()
d1 = today.strftime("%d/%m/%Y")

__date = str(d1).replace("/","-")


## send email of avalailable vaccination centres
def send_email(res):
	# turn on allow less secure apps to get email
	#  https://myaccount.google.com/lesssecureapps
	# suggest to use a backup account for this to preserve security
	
	subject = 'Vaccine slot available for pincode ' + __pincode
	body = "Following vaccines centers are found \n\n Query Time :  "+ctime(time())+"\n\n" + res

	email_text = """\
From: %s
To: %s 
Subject: %s
%s
""" % (sent_from, ", ".join(to), subject, body)
	print(email_text)

	try:
	    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
	    server.ehlo()
	    server.login(email_user, email_password)
	    server.sendmail(sent_from, to, email_text)
	    server.close()

	    print('Email sent!')
	except Exception as e:
	    print('Something went wrong...')
	    print (e)



def parse_json_pincode(result):
    output = []
    sessions = result['sessions']
    if len(sessions):
        return output
    for session in sessions:
        if session['available_capacity'] >= 0:
            res = { 'name': session['name'], 'block_name':session['block_name'],'age_limit':session['min_age_limit'], 'vaccine_type':session['vaccine'] , 'date':session['date'],'available_capacity':session['available_capacity'] }
            output.append(res)
    return output

## main function
def call_api():
    print(ctime(time()))
    api_pin = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode=" + __pincode + "&date=" + __date

    # print(api_pin)
    response = requests.get(api_pin)
    # print(response)
    if response.status_code == 200:
        print("API call success")
        result = response.json()
        output = parse_json_pincode(result)
        if len(output) > 0:
            print("Vaccines available\n")
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
                # print(center)
            send_email(result_str)

        else:
            print("Vaccines not available \n")
    else:
        print("something went wrong :(\nStatus code {} \nTrying again.....\n".format(response.status_code))

t = datetime.now()

if __name__ == '__main__':
    call_api()
    while True:
        delta = datetime.now()-t
        if delta.seconds >= minutes * 60:
            call_api()
            t = datetime.now()
        
