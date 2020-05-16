---
title: ubuntu15.04搭建OpenVPN服务器
date: 2016-09-05 08:55:26
tags: 搭建环境
---
公司分部需要连接公司内部的服务器，但是该服务器只允许公司内部的网络访问。

为了解决这个问题，打算使用VPN。对于VPN以前使用最多的是PPTP这个解决方案，但是PPTP相对于openvpn来说，没有openvpn安全，而且PPTP在linux下命令行支持不是很好，稳定性也不如openvpn。所以最后就选择openvpn来搭建VPN。

PS：本文在ubuntu 14.04上安装，openvpn服务器地址为192.168.1.8。
<!-- more -->
有关openvpn在centos6.6 64bit的配置完全可以使用，已经经过验证。文章后有centos详细配置命令及步骤。

### 一、openvpn原理

openvpn通过使用公开密钥（非对称密钥，加密解密使用不同的key，一个称为Publice key，另外一个是Private key）对数据进行加密的。这种方式称为TLS加密

openvpn使用TLS加密的工作过程是，首先VPN Sevrver端和VPN Client端要有相同的CA证书，双方通过交换证书验证双方的合法性，用于决定是否建立VPN连接。

然后使用对方的CA证书，把自己目前使用的数据加密方法加密后发送给对方，由于使用的是对方CA证书加密，所以只有对方CA证书对应的Private key才能解密该数据，这样就保证了此密钥的安全性，并且此密钥是定期改变的，对于窃听者来说，可能还没有破解出此密钥，VPN通信双方可能就已经更换密钥了。

### 二、安装openvpn

openvpn的安装我们分为apt-get方式和源码方式，下面我们只讲解apt-get方式的安装。有关源码方式安装openvpn，可自行百度。

apt-get方式安装，我们可以使用如下命令：
sudo apt-get -y install openvpn libssl-dev openssl
![](../../../../asset/p1.png)
openvpn安装完毕后，我们来查看openvpn的版本，如下：
openvpn --version
![](../../../../asset/p2.png)

通过上图，我们可以看到openvpn目前的版本为2.3.2。这个版本号，建议记住。

我们再来查看下openvpn安装时产生的文件，如下：
dpkg -L openvpn |more
![](../../../../asset/p3.png)

通过上图，我们可以很明显的看出openvpn已经有相关配置的模版了。
openvpn安装完毕后，我们再来安装easy-rsa。
easy-rsa是用来制作openvpn相关证书的。
安装easy-rsa，使用如下命令：
sudo apt-get -y install easy-rsa
![](../../../../asset/p4.png)

查看easy-rsa安装的文件，如下：
dpkg -L easy-rsa |more
![](../../../../asset/p5.png)
通过上图，我们可以很明显的看到easy-rsa已经安装到/usr/share/easy-rsa/目录下。

### 三、制作相关证书

根据第一章节openvpn的工作原理，我们可以知道openvpn的证书分为三部分：CA证书、Server端证书、Client端证书。

下面我们通过easy-rsa分别对其进行制作。

#### 3.1 制作CA证书

openvpn与easy-rsa安装完毕后，我们需要在/etc/openvpn/目录下创建easy-rsa文件夹，如下：

sudo mkdir /etc/openvpn/easy-rsa/
![](../../../../asset/p6.png)


然后把/usr/share/easy-rsa/目录下的所有文件全部复制到/etc/openvpn/easy-rsa/下，如下：

