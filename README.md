# server_status
服务器常规指标采集

！！！本脚本基于python3.10版本，以下版本未测试
<!-- 如需使用脚本，请将需要统计主机信息写入 /config/host 配置文件中 -->
; 密钥认证示例
[work1]
127.0.0.1
192.168.163.200

[work1:vars]
ssh_port=22
ssh_user=root
ssh_authentication=key_filename
ssh_rsa=/develop/python/server_status/chenyunzhong

; 密码认证示例
[work2]
127.0.0.1
192.168.163.200

[work2:vars]
ssh_port=22
ssh_user=root
ssh_authentication=password
ssh_rsa=123456

; ssh认证示例
[work2]
127.0.0.1
192.168.163.200

[work2:vars]
ssh_port=22
ssh_user=root

以上为配置文件示例
运行程序：python3 main.py
运行结果，如图所示
![Alt text](image.png)