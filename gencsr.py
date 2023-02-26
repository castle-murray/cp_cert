#!/opt/imh-python/bin/python3
"""CLI tool to run as a cPanel user which creates a """
from cpapis import uapi, CpAPIExecFail, CpAPIErrorMsg
import re
import sys



def gen_key() -> str:
    data = uapi('SSL::generate_key')['result']['data']
    return data['id']

def gen_csr(key_id) -> str:
    csr_data = uapi('SSL::generate_csr',
                    args={'domains': DOMAIN,
                    'localityName': CITY,
                    'stateOrProvinceName': STATE,
                    'countryName': CCODE,
                    'organizationName': ORG,
                    'organizationalUnitName': DEPT,
                    'emailAddress': EMAIL,
                    'key_id': key_id},
    )['result']['data']
    return csr_data['text']

def get_docroot(domain):
        dom_info = uapi('DomainInfo::single_domain_data', args={'domain':domain})['result']
        if dom_info['errors'] != None:
                for item in dom_info['errors']:
                        print(item)
                print("No docroot? Use CNAME or Email validation.")
        else:
            return dom_info['data']['documentroot']

## taking inputs 
DOMAIN = str(input("Domain: "))
if not DOMAIN:
    sys.exit('No domain provided.')

CITY = str(input("City: "))
if not CITY:
        sys.exit('No city provided.')

STATE = str(input("State (not abrv): "))
if not STATE:
        sys.exit('No state provided.')

CCODE = str(input("2 letter country code: "))
if not len(CCODE) == 2:
    sys.exit("2 letters in a country code.")

CCODE = CCODE.upper() ## uppercase to match CC list

## this part isn't strictly necessary but it's cool to match against a list for iput validation. 
with open("cc_list.txt", 'r') as ccodes:
    ccode_list = ccodes.read().splitlines()
    try:
        ccode_list.index(CCODE)
    except:
            sys.exit("Not a valid country code.")

## as the next two say, they can be blank. 
ORG = str(input("Organization: (can be blank) ") or "None")
DEPT = str(input("Department: (can be blank) ") or "None")
EMAIL = str(input("email address: "))
if not EMAIL:
    sys.exit("No email provided")


## generate a private key and store the ID as a var.

##
try:
        private_key = gen_key()
        print(gen_csr(private_key))
        print(get_docroot(DOMAIN))

except CpAPIErrorMsg as exc:
        print(exc)
