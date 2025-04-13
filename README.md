# 🔐 A Secure Two-party Basic Arithmetic Evaluation System using Homomorphic Encryption #

## ✨ Overview 

This repository presents a secure two-party arithmetic evaluation system leveraging **Homomorphic Encryption (HE)** to enable computations on encrypted data without decryption. The system employs a **client-server model**, where a client encrypts input data and selects an arithmetic operation, which is then evaluated homomorphically on the server. The result is returned in encrypted form, preserving data privacy and confidentiality throughout the process.

This project is powered by the **TenSEAL library** and includes a **Tkinter-based GUI** for user interaction. It supports multiple homomorphic schemes including **BFV, Paillier, and CKKS**, covering both integer and floating-point arithmetic.

## 🎯 Key Features 


- 🔢 Arithmetic Operation Support: Addition, Subtraction, Multiplication, Division, Squaring, Cubing, and Percentage calculation.

- 🔐 Homomorphic Encryption Schemes:

      BFV: Efficient integer arithmetic.

      Paillier: Additive-only integer HE.

      CKKS: Approximate real number (floating-point) computation.

- 🖥️ Secure Two-Party Computation:

      Encrypted data transmission via socket programming.

      The server computes directly on ciphertexts.

- 🎨 Graphical User Interface:

      Intuitive Tkinter-based client interface.

      Real-time encrypted result display.

- ⚙️ Cross-platform Compatibility:

      Tested on Windows and Linux environments.




## 🧪 Research Scope

This project is designed with a focus on academic and applied cryptography research. It demonstrates a foundational step toward privacy-preserving data computation systems in fields like secure cloud computing, privacy-preserving healthcare analytics, and confidential financial modelling.

## 📁 File Structure

📦 Homomorphic-Arithmetic-System
├── client.py         # GUI-based client application
├── server.py         # Server-side logic for HE computations
├── README.md         # Project documentation
├── requirements.txt  # Python dependencies


  

## Technologies Used 🚀

- **Python 3**
- **TenSEAL✅** (Homomorphic Encryption Library)
- **Socket Programming✅**
- **Tkinter✅** (GUI for Client)
- **Pickle✅** (Serialization)

## ⚙️ Installation Guide

### 🪟 Windows Setup

####  Install pip Manually 
- If pip is missing, do this:

- Download get-pip.py from:

- https://bootstrap.pypa.io/get-pip.py
- (Right-click → Save As)

- Open the Command Prompt where the file is saved.

Run this:
   ```bash
   python get-pip.py
   ```
Upgrade pip:
   ```bash
   python -m pip install --upgrade pip
   ```

1. Prerequisites
   -  Install python latest version -> https://www.python.org/downloads/

2. Install Dependencies

  - Install numpy
  
     ```bash
        pip install numpy
     ```
  - Install tenseal
  
    ```bash
      pip install tenseal
    ```
 ##### ℹ️ Note: socket, pickle, and tkinter are built-in with Python on Windows, so no need for separate installation.

3. Run the Application

### Start the Server

```bash
python3 server.py
```

### Start the Client

```bash
python3 client.py
```

### 🐧 Linux Environment

1. Prerequisites

 - Install Python 3.13
  ```bash
    sudo apt update
    sudo apt install python3
  ```
   
 - Install Pip
 ```bash
   sudo apt update 
   sudo apt install python3-pip
 ```
    
   

2. Install Dependencies
  ```bash
    sudo apt update
    pip3 install numpy
    pip3 install tenseal
  ```

3. Install Tkinter (if not pre-installed)
  ```bash
    sudo apt update
    sudo apt-get install python3-tk
  ```

4. How to Run

### Start the Server

```bash
 python3 server.py
```

### Start the Client

```bash
python3 client.py
```


## Usage

1. Open the client application.
2. Enter a numerical value in the input field.
3. Select an operation (Addition, Subtraction, Multiplication, Percentage , Division , Fraction , Square).
4. The encrypted data is sent to the server, computed securely, and the encrypted result is returned.
5. The client decrypts the result and displays it.

## File Structure


│── client.py   # Client-side application with Tkinter GUI               
│── server.py   # Server handling encrypted computations      
│── README.md   # Documentation


## Contributors
- **[Sohel Mollick](https://github.com/sohel440)**
- **[Subhankar Dawn](https://github.com/Subhankar200)**
- **[Subhankar Halder](https://github.com/subhankar-732121)**
- **[Madhusudan Das](https://github.com/MADHUSUDAN-DAS)**

##
