# py_buaa_login

一个十分笨重的（基于 selenium）北航校园网自动化登录脚本。

> [!IMPORTANT]
> 校园网登录前，需要关闭系统代理以免 https://gw.buaa.edu.cn 无法正常访问

## 安装方式

> [!IMPORTANT]
> 请使用 pypi 官方软件源，此包 **通常无法** 从 pypi 非官方镜像源下载。
> 请使用 `python>=3.10`

```bash
pip install py_buaa_login
```

## 使用方式

### 登录校园网

```bash
# 从命令行参数获得用户名和口令
python -m py_buaa_login login "<username>" "<password>"

# 从标准输入或者文件获取用户名和口令
# 第一行内容将被作为用户名
# 第二行内容将被作为口令
python -m py_buaa_login login --stdin
```

### 校园网退出登录

```bash
python -m py_buaa_login logout
```

### 查询网络是否可用

```bash
python -m py_buaa_login status
```

### 显示使用指南

```bash
python -m py_buaa_login --help
python -m py_buaa_login
```

## 编程接口

```python
# 检查登录情况
# 返回 True 表示网络可用
from py_buaa_login import login_check
print(login_check())

# 试图登录校园网
# 返回 True 表示登录成功
from py_buaa_login import login
print(login(username, password))

# 试图退出登陆校园网
# 返回 True 表示退出登录成功
from py_buaa_login import logout
print(logout())
```
