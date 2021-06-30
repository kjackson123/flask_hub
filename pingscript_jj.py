# Import modules
import subprocess
import ipaddress
import socket

# Prompt the user to input a network address
net_addr = raw_input("Enter a network address in CIDR format(ex.192.168.1.0/24): ")

#print(net_addr)

# Create the network
ip_net = ipaddress.ip_network(unicode(net_addr))
#print(ip_net)


# Get all hosts on that network
all_hosts = list(ip_net.hosts())
#print(str(all_hosts[0]))

# Configure subprocess to hide the console window
# info = subprocess.STARTUPINFO()
# info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
# info.wShowWindow = subprocess.SW_HIDE

# For each IP address in the subnet,
# run the ping command with subprocess.popen interface
for i in range(75,79):
    output = subprocess.Popen(['ping', '-c', '1', '-w', '2', '-W', '3', str(all_hosts[i])],stdout=subprocess.PIPE)
    res = str(output)
    out = output.communicate() 
    #print(out)
	
    if "Destination host unreachable" in out
        print(str(all_hosts[i]), "is Offline(host unreachable)")
    elif "Request timed out" in res.decode('utf-8'):
        print(str(all_hosts[i]), "is Offline(timedout)")
    else:
        print(str(all_hosts[i]), "is Online")


#subprocess.Popen
#stdout=subprocess.PIPE

#range(len(all_hosts)