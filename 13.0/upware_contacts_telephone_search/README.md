# upware_contacts_telephone_search
This module  adds a new default search field called 'Algemeen' to the contacts module. 
## Purpose
Our client searches for customers mainly by phone number without spaces, plus signs, underscores, ...
## Install
Install the module via Apps > Clear Filter | Search "upware_contacts" > Install.

![installation](https://i.gyazo.com/8d07d9ccc74ea34197e05fb49350292d.png)
## Functionality
This field needs to search in the following fields:

* phone_field_sanitized
* mobile_field_sanitized
* email
* city
* street
* zip
* ref
* name

### Behaviour - at installation
When the module is installed it will sanitize all phone and mobile fields and save it into the fields.
### Behaviour - at runtime
When a user edits the phone or mobile field it will recalculate the sanitized version.
## Testing
Go to the contacts module and search by 'Algemeen'. 

![query](https://i.gyazo.com/0ccb2f615e533002c2fa2d832a2afe93.gif)

Normally a user cannot find Brandon Freeman by querying his phonenumber using "68732" as term. You need to search for "(355)-687-3262", this module fixes that.