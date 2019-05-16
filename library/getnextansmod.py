
import requests
import json
requests.packages.urllib3.disable_warnings()
import re
from bs4 import BeautifulSoup
from ansible.module_utils.basic import *

def main():
        fields = {
        "req_no": {"default": True, "type": "str"},
        "username": {"default": True, "type": "str"},
        "password": {"default": True, "type": "str", "no_log":True},
        }
        module = AnsibleModule(argument_spec = fields )
        reqnum = module.params["req_no"]
        user = module.params["username"]
        pwd = module.params["password"]

        url = 'https://cantiresb.service-now.com/api/now/table/sc_req_item?sysparm_query=request.number%3D'+reqnum+'&sysparm_limit=1'
        headers = {"Accept":"application/xml"}
        response = requests.get(url, auth=(user, pwd), headers=headers)


        soup = BeautifulSoup(response.text,'xml')
        titles = soup.find_all('description')
        data = ""
        for title in titles:
                data = title.get_text()

        number=re.search(r"(?<=Number of IP's required\?\:)(.*)",data)
        numberpayload = int(number.group(0))
	fqdn=re.findall(r"(?<=FQDN/Hostname/Device Name for which IP's are requested\?\: )(.*?)(?=VLAN)",data, re.DOTALL)
	fqdnlist= fqdn[0].split('\n')
	fqdnlistclean = filter(None,fqdnlist)

	ipsubnet=re.search(r"(?<=IP Subnet\:)(.*)",data)
        ipsubnetval= ipsubnet.group(0)

        sep = ":"
        url = "https://10.2.61.100/wapi/v2.7/network?network="+ipsubnetval
        response = requests.request("GET", url, auth=(user,pwd),verify=False)
        values= response.text
        jsonv = json.loads(values)
        x = jsonv[0]['_ref']
        refid = x.split(sep,1)[0]

        url = "https://10.2.61.100/wapi/v2.7/"+refid+"?_function=next_available_ip"
        headers = {'content-type': "application/json"}
        nextipparams = { "num": numberpayload }
	payload = json.dumps(nextipparams)

	response = requests.request("POST", url, auth=(user,pwd),data=payload,  headers=headers,verify=False)
        ipjson = response.text
        ipjsonload = json.loads(ipjson)
	nextavlist = ipjsonload['ips']
	servicenowupdatelist = []
	for postfqdn,postnextip in zip(fqdnlistclean,nextavlist):

        	url = "https://10.2.61.100/wapi/v2.7/record:host"
		values = { "name":postfqdn, "ipv4addrs":[{"ipv4addr":postnextip}],"view": "External" }
		snvalues =  postfqdn+": "+postnextip+" "
		servicenowupdatelist.append(snvalues)
		payload = json.dumps(values)
       		headers = {'content-type': "application/json"}
        	response = requests.request("POST", url, auth=(user, pwd), data=payload, headers=headers,verify=False)

	sysidurl = 'https://cantiresb.service-now.com/api/now/table/sc_req_item?sysparm_query=request.number='+reqnum
	headers = {"Accept":"application/xml"}
	snresponse = requests.get(sysidurl, auth=(user, pwd), headers=headers)
	snxmldata = snresponse.text

	soup = BeautifulSoup(snxmldata,'xml')
	getsysidtag = soup.find_all('sys_id')
	sysid = ""
	for sysidtag in getsysidtag:
        	sysid = sysidtag.get_text()



	updateurl = 'https://cantiresb.service-now.com/api/now/table/sc_req_item/'+sysid
	headers = {"Content-Type":"application/xml","Accept":"application/xml"}
	values = ''.join(servicenowupdatelist)
	payload = "<request><entry><comments>"+str(values)+"</comments></entry></request>"
	response = requests.put(updateurl, auth=(user, pwd), headers=headers, data=payload)

	
        theReturnValue = {"success"}
        module.exit_json(changed=False, meta=theReturnValue)

if __name__ == '__main__':
    main()

