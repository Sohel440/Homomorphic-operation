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


## 🎯 Technical Highlights:


- 🚀 Multi-scheme Support:


      BFV: Efficient integer arithmetic.

      Paillier: Additive-only integer HE.

      CKKS: Approximate real number (floating-point) computation.

- 🔒 Secure Socket Communication:

      Encrypted data transmission via socket programming.
 
      The server computes directly on ciphertexts.

- 🎨 Graphical User Interface:

      Intuitive Tkinter-based client interface.

      Real-time encrypted result display.

- ⚙️ Cross-platform Compatibility:

      Tested on Windows and Linux environments.

## ⚙️ Installation Guide

### 🪟 Windows Setup

#### Prerequisites

##### Install Python latest version

    -> https://www.python.org/downloads/

#####  Install pip  

- If pip is missing, do this:

- Download get-pip.py from:

      https://bootstrap.pypa.io/get-pip.py
  
      (Right-click → Save )

- Open the Command Prompt where the file is saved.

      Run this:
      
      python get-pip.py
      
      Upgrade pip:
      
      python -m pip install --upgrade pip
       

   

#### Install Dependencies

  - Install numpy
  
        
        pip install numpy
     
  - Install TenSEAL
  
      
        pip install tenseal
        
    
 ##### ℹ️ Note: socket, pickle, and tkinter are built-in with Python on Windows, so no need for separate installation.

 ### 🐧 Linux Environment

#### Prerequisites

 ##### Install Python latest version:
 
    
    sudo apt update
    sudo apt install python3

   
#####  Install pip  

   
     sudo apt update 
    sudo apt install python3-pip

    
#### Install Dependencies   

##### Install Numpy and TenSEAL
  
    sudo apt update
    pip3 install numpy
    pip3 install tenseal
    

##### Install Tkinter (if not pre-installed)

 
    sudo apt update
    sudo apt-get install python3-tk


## Technologies Used 🚀

- **Python 3**
- **TenSEAL✅** (Homomorphic Encryption Library)
- **Socket Programming✅**
- **Tkinter✅** (GUI for Client)
- **Pickle✅** (Serialization)



## 🚀 Usage

- 1. Start the Server

     
         python3 server.py
        
    Server runs on 127.0.0.1:12345 by default

- 2. Launch the Client GUI

         python3 client.py
         
- 3. Perform Operations:

     - Enter numeric values

     - Select encryption scheme

     - Choose operation (buttons auto-adjust based on scheme)

     - View decrypted results in the output box
           
## 🧠 Supported Operations

| **Operation**     | **BFV** | **Paillier** | **CKKS** |
|-------------------|:-------:|:------------:|:--------:|
| Addition          | ❌      | ✅           | ✅       |
| Subtraction       | ❌      | ✅           | ✅       |
| Multiplication    | ✅      | ❌           | ✅       |
| Division          | ❌      | ❌           | ✅       |
| Square / Cube     | ✅      | ❌           | ✅       |
| Percentage        | ❌      | ❌           | ✅       |
| Dot Product       | ❌      | ❌           | ✅       |      



## 📁 File Structure

homomorphic-calculator/
├── client.py            # GUI client application
├── server.py            # HE computation server
├── README.md            # This documentation
└── requirements.txt     # Dependencies
  
## 🛠️ Troubleshooting

| **Issue**                          | **Solution**                                      |
|------------------------------------|---------------------------------------------------|
| ImportError: No module named 'tenseal' | Run `pip install tenseal`                        |
| Socket connection errors           | Verify the server is running before starting the client |
| Paillier division attempts         | Use the CKKS scheme for division operations       |



## 👥 Contributors
- **[Sohel Mollick](https://github.com/sohel440)**
- **[Subhankar Dawn](https://github.com/Subhankar200)**
- **[Subhankar Halder](https://github.com/subhankar-732121)**
- **[Madhusudan Das](https://github.com/MADHUSUDAN-DAS)**

## 🧪 Research Applications

Ideal for:

 - Privacy-preserving cloud computations

 - Secure medical data analysis

 - Confidential financial modelling













