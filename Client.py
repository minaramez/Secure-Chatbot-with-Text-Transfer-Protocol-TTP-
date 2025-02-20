import socket #network functions - used in this code to create sockets, bind sockets, send and recieve data
import random #library that generates random numbers but can also generate random letters when working with string libray 
import string #library that has preset ascii and digits. can be randomized when working with random library

#open socket using IPv4, UDP connection.
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

server_address = ('localhost', 8000) 

#this defining method is used to send to the server all the session information required for the server and the client to initalize the connection.
#what is sent to the server is in the following form:
#(SS, TTP, v1.0, is always sent to the server as a standard
#encryption required, and encryption info are user input that are filled in after the standard packet depending on what the user chooses.
#for example, if a user chooses encryption and chooses DES, the packet sent to the server will look like the following: 
# (SS, TTP, v1.0, 1)
#(EC, DES, client_session_key) or (EC, Authentication, username:password)
def send_encryption_info(client, encryption_required, encryption_info): 
    encryption_packet = f"(SS, TTP, v1.0, {encryption_required})"
    client.sendto(encryption_packet.encode(), server_address) 
    client.sendto(encryption_info.encode(), server_address) 

#similarly to the above function, if the user chooses no encryption, the packet sent will be standard: (SS, TTP, v1.0, 0)
#an empty string fills encryption_info if no encryption to avoid more complex code on the server side.
def send_encryption_info_if_no_enc(client, encryption_info): 
    encryption_packet = f"(SS, TTP, v1.0, 0)"
    client.sendto(encryption_packet.encode(), server_address) 
    client.sendto(encryption_info.encode(), server_address) 

#this defining method will recieve the confirmation from the server, either CC, SS, or EE. Depending on the encryption status.
#it recieves confirmation_message from the server, decodes it, and prints it.
#confirmation message stores the data recieved from the client and server_address recieves the address of the server
def receive_confirmation(client):
    confirmation_message, server_address = client.recvfrom(4096) 
    print("received confirmation: ", confirmation_message.decode()) 

#the next two defining methods will create a username:password using string and random libraries. 
#the username will only contain lowercase letters, so letters is defined as a string with the present string function ascii lowercase
# ''.join() will join all the randomized characters and the '' ensures that there are no spaces between the characters
#inside the join, random is used with the preset function choice to randomly choose.
#random.choice randomly chooses a letter based on the range of the for loop provided for the function.
def generate_username():
    letters = string.ascii_lowercase
    username = ''.join(random.choice(letters) for _ in range(5))
    return username

#password is similar to the above function, except characters is defined as both, ascii letters and digits. 
def generate_password():
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for _ in range(7))
    return password

#defining method that will be called inside the while loop later in the code. Its purpose is to take the user input for the message. 
#it is basically a simple input that will be called multiple times within the code.
def handle_client_message():
    print("")
    client_message = input("Please enter your message: ")
    return client_message

#simple input that will take the users choice of 1 or Enter for encryption or no encryption.
encryption_required = input("Click 1 For Encypting this Chat, or Click Enter for No Encryption: ") 
print("")


#The entire code is wrapped in this try-except block. 
try:

    #in this if block, if the user input 1 (Yes for Encryption), the user will be asked the kind of encryption they want to use.
    if encryption_required == "1":
        
        #simple input for kind of encryption. 1 for DES, Enter for Authentication.
        encryption_algorithm = input("Type 1 for DES, Press enter for Authentication: ")
        print("")


        if encryption_algorithm == "1":
            #packet that will be sent to the server will look like: (SS, TTP, v1.0, 1)
            encryption_info = "(EC, DES, client_session_key)"

            #this try-except block will call send_encrypt_info and pass encryption_required and encrypted_info
            #since this is DES, (SS, TTP, v1.0, 1) and (EC, DES, client_session_key) will be sent
            try:
                send_encryption_info(client, encryption_required, encryption_info)
                receive_confirmation(client)
                print("")
                print("Using DEC with Session Key")

                #client recieves session key from the server after sending encryption information
                sessionkey, server_address = client.recvfrom(4096)
                print("received session key:", sessionkey.decode())


            except Exception as e:
                print("Exception-Event-Packet from Client Side (EE): ", e)
        
        #Similar to above if block. If user inputs enter or any other input (except 1), the client will send (SS, TTP, v1.0, 1) and (EC, Authentication, username:password) packets to server
        elif encryption_algorithm == "" or encryption_algorithm != "1":
            encryption_info = "(EC, Authentication, username:password)"
            try:
                send_encryption_info(client, encryption_required, encryption_info)
                receive_confirmation(client)
                print("Using Authentication with username and password")

                #client generates the username and password, combines them in the form of username:password, prints them, and sends the combined version to server.
                username = generate_username()
                password = generate_password()
                userpass = f"{username}:{password}"

                print("sending username:password:", userpass)
                userpasssend = client.sendto(userpass.encode(), server_address)
                
            except Exception as e:
                print("Exception-Event-Packet from Client Side (EE): ", e)

    #this else if block serves the purpose of no encryption. it takes Enter key or anything except 1 for the encryption_required input
    #this function keeps encryption_info as empty string, since there isnt an encryption algorithm. 
    #in the case of no encryption, send_encryption_info_if_no_enc is called. this is similar to the send_encryption_info_ block, 
    #except it passes an empty string to encryption_info, and doesnt take an argument for encryption_required
    #what is sent to the server is (SS, TTP, v1.0, 0)  
    elif encryption_required == "" or encryption_required != "1":
        encryption_info = ""
        send_encryption_info_if_no_enc(client, encryption_info)        
        receive_confirmation(client)
        print("Not using Encryption")

    #this while true handles all the client messages. it repeats infintely many times until the user inputs 'end'
    while True:

        #this calls clientmessagecall to take user input and return client message
        clientmessagecall = handle_client_message()

        #this if block checks if the user's message contains the word "permission".
        #if the word permission is in the message, the message goes through this if block.
        #this if block allows permission only if Authentication algorithm was chosen. 
        if "permission" in clientmessagecall:

            #if the word "permission" is present, the encryption algorithm the user is using is detected.
            #if the user is using Authentication algorithm, permission message is sent to the server which handles it accordingly (more in server comments)
            #after sending the message to the server, the client recieves an credentials packet and authentication input request
            #the client then enters their username:pasword and it is sent to the server
            if encryption_algorithm == "" or encryption_algorithm != "1":
                client.sendto(clientmessagecall.encode(), server_address)
                perm_packet,server_address = client.recvfrom(4096)
                print("Packet Type:", perm_packet.decode())
                auth_request,server_address = client.recvfrom(4096)
                auth_submit = input(auth_request.decode())
                client.sendto(auth_submit.encode(), server_address)

                #this try-except block handles the recievable from the user, either permission granted or denied, 
                #and if both, a permission error is raised from the server and sent to the client
                try:
                    granted, server_address = client.recvfrom(4096)
                    print("Authentication:", granted.decode())
                except:
                    try:
                        denied,server_address = client.recvfrom(4096)
                        print("Authentication:", denied.decode())
                    finally:
                        peerror, server_address = client.recvfrom(4096)
                        print(peerror.decode())
                        break

            #this code block handles the ocassion where the user chose DES algorithm, but entered permission as a message.
            #the while true loop will continue to loop as many times as it needs to until the user stop inputting permission
            #if permission is finally not in the user input, the loop is broken and the chatting continues
            elif encryption_algorithm == "1":
                while True:
                    print("you may not use permission with DES")
                    clientmessagecall = handle_client_message()
                    if "permission" not in clientmessagecall:
                        client.sendto(clientmessagecall.encode(), server_address)
                        response, server_address = client.recvfrom(4096)
                        print("Packet Type:", response.decode())
                        break

        #if the user enters 'end' the message and an end packet is sent, and a goodbye message is recieved from the server, and the execution is broken only on the client side.         
        elif clientmessagecall == "end":
            client.sendto(clientmessagecall.encode(), server_address)
            endpacket = ("ED")
            client.sendto(endpacket.encode(), server_address)
            endsend, server_address = client.recvfrom(4096)
            print(endsend.decode())
            client.close()
            break

        #if the user input is help, a list of applicable inputs is shown for the user.
        #this help menu is also sent from the server side.     
        elif clientmessagecall == "help":
            client.sendto(clientmessagecall.encode(), server_address)
            response, server_address = client.recvfrom(4096)
            print("")
            print(response.decode())

        #this code block handles everything that is not permission, end, or help. 
        else:
            #this try-except block handles when, where, what, search, etc.   
            try:
                client.sendto(clientmessagecall.encode(), server_address)
                response, server_address = client.recvfrom(4096)
                print("Packet Type:", response.decode())

            #this except block handles all incorrect user inputs, and suggests the help menu.
            #it recieves the error packet EE, and the error.
            except:
                userinputerror,server_address = client.recvfrom(4096)
                print("Packet Type:", userinputerror.decode())

#exception block from the client. 
except Exception:
    print ("Exception-Event-Packet from Client Side (EE)")
