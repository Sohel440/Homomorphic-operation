# client.py
# ******************* client Side ******************* #
# operation: 1. Addition 2. subtraction 3.Multiplication 4.divition 5.fraction 6.square 7.Cube 8.percentage 9. dot product 10. membership check 11. Matrix multiplication

# ---------------------------------------------------------------------------------------------------------------------------
import socket
import pickle
import tenseal as ts
from phe import paillier
import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np

def setup_encryption(scheme):
    if scheme == 'bfv':
        context = ts.context(ts.SCHEME_TYPE.BFV, poly_modulus_degree=2**14, coeff_mod_bit_sizes=[60, 40, 60], plain_modulus=536903681)
    elif scheme == 'ckks':
        context = ts.context(ts.SCHEME_TYPE.CKKS, poly_modulus_degree=2**14, coeff_mod_bit_sizes=[60, 40, 40, 60])
        context.global_scale = 2**40
    else:
        raise ValueError("Invalid scheme")
    context.generate_galois_keys()
    return context

def encrypt_value(context, scheme, value):
    if scheme == 'bfv':
        return ts.bfv_vector(context, [int(value)])
    return ts.ckks_vector(context, [value])

def send_to_server(data):
    HOST, PORT = '127.0.0.1', 12345
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
        return pickle.loads(buffer)

class HomomorphicApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Homomorphic Encryption Client")
        self.geometry("850x700")
        self.create_widgets()

    def create_widgets(self):
        # Input for scalar value
        tk.Label(self, text="Enter scalar value:").pack()
        self.entry = tk.Entry(self)
        self.entry.pack()

        # Input for matrix size
        tk.Label(self, text="Enter matrix dimensions (m x n):").pack()
        self.size_entry = tk.Entry(self)
        self.size_entry.pack()

        # Input for matrix values
        self.matrix_entry_label = tk.Label(self, text="Enter matrix values (comma-separated):")
        self.matrix_entry_label.pack()
        self.matrix_entry = tk.Entry(self)
        self.matrix_entry.pack()

        # Encryption scheme selection
        tk.Label(self, text="Select encryption scheme:").pack()
        self.scheme = tk.StringVar(value="ckks")
        self.scheme_menu = ttk.Combobox(self, textvariable=self.scheme, values=["bfv", "ckks", "paillier"])
        self.scheme_menu.pack()
        self.scheme_menu.bind("<<ComboboxSelected>>", self.update_buttons_state)

        # Operation buttons
        self.operations = {
            "add": tk.Button(self, text="Add", command=lambda: self.process("add")),
            "subtract": tk.Button(self, text="Subtract", command=lambda: self.process("subtract")),
            "multiply": tk.Button(self, text="Multiply", command=lambda: self.process("multiply")),
            "divide": tk.Button(self, text="Divide", command=lambda: self.process("divide")),
            "square": tk.Button(self, text="Square", command=lambda: self.process("square")),
            "cube": tk.Button(self, text="Cube", command=lambda: self.process("cube")),
            "percentage": tk.Button(self, text="Percentage", command=lambda: self.process("percentage")),
            "dot": tk.Button(self, text="Dot Product", command=lambda: self.process("dot")),
            "membership": tk.Button(self, text="Private Set Membership", command=lambda: self.process("membership")),
            "matmul": tk.Button(self, text="Matrix Multiplication", command=lambda: self.process("matmul")),
        }

        for btn in self.operations.values():
            btn.pack()

        # Result display box
        self.result_box = tk.Text(self, width=90, height=20)
        self.result_box.pack()

        self.update_buttons_state()

    def update_buttons_state(self, event=None):
        scheme = self.scheme.get()
        for op, btn in self.operations.items():
            if scheme == "paillier":
                btn.config(state="normal" if op in ["add", "subtract", "membership"] else "disabled")
            elif scheme == "bfv":
                btn.config(state="normal" if op in ["add", "subtract","multiply", "square", "cube", "dot", "matmul"] else "disabled")
            else:
                btn.config(state="normal" if op in ["add", "subtract","multiply", "square", "divide", "cube", "percentage", "dot", "matmul"] else "disabled")

            if scheme == "paillier":
                self.size_entry.config(state="disabled")
                self.matrix_entry.config(state="disabled")
                self.matrix_entry_label.config(state="disabled")
            else:
                self.size_entry.config(state="normal")
                self.matrix_entry.config(state="normal")
                self.matrix_entry_label.config(state="normal")

    def process(self, op):
        try:
            scheme = self.scheme.get()

            if scheme == 'paillier':
                # Setup Paillier keys
                pub_key, priv_key = paillier.generate_paillier_keypair()

                val = float(self.entry.get())

                enc_val = pub_key.encrypt(val)

                data = {
                    'operation': op,
                    'scheme': scheme,
                    'public_key': {'n': pub_key.n},
                    'encrypted_client_value': {
                        'ciphertext': enc_val.ciphertext(),
                        'exponent': enc_val.exponent
                    }
                }

                response = send_to_server(data)
                
                if op == "membership":
                    decrypted_differences = [
                        priv_key.decrypt(paillier.EncryptedNumber(pub_key, r['ciphertext'], r['exponent']))
                        for r in response['results']
                    ]
                    membership_found = any(diff == 0 for diff in decrypted_differences)

                    self.result_box.delete("1.0", tk.END)
                    self.result_box.insert(tk.END, f"Membership Found: {membership_found}\n")
                    return
                # Decrypt results
                decrypted = [
                    priv_key.decrypt(paillier.EncryptedNumber(pub_key, r['ciphertext'], r['exponent']))
                    for r in response['results']
                ]

                self.result_box.delete("1.0", tk.END)
                self.result_box.insert(tk.END, f"Operation: {op}\n")
                for i, v in enumerate(decrypted, 1):
                    self.result_box.insert(tk.END, f"Result {i}: {v}\n")
                return

            # For BFV/CKKS
            context = setup_encryption(scheme)

            if op in ['dot', 'matmul']:
                # Get matrix dimensions
                size_input = self.size_entry.get().strip()
                if "x" not in size_input:
                    messagebox.showerror("Error", "Invalid matrix size. Please enter in m x n format.")
                    return
                m, n = size_input.split("x")
                m, n = int(m.strip()), int(n.strip())

                # Get matrix values
                matrix_input = self.matrix_entry.get().strip()
                matrix_values = [float(x.strip()) for x in matrix_input.split(",")]
                if len(matrix_values) != m * n:
                    messagebox.showerror("Error", f"Please enter {m * n} values for the matrix.")
                    return

                matrix = np.array(matrix_values).reshape(m, n)

                # Encrypt matrix
                tensor = ts.ckks_tensor(context, matrix) if scheme == 'ckks' else ts.bfv_tensor(context, matrix)

                data = {
                    'operation': op,
                    'scheme': scheme,
                    'context': context.serialize(),
                    'encrypted_tensor': tensor.serialize()
                }
                response = send_to_server(data)

                decrypted_tensor = ts.ckks_tensor_from(context, response['results'][0]) if scheme == 'ckks' \
                    else ts.bfv_tensor_from(context, response['results'][0])

                result = decrypted_tensor.decrypt().tolist()

                self.result_box.delete("1.0", tk.END)
                self.result_box.insert(tk.END, f"Operation: {op}\n")
                self.result_box.insert(tk.END, f"{op.capitalize()} Result (matrix):\n")
                for row in result:
                    self.result_box.insert(tk.END, f"{row}\n")
                return

            # For scalar operations
            val = float(self.entry.get())
            if op == 'divide' and val == 0:
                messagebox.showerror("Error", "Division by zero")
                return
            if op == 'divide':
                val = 1 / val
            elif op == 'percentage':
                val /= 100

            enc_val = encrypt_value(context, scheme, val)
            data = {
                'operation': op,
                'scheme': scheme,
                'context': context.serialize(),
                'encrypted_client_value': enc_val.serialize()
            }
            response = send_to_server(data)

            decrypted = [
                ts.ckks_vector_from(context, r).decrypt()[0] if scheme == 'ckks'
                else ts.bfv_vector_from(context, r).decrypt()[0]
                for r in response['results']
            ]

            self.result_box.delete("1.0", tk.END)
            self.result_box.insert(tk.END, f"Operation: {op}\n")
            for i, v in enumerate(decrypted, 1):
                self.result_box.insert(tk.END, f"Result {i}: {v}\n")

        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    app = HomomorphicApp()
    app.mainloop()

