# Vaccine spotter for India using pincode

Vaccine spotter is a simple tool for tracking the availability of Covid vaccines in any state in India by pincode.
It uses the [api](https://apisetu.gov.in/public/marketplace/api/cowin/cowin-public-v2#/Appointment%20Availability%20APIs/findByPin) from COWIN site to monitor for vaccine availability and sent an immediate email :envelope: to user.
 ✨

## Features

- Check availability of vaccine by providing pincode or district code of your area
- Run in the terminal and monitor the vaccine availability
- Send email to email address set by user immediately when there is vaccines available
- set age range to check availability in that range.


## Set Up

Vaccine-spotter requires [python3](https://www.python.org/downloads/) to run

Project dependencies can be installed using the following command:

``` sh
pip install -r requirements.txt
```

Note :notebook: For gmail, the less secure apps connection needs to be turned on for email to work from [here](https://myaccount.google.com/lesssecureapps).
for other mail providers the smpt address should be modified.



## Usage
for running these scripts you've to set the email details in [config file](config.yml) file.
Edit following part of code in config.yml file
``` sh 
email:
  sent_from : "<sender_email>" 
  email_password : "<sender_password>"

  # [edit] enter receiver email details
  to : ["<receiver_email_id>"]
```

There are two ways in which you can see vaccine availability
1. vaccine spotter by pincode.
set your area pincode in [config file](config.yml) file here for example. FInd pincode of your area [here](https://www.indiapost.gov.in/VAS/Pages/findpincode.aspx)
``` sh 
area_info:
# [edit] enter your district code or pincode
  __district_code : "<district_code>" 
  __pincode : "<pincode>"
```
Run  
```sh
python3 vaccine-spotter-by-pincode.py

```
Then it'll search for vaccine availability in your area.


2. vaccine spotter by district code
Set district code in the [config file](config.yml) file.
To know your district code follow these steps:

- see your state code [here](https://cdn-api.co-vin.in/api/v2/admin/location/states) 

- Now edit your state code in this url https://cdn-api.co-vin.in/api/v2/admin/location/districts/{your_state_code} 
  e.g. https://cdn-api.co-vin.in/api/v2/admin/location/districts/16 for karnataka

- on the above url here you can see your district code.


enter the district code in [config file](config.yml) file

``` sh 

area_info:
# [edit] enter your district code or pincode
  __district_code : "<district_code>"
``` 

Run the script after setting the values 
```sh
python3 vaccine-spotter-by-pincode.py

```
It'll search for availibility of vaccine centers in that area.


## Development

Want to contribute? Great! 
Feel free to raise a pull request :hugs:
