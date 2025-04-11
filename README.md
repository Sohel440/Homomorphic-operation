# A Secure Two-party Basic Arithmatic Evaluation System using Homomorphic Encryption #

## Overview ✨

This project implements a **secure two-party basic arithmatic evaluation system** using **Homomorphic Encryption** with the use of **TenSEAL** library. We develop a graphical user interface (GUI) where a client can choose which operation it wants to perform on the server side with its dataset of items in a  secure way. The client encrypts its own dataset of items using any of the following schemes, i.e., **BFV encryption**, **Paillier encryption**,  **CKKS encryption**, and send the result to the server end, and finally, the server  **homomorphically evaluates the desired operation** on the encrypted data without performing any decryption. The result is then sent back to the client where it can decrypt  and get back the required result.

## Features 🛠️

- **BFV Homomorphic Encryption** for integer arithmetic operation.
- **Paillier Homomorphic Encryption** for only additive homomorphic arithmetic operation.
- **CKKS Homomorphic Encryption** for floating-point arithmetic operation.
- **Secure Client-Server Communication** using socket programming model.
- **GUI-Based Client Application** is built with Tkinter for the user interaction.
- Supports Multiple Operations: **Addition**, **Subtraction**, **Multiplication**, **Division**, **Cube**, **Squaring**, and **Percentage Calculations**.

## Technologies Used 🚀

- **Python 3**
- **TenSEAL✅** (Homomorphic Encryption Library)
- **Socket Programming✅**
- **Tkinter✅** (GUI for Client)
- **Pickle✅** (Serialization)

## 🔧 Installation

### Windows Environment ######

####  Install pip Manually 
- If pip is missing, do this:

- Download get-pip.py from:

- https://bootstrap.pypa.io/get-pip.py
- (Right-click → Save As)

- Open Command Prompt where the file is saved.

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
