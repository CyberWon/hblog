# Python自动化运维学习（六）

标签（空格分隔）： python学习


---

# paramiko
> paramiko 是一个ssh的连接客户端。安装他可以使用下面命令
```python
pip install paramiko==1.17.0
```

## 连接单服务器
```python
import paramiko
ssh = paramiko.SSHClient()

ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ssh.connect("某IP地址",22,"用户名", "口令")

stdin, stdout, stderr = ssh.exec_command("你的命令")

print stdout.readlines()

ssh.close()
```

## 把这些封装在一个类里面
```python
import paramiko
class MySSH():
    def __init__(self,hostname=None,password=None,username=None,port=22):
        self.hostname=hostname
        self.password=password
        self.username=username
        self.port=port
        #创建一个ssh客户端
        self.s=paramiko.SSHClient()
        #连接时候自动加载策略。默认对方主机的指纹没在自己电脑上是连接不上的。
        self.s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            #在类初始化的时候就进行连接。
            self.s.connect(hostname = self.hostname,username=self.username, password=self.password,port=self.port)
        except Exception as e:
            #链接时候发生错误将错误的信息显示出来
            print(e)
    def run(self,command):
        #执行命令的输出结果是tuple（stdin,stdout,stderr）,所以这样写。获取各个对应的值
        #执行命令是通过exec_command('要执行的命令')
        stdin,stdout,stderr=self.s.exec_command(command)
        print(stdout.read())
    def close(self):
        self.s.close()
if __name__=='__main__':
    ssh1=MySSH(hostname='127.0.0.1',username='root',password='123456',port=19957)
    ssh2=MySSH(hostname='127.0.0.2',username='root',password='123456')
    ssh1.run('hostname')
    ssh2.run('hostname')
    ssh1.close()
    ssh2.close()
```
输出结果：
>VM_146_166_centos
VM_146_166_centos

## 项目实践：批量更改多服务器密码
```shell
# coding:utf-8
import random,paramiko,csv,sys
#定义随机生成密码函数
def randomPass():
    #passStr:随机从这些字符串生成组成密码
    passStr="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    #passLength:密码长度
    passLength=16
    #使用循环,每次从passStr选择一个字符赋值给newPass,直到达到passLength定义的长度
    newPass=""
    for x in xrange(passLength):
        newPass+=random.choice(passStr)
    #返回随机生成的密码
    return  newPass
#定义ssh连接函数并执行修改密码
def sshConn(hostname,username,password,edituser,newPass):
    #创建SSH连接
    ssh=paramiko.SSHClient()
    #自动添加hostkey ,使用这个是为了在Windows下面可以使用
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #修改密码的命令
    execEditPass="echo %s:"% (edituser)+"%s|chpasswd"  % (newPass)
    try:
        #开始SSH连接
        ssh.connect(hostname=hostname,username=username,password=password)
        #执行的命令
        stdin,stdout,stderr=ssh.exec_command(execEditPass)
        #输出账号修改后的信息
        print hostname+":"+edituser+":"+newPass
    #发生错误时候显示错误信息
    except Exception,e:
        print "Error:"+str(e)
    #不管运行是否正常,强制关闭ssh连接
    finally:
        ssh.close()
        return newPass
def readUser(csvUser):
    try:
        #打开账号配置文件
        userCsv=file(csvUser,'rb')
        #以csv格式 读取
        userLine=csv.reader(userCsv)
        #利用循环实现批量更改 1:hostname 2.username 3.password 4.要修改的用户名
        for user in userLine:
            #使用sshConn来进行密码更改
            sshConn(user[1],user[2],user[3],user[4],randomPass())
        userCsv.close()
    #发生错误时候显示错误信息
    except Exception,e:
        print "Error:"+str(e)
def main():
    readUser('user.csv')
if __name__=="__main__":
    main()
```
user.csv内容
,IP,用户名,密码,要修改的用户名
```csv
,123456,root,123456,shuaibo
,123456,root,123456,shuaibo
```
> 上面是我没系统学习python之前写的。试着自己使用类的形式重新写一篇。具体思路就是上面的这种