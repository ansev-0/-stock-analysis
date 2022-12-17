import json

class GetCredentials:
    
    def __call__(self):
        with open("filestore/credentials/openai/token.json") as f:
            token = json.load(f)["token"]
        return token