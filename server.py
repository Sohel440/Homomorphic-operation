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
import zlib
from multiprocessing import Pool
import dataset

# Cache for pre-encrypted Paillier datasets per public key
paillier_dataset_cache = {}
# Cache for TenSEAL context to avoid resending
context_cache = {}

def encrypt_value(pub_key, val):
    return pub_key.encrypt(val)

def pre_encrypt_dataset(pub_key):
    pub_key_n = pub_key.n
    if pub_key_n in paillier_dataset_cache:
        print(f"Using cached pre-encrypted dataset for public key n={pub_key_n}")
        return paillier_dataset_cache[pub_key_n]
    
    encrypt_start = time.time()
    with Pool() as pool:
        encrypted_dataset = pool.starmap(encrypt_value, [(pub_key, val) for val in dataset.array_dataset])
    paillier_dataset_cache[pub_key_n] = encrypted_dataset
    print(f"Pre-encrypted dataset with {len(dataset.array_dataset)} elements | Time taken: {time.time() - encrypt_start:.4f} seconds")
    return encrypted_dataset

def compute_op(enc_server_val, enc_client_val, operation):
    if operation == 'add':
        res = enc_server_val + enc_client_val
    elif operation == 'subtract':
        res = enc_server_val - enc_client_val
    elif operation == 'membership':
        res = enc_server_val - enc_client_val
    return {'ciphertext': res.ciphertext(), 'exponent': res.exponent}

def send_data_in_chunks(conn, data, chunk_size=8192):
    try:
        start_time = time.time()
        serialized_data = zlib.compress(pickle.dumps(data))
        data_size = len(serialized_data)
        
        print(f"Sending data of size: {data_size} bytes (compressed)")
        
        conn.sendall(data_size.to_bytes(8, byteorder='big'))
        
        for i in range(0, data_size, chunk_size):
            chunk = serialized_data[i:i + chunk_size]
            conn.sendall(chunk)
            print(f"Sent {min(i + chunk_size, data_size)}/{data_size} bytes | Time elapsed: {time.time() - start_time:.4f} seconds")
        
        print(f"Total time to send data: {time.time() - start_time:.4f} seconds")
    except ConnectionAbortedError as e:
        print(f"Connection aborted while sending data: {e}")
        raise
    except Exception as e:
        print(f"Error sending data: {e}")
        raise

def receive_full_data(conn):
    try:
        conn.settimeout(600.0)
        start_time = time.time()
        
        size_data = b""
        while len(size_data) < 8:
            chunk = conn.recv(8 - len(size_data))
            if not chunk:
                raise ConnectionError("Connection closed while receiving data size")
            size_data += chunk
        data_size = int.from_bytes(size_data, byteorder='big')
        print(f"Expected data size: {data_size} bytes | Time taken to receive size: {time.time() - start_time:.4f} seconds")
        
        buffer = b""
        while len(buffer) < data_size:
            chunk = conn.recv(min(8192, data_size - len(buffer)))
            if not chunk:
                raise ConnectionError("Connection closed while receiving data")
            buffer += chunk
            print(f"Received {len(buffer)}/{data_size} bytes | Time elapsed: {time.time() - start_time:.4f} seconds")
        
        print(f"Total time to receive data: {time.time() - start_time:.4f} seconds")
        return pickle.loads(zlib.decompress(buffer))
    except socket.timeout:
        print("Socket timeout while receiving data")
        raise
    except Exception as e:
        print(f"Error receiving data: {e}")
        raise

