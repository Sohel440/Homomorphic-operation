#Subhankar Dawn
#Sohel Mollick
import tenseal as ts
import pickle
import socket
import tkinter as tk
from tkinter import messagebox

def setup_encryption():
    """Sets up the CKKS encryption context."""
    context = ts.context(ts.SCHEME_TYPE.CKKS, poly_modulus_degree=8192, coeff_mod_bit_sizes=[60, 40, 60])
    context.generate_galois_keys()
    context.global_scale = 2**40
    return context

def encrypt_value(context, value):
    """Encrypts a single value using CKKS."""
    return ts.ckks_vector(context, [value])

def send_data_to_server_and_receive(data):
    """Sends encrypted data to the server and receives the response."""
    HOST = '127.0.0.1'
    PORT = 12345
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(pickle.dumps(data))
        s.shutdown(socket.SHUT_WR)

        buffer = b""
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            buffer += chunk

    if not buffer:
        raise ValueError("Error: No response from server")

    response = pickle.loads(buffer)

    if 'error' in response:
        raise ValueError(f"Server Error: {response['error']}")

    return response

def decrypt_result(context, encrypted_result):
    """Decrypts the received encrypted result."""
    return ts.ckks_vector_from(context, encrypted_result).decrypt()

class HomomorphicEncryptionGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Homomorphic Encryption Calculator")
        self.geometry("800x600")
        self.create_widgets()

    def create_widgets(self):
        """Creates GUI components."""
        tk.Label(self, text="Enter a number:").pack()
        self.entry_value = tk.Entry(self)
        self.entry_value.pack()
        
        self.add_button = tk.Button(self, text="Encrypt and Add", command=lambda: self._encrypt_and_send('add'))
        self.add_button.pack()
        
        self.sub_button = tk.Button(self, text="Encrypt and Subtract", command=lambda: self._encrypt_and_send('subtract'))
        self.sub_button.pack()
        
        self.mul_button = tk.Button(self, text="Encrypt and Multiply", command=lambda: self._encrypt_and_send('multiply'))
        self.mul_button.pack()
        
        self.div_button = tk.Button(self, text="Encrypt and Divide", command=lambda: self._encrypt_and_send('divide'))
        self.div_button.pack()

        self.sqr_button = tk.Button(self, text="Encrypt and Square", command=lambda: self._encrypt_and_send('square'))
        self.sqr_button.pack()

        # self.rem_button = tk.Button(self, text="Encrypt and Remainder", command=lambda: self._encrypt_and_send('remainder'))
        # self.rem_button.pack()

        self.perc_button = tk.Button(self, text="Encrypt and Percentage", command=lambda: self._encrypt_and_send('percentage'))
        self.perc_button.pack()

        self.result_text = tk.Text(self, width=80, height=15)
        self.result_text.pack()
    
    def _encrypt_and_send(self, operation):
        """Handles user input, encrypts it, sends it to the server, and displays results."""
        try:
            value = float(self.entry_value.get())  
            if operation == "divide":
                if value == 0:
                    messagebox.showerror("Invalid Input", "Cannot divide by zero.")
                    return
                value = 1 / value  # Send reciprocal instead of original value
            # elif operation == "remainder":
            #     if value == 0:
            #         messagebox.showerror("Invalid Input", "Cannot compute remainder with zero divisor.")
            #         return
            #     value =1 / value
                
            elif operation == "percentage":
                value /= 100  # Convert to fraction (e.g., 50% -> 0.5)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number.")
            return

        context = setup_encryption()
        encrypted_value = encrypt_value(context, value)
        
        encrypted_data = {
            'context': context.serialize(),
            'encrypted_client_value': encrypted_value.serialize(),
            'operation': operation
        }

        try:
            result_data = send_data_to_server_and_receive(encrypted_data)
            results = []
            for encrypted_result in result_data['encrypted_results']:
                if encrypted_result is None:
                    results.append("Error in computation")
                else:
                    results.append(decrypt_result(context, encrypted_result))

            results_text = f"Operation: {operation.capitalize()}\n"
            for i, result in enumerate(results):
                results_text += f"Server value {i+1}: {result}\n"

            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, results_text)
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    app = HomomorphicEncryptionGUI()
    app.mainloop()
