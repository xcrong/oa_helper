## 一 缘起

每当错过一些重要的OA公告时，我便想：如何能及时接收到最新的OA呢？

这次，我行动了起来，写了一个爬虫：

1. 每隔60分钟，便抓取一次OA首页，获取到10条最新的OA公告
2. 逐条检查OA条目是否在数据库中。如果在，则跳过；如果不在，则添加到待处理列表
3. 将筛选出来的新OA公告发送到微信绑定的邮箱

如此，便可以在微信中接收最近一个小时所更新的公告。

## 二 基本使用

**NOTICE: 假设本项目执行的设备上已有Python环境**

1. clone 本仓库到本地

```shell
git clone https://github.com/gty20010709/oa_helper 
# 也可以点击右上角的 Code - Downlaod ZIP
```

2. 进入项目文件夹

```shell
cd oa_helper
```

3. 环境准备

```shell
# 手动准备运行环境(如果有 poetry 不用如此麻烦，详见下方)
# 创建虚拟环境 
python -m venv .venv
# 激活虚拟环境, 根据系统选择
## Windows CMD
.venv\Scripts\activate.bat
## Windows PowerShell
.venv\Scripts\Activate.ps1
## Linux/MacOS：
source .venv/bin/activate 
# 安装依赖
pip install -r requirements.txt

# 如果有 poetry ，直接按下面的命令即可准备好运行环境
poetry install
poetry shell
```

4. 填写配置文件 `config.ini`

为了将公告发送到微信所绑定的邮箱，需要提供一个**发件箱的帐号和密码**。
推荐使用环境变量的方式配置帐号和密码，明文存储可能会被其他流氓软件读取，从而造成意料之外的事情。环境变量的配置方式可以上网查看教程，或者问ChatGPT [doge]

当然，明文存储也能用。

默认是使用自己的学校邮箱作为发件箱，如果使用其他邮箱，需要注意更改smtp 服务器和端口，可从邮箱服务商处查到。

——————————————————————————————


接收邮件列表那里，填入微信所绑定的邮箱地址。

可以打开微信查看：**我 - 设置 - 通用 - 辅助功能 - QQ邮箱提醒**

这里是可以填多个邮箱地址的，也既是说：**一人运行程序，可以多人享受服务。**

5. 运行Python脚本 `oa_scheduler.py`

```shell
python oa_scheduler.py
```

**PS：程序需要保持后台运行。**

## 三 进阶使用

1. 自定义工作时间和更新间隔
   默认情况，程序每天早上八点到晚上六点（只看整点)工作，抓取间隔是60分钟。
   可以通过修改 `config.ini` 中的第三节 `[schedule]`进行配置。
2. 自定义邮件模板
   默认的邮件模板是非常简洁的，就是一个单纯的无序列表。
   如果掌握 Jinja2 模板语言的话，可以通过更改 `template.html` 来自定义邮件模板。

## 四 写在后面

在下的Python技能有待提高，程序不如人意的地方，欢迎指出。

在下这个小程序，只是一块砖，希望能引出大佬的玉来。
