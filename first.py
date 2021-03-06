def signallevel():

 import sys
 import time
 import select
 import paramiko


 host = '192.168.0.171'
 i = 1
 user=""
 password=""
 #
 # Try to connect to the host.
 # Retry a few times if it fails.
 #

 while True:
    print("Trying to connect to %s (%i/10)" % (host, i))

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, username=user, password=password)
        print("Connected to %s" % host)
        break
    except paramiko.AuthenticationException:
        print("Authentication failed when connecting to %s" % host)
        sys.exit(1)
    except:
        print("Could not SSH to %s, waiting for it to start" % host)
        i += 1
        time.sleep(2)

    # If we could not connect within time limit
    if i == 10:
        print("Could not connect to %s. Giving up" % host)
        sys.exit(1)

 # Send the command (non-blocking)
 stdin, stdout, stderr = ssh.exec_command("iwconfig")

 # Wait for the command to terminate
 while not stdout.channel.exit_status_ready():
    # Only print data if there is data to read in the channel
    if stdout.channel.recv_ready():
        rl, wl, xl = select.select([stdout.channel], [], [], 0.0)
        if len(rl) > 0:
            # Print data from stdout
            outt=stdout.channel.recv(2028).decode("utf-8")

 slice=outt[330:370]
 signal_level=slice[slice.find('dBm')-4:slice.find('dBm')]




 print(signal_level)
 print("Command done, closing SSH connection")
 ssh.close()

 return signal_level

with open("empty.txt", 'a') as out:
    out.write("0" + signallevel() + '\n')





