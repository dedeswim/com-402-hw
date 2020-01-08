# The implementation of the mock privacy-preserving Prediction-as-a-Service server, respond to model evaluation request with prediction score.
from flask import Flask, request, jsonify
from phe import paillier


app = Flask(__name__)

model_coeffs = [0.13526855, 0.02712842, 0.18588048, 0.0145351 , 0.05692263,
                0.10989505, 0.16611514, 0.04010465, 0.05390962, 0.15565836]
model_bias = 0.05458201
precision = 2**(-16)

ERR_BAD_ENCODING = "Bad request encoding"
ERR_NO_PUB_KEY = "No public key sent"
ERR_NO_INPUT = "No input provided"
ERR_BAD_DIM = "Wrong input vector dimension"
ERR_ATTACK_DETECT = "Weird query... Potential attempt to steal the model detected: repeated input ciphertexts."
ERR_BAD_PK = "Public key is incorrect or incorrectly formatted"
ERR_BAD_IN = "Input ciphertext vector is incorrect or incorrectly formatted"


@app.route("/prediction", methods=['POST'])
def prediction():
    try:
        query = request.json if request.method == "POST" and request.json else {}
        cipher = query.get("enc_feature_vector")
        pk_n = query.get("pub_key_n")
    except:
        return ERR_BAD_ENCODING, 400

    if pk_n is None:
        return ERR_NO_PUB_KEY, 400

    if cipher is None:
        return ERR_NO_INPUT, 400

    if not isinstance(cipher, list) or len(cipher) != len(model_coeffs):
        return ERR_BAD_DIM, 400

    if len(set(cipher)) <= 2:
        return ERR_ATTACK_DETECT, 403
    
    try:
        pk = paillier.PaillierPublicKey(pk_n)
        model_coeffs_enc =  [paillier.EncodedNumber.encode(pk, coeff, precision=precision) for coeff in model_coeffs]
        model_bias_enc = paillier.EncodedNumber.encode(pk, model_bias, precision=precision)
    except:
        return ERR_BAD_PK, 400

    try:
        cts = []
        for ct in cipher:
            if not isinstance(ct, int) or ct < 0 or ct > pk.nsquare:
                raise
            cts += [paillier.EncryptedNumber(pk, ct, -4)] 
        cres = sum((ct*coeff for (ct, coeff) in zip(cts, model_coeffs_enc))) + model_bias_enc
        ctres = cres.ciphertext()
    except:
        return ERR_BAD_IN, 400

    return_dict = {
        "enc_prediction": ctres
    }

    return jsonify(return_dict), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)