sudo cp -r /usr/share/easy-rsa/* /etc/openvpn/easy-rsa/
![](../../../../asset/p7.png)


当然，我们也可以直接在/usr/share/easy-rsa/制作相关的证书，但是为了后续的管理证书的方便，我们还是把easy-rsa放在了openvpn的启动目录下。

注意：由于我们现在使用的是ubuntu系统，所以我们必须切换到root用户下才能制作相关证书，否则easy-rsa会报错。如果是centos系统，则不存在此问题。

切换到root用户下，使用如下命令：

sudo su
![](../../../../asset/p8.png)


在开始制作CA证书之前，我们还需要编辑vars文件，修改如下相关选项内容即可。如下：

sudo vi /etc/openvpn/easy-rsa/vars

export KEY_COUNTRY="CN"

export KEY_PROVINCE="HZ"

export KEY_CITY="HangZhou"

export KEY_ORG="ilanni"

export KEY_EMAIL="ilanni@ilanni.com"

export KEY_OU="ilanni"

export KEY_NAME="vpnilanni"
![](../../../../asset/p9.png)


vars文件主要用于设置证书的相关组织信息，红色部分的内容可以根据自己的实际情况自行修改。

其中export KEY_NAME="vpnilanni"这个要记住下，我们下面在制作Server端证书时，会使用到。

注意：以上内容，我们也可以使用系统默认的，也就是说不进行修改也是可以使用的。

然后使用source vars命令使其生效，如下：

source vars

./clean-all
![](../../../../asset/p10.png)


注意：执行clean-all命令会删除，当前目录下的keys文件夹。

现在开始正式制作CA证书，使用如下命令：

./build-ca
![](../../../../asset/p11.png)


一路按回车键即可。制作完成后，我们可以查看keys目录。如下：

ll keys/
![](../../../../asset/p12.png)


通过上图，我们可以很明显的看到已经生成了ca.crt和ca.key两个文件，其中ca.crt就是我们所说的CA证书。如此，CA证书制作完毕。

现在把该CA证书的ca.crt文件复制到openvpn的启动目录/etc/openvpn下，如下：

cp keys/ca.crt /etc/openvpn/

ll /etc/openvpn/
![](../../../../asset/p13.png)


#### 3.2 制作Server端证书

CA证书制作完成后，我们现在开始制作Server端证书。如下：

./build-key-server vpnilanni
![](../../../../asset/p14.png)
![](../../../../asset/p15.png)



注意：上述命令中vpnilanni，就是我们前面vars文件中设置的KEY_NAME

查看生成的Server端证书，如下：

ll keys/
![](../../../../asset/p16.png)


通过上图，可以很明显的看到已经生成了vpnilanni.crt、vpnilanni.key和vpnilanni.csr三个文件。其中vpnilanni.crt和vpnilanni.key两个文件是我们要使用的。

现在再为服务器生成加密交换时的Diffie-Hellman文件，如下：

./build-dh
![](../../../../asset/p17.png)


查看生成的文件，如下：

ll keys/
![](../../../../asset/p18.png)


通过上图，我们可以很明显的看出已经生成了dh2048.pem，这个文件。

以上操作完毕后，把vpnilanni.crt、vpnilanni.key、dh2048.pem复制到/etc/openvpn/目录下，如下：

cp keys/vpnilanni.crt keys/vpnilanni.key keys/dh2048.pem /etc/openvpn/
![](../../../../asset/p19.png)


如此，Server端证书就制作完毕。

#### 3.3 制作Client端证书

Server端证书制作完成后，我们现在开始制作Client端证书，如下：

./build-key ilanni
![](../../../../asset/p20.png)
![](../../../../asset/p21.png)



注意：上述命令中的ilanni，是客户端的名称。这个是可以进行自定义的。

如果你想快速生成用户证书不需要手工交互的话，可以使用如下命令：

./build-key --batch test1
![](../../../../asset/p22.png)
![](../../../../asset/p23.png)



查看生成的证书，如下：

ll keys/
![](../../../../asset/p24.png)


通过上图，我们可以很明显的看出已经生成了ilanni.csr、ilanni.crt和ilanni.key这个三个文件。其中ilanni.crt和ilanni.key两个文件是我们要使用的。

如此，Client端证书就制作完毕。

### 四、配置Server端

所有证书制作完毕后，我们现在开始配置Server端。Server端的配置文件，我们可以从openvpn自带的模版中进行复制。如下：

cp /usr/share/doc/openvpn/examples/sample-config-files/server.conf.gz /etc/openvpn/

cd /etc/openvpn/
![](../../../../asset/p25.png)


解压server.conf.gz 文件，使用如下命令：

gzip -d server.conf.gz
![](../../../../asset/p26.png)


注意：上述命令的意思是解压server.conf.gz文件后，然后删除原文件。

现在我们来修改server.conf文件，如下：

grep -vE "^#|^;|^$" server.conf

port 1194

proto tcp

dev tun

ca ca.crt

cert vpnilanni.crt

key vpnilanni.key

dh dh2048.pem

server 10.8.0.0 255.255.255.0

ifconfig-pool-persist ipp.txt

keepalive 10 120

comp-lzo

persist-key

persist-tun

status openvpn-status.log

verb 3
![](../../../../asset/p27.png)


与原模版文件相比，在此我修改几个地方。

第一、修改了openvpn运行时使用的协议，由原来的UDP协议修改为TCP协议。生成环境建议使用TCP协议。

第二、修改了openvpn服务器的相关证书，由原来的server.csr、server.key修改为vpnilanni.crt、vpnilanni.key。

第三、修改了Diffie-Hellman文件，由原来的dh1024.pem修改为dh2048.pem。

注意：上述server.conf文件中vpnilanni.crt、vpnilanni.key、dh2048.pem要与/etc/openvpn/目录下的相关文件一一对应。

同时，如果上述文件如果没有存放在/etc/openvpn/目录下，在server.conf文件中，我们要填写该文件的绝对路径。如下所示：
![](../../../../asset/p28.png)


配置文件修改完毕后，我们现在来启动openvpn，使用如下命令：

/etc/init.d/openvpn start

netstat -tunlp |grep 1194
![](../../../../asset/p29.png)


通过上图，我们可以很明显的看出openvpn已经在此启动，而且也确实使用的TCP协议的1194端口。

### 五、配置Client端

Server端配置并启动后，我们现在来配置Client端。Client端根据操作系统的不同，又分为Linux OS上和Windows OS上。以下我们对此一一惊醒讲解。

#### 5.1 在Windows OS上

无论是在Windows OS还是在Linux OS上Client端的配置，我们都需要把Client证书、CA证书以及Client配置文件下载下来。

先来下载Client证书和CA证书，Client证书我们主要使用crt和key结尾的两个文件，而CA证书我们主要使用crt结尾的文件。如下：
![](../../../../asset/p30.png)


先把这几个文件复制到/home/ilanni/目录下，然后再把openvpn客户端的配置文件模版也复制到/home/ilanni/目录下。如下：

cp ilanni.crt ilanni.key ca.crt /home/ilanni/

cp /usr/share/doc/openvpn/examples/sample-config-files/client.conf /home/ilanni/
![](../../../../asset/p31.png)


修改以上几个文件的用户属性，如下：

chown ilanni:ilanni ilanni.*

chown ilanni:ilanni ca.crt
![](../../../../asset/p32.png)


修改完毕后，退出root用户，回到ilanni用户的家目录下，然后使用sz命令把这几个文件下载下来。如下：

sz -y ilanni.crt ilanni.key ca.crt client.conf
![](../../../../asset/p33.png)
![](../../../../asset/p34.png)



下载完毕后，把client.conf文件重命名为client.ovpn，然后进行编辑，如下：

client

dev tun

proto tcp

remote 192.168.1.8 1194

resolv-retry infinite

nobind

persist-key

persist-tun

ca ca.crt

cert ilanni.crt

key ilanni.key

ns-cert-type server

comp-lzo

verb 3
![](../../../../asset/p35.png)


Client配置文件client.ovpn，我修改了几个地方：

第一、使用的协议，由原来的UDP修改为TCP，这个一定要和Server端保持一致。否则Client无法连接。

第二、remote地址，这个地址要修改为Server端的地址。

第三、Client证书名称，这个要和我们现在使用的Client证书名称保持一直。

以上修改完毕后，我们要把这个几个文件放在同一个文件夹中，并且一定要保持client.ovpn这个文件名称是唯一的。否则在openvpn客户端连接时，会报错。如下：
![](../../../../asset/p36.png)


安装openvpn for windows客户端，我们可以从这个地址下载，如下：http://build.openvpn.net/downloads/releases/

注意：下载的客户端版本号一定要与服务器端openvpn的版本一直，否则可能会出现无法连接服务器的现象。

我们现在服务器端的openvpn版本是2.3.2，所以客户端也建议使用2.3.2的版本。

下载并安装后，把testilanni这个文件夹复制到openvpn客户端安装的config文件夹。如下：
![](../../../../asset/p37.png)


现在我们来启动openvpn客户端连接Server，如下：
![](../../../../asset/p38.png)

注意：上图中的client就是根据client.ovpn，这个文件名来的。

点击connect，会出现如下的弹窗：
![](../../../../asset/p39.png)


如果配置都正确的话，会出现如下的提示：
![](../../../../asset/p40.png)


通过上图，我们可以很明显的看到Client已经正确连接Server端，并且获得的IP地址是10.8.0.6。

下面我们在本机查看下，该IP地址，如下：
![](../../../../asset/p41.png)


通过上图，我们可以看到本机确实已经连接到Server端，而且获得的IP地址也确实为10.8.0.6。

#### 5.2 在Linux OS上

在Windows OS上测试完毕后，我们现在在切换到linux系统。在此我们以ubuntu14.04为例。

要在ubuntu上连接openvpnServer端，我们需要先安装openvpn软件，如下：

sudo apt-get -y install openvpn
![](../../../../asset/p42.png)


安装完毕后，把我们刚刚在Windows系统配置的文件上传到ubuntu系统中。如下：
![](../../../../asset/p43.png)


注意：上传完毕后，我们不需要修改任何配置文件。因为这几个文件在Windows下已经可以正确连接openvpn Server端。

注意：在连接Server端之前，一定要切换到root用户下。因为在连接Server端时，openvpn会在本机创建一个虚拟网卡，如果使用普通用户的话，是没有权限创建虚拟网卡的。

切换到root用户，使用sudo su命令，如下：

sudo su
![](../../../../asset/p44.png)


现在开始连接Server端，使用如下命令：

openvpn --config client.ovpn
![](../../../../asset/p45.png)


如果出现上图的信息，说明已经正确连接Server端。

现在我们在本机使用ifconfig进行查看，在此建议重新开启一个新的ssh窗口，如下：

ifconfig
![](../../../../asset/p46.png)


通过上图，我们可以很明显的看出，本机已经正确连接Server端，并且也在本机虚拟出一个叫tun0的虚拟网卡。

如果想让ubuntu开机启动并后台运行的话，可以把这条命令写入rc.local文件中。如下：

/usr/sbin/openvpn --config /home/ilanni/testilanni/client.ovpn >/var/log/openvpn.log &
![](../../../../asset/p47.png)


注意，命令末尾的&符号不能省略，否则将可能阻塞系统的正常启动。

同时这个时候，client.ovpn文件中有关证书的配置一定要写成绝对路径，要不然系统会报错。如下：
![](../../../../asset/p48.png)


如果是centos系统的话，我们首先需要安装epel源，然后安装openvpn软件包。如下：

rpm -ivh http://dl.fedoraproject.org/pub/epel/epel-release-latest-6.noarch.rpm

yum -y install openvpn

以上安装完毕后，把Windows已经成功连接的Client相关文件上传到centos系统中，然后连接方法和ubuntu系统上一样。

注意：如果在centos系统要开机启动的话，也是和ubuntu系统是一样的，但是有一点需要指出就是Client相关配置文件不能放在/root目录下。

给一个正确配的例子，如下：
![](../../../../asset/p49.png)
![](../../../../asset/p50.png)
![](../../../../asset/p51.png)

因为centos的openvpn server配置和unubutn基本一样，所以就不再单独写一篇有关centos下安装配置openvpn sever的文章。

但是附上在centos下，所有执行的命令。如下：

rpm -ivh http://dl.fedoraproject.org/pub/epel/epel-release-latest-6.noarch.rpm

yum -y install openvpn

rpm -ql openvpn

cat /usr/share/doc/openvpn-2.3.7/sample/sample-config-files/README

http://openvpn.net/howto.html

yum -y install easy-rsa

rpm -ql easy-rsa

cd /usr/share/easy-rsa/2.0/

vim vars

export KEY_COUNTRY="CN"

export KEY_PROVINCE="HangZhou"

export KEY_CITY="HZ"

export KEY_ORG="ilanni"

export KEY_EMAIL="ilanni@ilanni.com"

export KEY_OU="MyOrganizationalUnit"

export KEY_NAME="ilanni"

source vars

./clean-all

./build-ca

./build-key-server ilanni

./build-dh

./build-key centos

cd&#160; keys

cp ca.crt ilanni.key ilanni.crt /etc/openvpn/

cp ca.crt centos.key centos.crt /root/

cp /usr/share/doc/openvpn-2.3.7/sample/sample-config-files/client.conf /root

cp /usr/share/doc/openvpn-2.3.7/sample/sample-config-files/server.conf /etc/openvpn/

服务器端配置文件：

vim /etc/openvpn/server.conf

grep -vE ";|#|^$" /etc/openvpn/server.conf

port 1194

proto udp

dev tun

ca ca.crt

cert ilanni.crt

dh dh2048.pem

server 10.8.0.0 255.255.255.0

ifconfig-pool-persist ipp.txt

keepalive 10 120

comp-lzo

persist-key

persist-tun

status openvpn-status.log

verb 3

客户端配置文件：

grep -vE ";|#|^$" centos.conf

client

dev tun

proto udp

remote 182.254.223.140 1194

resolv-retry infinite

nobind

persist-key

persist-tun

ca ca.crt

cert centos.crt

key centos.key

remote-cert-tls server

comp-lzo

verb 3

来源：http://www.ilanni.com

