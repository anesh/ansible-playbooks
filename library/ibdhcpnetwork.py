import requests
import json
import re
requests.packages.urllib3.disable_warnings()
from os.path import expanduser
from ansible.module_utils.basic import *

def main():
	home = expanduser("~")
	fields = {
        "network": {"default": True, "type": "str"},
	"username": {"default": True, "type": "str"},
        "comment":  {"default": True, "type": "str"},
        "password": {"default": True, "type": "str", "no_log":True},
        }
        module = AnsibleModule(argument_spec = fields )
        networkval = module.params["network"]
	userval = module.params["username"]
	passval = module.params["password"]
	commval = module.params["comment"]

	user = userval
	pwd = passval
	url = 'https://10.2.61.100/wapi/v2.7/network'

	headers = {'content-type': "application/json"}


	json_data = { "network": networkval,
     	      "members": [
               {
                  "_struct": "dhcpmember",
                  "ipv4addr" : "p0adajpdhcp00.ns.ctc"

               },
               {
                  "_struct": "dhcpmember",
                  "ipv4addr" : "p0adwpbdhcp00.ns.ctc"

               }

             ],
	     "comment":commval	
            }

	payload = json.dumps(json_data)
	response = requests.post(url, auth=(user, pwd), headers=headers, data=payload,verify=False)
	module.exit_json(changed=False,meta=response.text)
if __name__ == '__main__':
    main()