def handle_client(conn):
    global context_cache
    start_time = time.time()
    operation = "unknown"
    scheme = "unknown"
    try:
        print("Receiving data from client...")
        encrypted_data = receive_full_data(conn)

        operation = encrypted_data['operation']
        scheme = encrypted_data['scheme']

        results = []

        print(f"Operation: {operation} | Scheme: {scheme}")

        server_dataset_dot = np.array([[73, 0.5, 8, 7, 5, 1],
                                      [81, -5, 66, 3, 4, 2],
                                      [-100, -78, -2, 2, 8, 3],
                                      [0, 9, 17, 9, 12, 4],
                                      [69, 11, 10, 7, 5, 5],
                                      [69, 13, 10, 7, 5, 6]])
        
        server_dataset_matmul = np.array([[73, 0.5, 8, 7, 5, 1],
                                         [81, -5, 66, 3, 4, 2],
                                         [-100, -78, -2, 2, 8, 3],
                                         [0, 9, 17, 9, 12, 4],
                                         [69, 11, 10, 7, 5, 5],
                                         [69, 13, 10, 7, 5, 6]])

        computation_start = time.time()
        if scheme == 'paillier':
            pub_key = paillier.PaillierPublicKey(n=encrypted_data['public_key']['n'])
            enc_client_val = paillier.EncryptedNumber(pub_key,
                                                      encrypted_data['encrypted_client_value']['ciphertext'],
                                                      encrypted_data['encrypted_client_value']['exponent'])
            
            encrypted_server_dataset = pre_encrypt_dataset(pub_key)

            operation_start = time.time()
            if operation in ['add', 'subtract', 'membership']:
                with Pool() as pool:
                    results = pool.starmap(compute_op, [(enc_server_val, enc_client_val, operation) for enc_server_val in encrypted_server_dataset])
            else:
                raise ValueError(f"Unsupported operation '{operation}' for Paillier")
            print(f"Time for Paillier operation '{operation}': {time.time() - operation_start:.4f} seconds")

        else:
            context_hash = hash(str(encrypted_data['context']))
            if context_hash in context_cache:
                context = context_cache[context_hash]
            else:
                context = ts.context_from(encrypted_data['context'])
                context_cache[context_hash] = context

            if operation in ['add', 'subtract', 'multiply']:
                enc_client_vals = [
                    ts.ckks_vector_from(context, val) if scheme == 'ckks' else ts.bfv_vector_from(context, val)
                    for val in encrypted_data['encrypted_client_values']
                ]
                array_dataset = dataset.ckks_normal_array if scheme == 'ckks' else dataset.bfv_normal_array
                
                for enc_client_val in enc_client_vals:
                    op_results = []
                    for val in array_dataset:
                        enc_val = ts.ckks_vector(context, [val]) if scheme == 'ckks' else ts.bfv_vector(context, [val])
                        if operation == 'add':
                            res = enc_client_val + enc_val
                        elif operation == 'subtract':
                            res = enc_val - enc_client_val
                        elif operation == 'multiply':
                            res = enc_client_val * enc_val
                        op_results.append(res.serialize())
                    results.append(op_results)
            elif operation in ['divide', 'percentage']:
                enc_client_val = ts.ckks_vector_from(context, encrypted_data['encrypted_client_value']) \
                    if scheme == 'ckks' else ts.bfv_vector_from(context, encrypted_data['encrypted_client_value'])

                array_dataset = dataset.ckks_normal_array if scheme == 'ckks' else dataset.bfv_normal_array
                
                for val in array_dataset:
                    enc_val = ts.ckks_vector(context, [val]) if scheme == 'ckks' else ts.bfv_vector(context, [val])
                    res = enc_val * enc_client_val
                    results.append(res.serialize())
                    
            elif operation in ['square', 'cube']:
                enc_client_vals = ts.ckks_vector_from(context, encrypted_data['encrypted_client_value']) \
                    if scheme == 'ckks' else ts.bfv_vector_from(context, encrypted_data['encrypted_client_value'])

                if operation == 'square':
                    res = enc_client_vals * enc_client_vals
                elif operation == 'cube':
                    square = enc_client_vals * enc_client_vals
                    res = square * enc_client_vals
                results.append(res.serialize())
                    
            elif operation == "membership" and scheme == "bfv":
                enc_client_val = ts.bfv_vector_from(context, encrypted_data['encrypted_client_value'])
                array_dataset = dataset.bfv_membership_array
                for val in array_dataset:
                    enc_val = ts.bfv_vector(context, [val])
                    res = enc_val - enc_client_val
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

            print(f"Time for {scheme} operation '{operation}': {time.time() - computation_start:.4f} seconds")

        print(f"Total computation time for operation '{operation}' using '{scheme}' scheme: {time.time() - computation_start:.4f} seconds")

        send_data_in_chunks(conn, {'results': results})
        print("Results sent to client.")

    except Exception as e:
        print(f"Error: {e}")
        try:
            send_data_in_chunks(conn, {'error': str(e)})
        except:
            pass
    finally:
        execution_time = time.time() - start_time
        print(f"Total execution time for operation '{operation}' using '{scheme}' scheme: {execution_time:.4f} seconds")
        conn.close()

def main():
    HOST, PORT = '127.0.0.1', 12345
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1024 * 1024)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1024 * 1024)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        if hasattr(socket, 'TCP_KEEPIDLE'):
            s.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 10)
            s.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 5)
            s.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 3)
        
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server is running on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            conn.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 2* 1024 * 1024)
            conn.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 2* 1024 * 1024)
            conn.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            if hasattr(socket, 'TCP_KEEPIDLE'):
                conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 5)
                conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 2)
                conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 5)
            
            print("Connected by", addr)
            handle_client(conn)

if __name__ == "__main__":
    main()
