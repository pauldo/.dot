# 交互式 sing-box 配置生成器

需要 Python 3.9+。脚本独立运行，不依赖此前的 JSON 模板或第三方 Python 包。

```sh
python3 sing-box-generator/generate.py
```

默认检测 PATH 中 `sing-box version` 的版本，可选择 **1.12、1.13、1.14** 或对应完整版本号。未安装核心或本机版本不在此范围时，需要手动选择。目标版本只控制生成格式，不会下载或切换核心。

可指定用于版本检测及生成 REALITY 密钥的核心，以及新的输出目录：

```sh
python3 sing-box-generator/generate.py \
  --sing-box /path/to/sing-box \
  --output /tmp/my-sing-box-config
```

交互内容包括服务器 IPv4/IPv6、客户端平台、启用的协议、各协议端口、监听地址、TLS 域名和证书路径、REALITY SNI、本机代理/API 端口、bootstrap DNS、默认节点。多个协议可输入 `1,3,5` 或节点 tag，默认全部启用。同一传输类型的端口冲突会要求重新填写；TCP 与 UDP 可以共用端口号。

支持 VLESS + REALITY + Vision、VLESS + TLS + Vision、VMess + WS + TLS、Trojan + TLS、Hysteria 1/2、Shadowsocks 2022。UUID、认证密码、混淆密码、SS 2022 密钥、API 密码、WS 路径自动生成；REALITY 密钥通过本机核心生成，无法生成时可以输入一对已有密钥。

默认输出到本目录的 `output/<版本>-<时间>/`，已加入 `.gitignore`。每次使用新目录，拒绝覆盖已有目录；POSIX 系统下目录权限为 700，文件为 600。

| 文件 | 用途 |
| --- | --- |
| `server.json` | 已填入生成凭据的服务端配置 |
| `client.json` | 本机 SOCKS5 / HTTP 代理客户端 |
| `client-tun.json` | TUN 客户端，保留本机代理端口 |
| `README.md` | 本次端口、运行命令、分流模板替换说明 |

两份客户端各自完整，选择一份运行。普通 TLS 节点仍需准备真实证书；生成器不会申请证书或启动服务。

## 站点与 App 的独立出口模板

两个客户端中都包含以下配置：

| 位置 | 搜索内容 | 手动替换方式 |
| --- | --- | --- |
| `route.rules` 和 `dns.rules` | `replace-site.example.invalid` | 换成指定站点域名，可填写多个 |
| Linux/macOS 的路由及 DNS 规则 | `REPLACE_APP`、示例完整路径 | 换成进程名或可执行文件路径 |
| Windows 的路由及 DNS 规则 | `REPLACE_APP.exe`、示例完整路径 | 换成进程名或可执行文件路径 |
| Android 的路由及 DNS 规则 | `invalid.example.replace_app` | 换成指定 App 的包名 |
| `outbounds` | `site-node`、`app-node` | 分别换成实际的独立上游节点信息，保留 tag |
| `outbounds` | `site-proxy`、`app-proxy` | 两个独立选择组，也可分别选择 `direct` |

示例站点和 App 不会匹配正常流量。`site-node`、`app-node` 初始复制默认节点，**获得不同出口 IP 需要将它们换成真正不同的上游服务器**。也可以直接把对应选择组的 `default` 改成 `direct`，让指定流量直连。第二台上游服务器需要自行部署。

站点规则先于 App 规则，私有 IP 直连先于两者。域名匹配依赖可见的域名信息；App 规则依赖平台权限和进程识别，建议配合 TUN。桌面使用 `process_name`/`process_path`，Android 使用 `package_name`；无法用这些规则识别网关后另一台设备上的 App，iOS 不支持此处的任意 App 进程分流。系统 DNS 代应用查询时，DNS 请求可能无法归属原 App。

## 版本处理与验证

| 配置项 | 1.12 / 1.13 | 1.14 |
| --- | --- | --- |
| 新版带 `type` 的 DNS server、`default_domain_resolver`、规则 action | 使用 | 使用 |
| Hysteria 2 `bbr_profile` | 不写入 | `standard` |
| TUN `dns_mode` | 不写入，保留端口 53 接管规则 | `hijack` |
| Android 应用规则 | `package_name` | `package_name`，不依赖新版正则字段 |

1.12/1.13 使用 TUN 时，可按系统情况把系统 DNS 指向 `172.19.0.2`；1.14 使用新的 TUN DNS 配置。TUN 地址冲突、网络管理权限、真实证书和服务端防火墙需要按实际环境处理。

脚本只写文件，不把另一个系列核心的检查结果作为目标版本的验证结果。使用前运行目标核心的 `sing-box check -c <文件>`，生成目录中的 README 有完整命令。

运行测试：

```sh
python3 -m unittest discover -s sing-box-generator -v

# 可选：提供三种核心，校验三个配置、四种客户端平台的 36 个组合
SING_BOX_1_12=/path/to/sing-box-1.12 \
SING_BOX_1_13=/path/to/sing-box-1.13 \
SING_BOX_1_14=/path/to/sing-box-1.14 \
python3 -m unittest discover -s sing-box-generator -v
```

参考：[迁移文档](https://sing-box.sagernet.org/migration/)、[路由规则与平台支持](https://sing-box.sagernet.org/configuration/route/rule/)、[TUN DNS](https://sing-box.sagernet.org/configuration/inbound/tun/)、[Hysteria 2](https://sing-box.sagernet.org/configuration/outbound/hysteria2/)。
