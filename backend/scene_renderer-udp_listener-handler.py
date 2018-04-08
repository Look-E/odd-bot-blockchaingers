# copy and paste server_dbg_py here and change the game_logic to refer to this text block for better performance?

#
# This script receives 3 doubles on port 21567
# sets them as global x,y,z coords of the cube
#

from bge import logic
from struct import pack,unpack
import pickle
import time

scene = logic.getCurrentScene()
car = scene.objects["car.001"]

try:
    data, client = logic.Sock.recvfrom(4096)
    d = pickle.loads(data)
    print(d)
    car.worldPosition[0] = d['x']
    car.worldPosition[1] = d['y']
#    car.worldPosition[2] = d['z']
    print(car.worldPosition)
    #time.sleep(0.1)
    
except:
    pass
   

# Send things back
# try:
#    data_back=pack('ddd',0.1,0.2,0.300001)
#    logic.Sock.sendto(data_back, client )
#
#except:
#    pass

