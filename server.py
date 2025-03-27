
import socket
import pickle
import tenseal as ts

def receive_full_data(conn):
    buffer = b""
    while True:
        data = conn.recv(4096)
        if not data:
            break
        buffer += data
    return buffer

def handle_client(conn):
    try:
        print("Receiving data from client...")
        data = receive_full_data(conn)
        encrypted_data = pickle.loads(data)

        context = ts.context_from(encrypted_data['context'])
        encrypted_client_value = ts.ckks_vector_from(context, encrypted_data['encrypted_client_value'])
        operation = encrypted_data['operation']

        print(f"\n[Server] Performing homomorphic {operation} operation...")

        server_dataset = [10, 20, 30, 40, 50]
        encrypted_server_dataset = [ts.ckks_vector(context, [value]) for value in server_dataset]

        results = []
        for encrypted_server_value in encrypted_server_dataset:
            if operation == 'add':
                result = encrypted_client_value + encrypted_server_value
            elif operation == 'subtract':
                result = encrypted_server_value - encrypted_client_value
            elif operation == 'multiply':
                result = encrypted_client_value * encrypted_server_value
            elif operation == 'divide':
                result = encrypted_server_value * encrypted_client_value  # Using multiplication
            elif operation == 'square':
                    result = encrypted_server_value * encrypted_server_value
            elif operation == 'percentage':
                    result = encrypted_server_value * encrypted_client_value
            else:
                raise ValueError("Unknown operation")
            
            results.append(result.serialize())

        result_data = {'encrypted_results': results}
        conn.sendall(pickle.dumps(result_data))
        print("Results sent back to client.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

def main():
    HOST = '127.0.0.1'
    PORT = 12345
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server is listening on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            print(f"Connected by {addr}")
            handle_client(conn)

if __name__ == "__main__":
    main()
