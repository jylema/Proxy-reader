#!/usr/bin/env python

# run as python script

print('This script activates the httpProxyServer if both are in the same directory.')
print('Currently the proxy server is on localhost 127.0.0.1 and on port 12346. Do you want to change address or port?')

answer = input("Yes or No?:  ")

if(answer == 'Yes' or answer == 'yes' or answer == 'y' or answer == 'Y' ):
    addr_ans = input('New Address - in AF_INET format, please: ')
    port_ans = input('New Port: ')
    server = httpProxyServer(host_name=addr_ans, port_num=int(port_ans))
    server.activateServer()
else:
    server = httpProxyServer()
    server.activateServer()