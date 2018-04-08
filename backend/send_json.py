import sys
import json
#import socket
from time import sleep

# Revision list
# * Added large payload support

#print("Hello from scene_udp_sender.")    

# create the UDP socket
#sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    
#def _send_json (json_data, host, port, NAX_UDP_SIZE=1460):    
def _send_json (json_data, sock, NAX_UDP_SIZE=1460):    
    if (len(json_data) > NAX_UDP_SIZE):        
        print("ERROR: UDP data payload too big")
        return
        
    #print ("DEBUG: Sending out:", json_data)
    #return
    
    #sock.setblocking(1)
    #sock.sendto(bytes(json_data, 'utf8'))#, (host,int(port)))
    sock.send(bytes(json_data, 'utf8'))#, (host,int(port)))
   
#def send_json (json_data, host, port, MAX_UDP_SIZE=1460, CHUNK_SIZE=1024):    
def send_json (json_data, sock, MAX_UDP_SIZE=1460, CHUNK_SIZE=1024):    
    # Check size
    if (len(json_data)<MAX_UDP_SIZE):
        #print ("DEBUG: Sending one chunk and one chunk only")
        _send_json (json_data, sock)         
        return
        
    # print ("DEBUG: json_data is to large, splitting it up")
    
    # convert to dictionary
    scene_data = json.loads(json_data)
        
    # extract mode
    mode = ""
    if 'mode' in scene_data:
        mode = scene_data['mode']
        del scene_data['mode']
      
    # pass the mode into the first chunk
    tmp_dict = dict()   
    tmp_dict['mode']=mode
    # Prevent we delete the scene when sending the next chunk
    if (mode=="create_scene"):
        # print ("DEBUG: changing mode for next chunk into change_scene")
        mode="change_scene"                
                
    # iterate accross objects
    for object_name, object_data in scene_data.items() :    
        # print ("object_name =", object_name);
        # print ("object_data =", object_data);    
        
        json_data = json.dumps(tmp_dict)
        if (len(json_data) > CHUNK_SIZE):            
            _send_json (json_data, sock)
            tmp_dict = dict()    
            tmp_dict['mode']=mode
        
        tmp_dict[object_name]=object_data

    if (len(tmp_dict) > 0):
        # print ("Wrapping up, sending last chunk")
        json_data = json.dumps(tmp_dict)
        
        _send_json (json_data, sock)#, host, port)    
    # else:
    #    print ("Wrapping up, nothing to send")
    
def test1():
    print("Hello from Test1")
    json_data = """
    {
      "car.001": {
        "type": "car",
        "loc": {
          "y": 0.0,
          "z": 0.0,
          "x": 0.0
        },
        "rot": {
          "y": 0.0,
          "z": 0.0,
          "x": 0.0
        }
      }
    }
    """
    print ("subtest A")
    send_json(json_data, addr)   
    print ("subtest B")
    send_json(json_data, addr, 1, 32)
    
def test2():
    print("Hello from Test2")
  
    json_data = """
    {
      "mode": "create_scene",
      "car.001": {      
        "type": "car",
        "loc": {
          "y": 0.0,
          "z": 0.0,
          "x": 0.0
        },
        "rot": {
          "y": 0.0,
          "z": 0.0,
          "x": 0.0
        }
      },
      "car.002": {      
        "type": "car",
        "loc": {
          "y": 0.0,
          "z": 0.0,
          "x": 0.0
        },
        "rot": {
          "y": 0.0,
          "z": 0.0,
          "x": 0.0
        }
      }
    }
    """
    
    print ("subtest A")
    send_json(json_data, addr)
    
    print ("subtest B")    
    send_json(json_data, addr, 1, 32)
    
def main():
  host = "127.0.0.1"
  port = 10000
  
  if (len(sys.argv) < 2):
    print("Usage: send_json.py filename [target] [port]")
    return
  
  if (len(sys.argv) >= 2):  
    filename = sys.argv[1]

  if (len(sys.argv) >= 3):  
    host = sys.argv[2]

  if (len(sys.argv) >= 4):  
    port = sys.argv[3]

  print("Sending {0} to {1}:{2}".format(filename, host, port))
  
  fh = open(sys.argv[1], 'rb')
  json_data=fh.read() 
      
  #print ("DEBUG: file contents: ", json_data)  
  send_json (str(json_data, 'UTF-8'), host,port)

# test1()
# test2()
  
#main()

    