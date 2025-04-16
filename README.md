# 🔐 Secure Two-Party Arithmetic Evaluation System with Homomorphic Encryption

## ✨ Overview 

This project implements a **secure two-party computation system** using **Homomorphic Encryption (HE)**, enabling privacy-preserving arithmetic operations on encrypted data. The system follows the client-server model where:

- **Client** encrypts input data and selects operations.

- **Server** performs computations without decrypting the data.

- Results remain encrypted until returned to the client.

Built with **TenSEAL**, the system supports multiple HE schemes **(BFV, Paillier, CKKS)** for **integer and floating-point** operations, featuring a user-friendly **Tkinter GUI**.


## 🎯 Key Features

| **Feature**         | **Supported Schemes** | **Description**                          |
|---------------------|------------------------|------------------------------------------|
| Basic Arithmetic    | All                    | Add, Subtract, Multiply                  |
| Advanced Math       | CKKS / BFV             | Division, Square, Cube                   |
| Percentage          | CKKS                   | Secure percentage calculations           |
| Matrix Operations   | CKKS                   | Dot product for 2x2 tensors              |
| Data Privacy        | -                      | End-to-end encrypted computations        |



- 🔢 Arithmetic Operation Support: **Addition**, **Subtraction**, **Multiplication**, **Division**, **Square**, **Cube**, and **Percentage Calculation**.

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
``` 
├─ client.py         # GUI-based client application
├─ server.py         # Server-side logic for HE computations
├─ README.md         # Project documentation

```
  

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

- First Start the Server

```bash
python3 server.py
```

- Then Start the Client

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

- First Start the Server

```bash
 python3 server.py
```

- Then Start the Client

```bash
python3 client.py
```


## Usage

1. Open the client application.
2. Enter a numerical value in the input field.
3. Select an operation (Addition, Subtraction, Multiplication, Percentage , Division , Fraction , Square).
4. The encrypted data is sent to the server, computed securely, and the encrypted result is returned.
5. The client decrypts the result and displays it.




## Contributors
- **[Sohel Mollick](https://github.com/sohel440)**
- **[Subhankar Dawn](https://github.com/Subhankar200)**
- **[Subhankar Halder](https://github.com/subhankar-732121)**
- **[Madhusudan Das](https://github.com/MADHUSUDAN-DAS)**


