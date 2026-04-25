# py_buaa_login

一个十分笨重的（基于 selenium）北航校园网自动化登录脚本。

## 安装方式

> [!IMPORTANT]
> - 请使用 pypi 官方软件源，此包 **通常无法** 从 pypi 非官方镜像源下载。
>
> - 请使用 `python>=3.13`

```bash
pip install py_buaa_login
```

## 使用方式

### 初次测试

在使用此脚本登录校园网前，脚本初次运行可能会从外网下载 ChromeDrive。因此建议在有外网的环境下进行初次运行测试，测试内容为：

```bash
python -m py_buaa_login test "https://www.google.com"
```

如果程序输出 `Test successfully.` 则说明 selenium 中的 ChromeDrive 可用。

> [!NOTE]
> 如果你的电脑有图形界面，并且你想要测试 selenium 的 ChromeDrive 图形显示是否正确，可以带 `--head` 参数进行测试，可以弹出图形用户界面的网页则说明图形用户界面显示正常。

### 登录校园网

> [!NOTE]
> 登录校园网以及登出校园网时，可能需要等待大概 10 秒，属正常现象。

> [!IMPORTANT]
> 执行校园网登录前，需要关闭系统代理以免 [https://gw.buaa.edu.cn](https://gw.buaa.edu.cn) 无法正常访问

```bash
# 从命令行参数获得用户名和口令
python -m py_buaa_login login "<username>" "<password>"

# 从标准输入或者文件获取用户名和口令
# 第一行内容将被作为用户名
# 第二行内容将被作为口令
python -m py_buaa_login login --stdin
```

### 登出校园网

> [!IMPORTANT]
> 执行校园网登出前，需要关闭系统代理以免 [https://gw.buaa.edu.cn](https://gw.buaa.edu.cn) 无法正常访问

```bash
python -m py_buaa_login logout
```

### 查询网络是否可用

> [!NOTE]
> 查询网络是否可用时，可能需要等待大概 10 秒，属正常现象。

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
# 在确定有网络的前提下检查 selenium ChromeDrive 是否可用
# 返回 True 表示 selenium ChromeDrive 可用
from py_buaa_login import test
print(test(True))

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
