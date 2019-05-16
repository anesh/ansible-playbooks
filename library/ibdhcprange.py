import requests
import json
import re
requests.packages.urllib3.disable_warnings()
from bs4 import BeautifulSoup
from os.path import expanduser
from ansible.module_utils.basic import *


def main():
        home = expanduser("~")
        fields = {
	"start": {"default": True, "type": "str"},
        "end": {"default": True, "type": "str"},
        "username": {"default": True, "type": "str"},
        "password": {"default": True, "type": "str", "no_log":True},
        }

	module = AnsibleModule(argument_spec = fields )
        startval = module.params["start"]
        userval = module.params["username"]
        passval = module.params["password"]
        endval = module.params["end"]

        user = userval
        pwd = passval



	url = 'https://10.2.61.100/wapi/v2.7/range'


	headers = {'content-type': "application/json"}


	json_data = { 
     			"start_addr": startval,
     			"end_addr": endval,
     			"server_association_type": "FAILOVER" ,
     			"failover_association": "DHCP-FO" 
		   }





	payload = json.dumps(json_data)
	response = requests.post(url, auth=(user, pwd), headers=headers, data=payload,verify=False)
        module.exit_json(changed=False,meta=response.text)
if __name__ == '__main__':
    main()
