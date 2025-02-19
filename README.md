# fuzz_dawang爆破工具

## 它支持多种协议有 ftp mysql ssh redis 和目录扫描的功能并且有两种加速方案 分别采用了线程池和异步协程的方案加速爆破进程

### 使用步骤

#### 1.pip install -r requirements.txt

#### 2.填写你要爆破的ip或域名

#### 3.选择你要爆破的协议

#### 4.等待结果

### 两个py文件是不通过的加速方案Thread fuzz.py是基于线程池 Asynchronous fuzz.py基于异步协程 
