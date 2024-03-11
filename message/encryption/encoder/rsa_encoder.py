from jwcrypto import jwk, jwe
from jwcrypto.common import json_decode

from message.message_encryption.message_encoder. message_encoder import  MessageEncoder


class RSAEncoder( MessageEncoder):
    def encode(self,content):
        public_key = jwk.JWK()
        private_key = jwk.JWK.from_json(open('../.secret_code', 'rb').read())
        public_key.import_key(**json_decode(private_key.export_public()))
        protected_header = {
            "alg": "RSA-OAEP-256",
            "enc": "A256CBC-HS512",
            "typ": "JWE",
            "kid": public_key.thumbprint(),
        }
        jwe_token = jwe.JWE(content.encode('utf-8'),
                           recipient=public_key,
                           protected=protected_header)
        enc = jwe_token.serialize()
        return enc

