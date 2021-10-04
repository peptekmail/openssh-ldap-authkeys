import re
from cryptography import x509
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend 
from asn1crypto import pem
from asn1crypto import x509 as asn1x509

def cert_to_sshkey(certfile):
    """
    Convert derfile to ssh pubkey. Todo validate cert
    """
    try:
        cert = x509.load_pem_x509_certificate(certfile, backend=default_backend())
        return cert.public_key().public_bytes(encoding=serialization.Encoding.OpenSSH,format=serialization.PublicFormat.OpenSSH)
    except Exception:
        #cryptography failed to parse the cert, do it step by step
        key_type, algo, data = pem.unarmor(certfile)
        k = asn1x509.Certificate.load(data)
        a = serialization.load_der_public_key(k.public_key())
        return a.public_bytes(encoding=serialization.Encoding.OpenSSH,format=serialization.PublicFormat.OpenSSH)

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

