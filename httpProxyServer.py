import sys, socket, datetime

class httpProxyServer:
    
    def __init__(self, host_name='127.0.0.1', port_num=12346):
        
        self.hostName = host_name
        self.portNum = port_num
        
    def activateServer(self):
        
        try:
            
            print('Please make sure your browser/Wi-Fi is customized to work with this HTTP proxy')
            
            # Initiates a TCP process starting with an initialized socket
            self.servSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # Allows the socket to be re-used on the same address
            self.servSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            # Binds socket to public host and port
            self.servSock.bind((self.hostName, self.portNum))

            # Gets socket to listen for connections
            self.servSock.listen(10)
            
            print('Listening from {} on port {} '.format(self.hostName, self.portNum))

            # Permanently listens for connections
            while True:

                # Accepting a connection
                (connectSock, connectAddr) = self.servSock.accept()

                # Get request from browser 
                req = connectSock.recv(32768)
                
                parsedRequest = self.parse_request(req)
                
                returnInfo = socket.getaddrinfo(parsedRequest['SITE'], int(parsedRequest['PORT_NUM']))
                
                returnSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                returnSock.settimeout(600)
                returnSock.connect(returnInfo.pop()[4])
                returnSock.sendall(req)
                
                while True:
                    # recieves data from server, sends to client
                    temp = returnSock.recv(32768)
                    
                    if(len(temp) > 0):
                        connectSock.send(temp)
                    else:
                        break
                
                returnSock.close()
                connectSock.close()
            
                
            
        except KeyboardInterrupt:
            print('User has shut down proxy')
            sys.exit(0)
        except BrokenPipeError as e:
            print('Connection closed on the other side')
            pass
        except ConnectionRefusedError as e:
            print('Server was not available to connect with')
            pass
        except OSError as e:
            print('Could not connect to unidentified website: ', e)
            sys.exit(0)
        except Exception as e:
            print('Server connection failed because of: ', e)
            sys.exit(0)
        finally:
            sys.exit(0)
    
    def parse_request(self, request):
        
        parts = {}
        if(isinstance(request, bytes)):
            requestLine = (request.decode('utf-8')).split('\n')[0]
        else:
            requestLine = request.split('\n')[0]
        print(requestLine)
        requestLineParts = requestLine.split(' ')
        parts['REQUEST_TYPE'] = requestLineParts[0]
        if(len(requestLineParts) > 1):
            parts['VERSION'] = requestLineParts[2]
        else:
            parts['VERSION'] = 'Unknown'
        print('VERSION: {}'.format(parts['VERSION']))
    
        absoluterequestURI = requestLineParts[1]
        
        # Checking if URL begins with http:// or just the path
        httpBegin = absoluterequestURI.find("://")
                
        if(httpBegin == -1):
            path = absoluterequestURI
        else:
            path = absoluterequestURI[(httpBegin+3):]
            
        if('http' in path):
            path = path[:(path.index('http'))]
            
        if('/' in path):
            path = path[:(path.index('/'))]
        
        if(':' in path):
            parts['PORT_NUM'] = (path[path.index(':'):])[1:]
            parts['SITE'] = path[:(path.index(':'))]
        else:
            parts['PORT_NUM'] = '80'
            parts['SITE'] = path
            
        
        parts['TIME'] = str(datetime.datetime.now())
        
        print('REQUEST_TYPE: {}'.format(parts['REQUEST_TYPE']))
        print('PORT_NUM: {}'.format(parts['PORT_NUM']))
        print('SITE: {}'.format(parts['SITE']))
        print('TIME: {}'.format(parts['TIME']))
        
        
        return parts
        
        
        
            
        
        

            
            
        
        
        
        
        
    
    

