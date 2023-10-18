from fabric2 import Connection


class SSHCmd():

    def __init__(self, host, user, passwd, timeout=30, type='password', port=22):
        self.host = host
        self.user = user
        self.type = type
        self.port = port
        self.passwd = passwd
        self.timeout = timeout
        self.conn = self._conection()

    def _conection(self):
        match self.type:
            case 'password' | "key_filename":
                conn = Connection(
                    host=self.host,
                    user=self.user,
                    connect_kwargs={
                        type: self.passwd
                    },
                    connect_timeout=self.timeout
                )
            case _:
                conn = Connection(
                    host=self.host,
                    user=self.user,
                    connect_timeout=self.timeout
                )
        return conn

    def cmd(self, cmd, hide=True, warn=True):
        try:
            result = self.conn.run(cmd, encoding='utf-8', hide=hide, warn=warn)

            stdout, stderr = result.stdout.strip(), result.stderr.strip()
            if stderr:
                raise stderr
            return stdout
        except Exception as e:
            print(e)
            raise e
