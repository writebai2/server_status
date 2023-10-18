import subprocess
from collections import OrderedDict


class Server_info():
    def BatchCMD(self, command):
        # 执行命令
        try:
            obj = subprocess.Popen(command, shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
            result_err = obj.stderr.read().decode()

            if len(result_err) != 0:
                print('命令: {} 执行错误,err: {}'.format(command, result_err))
                return None

            result = obj.stdout.read().decode()
            if len(result) != 0:
                return result
            else:
                return None
        except Exception as e:
            print('命令: {} 执行错误,err: {}'.format(command, e))
            return None

    def server_name(self):
        # 获取服务器名称
        name = self.BatchCMD('hostname').replace("\n", "")
        return name

    def server_cpu_number(self):
        # 获取cpu核数
        cmd = "cat /proc/cpuinfo  | grep 'processor' | wc -l"
        cpu_number = self.BatchCMD(cmd).replace("\n", "")
        return cpu_number

    def server_mem(self):
        # 内存使用情况
        # cmd = "vmstat 2 1 | awk 'NR==3 {print $4 \":\" $5 \":\" $6}'"
        cmd = "free -m | awk 'NR==2{print $2 \":\" $4 \":\" $6}'"
        os_ref = self.BatchCMD(cmd)
        mem_total = round(int(os_ref.split(":")[0].replace("\n", "")) / 1024, 2)
        mem_free = round(int(os_ref.split(":")[1].replace("\n", "")) / 1024, 2)
        mem_buf = round(int(os_ref.split(":")[2].replace("\n", "")) / 1024, 2)
        percentage = round(100 - ((mem_free + mem_buf) / mem_total) * 100, 2)
        ref_dict = {"mem_total": mem_total, "mem_free": mem_free, "percentage": "{}%".format(percentage)}
        return ref_dict

    def server_cpu(self):
        # 计算cpu使用率
        cmd = "vmstat  | awk 'END {print $13 \":\" $14 \":\" $15}'"
        os_ref = self.BatchCMD(cmd).replace("\n", "")
        os_list = os_ref.split(":")
        ref_dict = {"us": os_list[0], "sys": os_list[1], "idea": os_list[2]}
        return ref_dict

    def server_cpu_load(self):
        # cpu 15分钟 负载统计
        cmd = "cat /proc/loadavg | awk '{print $1 \":\" $2 \":\" $3}'"
        os_ref = self.BatchCMD(cmd).replace("\n", "")
        os_list = os_ref.split(":")
        ref_dict = {"1avg": os_list[0], "5avg": os_list[1], "15avg": os_list[2]}
        return ref_dict

    def server_disk(self):
        # 统计磁盘信息
        disks = ["/"]
        num = 1024 * 1024
        disk_dic = {}
        for disk in disks:
            cmd = "df {} | awk 'NR==2{{print $2 \":\" $4 \":\" $5}}'".format(disk)
            os_ref = self.BatchCMD(cmd).replace("\n", "")
            os_list = os_ref.split(":")
            disk_total = round(float(os_list[0]) / num, 2)
            disk_free = round(float(os_list[1]) / num, 2)
            percentage = os_list[2]
            ref_dict = {"disk_total": disk_total, "disk_free": disk_free, "percentage": percentage}
            disk_dic = {"/": ref_dict}
        return disk_dic

    def server_process_number(self):
        # 统计进程数
        cmd = "ps -ef | wc -l"
        process_number = self.BatchCMD(cmd)
        if process_number is not None:
            process_number = int(process_number) - 2
        return process_number

    def server_disk_io(self):
        # 磁盘io统计
        cmd = "vmstat 2 1 | awk 'NR==3{print $16}'"
        disk_io = self.BatchCMD(cmd).replace("\n", "")
        return disk_io

    def server_network(self):
        # 测试网络状态码
        cmd = "curl -sI  https://www.baidu.com | grep 'HTTP' | awk '{print $2}'"
        http_status = self.BatchCMD(cmd)
        if http_status is None:
            cmd = "curl -sI  https://www.google.com.hk | grep 'HTTP' | awk '{print $2}'"
            http_status = self.BatchCMD(cmd)
        if http_status is None:
            return http_status
        http_status = http_status.replace("\n", "")
        return http_status

    def server_ip(self):
        cmd = "hostname -I | awk '{print $1}'"
        ip = self.BatchCMD(cmd).replace("\n", "")
        return ip


def main():
    ssh = Server_info()
    server_dict = OrderedDict()

    server_dict["name"] = ssh.server_name()
    server_dict["address"] = ssh.server_ip()
    server_dict["cpu_number"] = ssh.server_cpu_number()
    server_dict["cpu"] = ssh.server_cpu()
    server_dict["cpu_load"] = ssh.server_cpu_load()
    server_dict["mem"] = ssh.server_mem()
    server_dict["disk"] = ssh.server_disk()
    server_dict["disk_io"] = ssh.server_disk_io()
    server_dict["process_number"] = ssh.server_process_number()
    server_dict["network"] = ssh.server_network()
    print(server_dict)


if __name__ == "__main__":
    main()
