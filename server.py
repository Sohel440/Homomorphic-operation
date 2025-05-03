# server.py
# ******************* Server Side ******************* #
# operation: 1. Addition 2. subtraction 3.Multiplication 4.divition 5.fraction 6.square 7.Cube 8.percentage 9. dot product 10. membership check 11. Matrix Multiplication
# ----------------------------------------------------------------------------------------------------------------------
import socket
import pickle
import tenseal as ts
from phe import paillier
import numpy as np
import time

# 1x5 5x3

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
    start_time = time.time()
    try:
        print("Receiving data from client...")
        data = receive_full_data(conn)
        encrypted_data = pickle.loads(data)

        operation = encrypted_data['operation']
        scheme = encrypted_data['scheme']

        results = []

        print(f"Operation: {operation} | Scheme: {scheme}")

        # Fixed datasets
        server_dataset_dot = np.array([[1.0, 2.0], [3.0, 4.0]])
        server_dataset_matmul = np.array([[73, 0.5, 8],
                                          [81, -5, 66],
                                          [-100, -78, -2], 
                                          [0, 9, 17], 
                                          [69, 11, 10]])

        if scheme == 'paillier':
            # Handle Paillier separately
            pub_key = paillier.PaillierPublicKey(n=encrypted_data['public_key']['n'])
            enc_client_val = paillier.EncryptedNumber(pub_key,
                                                      encrypted_data['encrypted_client_value']['ciphertext'],
                                                      encrypted_data['encrypted_client_value']['exponent'])
            array_dataset =  [1004,1005,1006,1007,1015,1016,1017,1018,1019,52,1053,1054,1055,1056,1057,1058,1059,1060,1061,1062,1063,1064,1065,1066,1067,1068,1069,1070,1071,1072,1073,1074,1075,1076,1077,1084,1085,1086,1087,1131,1132,1133,1134,1135]  
            encrypted_server_dataset = [pub_key.encrypt(val) for val in array_dataset]

            if operation in ['add', 'subtract']:
                for enc_server_val in encrypted_server_dataset:
                    if operation == 'add':
                        res = enc_server_val + enc_client_val
                    elif operation == 'subtract':
                        res = enc_server_val - enc_client_val
                    results.append({'ciphertext': res.ciphertext(), 'exponent': res.exponent})

            elif operation == "membership":
                for enc_server_val in encrypted_server_dataset:
                    enc_diff = enc_server_val - enc_client_val
                    results.append({'ciphertext': enc_diff.ciphertext(), 'exponent': enc_diff.exponent})
            else:
                raise ValueError(f"Unsupported operation '{operation}' for Paillier")

        else:
            # Handle BFV/CKKS
            context = ts.context_from(encrypted_data['context'])

            if operation in ['add', 'subtract', 'multiply', 'divide', 'square', 'cube', 'percentage']:
                enc_client_val = ts.ckks_vector_from(context, encrypted_data['encrypted_client_value']) \
                    if scheme == 'ckks' else ts.bfv_vector_from(context, encrypted_data['encrypted_client_value'])

                array_dataset = [122, 90] if scheme == 'ckks' else [12, 24]

                for val in array_dataset:
                    enc_val = ts.ckks_vector(context, [val]) if scheme == 'ckks' else ts.bfv_vector(context, [val])
                    if operation == 'add':
                        res = enc_client_val + enc_val
                    elif operation == 'subtract':
                        res = enc_val - enc_client_val
                    elif operation == 'multiply':
                        res = enc_client_val * enc_val
                    elif operation == 'divide':
                        res = enc_val * enc_client_val  # because client sends 1/x
                    elif operation == 'square':
                        res = enc_val * enc_val
                    elif operation == 'cube':
                        if scheme == 'ckks':
                            squared = enc_val * enc_val
                            squared = ts.ckks_vector_from(context, squared.serialize())
                            res = squared * enc_val
                        else:
                            res = enc_val * enc_val * enc_val
                    elif operation == 'percentage':
                        res = enc_val * enc_client_val
                    else:
                        raise ValueError(f"Unsupported operation '{operation}' for {scheme}")

                    results.append(res.serialize())

            elif operation == "dot":
                enc_client_tensor = ts.ckks_tensor_from(context, encrypted_data['encrypted_tensor']) \
                    if scheme == 'ckks' else ts.bfv_tensor_from(context, encrypted_data['encrypted_tensor'])

                if enc_client_tensor.shape[1] != server_dataset_dot.shape[0]:
                    raise ValueError("Matrix dimensions for dot product do not match.")

                server_tensor = ts.ckks_tensor(context, server_dataset_dot) if scheme == 'ckks' \
                    else ts.bfv_tensor(context, server_dataset_dot)

                res_tensor = enc_client_tensor.dot(server_tensor)
                results = [res_tensor.serialize()]

            elif operation == "matmul":
                enc_client_tensor = ts.ckks_tensor_from(context, encrypted_data['encrypted_tensor']) \
                    if scheme == 'ckks' else ts.bfv_tensor_from(context, encrypted_data['encrypted_tensor'])

                if enc_client_tensor.shape[1] != server_dataset_matmul.shape[0]:
                    raise ValueError("Matrix dimensions for matrix multiplication do not match.")

                server_tensor = ts.ckks_tensor(context, server_dataset_matmul) if scheme == 'ckks' \
                    else ts.bfv_tensor(context, server_dataset_matmul)

                res_tensor = enc_client_tensor.mm(server_tensor)
                results = [res_tensor.serialize()]

            else:
                raise ValueError(f"Unsupported operation '{operation}' for {scheme}")

        # Send results back
        conn.sendall(pickle.dumps({'results': results}))
        print("Results sent to client.")

    except Exception as e:
        print("Error:", e)
    finally:
        execution_time = time.time() - start_time
        print(f"Execution time for operation '{operation}' using '{scheme}' scheme: {execution_time:.4f} seconds")
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

