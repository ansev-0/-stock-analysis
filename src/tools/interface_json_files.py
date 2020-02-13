import json
import os

class JsonResponseFiles:
    
    def __init__(self,path=''):
        self.path = path
        
    def read(self,name):
        file=open(self.path+name, "r")
        json_file = file.read()
        file.close()
        return json.loads(json_file)
        
    def write(self,json_file,name):
        file=open(self.path+name, 'w')
        json_file= json.dumps(json_file)
        file.write(json_file)
        file.close()
        
    def delete(self, name):
        os.remove(self.path + name)

