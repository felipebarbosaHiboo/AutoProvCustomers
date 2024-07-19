import paramiko  # Importing the paramiko module for SSH operations
import sys  # Importing sys module for system operations

# SSH details for the jump server
jump_server = {
    'hostname': 'jump.hiboonetworks.com',  # Hostname of the jump server
    'port': 4422,  # Port number for SSH connection
    'username': 'felipebarbosa',  # Username for SSH connection
    'password': 'dota-1LUNA-mouse'  # Password for SSH connection
}

# SSH details for the routers
router_credentials = {
    'username': 'admfelipeb',  # Username for SSH connection to routers
    'password': 'dota-1LUNA-mouse'  # Password for SSH connection to routers
}


# Function to read router IPs from a file
def read_router_ips(file_path):
    try:
        with open(file_path, 'r') as file:  # Open the file containing router IPs
            router_ips = file.read().splitlines()  # Read and split lines into a list
        return router_ips  # Return the list of router IPs
    except Exception as e:  # Handle any exceptions
        print(f"Error reading file: {e}")  # Print error message
        sys.exit(1)  # Exit the program


# Function to SSH into a router and execute a command
def ssh_into_router(router_ip, command):
    client = paramiko.SSHClient()  # Create a new SSH client
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Automatically add unknown host keys
    try:
        # Connect to the router
        client.connect(router_ip, username=router_credentials['username'], password=router_credentials['password'])
        stdin, stdout, stderr = client.exec_command(command)  # Execute the command on the router
        print(f"Output from {router_ip}:\n{stdout.read().decode()}")  # Print the command output
        print(f"Errors from {router_ip}:\n{stderr.read().decode()}")  # Print any errors
    except Exception as e:  # Handle any exceptions
        print(f"Error connecting to {router_ip}: {e}")  # Print error message
    finally:
        client.close()  # Close the SSH connection


# Function to set up jump server connection
def setup_jump_connection(jump_hostname, jump_port, jump_username, jump_password):
    try:
        jump_client = paramiko.SSHClient()  # Create a new SSH client for the jump server
        jump_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Automatically add unknown host keys
        jump_client.connect(jump_hostname, port=jump_port, username=jump_username,
                            password=jump_password)  # Connect to the jump server
        transport = jump_client.get_transport()  # Get the transport object for the SSH connection
        return jump_client, transport  # Return the SSH client and transport object
    except Exception as e:  # Handle any exceptions
        print(f"Failed to connect to jump server: {e}")  # Print error message
        return None, None  # Return None if connection fails


# Function to SSH into a router and execute a command via the jump server
def ssh_into_router(router_ip, command, transport):
    client = paramiko.SSHClient()  # Create a new SSH client for the router
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Automatically add unknown host keys
    try:
        client.connect(
            router_ip,
            username=router_credentials['username'],
            password=router_credentials['password'],
            sock=transport.open_channel('direct-tcpip', (router_ip, 22), ('127.0.0.1', 9999))
            # Open a direct TCP channel through the jump server
        )
        stdin, stdout, stderr = client.exec_command(command)  # Execute the command on the router
        print(f"Output from {router_ip}:\n{stdout.read().decode()}")  # Print the command output
        print(f"Errors from {router_ip}:\n{stderr.read().decode()}")  # Print any errors
    except Exception as e:  # Handle any exceptions
        print(f"Error connecting to {router_ip}: {e}")  # Print error message
    finally:
        client.close()  # Close the SSH connection


# Main function
def main():
    router_list_file = 'routers.txt'  # File containing the list of router IPs

    # Set up jump server connection
    jump_client, transport = setup_jump_connection(
        jump_server['hostname'], jump_server['port'],
        jump_server['username'], jump_server['password']
    )
    if jump_client is None or transport is None:  # Check if the jump server connection was successful
        sys.exit(1)  # Exit the program if connection fails

    try:
        router_ips = read_router_ips(router_list_file)  # Read the list of router IPs from the file
        for router_ip in router_ips:  # Iterate over each router IP
            print(f"Connecting to router {router_ip} through the tunnel...")  # Print message
            ssh_into_router(router_ip, 'show interfaces terse',
                            transport)  # SSH into the router and execute the command
    except Exception as e:  # Handle any exceptions
        print(f"\rError: {e}")  # Print error message
    finally:
        if jump_client:  # Check if the jump client is connected
            jump_client.close()  # Close the jump server connection
            print("Jump server connection closed")  # Print message


if __name__ == '__main__':  # Check if the script is being run directly
    main()  # Call the main function
