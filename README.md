# **🔐 Secure Chatbot with Text Transfer Protocol (TTP)**  
**📌 Educational Project - Not for Production Use**  

## **📖 About the Project**
This project is an **educational implementation** of a **secure chatbot system** using a **custom Text Transfer Protocol (TTP)** over **UDP sockets** in Python. The system includes:  
- **A Client Application** (`Client.py`)  
- **A Server Application** (`Server.py`)  

The chatbot can **answer predefined queries**, **search Google**, **provide location and time information**, and **authenticate users using username-password or DES encryption**.  

## **🚀 Features**
✅ **Implements a Custom Text Transfer Protocol (TTP)**  
✅ **Supports Secure and Non-Secure Communication**  
✅ **User Authentication & Encryption (DES or Password-Based)**  
✅ **Handles Various Query Types ("what", "where", "when", "search")**  
✅ **Google Search Integration**  
✅ **Permission-Based Access for Certain Queries**  
✅ **Multithreaded UDP Server**  
✅ **Error Handling and Exception Packets (EE)**  

---

## **⚠️ Disclaimer**
**This project is strictly for educational purposes.**  
❌ **Do NOT use it in real-world secure communications.**  
❌ **It does not implement real encryption (e.g., TLS/SSL).**  
❌ **User authentication is not securely stored or hashed.**  

---

## **📜 Protocol Design (Text Transfer Protocol - TTP)**
TTP is a **custom protocol** designed to facilitate **client-server communication** for chatbot functionality. It operates in **three phases**:

### **1️⃣ Setup Phase**
1. **Start-Packet (SS)** – Sent from **Client → Server** to initiate communication.  
   - `(SS, TTP, v1.0, 0)` → No encryption  
   - `(SS, TTP, v1.0, 1)` → Encryption required  

2. **Encryption-Packet (EC)** – Sent by the client if encryption is required.  
   - `(EC, DES, client_session_key)` → Uses DES encryption  
   - `(EC, Authentication, username:password)` → Uses plain authentication  

3. **Confirm-Connection-Packet (CC)** – Sent from **Server → Client** to confirm a successful connection.  

4. **Session-Key-Packet (SK)** – Sent from **Server → Client** if using **DES encryption**.  

---

### **2️⃣ Operation Phase**
After setup, the client can **send queries** to the server. The server **responds** with predefined responses based on message content:

| **Client Query**       | **Server Response** (Packet-Type) |
|------------------------|----------------------------------|
| "hello", "good morning" | Greetings (GR) |
| "what is X?"          | Information Response (IR) |
| "where is X?"        | Location Response (LR) |
| "when is X?"         | Time Response (TR) |
| "search X"           | Google Search Response (RR) |
| "permission" (Auth users only) | Permission Response (PR) |

---

### **3️⃣ Closing Phase**
- If the client sends `"end"`, the server responds with a **Close-Packet (ED)** and terminates the session.

---

## **💻 Installation & Usage**
### **🔹 Prerequisites**
- Python 3  
- A terminal or shell environment  

### **🔹 Clone the Repository**
```bash
git clone https://github.com/minaramez/Secure-Chatbot-with-Text-Transfer-Protocol-TTP-.git
cd Secure-Chatbot-with-Text-Transfer-Protocol-TTP-
```

### **🔹 Running the Server**
```bash
python3 Server.py
```

### **🔹 Running the Client**
```bash
python3 Client.py
```

---

## **📝 Example Usage**
### **1️⃣ Start the Server**
```
starting up on localhost port 8000
waiting to receive message
```

### **2️⃣ Start the Client**
```
Click 1 For Encrypting this Chat, or Click Enter for No Encryption: 1
Type 1 for DES, Press enter for Authentication:
Using Authentication with username and password
sending username:password: a1b2c:3d4e5f
received confirmation: (CC)
```

### **3️⃣ Querying the Chatbot**
**Client:**
```
what is python?
```
**Server Response:**
```
Information Response (IR)
Response: Python is one of the easiest programming languages.
```

### **4️⃣ Ending the Chat**
**Client:**
```
end
```
**Server:**
```
Received Packet: (ED)
Sending Response: Goodbye! Hope to see you again.
```

### License
This script is released under the **MIT License**, which allows modification, distribution, and use with minimal restrictions.