from message.message_encryption.message_decoder.message_decoder import MessageDecoder
from jwcrypto import jwk, jwe
from jwcrypto.common import json_decode


class RSADecoder(MessageDecoder):
    def decode(self, payload): 
        private_key = jwk.JWK.from_json(open('.secret_code', 'rb').read()) 
        jwe_token = jwe.JWE()
        jwe_token.deserialize(payload, private_key)
        payload = jwe_token.payload
        print(payload)

        