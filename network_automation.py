import paramiko
import concurrent.futures

def string_to_list(string):
    ip_list = string.splitlines()
    return ip_list

def text_to_list(file_path):
    with open(file_path, 'r') as file:
        text_list = []
        for text in file:
            text_list.append(text.replace('\n',''))
    return text_list

def ssh_device(ip_address, username, password):

    print(f'\nConnecting to IP {ip_address} ...')

    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(ip_address, '22', username, password, look_for_keys=False, allow_agent=False)

        if ssh_client.get_transport().is_active():
            print(f'Connected to IP {ip_address}')

            return ssh_client

    except:
        print(f'\nCould not connect to IP {ip_address}')

def send_command(ssh_client, command):
    stdin, stdout, stderr = ssh_client.exec_command(command)
    error = stderr.read()
    if error:
        print(error)
    else:
        return stdout.read().decode("ascii").strip("\n")

def get_hostname(ssh_client):
    hostname = ''
    output = send_command(ssh_client, 'show ver\n')
    output = output.splitlines()
    output = output[7]

    for i in output:
        if i == ' ':
            return hostname

        hostname = hostname + i

    return hostname

def get_snmp_location(ssh_client):
    snmp_location = send_command(ssh_client, 'show snmp location\n')
    return snmp_location

def theading(function, as_zid, as_account_password, ip_list):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(function, as_zid, as_account_password, ip_list)

def get_device_info(as_zid, as_account_password, ip_address):
    try:
        ssh_client = ssh_device(ip_address, as_zid, as_account_password)
        hostname = get_hostname(ssh_client)
        ssh_client = ssh_device(ip_address, as_zid, as_account_password)
        snmp_location = get_snmp_location(ssh_client)  
        device = dict(hostname = hostname,
                    ip_address = ip_address,                       
                    snmp_location = snmp_location)

        close_connection(ssh_client) 
        return device
    except:
        close_connection(ssh_client)
        print(f'{ip_address} is not reachable')

def close_connection(ssh_client):
    try:
        ssh_client.close()
        print('Conection closed')
    except:
        pass