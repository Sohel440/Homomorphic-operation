# *******************server side program*******************#
# operation: 1. Addition 2. subtraction 3.Multiplication 4.divition 5.fraction 6.square 7.Cube 8.percentage
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

        # Deserialize context based on encrypted data
        context = ts.context_from(encrypted_data['context'])
        operation = encrypted_data['operation']
        scheme = encrypted_data['scheme']  # Explicitly pass scheme from the client

        # Handle client value encryption based on scheme
        encrypted_client_value = None

        # Check the scheme passed from the client
        if scheme == 'bfv':
            encrypted_client_value = ts.bfv_vector_from(context, encrypted_data['encrypted_client_value'])
        elif scheme == 'ckks':
            encrypted_client_value = ts.ckks_vector_from(context, encrypted_data['encrypted_client_value'])
        else:
            raise ValueError("Unsupported encryption scheme")

        print(f"\n[Server] Performing homomorphic {operation} operation...")

        # Create a sample server dataset - > 634  no. of data provided
        server_dataset = [ 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,1,2,3,4,5,6,7,8,9,10,11,12,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,4,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,1,2,3,4,5,6,7,8,9,16,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,1,2,3,28,29,30,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,14]
        encrypted_server_dataset = []

        # Encrypt server dataset based on the scheme
        for value in server_dataset:
            if scheme == 'bfv':
                encrypted_server_dataset.append(ts.bfv_vector(context, [value]))
            elif scheme == 'ckks':
                encrypted_server_dataset.append(ts.ckks_vector(context, [value]))

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
            elif operation == 'cube':
                squared = encrypted_server_value * encrypted_server_value
                result = squared * encrypted_server_value
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
