import re
from cryptography import x509
from cryptography.hazmat.primitives import serialization

def cert_to_sshkey(certfile):
    """
    Convert derfile to ssh pubkey. Todo validate cert
    """
    cert = x509.load_pem_x509_certificate(certfile)
    return cert.public_key().public_bytes(encoding=serialization.Encoding.OpenSSH,format=serialization.PublicFormat.OpenSSH)

def basedn_to_domain(basedn):
    """
    Convert an LDAP base DN "dc=example,dc=com" into a DNS domain "example.com".
    """
    if not isinstance(basedn, str):
        raise TypeError("basedn is expected to be a string")

    basedn = basedn.lower()
    expr = re.compile(r'^(dc=[a-z0-9-]+)(, *dc=[a-z0-9-]+)*$')

    if not expr.match(basedn):
        raise ValueError("basedn must consist of only \"dc\" components to use DNS SRV lookup")

    domain = []
    basedn = re.split(', *dc=', basedn[3:])

    return '.'.join(basedn)

def domain_to_basedn(domain):
    """
    Convert a domain (example.com) to base DN (dc=example,dc=com)
    """
    dn = []
    for part in domain.lower().split('.'):
        dn.append("dc=%s" % (part))

    return ','.join(dn)

