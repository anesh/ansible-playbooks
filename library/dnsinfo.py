import dns.resolver
import yaml
from os.path import expanduser
from ansible.module_utils.basic import *

def main():
	home = expanduser("~")
        intresolver = dns.resolver.Resolver()
        intresolver.nameservers = ['10.255.255.253']
        intresolver.timeout = 2
        intresolver.lifetime = 2

        extresolver = dns.resolver.Resolver()
        extresolver.nameservers = ['199.202.145.0']
        extresolver.timeout = 2
        extresolver.lifetime = 2


	arecordans = []

        module = AnsibleModule(argument_spec = {} )
	with open(home+'/ansible-playbooks/group_vars/rdata.yml') as f:
                dataMap = yaml.safe_load(f)
	for data in dataMap['rdata']:
                fqdnval = data['fqdn']
		view = data['view']

		try:
			if view == "Internal":
                        	answers= intresolver.query(fqdnval, 'A')
		
		except:
                        arecordans.append("cannotberesolved"+" : "+fqdnval)
		try:
                	if view == "External":
                        	answers= extresolver.query(fqdnval, 'A')
		except:
                        arecordans.append("cannotberesolved"+" : "+fqdnval)

		for answer in answers:
        		arecordans.append(answer.to_text()+" : "+fqdnval)


        module.exit_json(changed=False, meta=arecordans)

if __name__ == '__main__':
    main()

