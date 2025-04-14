#********************client side code with Paillier option in GUI ---------------------->:
import socket
import pickle
import tenseal as ts
from phe import paillier
import tkinter as tk
from tkinter import ttk, messagebox

def setup_encryption(scheme):
    if scheme == 'bfv':
        context = ts.context(ts.SCHEME_TYPE.BFV, poly_modulus_degree=2**14,
                             coeff_mod_bit_sizes=[60, 40, 60], plain_modulus= 536903681)
    elif scheme == 'ckks':
        context = ts.context(ts.SCHEME_TYPE.CKKS, poly_modulus_degree=8192,
                             coeff_mod_bit_sizes=[60, 40, 40, 60])
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
        self.geometry("800x600")
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Enter value:").pack()
        self.entry = tk.Entry(self)
        self.entry.pack()

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
            "percentage": tk.Button(self, text="Percentage", command=lambda: self.process("percentage"))
        }

        for btn in self.operations.values():
            btn.pack()

        self.result_box = tk.Text(self, width=80, height=20)
        self.result_box.pack()

        self.update_buttons_state()  # Initialize button states

    def update_buttons_state(self, event=None):
        scheme = self.scheme.get()
        for op, btn in self.operations.items():
            if scheme == "paillier" and op not in ["add", "subtract"]:
                btn.config(state="disabled")
            elif scheme == 'bfv':
                btn.config(state="normal" if op in ["add", "subtract","multiply","square","cube" ,"percentage"] else "disable")
            else:
                btn.config(state="normal")

    def process(self, op):
        try:
            val = float(self.entry.get())
            if op == 'divide' and val == 0:
                messagebox.showerror("Error", "Division by zero")
                return
            if op == 'divide':
                val = 1 / val
            elif op == 'percentage':
                val /= 100
        except:
            messagebox.showerror("Invalid Input", "Enter a valid number")
            return

        scheme = self.scheme.get()

        try:
            if scheme == "paillier":
                pub_key, priv_key = paillier.generate_paillier_keypair()
                enc_val = pub_key.encrypt(val)
                data = {
                    'operation': op,
                    'scheme': 'paillier',
                    'public_key': {'n': pub_key.n},
                    'encrypted_client_value': {
                        'ciphertext': enc_val.ciphertext(),
                        'exponent': enc_val.exponent
                    }
                }
                response = send_to_server(data)
                decrypted = []
                for res in response['results']:
                    enc_res = paillier.EncryptedNumber(pub_key, res['ciphertext'], res['exponent'])
                    decrypted.append(priv_key.decrypt(enc_res))

            else:
                context = setup_encryption(scheme)
                enc_val = encrypt_value(context, scheme, val)
                data = {
                    'operation': op,
                    'scheme': scheme,
                    'context': context.serialize(),
                    'encrypted_client_value': enc_val.serialize()
                }
                response = send_to_server(data)
                decrypted = [ts.ckks_vector_from(context, r).decrypt()[0] if scheme == 'ckks'
                             else ts.bfv_vector_from(context, r).decrypt()[0]
                             for r in response['results']]

            self.result_box.delete("1.0", tk.END)
            self.result_box.insert(tk.END, f"Operation: {op}\n")
            for i, v in enumerate(decrypted, 1):
                self.result_box.insert(tk.END, f"Result {i}: {v}\n")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    app = HomomorphicApp()
    app.mainloop()
