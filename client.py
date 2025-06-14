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
import zlib
import time

def setup_encryption(scheme):
    if scheme == 'bfv':
        context = ts.context(ts.SCHEME_TYPE.BFV, poly_modulus_degree=8192, coeff_mod_bit_sizes=[60,40,40,60], plain_modulus=536903681)
    elif scheme == 'ckks':
        context = ts.context(ts.SCHEME_TYPE.CKKS, poly_modulus_degree=8192, coeff_mod_bit_sizes=[60, 40, 40, 60])
        context.global_scale = 2**40
    else:
        raise ValueError("Invalid scheme")
    context.generate_galois_keys()
    return context

def encrypt_value(context, scheme, value):
    if scheme == 'bfv':
        return ts.bfv_vector(context, [int(v) for v in value])
    return ts.ckks_vector(context, value)

def send_to_server(data):
    HOST, PORT = '127.0.0.1', 12345
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 2 *1024 * 1024)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 2* 1024 * 1024)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            
            if hasattr(socket, 'TCP_KEEPIDLE'):
                s.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 5)
                s.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 2)
                s.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 5)
            
            s.connect((HOST, PORT))
            
            start_time = time.time()
            serialized_data = zlib.compress(pickle.dumps(data))
            data_size = len(serialized_data)
            
            print(f"Sending data of size: {data_size} bytes (compressed)")
            s.sendall(data_size.to_bytes(8, byteorder='big'))
            s.sendall(serialized_data)
            print(f"Total time to send data: {time.time() - start_time:.4f} seconds")
            
            s.settimeout(900.0)
            start_time = time.time()
            
            size_data = b""
            while len(size_data) < 8:
                chunk = s.recv(8 - len(size_data))
                if not chunk:
                    raise ConnectionError("Connection closed while receiving data size")
                size_data += chunk
            data_size = int.from_bytes(size_data, byteorder='big')
            print(f"Expected data size: {data_size} bytes | Time elapsed: {time.time() - start_time:.4f} seconds")
            
            buffer = b""
            while len(buffer) < data_size:
                chunk = s.recv(min(8192, data_size - len(buffer)))
                if not chunk:
                    raise ConnectionError("Connection closed while receiving data")
                buffer += chunk
                print(f"Received {len(buffer)}/{data_size} bytes | Time elapsed: {time.time() - start_time:.4f} seconds")
            total_time = time.time() - start_time
            print(f"Total time to receive data: {total_time:.4f} seconds")
            response = pickle.loads(zlib.decompress(buffer))
            
            if 'error' in response:
                raise ValueError(f"Server error: {response['error']}")
      
            return response, total_time
    except socket.timeout:
        print("Socket timeout while receiving data")
        raise
    except Exception as e:
        print(f"Error sending/receiving data: {e}")
        raise

class HomomorphicApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Homomorphic Encryption Client")
        self.geometry("800x600")
        self.paillier_keypair = None  # Store persistent Paillier keypair
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Enter single value for Paillier or comma-separated values (e.g., 1,2,3,4) for BFV/CKKS add/subtract/multiply/square/cube:").pack()
        self.entry = tk.Entry(self)
        self.entry.insert(0, " ")
        self.entry.pack()

        tk.Label(self, text="Enter matrix dimensions (m x n):").pack()
        self.size_entry = tk.Entry(self)
        self.size_entry.pack()

        self.matrix_entry_label = tk.Label(self, text="Enter matrix values (comma-separated):")
        self.matrix_entry_label.pack()
        self.matrix_entry = tk.Entry(self)
        self.matrix_entry.pack()

        tk.Label(self, text="Select encryption scheme:").pack()
        self.scheme = tk.StringVar(value="ckks")
        self.scheme_menu = ttk.Combobox(self, textvariable=self.scheme, values=["bfv", "ckks", "paillier"])
        self.scheme_menu.pack()
        self.scheme_menu.bind("<<ComboboxSelected>>", self.update_buttons_state)

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
            "matmul": tk.Button(self, text="Matrix Multiply", command=lambda: self.process("matmul")),
        }

        for btn in self.operations.values():
            btn.pack()

        self.result_box = tk.Text(self, width=80, height=15)
        self.result_box.pack()

        self.update_buttons_state()

    def update_buttons_state(self, event=None):
        scheme = self.scheme.get()
        for op, btn in self.operations.items():
            if scheme == "paillier":
                btn.config(state="normal" if op in ["add", "subtract", "membership"] else "disabled")
            elif scheme == "bfv":
                btn.config(state="normal" if op in ["add", "subtract", "multiply", "square", "cube", "dot", "matmul", "membership"] else "disabled")
            else:
                btn.config(state="normal" if op in ["add", "subtract", "multiply", "square", "divide", "cube", "percentage", "dot", "matmul"] else "disabled")

        if op in ["square", "cube", "membership", "add", "subtract", "multiply"]:
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
                values = [x.strip() for x in self.entry.get().strip().split(",")]
                if len(values) != 1:
                    messagebox.showerror("Error", "Please enter a single value for Paillier operations.")
                    return
                val = float(values[0])
                
                # Use persistent Paillier keypair or generate new one
                if self.paillier_keypair is None:
                    self.paillier_keypair = paillier.generate_paillier_keypair()
                pub_key, priv_key = self.paillier_keypair
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

                response, total_time = send_to_server(data)
                
                if op == "membership":
                    decrypted_differences = [
                        priv_key.decrypt(paillier.EncryptedNumber(pub_key, r['ciphertext'], r['exponent']))
                        for r in response['results']
                    ]
                    membership_found = any(diff == 0 for diff in decrypted_differences)

                    self.result_box.delete("1.0", tk.END)
                    self.result_box.insert(tk.END, f"Membership Found: {membership_found}\n")
                    self.result_box.insert(tk.END, f"Total Time: {total_time:.4f} seconds\n")
                    return

                decrypted = [
                    priv_key.decrypt(paillier.EncryptedNumber(pub_key, r['ciphertext'], r['exponent']))
                    for r in response['results']
                ]

                self.result_box.delete("1.0", tk.END)
                self.result_box.insert(tk.END, f"Operation: {op.capitalize()}\n")
                for i, v in enumerate(decrypted, 1):
                    self.result_box.insert(tk.END, f"Result {i}: {v}\n")
                self.result_box.insert(tk.END, f"Total Time: {total_time:.4f} seconds\n")
                return

            context = setup_encryption(scheme)

            if op in ['dot', 'matmul']:
                size_input = self.size_entry.get().strip()
                if "x" not in size_input:
                    messagebox.showerror("Error", "Invalid matrix size. Please enter in m x n format.")
                    return
                m, n = size_input.split("x")
                m, n = int(m.strip()), int(n.strip())

                matrix_input = self.matrix_entry.get().strip()
                matrix_values = [float(x.strip()) for x in matrix_input.split(",")]
                if len(matrix_values) != m * n:
                    messagebox.showerror("Error", f"Please enter {m * n} values for the matrix.")
                    return

                matrix = np.array(matrix_values).reshape(m, n)
                tensor = ts.ckks_tensor(context, matrix) if scheme == 'ckks' else ts.bfv_tensor(context, matrix)

                data = {
                    'operation': op,
                    'scheme': scheme,
                    'context': context.serialize(),
                    'encrypted_tensor': tensor.serialize()
                }
                response, total_time = send_to_server(data)

                decrypted_tensor = ts.ckks_tensor_from(context, response['results'][0]) if scheme == 'ckks' \
                    else ts.bfv_tensor_from(context, response['results'][0])
                result = decrypted_tensor.decrypt().tolist()

                self.result_box.delete("1.0", tk.END)
                self.result_box.insert(tk.END, f"Operation: {op.capitalize()}\n")
                for row in result:
                    self.result_box.insert(tk.END, f"{row}\n")
                self.result_box.insert(tk.END, f"Total Time: {total_time:.4f} seconds\n")
                return

            elif op in ['square', 'cube', 'add', 'subtract', 'multiply']:
                values = [float(x.strip()) for x in self.entry.get().strip().split(",")]
                if not values:
                    messagebox.showerror("Error", "Please enter at least one value.")
                    return

                if op in ['square', 'cube']:
                    enc_val = encrypt_value(context, scheme, values)
                    data = {
                        'operation': op,
                        'scheme': scheme,
                        'context': context.serialize(),
                        'encrypted_client_value': enc_val.serialize()
                    }
                else:
                    enc_vals = [encrypt_value(context, scheme, [val]) for val in values]
                    data = {
                        'operation': op,
                        'scheme': scheme,
                        'context': context.serialize(),
                        'encrypted_client_values': [enc_val.serialize() for enc_val in enc_vals]
                    }
                
                response, total_time = send_to_server(data)
                
                self.result_box.delete("1.0", tk.END)
                self.result_box.insert(tk.END, f"Operation: {op.capitalize()}\n")
                if op in ['square', 'cube']:
                    decrypted = ts.ckks_vector_from(context, response['results'][0]).decrypt() if scheme == 'ckks' \
                        else ts.bfv_vector_from(context, response['results'][0]).decrypt()
                    for i, (input_val, result_val) in enumerate(zip(values, decrypted), 1):
                        self.result_box.insert(tk.END, f"Result {i} ({input_val} {op}d): {result_val:.2f}\n")
                else:
                    for i, (val, val_results) in enumerate(zip(values, response['results']), 1):
                        decrypted = [ts.ckks_vector_from(context, r).decrypt()[0] if scheme == 'ckks'
                                    else ts.bfv_vector_from(context, r).decrypt()[0]
                                    for r in val_results]
                        self.result_box.insert(tk.END, f"Value {i} ({val}):\n")
                        for j, v in enumerate(decrypted, 1):
                            self.result_box.insert(tk.END, f"  Result {j}: {v:.2f}\n")
                self.result_box.insert(tk.END, f"Total Time: {total_time:.4f} seconds\n")
                return

            val = float(self.entry.get())
            if op == 'divide' and val == 0:
                messagebox.showerror("Error", "Division by zero")
                return
            if op == 'divide':
                val = 1.0 / val
            elif op == 'percentage':
                val /= 100

            enc_val = encrypt_value(context, scheme, [val])
            data = {
                'operation': op,
                'scheme': scheme,
                'context': context.serialize(),
                'encrypted_client_value': enc_val.serialize()
            }

            response, total_time = send_to_server(data)
            
            if op == 'membership':
                decrypted_differences = [
                    ts.bfv_vector_from(context, r).decrypt()[0]
                    for r in response['results']
                ]
                membership_found = any(diff == 0 for diff in decrypted_differences)
                
                self.result_box.delete("1.0", tk.END)
                self.result_box.insert(tk.END, f"Membership Found: {membership_found}\n")
                self.result_box.insert(tk.END, f"Total Time: {total_time:.4f} seconds\n")
                return

            decrypted = [
                ts.ckks_vector_from(context, r).decrypt()[0] if scheme == 'ckks'
                else ts.bfv_vector_from(context, r).decrypt()[0]
                for r in response['results']
            ]
            
            self.result_box.delete("1.0", tk.END)
            self.result_box.insert(tk.END, f"Operation: {op}\n")
            for i, v in enumerate(decrypted, 1):
                self.result_box.insert(tk.END, f"Result {i}: {v:.2f}\n")
            self.result_box.insert(tk.END, f"Total Time: {total_time:.4f} seconds\n")
            
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    app = HomomorphicApp()
    app.mainloop()
