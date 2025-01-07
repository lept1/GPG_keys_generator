import gnupg
from optparse import OptionParser
 
default_PP='123456pass'

parser = OptionParser()
# add options
parser.add_option("-u", "--user",
                  dest = "user",
                  help = "name of the user receiving th public key")
parser.add_option("-o", "--owner",
                  dest = "owner",
                  help = "name of the owner of the private key")
parser.add_option("-e", "--email",
                  dest = "email",
                  help = "email of the owner of the private key")
parser.add_option("-p", "--passphrase",
                  dest = "passphrase", default=default_PP,
                  help = "passphrase to generate keys")
 
(options, args) = parser.parse_args()

owner = options.owner
user = options.user
email = options.email
passphrase = options.passphrase

if owner is None:
    print('OWNER must be specified')
    parser.print_help()
    exit(0)
if user is None:
    print('USER must be specified')
    parser.print_help()
    exit(0)
if email is None:
    print('EMAIL must be specified')
    parser.print_help()
    exit(0)
if passphrase is None:
    print('PASSPHRASE must be specified')
    parser.print_help()
    exit(0)
elif passphrase==default_PP:
    print('using default PASSPHRASE...')


gpg = gnupg.GPG()


print('Generating keys...')
# generate key
input_data = gpg.gen_key_input(name_email=email, passphrase=passphrase)
key = gpg.gen_key(input_data)

# create ascii-readable versions of pub / private keys
ascii_armored_public_keys = gpg.export_keys(key.fingerprint)
ascii_armored_private_keys = gpg.export_keys(keyids=key.fingerprint, secret=True, passphrase=passphrase)

# export
pair_name=f"{owner}_{user}"

priv_file=f'{pair_name}_private_key.asc'
with open(priv_file, 'w') as f:
    f.write(ascii_armored_private_keys)
pub_file=f'{pair_name}_public_key.asc'

with open(pub_file, 'w') as f:
    f.write(ascii_armored_public_keys)

pass_file=f'{pair_name}_passphrase.txt'
with open(pass_file, 'w') as f:
    f.write(passphrase)

print(f'Keys generated.\nLook at the files:\n - {priv_file}\n - {pub_file}\n - {pass_file}')