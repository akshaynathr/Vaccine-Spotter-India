# Vaccine spotter for India



Vaccine spotter is a simple tool for tracking the availability of Covid vaccines in any state in India
It uses the api from COWIN site to monitor for vaccine availability and sent an immediate email to user.
 ✨

## Features

- Run in the terminal and monitor the vaccine availability
- Sent email to email address set by user immediately when there is vaccines available

### Update
- Now Vaccine spotter supports age filter as per request from many people
``` sh
# remove the age not needed to be monitored from the age list in script 
age = [18,45]

``` 

## Installation

Vaccine-spotter requires python3 to run

Set email details, district_id in the script 

** Note: For gmail to work, the lesssecureapps connection needs to be turned on for email to work :  https://myaccount.google.com/lesssecureapps **

``` sh 
# For gmail, the lesssecureapps connection needs to be turned on for email to work :  https://myaccount.google.com/lesssecureapps
# need to change the smpt address for other mail providers

email_user = '<your_email>@gmail.com'
email_password = '<password>'

sent_from = email_user
to = ['<your_email@gmail.com>']

# time gap
minutes = 1

__district = "district_id"
'''
Some examples: 
295 - Kasargod
296 - Thiruvananthapuram
298 - kollam
299 - Wayanad
300 - Pathanamthitta
302 - Malappuram
303 - thrissue
305 - Kozikode
306- idukki
307 - ernakulam
308 - palakkad
571 - Chennai
276 - Bangalore Rural
265 - Bangalore Urban
'''
``` 

Run the script after setting the values 
```sh
python vaccine_spotter.py

```
No data is collected from users . The script is open to verify
 
## Development

Want to contribute? Great!


