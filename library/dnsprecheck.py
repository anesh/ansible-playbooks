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
	flag = 0
        
	fields = {
        "fqdnpar": {"default": True, "type": "str"},
 	"viewpar": {"default": True, "type": "str"},
        }
        module = AnsibleModule(argument_spec = fields )
        fqdnval = module.params["fqdnpar"]
	viewval = module.params["viewpar"]
	try:
		if viewval == "Internal":
			answers= intresolver.query(fqdnval, 'A')
	except:
                arecordans.append("cannotberesolved"+" : "+fqdnval)
	try:
		if viewval == "External":
			answers= extresolver.query(fqdnval, 'A')
	except:
                arecordans.append("cannotberesolved"+" : "+fqdnval)


	for answer in answers:
        	arecordans.append(answer.to_text()+" : "+fqdnval)

	for record in arecordans:
		if "cannotberesolved" not in record:
			flag =flag +1 
		

        module.exit_json(changed=False,meta=flag)

if __name__ == '__main__':
    main()

