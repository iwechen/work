# CentOS 无桌面环境运行Selenium + Firefox

> 系统要求：
>
> - CentOS 7
> - Firefox 56.0+
> - Selenium 3.5+



1. 正常情况下，运行Selenium需要桌面环境，为了节省资源也可以将环境部署在无桌面的系统中。但是需要安装虚拟桌面环境Xvfb。

   `yum install xorg-x11-server-Xvfb`

2. 官方源里的Firefox版本太老，从官网下载安装

   ```bash
   cd /usr/local
   wget https://ftp.mozilla.org/pub/firefox/releases/56.0.2/linux-x86_64/en-US/firefox-56.0.2.tar.bz2
   tar xjvf firefox-56.0.2.tar.bz2
   ln -s /usr/local/firefox/firefox /usr/bin/firefox

   ```

3. 安装Firefox依赖包

   `yum install gtk3`

4. 安装 Selenium

   `pip install selenium`

5. 安装火狐驱动 `geckodriver`

   ```bash
   cd /usr/local/bin
   wget https://github.com/mozilla/geckodriver/releases/download/v0.19.1/geckodriver-v0.19.1-linux64.tar.gz
   tar xvzf geckodriver-*.tar.gz
   ln -s /usr/local/geckodriver /usr/bin/geckodriver
   ```



## 运行

启动虚拟桌面环境

`Xvfb :1 -screen 0 1024x768x24 &`

配置环境变量

`export DISPLAY=:1`

启动程序

```python
from selenium import webdriver

b = webdriver.Firefox()
b.get('http://www.baidu.com')
b.quit()
```

