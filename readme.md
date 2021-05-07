# Vaccine spotter for India

Vaccine spotter is a simple tool for tracking the availability of Covid vaccines in any state in India by pincode or district code.
It uses the [api](https://apisetu.gov.in/public/marketplace/api/cowin/cowin-public-v2#/Appointment%20Availability%20APIs/) from COWIN site to monitor for vaccine availability and sent an immediate email :envelope: to user.
 ✨

## Features

- Check availability of vaccine by providing pincode or district code of your area
- Run in the terminal and monitor the vaccine availability
- Send email to email address set by user immediately when there is vaccines available
- Set age range to check availability in that range.
- Set wait time before querying again the api


## Set Up

Vaccine-spotter requires [python3](https://www.python.org/downloads/) to run

Project dependencies can be installed using the following command:

``` sh
pip install -r requirements.txt
```

Note :notebook: For gmail, the less secure apps connection needs to be turned on for email to work from [here](https://myaccount.google.com/lesssecureapps).
for other mail providers the smpt address should be modified.



## Usage
For running these scripts you've to set the email details in [config file](config.yml) file.
Edit following part of [config file](config.yml#L2-6) file. You can also edit the wait time [here](config.yml#L18)


There are two ways in which you can see vaccine availability

### Using pincode
Set your area pincode [here](config.yml#L11). Find pincode of your area [here](https://www.indiapost.gov.in/VAS/Pages/findpincode.aspx)

Set query type to `"pincode"`: [here](config.yml#L17) 
```sh
query_type : "pincode"
```

Run `python3 vaccineSpotter.py`. 
Then it'll search for vaccine availability in your area.


### Using district code
Set query type to `"district_code"`: [here](config.yml#L17). Set your district code [here](config.yml#L10)..
To know your district code follow these steps:

- First see your state code [here](https://cdn-api.co-vin.in/api/v2/admin/location/states) 

- Now edit your state code in this url https://cdn-api.co-vin.in/api/v2/admin/location/districts/{your_state_code} 
  e.g. https://cdn-api.co-vin.in/api/v2/admin/location/districts/16 for karnataka

- Click on the url for your state you can see your district code by searching your district name.

Run `python3 vaccineSpotter.py`. 
Then it'll search for vaccine availability in your area.


## Development

Want to contribute? Great! 
Feel free to raise a pull request :hugs:
