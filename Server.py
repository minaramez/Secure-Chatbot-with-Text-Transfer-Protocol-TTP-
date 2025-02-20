import socket #network functions - used in this code to create sockets, bind sockets, send and recieve data
from datetime import datetime #module used to get the current date and time
import webbrowser #module that allows for searching and opening urls
import random #library that generates random numbers but can also generate random letters when working with string libray
import string #library that has preset ascii and digits. can be randomized when working with random library


#open socket using IPv4, UDP connection.
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#claiming the server address
server_address = ("localhost", 8000)

#printing server address in a presentable form
print("starting up on {} port {}".format(*server_address))

#constantly listening to incoming traffic from server_address
server.bind(server_address)

#defining method to send confirmation message to client CC
def send_confirmation_CC(server):
    confirmation_message = "(CC)"
    server.sendto(confirmation_message.encode(), client_address)

#defining method to send confirmation message to client SK
def send_confirmation_SK(server):
    confirmation_message = "(SS)"
    server.sendto(confirmation_message.encode(), client_address)

#defining method to send confirmation message to client EE
def send_confirmation_EE(server):
    confirmation_message = "(EE)"
    server.sendto(confirmation_message.encode(), client_address)

#defining method to generate session key to send to client later.
#session key is generated using string and random modules, and uses ascii letters and numbers and it loops 8 times to create 8 random digits/numbers
#the returned value is a combination of 8 random digits/numbers with no spaces
def generate_session_key():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(8))



#this is a crucial defining methon in the code. it takes the argument message and finds a response for it and returns packet and response that allign with the message
def handle_client_message(message):
    if "hello" in message:
        response = (
            "Greetings (packet-type: GR)\n"
            "Response: Hey! Hope you are doing well.")
        return response

    elif "good" in message:
        words = message.split()
        if len(words) == 1:
            response = "Greetings (packet-type: GR)"
            return response
        elif len(words) >= 2:
            greeting = words[1]
            response = (
                "Greetings (packet-type: GR)\n"
                f"{('Response: Good Morning right back at ya!' if greeting == 'morning' else 'Response: Hey friend, good day!')}"
            )
            return response
        
        else:
            return "Invalid message format."

    #for words like what, where, when, the message is split so that the packet can be sent according to "what", and the response can be sent according to the second word
    elif "what" in message:
        words = message.split()
        if len(words) == 1:
            response = "Information Response (packet-type: IR)"
            return response
        elif len(words) >= 2:
            query = words[1:]
            response = []
            if 'rit' in query:
                response.append("Response: RIT is an American University with 5 campuses.")
            elif 'python' in query:
                response.append("Response: Python is one of the easiest programming languages.")
            elif 'heart' in query:
                response.append("Response: The heart is an important organ in the human body.")
            elif 'shawarma' in query:
                response.append("Response: Shawarma is a sandwich consisting of meat or chicken, garlic sauce, pickles, and other vegetables in Lebanese bread.")
            elif 'computer' in query:
                response.append("Response: A computer is a device used to perform technological operations.")
            else:
                response.append("Response: Your query seems to be incorrect. Type 'help' for help.")
            response = "\n".join([
                "Information Response (packet-type: IR)",
                *response
            ])
            return response
        else:
            return "Invalid message format." 

    elif "where" in message:
        words = message.split()
        if len(words) == 1:
            response = "Location Response (packet-type: LR)\n"
            return response
        elif len(words) >= 2:
            location = words[1:]
            response = []
            if 'home'in location:
                response.append("Response: Home is in Downtown Dubai, Beside Dubai Mall.")
            elif 'rit'in location:
                response.append("Response: RIT is located in Dubai Silicon Oasis, United Arab Emirates.")
            elif 'kfc'in location:
                response.append("Response: The nearest KFC is in Dubai Silicon Oasis.")
            elif 'toilet'in location:
                response.append("Response: The nearest toilet is on the ground floor.")
            elif 'dubai'in location:
                response.append("Response: Dubai is located in the United Arab Emirates.")
            else:
                response.append("Response: Required location could not be found. Type 'help' for help.")
            response = "\n".join([
                "Location Response (packet-type: LR)",
                *response
            ])
            return response
        else:
            return "Invalid message format." 

    elif "when" in message:
        words = message.split()
        if len(words) == 1:
                response = (
                    "Time Response (packet-type: TR)\n"
                    f"Response: After Tomorrow, but i suggest you ask me 'when time', i will give you the time right now!"
                )
                return response
        elif len(words) >= 2:
            time = words[1:]
            if "time" in time:
                #below is produced using datetime python module
                #datetime.now() creates a datetime object from the library for the current date and time
                #the .strftime() is a method of datetime and it formats obejcts as strings
                #%Y is year, %m is month, %d is day of the month, %H is hour, %M is minute, %S is second
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
                response = (
                    "Time Response (packet-type: TR)\n"
                    f"Response: The current time is: {current_time}"
                )
                return response
        else:
            return "Invalid message format."
        
    elif "search" in message:
        words = message.split()
        if len(words) == 1:
            response = "Google Search (packet-type: RR)"
            return response
        elif len(words) >= 2:
            target = message[7:]
            url = f"https://www.google.com/search?q={target}"
            #standard function of webbrowser module .open takes an argument which is our URl. 
            #This results in the code opening the OS default browser and searches google for the second word of the input
            webbrowser.open(url)
            response = (
                "Google Search (packet-type: RR)\n"
                f"Response: Searching Google for {target}."
            )
            return response
    
    #if user inputs help, the result is a list of applicable inputs the user may use
    elif message == 'help':
        response = (
            "It seems like you need help. \n"
            "Firstly, make sure your inputs are lowercase\n"
            "\n"
            "Here is a list of inputs you may use:\n"
            "Greeting: You may enter 'hello' or anything starting with 'good'\n"
            "Ex: hello, good morning, good evening.\n"
            "\n"
            "Query (what): your may enter your query in the form of: what ________\n"
            "Things you may ask about: rit, python, heart, shawarma, computer\n"
            "There is no specific format to the query. you may input 'what is rit' or 'what does rit mean'\n"
            "\n"
            "Location (where): your may enter your query in the form of: where ________\n"
            "Things you may ask about: home, rit, kfc, toilet, dubai\n"
            "There is no specific format to the query. you may input 'where is rit' or 'where can i find rit'\n"
            "\n"
            "Time (when): your may enter your query in the form of: when /__ time\n"
            "There is no specific format to the query. you may input 'when' or 'when is the time' or 'when time'\n"
            "\n"
            "authentication: permission - for '(EC, Authentication, username:password)' algorithm only \n"
            "\n"
            f"search: 'search _________' <-- Fill the blank with target to search. There are no limits to this code or to google!"
        )
        return response


#this defining method is wrapped in a try-except block by which this section of the code handles if 'permission' is in the message the user inputs
def handle_permission(message, client_address):
    try:
        #since the client handles the fact that only users using authentication algorithm may send 'permission', the code is set to only be concered 
        #with handling the message, and not the type of the algorithm along with the message, unlike the client code which is concerned with both.
        if "permission" in message:
            perm_packet = "Credentials (packet-type: PR)"
            server.sendto(perm_packet.encode(), client_address) #sending credentials packet to the client
            auth_request = "Enter your username and password in the format 'username:password': "
            server.sendto(auth_request.encode(), client_address) #sending request for authentication to the client
            auth_submit, client_address = server.recvfrom(4096) #recieving username:password from user
            auth_submitserv = auth_submit.decode()
            if auth_submitserv == userpassdec: #checking if the username:password is the same as saved username:password from intialization of execution
                granted = ("Access granted.") 
                server.sendto(granted.encode(), client_address) #if they are equal, access granted is sent to the user
                print("Sending Response: ", granted)
                return granted
            else:
                denied = ("Access denied.")
                server.sendto(denied.encode(), client_address) #if not equal, access denied is sent to the user
                print("Sending Response: ", denied)
                return denied
    except PermissionError as PE: #in the unlikely case of an error, a permission error is raised and sent to the user as an EE packet, along with the error message
        peerror = "Exception-Event-Packet (EE): " + str(PE)
        server.sendto(peerror.encode(), client_address)


#the purpose of this while loop is to run the code from the beginning again if the user inputs 'end'
while True:
    print("\nwaiting to receive message")
    print("")

    #the server recieves the first thing the client sends, the encryption packet (SS, TTP, v1.0, 0)/(SS, TTP, v1.0, 1)
    encryption_packet, client_address = server.recvfrom(4096)

    #the server recieves the second thing the client sends, the encryption information (EC, DES, client_session_key)/(EC, Authentication, username:password)
    encryption_info, client_address = server.recvfrom(4096)
    print("Session Information:")

    #the .format() is used to place the arguments encryption_packet and client_address in the corresponding {}, and len() is used to retrieve the bytes of a certain argument.
    print("received {} bytes from {}".format(len(encryption_packet), client_address))

    #since the encryption packet is sent in the form of (SS, TTP, v1.0, 0/1), we want to skip everything 
    #and only get the 0/1 at the end. this is going to tell us if there is encyption or not.
    #the way we do this is by using _ which are placeholders for something we dont require.
    #we then decode encryption.packet and split it at this point, our result would be ' 1)' or ' 0)'
    _, _, _, encryption_required = encryption_packet.decode().split(',')

    #we tackle the space and the ')' by choosing the 2nd character in the stripped encryption_required. 
    encryption_required_split = encryption_required[1].strip()
    encryption_algorithm = encryption_info.decode()

    #we can now compare our encryption_required value with preset values using an if block.
    #if encryption_required_split, which was initally the user input on the client side, is 1, then encryption is required, and the packet and algorithm as printed.
    if encryption_required_split == "1":
        print("Encryption is required: ", encryption_packet.decode())
        print("Encryption Algorithm:", encryption_algorithm)

        #within the first if block, there is another if block that checks if the encryption_algorithm matches with present data
        if encryption_algorithm == "(EC, DES, client_session_key)":

            #if the algorithm is DES, SK is sent, and a session key is generated and sent along with its required packet.
            send_confirmation_SK(server)
            sessionkey = generate_session_key()
            sessionkeypacket = f"(SK, {sessionkey})"
            print('sending session key: ', sessionkeypacket)
            send = server.sendto(sessionkeypacket.encode(), client_address)

        #if the algorithm is Auth., CC is sent, and username:password is recieved from the client
        elif encryption_algorithm == "(EC, Authentication, username:password)":
            send_confirmation_CC(server)
            userpass, client_address = server.recvfrom(4096)
            print("received username:password  :", userpass.decode())
            userpassdec = userpass.decode()

    #if encryption is not required, encryption packet is printed and EE is sent
    elif encryption_required_split == "0":
        print("Encyption is NOT required: ", encryption_packet.decode())
        send_confirmation_EE(server)

    #the second while loop within the first while loop. this while loops serves the purpose of recieving messages from the client infintely many times
    #until the client inputs 'end'
    while True:
        #the message is recieved fromr the client and then decoded
        clientmessagecall, client_address = server.recvfrom(4096)
        print("")
        print("Recieved Message:", clientmessagecall.decode())

        #message is initalized as clientmessagecall.decode()
        message = clientmessagecall.decode()

        #the code detects if permission is in the message, and sends it to the handle_permission method
        #we dont need to worry about algorithms in the server code because the client code handled it and only allowed 
        #authentication algorithm users to input permission
        if "permission" in message:
            handle_permission(message, client_address)

        #if the message is end, the end packet is recieved from the client, and a goodbye message is sent to 
        #the client and the while loop is broken, and the code starts the first while loop again and listens to incoming traffic
        elif message == "end":
            endpacket, client_address = server.recvfrom(4096)
            print("Recieved Packet: ", endpacket.decode())
            endsend = ("From Your Favorite Student's Server to you, Our Favorite Professor: GoodBye! Hope to see you again.")
            print("Sending Response: ", endsend)
            server.sendto(endsend.encode(), client_address)
            break
        
        #else block that handles all other messages, like when, where, hello, etc. 
        else:
            #the try block tries to get a response from the handle_client_method method
            try:
                response = handle_client_message(message)
                print("Sending Response: ", response)
                server.sendto(response.encode(), client_address)
            
            #if unable to find a match, it raises an exception as userinputerror, and sends the error packet EE, along with the error to the client.
            except Exception as userinputerror:
                print("Response Not Found, Sending Error Packet")
                userinputerror = (
                    "Exception-Event-Packet (EE)\n"
                    "Your Input is Incorrect. Type 'help' for help.")
                server.sendto(userinputerror.encode(), client_address)