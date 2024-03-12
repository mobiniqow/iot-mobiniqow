import ast
import json
from pathlib import Path

from jwcrypto import jwk, jwe

from ..decoder.decoder import Decoder


class RSADecoder(Decoder):
    def decode(self, payload):
        BASE_DIR = Path(__file__).resolve().parent.parent
        payload = payload.decode("utf-8")
        payload = json.loads(payload)
        private_key = jwk.JWK.from_json(open(BASE_DIR / '.secret_code', 'r').read())
        jwe_token = jwe.JWE()
        jwe_token.deserialize( payload , private_key)
        decrypted_payload = jwe_token.payload.decode("utf-8")
        decrypted_payload = decrypted_payload.replace("'", '"')
        return ast.literal_eval(decrypted_payload)
