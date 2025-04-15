# ******************* Server Side ******************* #
# operation: 1. Addition 2. subtraction 3.Multiplication 4.divition 5.fraction 6.square 7.Cube 8.percentage 9. mat mul
import socket
import pickle
import tenseal as ts
from phe import paillier
import numpy as np

def receive_full_data(conn):
    buffer = b""
    conn.settimeout(5.0)
    while True:
        try:
            data = conn.recv(4096)
            if not data:
                break
            buffer += data
        except socket.timeout:
            break
    return buffer

def handle_client(conn):
    try:
        print("Receiving data from client...")
        data = receive_full_data(conn)
        encrypted_data = pickle.loads(data)

        operation = encrypted_data['operation']
        scheme = encrypted_data['scheme']

        # Default dataset for dot product
        server_dataset = np.array([[1.0, 2.0], [3.0, 4.0]])

        results = []
       
        if scheme == 'paillier':
            array_dataset = [1000, 1002]
        elif scheme == 'bfv':
            array_dataset = [1000,2002]
        elif scheme == 'ckks':
            array_dataset= [122,90]

        if operation in ['add', 'subtract']:
            pub_key = paillier.PaillierPublicKey(n=encrypted_data['public_key']['n'])
            enc_client_val = paillier.EncryptedNumber(pub_key,
                                                      encrypted_data['encrypted_client_value']['ciphertext'],
                                                      encrypted_data['encrypted_client_value']['exponent'])
            encrypted_server_dataset = [pub_key.encrypt(val) for val in array_dataset]
            for enc_server_val in encrypted_server_dataset:
                res = enc_server_val + enc_client_val if operation == 'add' else enc_server_val - enc_client_val
                results.append({'ciphertext': res.ciphertext(), 'exponent': res.exponent})

        else:
            context = ts.context_from(encrypted_data['context'])

            if operation == "dot":
                # Decrypt client tensor and do dot product
                enc_client_tensor = ts.ckks_tensor_from(context, encrypted_data['encrypted_tensor'])
                server_tensor = ts.ckks_tensor(context, server_dataset)

                res_tensor = enc_client_tensor.dot(server_tensor)
                results = [res_tensor.serialize()]

            else:
                enc_client_val = ts.ckks_vector_from(context, encrypted_data['encrypted_client_value']) \
                    if scheme == 'ckks' else ts.bfv_vector_from(context, encrypted_data['encrypted_client_value'])

                

                for val in array_dataset:
                    enc_val = ts.ckks_vector(context, [val]) if scheme == 'ckks' else ts.bfv_vector(context, [val])
                    if operation == 'multiply':
                        res = enc_client_val * enc_val
                    elif operation == 'divide':
                        res = enc_val * enc_client_val
                    elif operation == 'square':
                        res = enc_val * enc_val
                    elif operation == 'cube':
                        res = enc_val **3
                    elif operation == 'percentage':
                        res = enc_val * enc_client_val
                    results.append(res.serialize())

        conn.sendall(pickle.dumps({'results': results}))
        print("Results sent to client.")

    except Exception as e:
        print("Error:", e)
    finally:
        conn.close()

def main():
    HOST, PORT = '127.0.0.1', 12345
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server is running on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            print("Connected by", addr)
            handle_client(conn)

if __name__ == "__main__":
    main()
