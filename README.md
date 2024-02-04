# server_status
服务器状态采集 - 多线程版

### ！！！本脚本基于python3.10版本测试，低于该版本未测试

<!-- 如需使用脚本，请将需要统计主机信息写入 /config/host 配置文件中 -->

- - -
#### 用途

```
本脚本用于采集服务器基本信息，例如cpu，内存，磁盘等内容，可自行新增采集指标

使用前，请安装python3.10或以上版本环境
服务器认证分为两种种方式，密钥、密码，请按照示例文件填写host文件
采集后会输出excel文件到本地，本脚本基于linux环境，不适用windows环境，请到服务器上运行脚本
```

------

### 线程以及队列设置
```
60：线程数
100：队列数
pool = Thread.ThreadPool(60, 100)
请根据运行主机配置，自行调整
```

#### host文件

```
; 密钥认证示例
[work1]
127.0.0.1
192.168.163.200

[work1:vars]
ssh_port=22
ssh_user=root
ssh_authentication=key_filename
ssh_rsa=./密钥文件
; 密码认证示例
[work2]
127.0.0.1
192.168.163.200

[work2:vars]
ssh_port=22
ssh_user=root
ssh_authentication=password
ssh_rsa=123456
```

以上为配置文件示例
运行程序：python3 main.py

运行结果，如图所示
![Alt text](image.png)