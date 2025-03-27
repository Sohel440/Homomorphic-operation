Packages Used in the Code and Their Purpose

1.Socket
Purpose: Enables communication between the client and server using TCP sockets.
Workings in Code:
i.On the server side, it creates a listening socket (socket.socket(socket.AF_INET, socket.SOCK_STREAM)) to accept client connections.
ii.The client connects to the server using a socket, sends encrypted data, and receives processed encrypted results back.

2.Pickle
Purpose: Serializes and deserializes Python objects for sending structured data between the client and server.
Workings in Code:
i.Used to serialize encryption data before sending (pickle.dumps(data)) and deserialize it after receiving (pickle.loads(data)).

3.TenSEAL
Purpose: Provides homomorphic encryption capabilities using CKKS encryption.
Workings in Code:
i.The client encrypts numerical values using ts.ckks_vector().
ii.The server performs encrypted arithmetic operations on these values without decrypting them.
iii.The results are sent back to the client, which decrypts them to get the final values.

4.Tkinter
Purpose: Used for creating the GUI (Graphical User Interface) of the client application.
Workings in Code:
i.Provides an interface where users can enter numbers and choose an operation (add, subtract, multiply, divide).
ii.Displays the encrypted computation results in a text box.

Installation of Required Packages
To run this project, install the following dependencies:

1.Install TenSEAL for Homomorphic Encryption
  
  First, install its dependencies:
  sudo apt install cmake g++ python3-dev
  
  Then, install TenSEAL:
  
  pip install tenseal

2.Install Pickle (Included in Python Standard Library)
  
  No separate installation is required since pickle comes with Python.

3.Install Tkinter for GUI Development

  For Linux:
  sudo apt-get install python3-tk

  For Windows: 
  Tkinter is pre-installed with Python.

4.Install Socket (Included in Python Standard Library)
  
  No installation is needed as it is built into Python.

Detailed Explanation of the Key Functions

1. Socket Communication (Client-Server Interaction)
   Server Side (handle_client(conn))
      i.Receives encrypted data from the client.
      ii.Deserializes the data using pickle.loads().
      iii.Uses the TenSEAL context to perform homomorphic operations.
      iv.Sends the encrypted results back to the client.
   Client Side (send_data_to_server_and_receive(data))
      i.Connects to the server using socket.connect().
      ii.Sends encrypted data.
      iii.Receives encrypted computation results and decrypts them.

2.Homomorphic Encryption Using TenSEAL
  Context Setup (setup_encryption())
      i.Defines encryption parameters (CKKS scheme, polynomial degree, etc.).
      ii.Generates necessary keys for encryption.
  Encryption (encrypt_value(context, value))
      i.Converts plaintext numerical values into encrypted CKKS vectors.
  Decryption (decrypt_result(context, encrypted_result))
      i.Converts encrypted results back into plaintext after receiving from the server.

3. GUI Implementation Using Tkinter
   Main GUI Class (HomomorphicEncryptionGUI)
      i.Creates buttons for mathematical operations (Add, Subtract, Multiply, Divide).
      ii.Takes user input and encrypts it before sending to the server.
      iii.Displays decrypted results after performing homomorphic computations.

Final Summary
This project demonstrates how to use homomorphic encryption to securely perform mathematical operations on encrypted data. The client encrypts user input, sends it to the server, which performs computations without decrypting the values, and returns the encrypted result. The client then decrypts and displays the final result.
This implementation is useful for privacy-preserving computations, such as secure medical data processing, financial transactions, and cloud computing applications where sensitive data must remain encrypted throughout the process.
