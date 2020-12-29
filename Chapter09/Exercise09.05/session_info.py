import base64
import json
import pprint
import sys

def get_session_dictionary(session_key):
    binary_key, payload = base64.b64decode(session_key).split(b':', 1)
    session_dictionary = json.loads(payload.decode())
    return session_dictionary

if __name__ == '__main__':
    if len(sys.argv)>1:
        session_key = sys.argv[1]
        session_dictionary = get_session_dictionary(session_key)
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(session_dictionary)
