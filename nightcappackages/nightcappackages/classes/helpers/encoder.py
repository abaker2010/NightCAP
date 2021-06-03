
import json
from typing import Any
from bson import json_util
from bson.objectid import ObjectId

class NightcapJSONEncoder(json.JSONEncoder):

    def encode(self, o: Any) -> str:
        # return super().encode(o)
        return json.dumps(json_util.dumps(o))

    
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        # return json.JSONEncoder.default(self, o)
        # def parse_json(data):
        return  json.loads(json_util.loads(o))
