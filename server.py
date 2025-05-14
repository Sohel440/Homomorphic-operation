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
# Pre-encrypted dataset for Paillier (will be populated on first request)
pre_encrypted_dataset = None
# Dataset with 1050 elements (1000 to 2049)
# array_dataset = [1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52 , 1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52 , 1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 1007, 1015, 1016, 1017, 1018, 1019, 52,1004, 1005, 1006, 100]  # 1050 elements: [1000, 1001, ..., 2049]

def encrypt_value(pub_key, val):
    return pub_key.encrypt(val)

def pre_encrypt_dataset(pub_key):
    global pre_encrypted_dataset
    encrypt_start = time.time()
    with Pool() as pool:
        pre_encrypted_dataset = pool.starmap(encrypt_value, [(pub_key, val) for val in dataset.array_dataset])
    print(f"Pre-encrypted dataset with {len(dataset.array_dataset)} elements | Time taken: {time.time() - encrypt_start:.4f} seconds")

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
        # Compress and serialize the data
        serialized_data = zlib.compress(pickle.dumps(data))
        data_size = len(serialized_data)
        
        print(f"Sending data of size: {data_size} bytes (compressed)")
        
        # Send the size of the data first (as a fixed-length 8-byte integer)
        conn.sendall(data_size.to_bytes(8, byteorder='big'))
        
        # Send the data in chunks
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
        # Receive the data size (8 bytes)
        conn.settimeout(120.0)  # Timeout for receiving data
        start_time = time.time()
        
        size_data = b""
        while len(size_data) < 8:
            chunk = conn.recv(8 - len(size_data))
            if not chunk:
                raise ConnectionError("Connection closed while receiving data size")
            size_data += chunk
        data_size = int.from_bytes(size_data, byteorder='big')
        print(f"Expected data size: {data_size} bytes | Time taken to receive size: {time.time() - start_time:.4f} seconds")
        
        # Receive the actual data
        buffer = b""
        while len(buffer) < data_size:
            chunk = conn.recv(min(8192, data_size - len(buffer)))
            if not chunk:
                raise ConnectionError("Connection closed while receiving data")
            buffer += chunk
            print(f"Received {len(buffer)}/{data_size} bytes | Time elapsed: {time.time() - start_time:.4f} seconds")
        
        print(f"Total time to receive data: {time.time() - start_time:.4f} seconds")
        return buffer
    except socket.timeout:
        print("Socket timeout while receiving data")
        raise
    except Exception as e:
        print(f"Error receiving data: {e}")
        raise

def handle_client(conn):
    global pre_encrypted_dataset
    start_time = time.time()
    # Initialize operation and scheme to avoid UnboundLocalError
    operation = "unknown"
    scheme = "unknown"
    try:
        print("Receiving data from client...")
        data = receive_full_data(conn)
        encrypted_data = pickle.loads(data)

        operation = encrypted_data['operation']
        scheme = encrypted_data['scheme']

        results = []

        print(f"Operation: {operation} | Scheme: {scheme}")

        # Fixed datasets
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
            # Handle Paillier
            pub_key = paillier.PaillierPublicKey(n=encrypted_data['public_key']['n'])
            enc_client_val = paillier.EncryptedNumber(pub_key,
                                                      encrypted_data['encrypted_client_value']['ciphertext'],
                                                      encrypted_data['encrypted_client_value']['exponent'])
            
            # Pre-encrypt dataset if not already done
            if pre_encrypted_dataset is None:
                pre_encrypt_dataset(pub_key)
            encrypted_server_dataset = pre_encrypted_dataset

            operation_start = time.time()
            if operation in ['add', 'subtract', 'membership']:
                # Parallelize Paillier operations
                with Pool() as pool:
                    results = pool.starmap(compute_op, [(enc_server_val, enc_client_val, operation) for enc_server_val in encrypted_server_dataset])
            else:
                raise ValueError(f"Unsupported operation '{operation}' for Paillier")
            print(f"Time for Paillier operation '{operation}': {time.time() - operation_start:.4f} seconds")

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
                    
            elif operation == "membership" and scheme =="bfv":
                enc_client_val = ts.bfv_vector_from(context, encrypted_data['encrypted_client_value'])
                array_dataset = dataset.array_dataset
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

        print(f"Total computation time for operation '{operation}' using '{scheme}' scheme: {time.time() - computation_start:.4f} seconds")

        # Send results back
        send_data_in_chunks(conn, {'results': results})
        print("Results sent to client.")

    except Exception as e:
        print("Error:", e)
    finally:
        execution_time = time.time() - start_time
        print(f"Total execution time for operation '{operation}' using '{scheme}' scheme: {execution_time:.4f} seconds")
        conn.close()

def main():
    HOST, PORT = '127.0.0.1', 12345
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Set socket options
        s.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1024 * 1024)  # 1MB receive buffer
        s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1024 * 1024)  # 1MB send buffer
        s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)  # Enable TCP keep-alive
        
        # Platform-specific keep-alive settings
        if hasattr(socket, 'TCP_KEEPIDLE'):
            s.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 10)  # Start keep-alive after 10 seconds
            s.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 5)  # Send keep-alive every 5 seconds
            s.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 3)   # Allow 3 failed probes
        
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server is running on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            # Apply socket options to the connection socket
            conn.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1024 * 1024)
            conn.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1024 * 1024)
            conn.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            if hasattr(socket, 'TCP_KEEPIDLE'):
                conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 10)
                conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 5)
                conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 3)
            
            print("Connected by", addr)
            handle_client(conn)

if __name__ == "__main__":
    main()
