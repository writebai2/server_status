from fabric import Connection


class MyCmd():
    # 自定义ssh连接处理
    def __init__(self, host, user='root',
                 authentication={"type": "", "passwd": ""},
                 timeout=30, port=22):
        self.host = host
        self.user = user
        self.type = authentication['type']
        self.port = port
        self.passwd = authentication['passwd']
        self.timeout = timeout
        self.conn = self._get_conection()

    def _get_conection(self):
        try:
            match self.type:
                case 'password':
                    conn = Connection(
                        host=self.host,
                        user=self.user,
                        port=self.port,
                        connect_kwargs={
                            "password": self.passwd
                        },
                        connect_timeout=self.timeout,
                    )
                case 'key_filename':
                    conn = Connection(
                        host=self.host,
                        user=self.user,
                        port=self.port,
                        connect_kwargs={
                            "key_filename": self.passwd
                        },
                        connect_timeout=self.timeout
                    )
                case _:
                    conn = Connection(
                        host=self.host,
                        user=self.user,
                        connect_timeout=self.timeout
                    )
            conn.open()
            return conn
        except Exception:
            raise Exception('SSH conection is err')

    def excet_cmd(self, cmd, hide=True, warn=True):
        if not self.conn:
            print("SSH connection failed. Command not executed")
            return None

        try:
            result = self.conn.run(cmd, encoding='utf-8', hide=hide, warn=warn)

            stdout, stderr = result.stdout.strip(), result.stderr.strip()
            if stderr:
                return stderr
            return stdout
        except Exception as e:
            raise e

    def server_name(self):
        # 获取服务器名称
        name = self.excet_cmd('hostname')
        return name

    def server_cpu_number(self):
        # 获取cpu核数
        cmd = "cat /proc/cpuinfo  | grep 'processor' | wc -l"
        cpu_number = self.excet_cmd(cmd)
        return cpu_number

    def server_mem(self):
        # 内存使用情况
        cmd = "free -m | awk 'NR==2{print $2 \":\" $4 \":\" $6}'"
        os_ref = self.excet_cmd(cmd)
        mem_total = round(int(os_ref.split(":")[0]) / 1024, 2)
        mem_free = round(int(os_ref.split(":")[1]) / 1024, 2)
        mem_buf = round(int(os_ref.split(":")[2]) / 1024, 2)
        percentage = round(100 - ((mem_free + mem_buf) / mem_total) * 100, 2)
        ref_dict = {"mem_total": f"{mem_total}G",
                    "mem_free": f"{mem_free}G", "percentage": f"{percentage}%"}
        return ref_dict

    def server_cpu(self):
        # 计算cpu使用率
        cmd = "vmstat  | awk 'END {print $13 \":\" $14 \":\" $15}'"
        os_ref = self.excet_cmd(cmd)
        os_list = os_ref.split(":")
        ref_dict = {
            "us": f"{os_list[0]}%", "sys": f"{os_list[1]}%", "idea": f"{os_list[2]}%"}
        return ref_dict

    def server_cpu_load(self):
        # cpu 15分钟 负载统计
        cmd = "cat /proc/loadavg | awk '{print $1 \":\" $2 \":\" $3}'"
        os_ref = self.excet_cmd(cmd)
        os_list = os_ref.split(":")
        ref_dict = {"1avg": os_list[0],
                    "5avg": os_list[1], "15avg": os_list[2]}
        return ref_dict

    def server_disk(self):
        # 统计磁盘信息
        disks = ["/"]
        num = 1024 * 1024
        disk_dic = {}
        for disk in disks:
            cmd = f"df {disk} | awk 'NR==2{{print $2 \":\" $4 \":\" $5}}'"
            os_ref = self.excet_cmd(cmd)
            os_list = os_ref.split(":")
            disk_total = round(float(os_list[0]) / num, 2)
            disk_free = round(float(os_list[1]) / num, 2)
            percentage = os_list[2]
            ref_dict = {"disk_total": f'{disk_total}G',
                        "disk_free": f'{disk_free}G', "percentage": percentage}
            disk_dic = {"/": ref_dict}
        return disk_dic

    def server_process_number(self):
        # 统计进程数
        cmd = "ps -ef | wc -l"
        process_number = self.excet_cmd(cmd)
        if process_number is not None:
            process_number = int(process_number) - 2
        return process_number

    def server_disk_io(self):
        # 磁盘io统计
        cmd = "vmstat 2 1 | awk 'NR==3{print $16}'"
        disk_io = self.excet_cmd(cmd)
        return disk_io

    def server_network(self):
        # 测试网络状态码
        cmd = "curl -sI  https://www.baidu.com | grep 'HTTP' | awk '{print $2}'"
        http_status = self.excet_cmd(cmd)
        if http_status is None:
            cmd = "curl -sI  https://www.google.com.hk | grep 'HTTP' | awk '{print $2}'"
            http_status = self.excet_cmd(cmd)
        if http_status is None:
            return http_status
        http_status = http_status
        return http_status

    def close_conn(self):
        # 关闭连接
        self.conn.close()
