import json
import copy
from utils.chatstore import *

class Historical_Data():
    def __init__(self,session_id):
        self.session_id = session_id
        self.data = GetChat(session_id)

    def get_history_strings(self):
        output=[]
        if self.data is not None:
            for message_list in self.data:
                for message in message_list:
                    output.append(message.get('Message'))
                    output.append(message.get('Response'))
        return output

    def store_history(self,session_id,Message,Response):
        SaveChat(session_id,Message,Response)
    
