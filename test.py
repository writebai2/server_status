from ssh import Cmd

if __name__ == "__main__":
    host = '192.168.204.128'
    user = 'root'
    password = '123456'
    conn = Cmd.SSHCmd(host=host, user=user, passwd=password)
    conn.cmd('pwd')
