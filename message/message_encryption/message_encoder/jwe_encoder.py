from jwcrypto import jwk, jwe
import json
eprot = {'alg': "RSA-OAEP", 'enc': "A128CBC-HS256"}
stringPayload = u'attack at dawn'
E = jwe.JWE(stringPayload, json.dumps(eprot))
E.add_recipient("pubKey")
encrypted_token = E.serialize(compact=True)
E = jwe.JWE()
E.deserialize(encrypted_token, key="privKey")
decrypted_payload = E.payload