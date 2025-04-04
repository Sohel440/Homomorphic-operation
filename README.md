# Homomorphic Arithmatic Evaluation in the Client-Server Model #

## Overview ✨

This project implements a **client-server application** using **Homomorphic Encryption** with the **TenSEAL** library. The client encrypts a numerical value using **BGV encryption**, **Paillier encryption**,  **CKKS encryption**, sends it to the server, and the server  **homomorphically evaluates the arithmatic operation** on the encrypted data without any decryption. The result is then sent back to the client where it can perform the decryption and get back the required result.

## Features 🛠️

- **BGV Homomorphic Encryption** for integer arithmetic operation.
- **Paillier Homomorphic Encryption** for only additive homomorphic arithmetic operation.
- **CKKS Homomorphic Encryption** for floating-point arithmetic operation.
- **Secure Client-Server Communication** using socket programming model.
- **GUI-Based Client Appication** is built with Tkinter for the user interaction.
- **Supports Multiple Operations**: *Addition*, *Subtraction*, *Multiplication*, *Division*, *Cube* , *Squaring* , and *Percentage* calculations.

## Technologies Used 🚀

- **Python 3**
- **TenSEAL✅** (Homomorphic Encryption Library)
- **Socket Programming✅**
- **Tkinter✅** (GUI for Client)
- **Pickle✅** (Serialization)

**************** **Installation** ********************

#### Windows Environment ######

1. Prerequisites

Ensure you have Python 3 installed along with the required dependencies.

2. Install Dependencies

```bash
pip install tenseal
```

3. How to Run

### Start the Server

```bash
python server.py
```

### Start the Client

```bash
python client.py
```

#### Linux Environment ######

1. Prerequisites

Ensure you have Python 3 installed along with the required dependencies.

2. Install Dependencies

```bash
pip install tenseal
```

3. How to Run

### Start the Server

```bash
python server.py
```

### Start the Client

```bash
python client.py
```


## Usage

1. Open the client application.
2. Enter a numerical value in the input field.
3. Select an operation (Addition, Subtraction, Multiplication, percentage , division , fraction , Square).
4. The encrypted data is sent to the server, computed securely, and the encrypted result is returned.
5. The client decrypts the result and displays it.

## File Structure

```
│── client.py   # Client-side application with Tkinter GUI
│── server.py   # Server handling encrypted computations
│── README.md   # Documentation
```

## Contributors
- **[Sohel Mollick](https://github.com/sohel440)**
- **[Subhankar Dawn](https://github.com/Subhankar200)**
- **[Subhankar Halder](https://github.com/subhankar-732121)**
- **[Madhusudan Das](https://github.com/MADHUSUDAN-DAS)**

##

