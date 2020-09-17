import paramiko


def transfer_set(hostname, username, password, timestr, source_path, target_path):
    print('Transfer Set Initiated.')
    print(timestr)
    
    #FILE TRANSFER
    transport = paramiko.Transport((hostname, 22))
    transport.connect(username=username, password=password)
    print('Connected successfully...')
    sftp = paramiko.SFTPClient.from_transport(transport)
    print('Transferring files...')
    sftp.put(source_path, target_path)
    print('Successfully transferred!')
    sftp.close()