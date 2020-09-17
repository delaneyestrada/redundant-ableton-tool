import paramiko
import os

def transfer_dir(hostname, username, password, timestr, source_path, target_path):
    print('Transfer All Initianted.')
    print(timestr)

    # MODIFY SFTPClient TO ALLOW DIRECTORY TRANSFERS
    class MySFTPClient(paramiko.SFTPClient):
        def put_dir(self, source, target):
            ''' Uploads the contents of the source directory to the target path. The
                target directory needs to exists. All subdirectories in source are 
                created under target.
            '''
            for item in os.listdir(source):
                if os.path.isfile(os.path.join(source, item)):
                    self.put(os.path.join(source, item), '%s/%s' % (target, item))
                else:
                    self.mkdir('%s/%s' % (target, item), ignore_existing=True)
                    self.put_dir(os.path.join(source, item), '%s/%s' % (target, item))

        def mkdir(self, path, mode=511, ignore_existing=False):
            ''' Augments mkdir by adding an option to not fail if the folder exists  '''
            try:
                super(MySFTPClient, self).mkdir(path, mode)
            except IOError:
                if ignore_existing:
                    pass
                else:
                    raise

   

    #FILE TRANSFER
    transport = paramiko.Transport((hostname, 22))
    transport.connect(username=username, password=password)
    print('Connected successfully...')
    sftp = MySFTPClient.from_transport(transport)
    sftp.mkdir(target_path, ignore_existing=True)
    print('Transferring files...')
    sftp.put_dir(source_path, target_path)
    print('Successfully transferred!')
    sftp.close()


    '''
    # CHECK IF TRANSFERRED DIRECTORY EXISTS
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=hostname,username=username,password=password)

    stdin, stdout, stderror = ssh.exec_command('[ -d '+ target_path + ' ] && echo exists || echo does not exist')

    while not stdout.channel.exit_status_ready() and not stdout.channel.recv_ready():
        time.sleep(1)

        stdoutstring = stdout.readlines()
        stderrstring = stderror.readlines()

        for stdoutrow in stdoutstring:
            print(stdoutrow)

        for stderr_row in stderrstring:
            print(stderr_row)    
    '''