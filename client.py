#********************client side code ---------------------->:
# here we use Both scheme , BFV for Integer and ckks for floatinng
import socket
import pickle
import tenseal as ts
import tkinter as tk
from tkinter import ttk 
from tkinter import messagebox


def setup_encryption(scheme):
    """Sets up the encryption context based on the selected scheme."""
    if scheme == 'bfv':
        context = ts.context(ts.SCHEME_TYPE.BFV, poly_modulus_degree=8192, coeff_mod_bit_sizes=[60, 40, 40, 60], plain_modulus=65537)
    elif scheme == 'ckks':
        context = ts.context(ts.SCHEME_TYPE.CKKS, poly_modulus_degree=8192, coeff_mod_bit_sizes=[60, 40, 40, 60])
    else:
        raise ValueError("Unsupported scheme type")
    context.generate_galois_keys()
    context.global_scale = 2**40
    return context, scheme

def encrypt_value(context, scheme, value):
    """Encrypts a single value using the specified encryption context."""
    if scheme == 'bfv':
        # BFV typically works with integers
        return ts.bfv_vector(context, [int(value)])
    elif scheme == 'ckks':
        # CKKS typically works with floating point numbers
        return ts.ckks_vector(context, [value])
    else:
        raise ValueError("Unsupported encryption scheme type")

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

def decrypt_result(context, scheme, encrypted_result):
    """Decrypts the received encrypted result."""
    if scheme == 'bfv':
        return ts.bfv_vector_from(context, encrypted_result).decrypt()
    elif scheme == 'ckks':
        return ts.ckks_vector_from(context, encrypted_result).decrypt()
    else:
        raise ValueError("Unsupported encryption scheme")

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

        # Add dropdown for scheme selection
        self.scheme_var = tk.StringVar(value="ckks")
        self.scheme_dropdown = ttk.Combobox(self, textvariable=self.scheme_var, values=["bfv", "ckks"])
        self.scheme_dropdown.pack()

        # Add operation buttons with the correct command reference
        operations = ["add", "subtract", "multiply", "divide", "square", "cube", "percentage"]
        for op in operations:
            btn = tk.Button(self, text=f"Encrypt and {op.capitalize()}", command=lambda op=op: self._encrypt_and_send(op))
            btn.pack()

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
            elif operation == "percentage":
                value /= 100  # Convert to fraction (e.g., 50% -> 0.5)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number.")
            return

        # Get the selected scheme from the dropdown
        scheme = self.scheme_var.get()

        # Setup encryption context
        context, scheme = setup_encryption(scheme)

        # Encrypt the value
        encrypted_value = encrypt_value(context, scheme, value)

        encrypted_data = {
            'context': context.serialize(),
            'encrypted_client_value': encrypted_value.serialize(),
            'operation': operation,
            'scheme': scheme  # Pass the scheme explicitly
        }

        try:
            result_data = send_data_to_server_and_receive(encrypted_data)
            results = []
            
            for encrypted_result in result_data['encrypted_results']:
                if encrypted_result is None:
                    results.append("Error in computation")
                else:
                    dec_val = decrypt_result(context, scheme, encrypted_result)
                    results.append(dec_val)
                    print(dec_val)

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
