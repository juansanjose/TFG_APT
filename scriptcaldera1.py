from audioop import mul
from http import server
import sys
import shlex
import os
import json
import random
import time
import requests
f = open('windows.json')
loaded_json = json.load(f)
#print(loaded_json[1]['ability_id'])
abilities_id=[]
defense_evansion=[]
lateral_movement=[]
credential_access=[]
discovery=[]
command_and_controll=[]
collection=[]
multiple=[]
execution=[]
impact=[]

# curl -H "KEY:dwhuG3DiRYZJce17qNBDpvhw4pz0VrhSA6Ief5Iy6qQ" -X POST 192.168.100.100:8888/plugin/access/abilities -d '{"paw":"cwnlof"}'


# id= sys.argv[1]
# tactic=sys.argv[2]
id= "rsaerp" 
tactic="discovery"


def seleccionar_abilidades(x,abilidad):
        
        if x=='defense-evansion':
            defense_evansion.append(abilidad)
        elif x=='lateral-movement':
            lateral_movement.append(abilidad)
        elif x=='credential-access':
            credential_access.append(abilidad)
        elif x=='discovery':
            
            discovery.append(abilidad)
        elif x=='command-and-controll':
            command_and_controll.append(abilidad)
        elif x=='collection':
            collection.append(abilidad)
        elif x== 'multiple':
            multiple.append(abilidad)
            
        elif x=='execution':
            execution.append(abilidad)
        elif x=='impact':
            impact.append(abilidad)




for x in range(len(loaded_json)):
    abilities_id.append(loaded_json[int(x)]['ability_id'])
    seleccionar_abilidades(tactic,loaded_json[int(x)]['ability_id'])  


# Variables to keep track and display
Sec = 0
Min = 0
# Begin Process


        
       



# ip= "192.168.100.100:8888"
# key=sys.argv(1)

# argumento número de habilidades a ejecutar

# Execute a given ability against an agent, outside the scope of an operation.
# dwhuG3DiRYZJce17qNBDpvhw4pz0VrhSA6Ief5Iy6qQ red:4s4Z_7YzYQa2rI_0WZfyWRGUqNgbV4qp511kKzQEydc
# http://192.168.100.100:8888/
# curl -H "KEY:$API_KEY" -X POST localhost:8888/plugin/access/exploit -d '{"paw":"$PAW","ability_id":"$ABILITY_ID","obfuscator":"plain-text"}'
# curl -u red:4s4Z_7YzYQa2rI_0WZfyWRGUqNgbV4qp511kKzQEydc --basic -X POST 192.168.100.100:8888/plugin/access/exploit -d '{"paw":"$PAW","ability_id":"$ABILITY_ID","obfuscator":"plain-text"}' -K myconfig.txt

# conocer las habilides de un agente 
# curl -H "KEY:dwhuG3DiRYZJce17qNBDpvhw4pz0VrhSA6Ief5Iy6qQ" -X POST localhost:8888/plugin/access/abilities -d '{"paw":"$PAW"}'

# ejecutar habilidades
#curl -H "KEY:dwhuG3DiRYZJce17qNBDpvhw4pz0VrhSA6Ief5Iy6qQ" -X POST localhost:8888/plugin/access/exploit -d '{"paw": "liwxvk" ,"ability_id": "3ee7020bd7459eab27bae7e95e752e25","obfuscator":"plain-text"}'



def eligir_abilidad(abilities):
    ejecutable=random.choice(abilities)
    return ejecutable

set_abilidades=set()
def añadir_abilidades(x):
        if x=='defense-evansion':
            for i in range(10):
                set_abilidades.add(random.choice(defense_evansion))
        elif x=='lateral-movement':
                for i in range(10):
                    set_abilidades.add(random.choice(lateral_movement))
        elif x=='credential-access':
                for i in range(10):
                    set_abilidades.add(random.choice(credential_access))
        elif x=='discovery':
                for i in range(10):
                    set_abilidades.add(random.choice(discovery))
        elif x=='command-and-controll':
                for i in range(10):
                    set_abilidades.add(random.choice(command_and_controll))
        elif x=='collection':
                for i in range(10):
                    set_abilidades.add(random.choice(collection))
        elif x== 'multiple':
                for i in range(10):
                    set_abilidades.add(random.choice(execution))
        elif x=='impact':
                for i in range(10):
                    set_abilidades.add(random.choice(impact))
         
añadir_abilidades("discovery")
API_KEY = "dwhuG3DiRYZJce17qNBDpvhw4pz0VrhSA6Ief5Iy6qQ"
headers = {
    'KEY': "ADMIN123",

}


 
if __name__ == '__main__':
    for abilidad in set_abilidades:
        # print(abilidad)
        data = '{"paw": "%s" ,"ability_id": "%s","obfuscator":"plain-text"}' % (id, abilidad)
        response = requests.post('http://192.168.100.100:8888/plugin/access/exploit',  headers=headers, data=data)
        print(response.text)
        time.sleep(1)   
    # data = '{"paw":"%s","ability_id":"ccdb8caf-c69e-424b-b930-551969450c57","obfuscator":"plain-text"}' % (id)
    # response = requests.post('http://192.168.100.100:8888/plugin/access/exploit',  headers=headers, data=data)
    # print(response.text)




    # abilidad_random=eligir_abilidad(abilities_id)
    # print(abilidad_random)
    # data = '{"paw":" %s" ,"ability_id":" %s","obfuscator":"plain-text"}' % (id, abilidad_random)
    # response = requests.post('http://192.168.100.100:8888/plugin/access/exploit',  headers=headers, data=data)
    # print(response.text)
    # while True:
    #     Sec += 1
    #     time.sleep(1)
    #     if Sec == 30:
    #         Sec = 0
    #         abilidad_random=eligir_abilidad(abilities_id)
    #         print(abilidad_random)
    #         data = '{"paw":" %s" ,"ability_id":" %s","obfuscator":"plain-text"}' % (id, abilidad_random)
    #         response = requests.post('http://192.168.100.100:8888/plugin/access/exploit',  headers=headers, data=data)

    #         print(response.text)
  




