# sing-box 1.14 服务端与客户端模板

按 **sing-box 1.14.3** 编写。2026-10-16 核对时，它是官方最新稳定版：[官方发布页](https://github.com/SagerNet/sing-box/releases/tag/v1.14.3)。

三份文件都是严格 JSON；`__大写名称__` 是需要手动替换的占位符，sing-box 不会自动展开它们。先复制模板并填写，再运行。不要将填写后的真实凭据提交到 Git。

| 文件 | 用途 |
| --- | --- |
| `server.json` | 服务端，同时提供下表七种接入方式 |
| `client.json` | 普通客户端，本机 `127.0.0.1:2080` 提供 SOCKS5 / HTTP 代理 |
| `client-tun.json` | TUN 客户端，接管系统流量，同时保留上述本机代理端口 |

两个客户端文件各自完整，**选择其中一份运行**，分别填写所用文件即可。服务端通常运行在 VPS，客户端运行在自己的设备。

## 协议组合和端口

| 客户端节点 tag | 组合 | 服务端端口 | 认证 |
| --- | --- | --- | --- |
| `vless-reality` | VLESS + TCP + REALITY + Vision | TCP 443 | UUID、REALITY 密钥对、short ID |
| `vless-tls` | VLESS + TCP + TLS + Vision | TCP 8444 | UUID、域名证书 |
| `vmess-ws-tls` | VMess AEAD + WebSocket + TLS | TCP 8443 | UUID、WS 路径、域名证书 |
| `trojan-tls` | Trojan + TCP + TLS | TCP 9443 | 密码、域名证书 |
| `hy2` | Hysteria 2 + QUIC + TLS + Salamander | UDP 443 | 密码、混淆密码、域名证书 |
| `hy1` | Hysteria 1 + QUIC + TLS + 混淆 | UDP 8443 | 认证字符串、混淆密码、域名证书 |
| `ss2022` | Shadowsocks 2022 | TCP 和 UDP 8388 | 16 字节随机密钥的 Base64 编码 |

REALITY 是 TLS 层的配置，这里将它与 VLESS 组合。各节点是并列的接入方式，每条连接使用客户端所选节点；不会把所有协议串联起来。

TCP 443 与 UDP 443 可以同时使用，TCP 8443 与 UDP 8443 也一样。需要在 VPS 安全组、系统防火墙和 NAT 映射中分别放行所用的 TCP / UDP 端口。监听采用 `0.0.0.0`，即 IPv4；需要 IPv6 时调整监听地址，并确认系统的双栈行为。

可以删除不用的服务端 inbound 和客户端 outbound；同时从客户端 `proxy.outbounds`、`auto.outbounds` 移除对应 tag，检查 `proxy.default` 仍指向保留的节点。

## 填写占位符

同名占位符在服务端、所用客户端中必须填相同的值。REALITY 私钥、公钥按下表分别填写。

| 占位符 | 填写内容 |
| --- | --- |
| `__SERVER_ADDRESS__` | VPS 公网 IP 或直连域名；仅客户端使用，不含协议前缀和端口 |
| `__TLS_DOMAIN__` | 你拥有证书的域名，例如 `proxy.example.com`；用于普通 TLS 的 SNI、证书验证及 WS Host |
| `__REALITY_SNI__` | REALITY 握手目标的域名；填写服务器可达、支持 TLS 1.3 的站点域名，不含 `https://` 或路径 |
| `__VLESS_UUID__` | VLESS + REALITY 的 UUID |
| `__VLESS_TLS_UUID__` | VLESS + TLS 的 UUID，可以单独生成 |
| `__VMESS_UUID__` | VMess 的 UUID |
| `__REALITY_PRIVATE_KEY__` | REALITY 私钥，仅放服务端 |
| `__REALITY_PUBLIC_KEY__` | 与私钥配对的 REALITY 公钥，仅放客户端 |
| `__REALITY_SHORT_ID__` | 本模板使用 8 个十六进制字符，例如生成命令输出的值 |
| `__VMESS_WS_PATH__` | 随机路径片段，不含开头的 `/`；模板已经添加 `/` |
| `__TROJAN_PASSWORD__` | Trojan 随机密码 |
| `__HY2_PASSWORD__` | Hysteria 2 认证密码 |
| `__HY2_OBFS_PASSWORD__` | Hysteria 2 Salamander 混淆密码 |
| `__HY1_PASSWORD__` | Hysteria 1 的 `auth_str`，直接填写字符串 |
| `__HY1_OBFS_PASSWORD__` | Hysteria 1 混淆密码，直接填写字符串 |
| `__SS_2022_KEY__` | `sing-box generate rand 16 --base64` 的输出 |
| `__CLASH_API_SECRET__` | 本机节点切换 API 的随机访问密码，仅客户端使用 |

在安装了 sing-box 1.14.3 的设备上生成：

```sh
# 分别运行三次，为三种 UUID 占位符生成不同值
sing-box generate uuid
sing-box generate uuid
sing-box generate uuid

# 同一次输出的一对私钥、公钥分别填写到两端
sing-box generate reality-keypair

# REALITY short ID
sing-box generate rand 4 --hex

# Shadowsocks 2022 AES-128 密钥：必须是 16 字节随机值的 Base64
sing-box generate rand 16 --base64

# 每个认证密码、混淆密码、API 密码分别生成一次
sing-box generate rand 32 --base64

# WS 路径片段
sing-box generate rand 12 --hex
```

Shadowsocks 的 `2022-blake3-aes-128-gcm` 不能直接使用普通文本密码。模板是单用户模式，服务端和客户端填写同一个 Base64 密钥即可。[Shadowsocks 官方使用说明](https://sing-box.sagernet.org/manual/proxy-protocol/shadowsocks/)

## TLS 证书与 REALITY

服务端普通 TLS 节点共用以下证书文件；可以修改各 inbound 的路径：

```text
/etc/sing-box/cert/fullchain.pem
/etc/sing-box/cert/privkey.pem
```

准备覆盖 `__TLS_DOMAIN__` 的有效证书和对应私钥，并让运行 sing-box 的用户能够读取。使用完整证书链。客户端可以直接连接 VPS 的 IP，但 `tls.server_name` 仍填写证书域名。

Hysteria 2 在 1.14 默认模拟 Chrome QUIC 握手，证书应使用 **ECDSA 或 RSA**；Ed25519 证书与此默认行为不兼容。模板保持证书验证开启。使用自签证书时，向客户端对应节点的 TLS 配置添加可信证书 `certificate_path`，并保留正确的证书域名。[Hysteria 2 客户端文档](https://sing-box.sagernet.org/configuration/outbound/hysteria2/)

VLESS + REALITY 节点不使用上述本地证书，而是使用 REALITY 密钥对。服务端 `reality.handshake.server` 与客户端 `tls.server_name` 在本模板中使用同一个 `__REALITY_SNI__`。握手目标必须从 VPS 可达，不要指回本机的 REALITY 监听端口；目标域名无需由你持有。

REALITY 的服务端 `short_id` 是数组，客户端是单个字符串。Vision 节点保持原始 TCP 传输，不添加 WS/gRPC transport 或 multiplex。[VLESS 配置](https://sing-box.sagernet.org/configuration/inbound/vless/)、[TLS / REALITY 配置](https://sing-box.sagernet.org/configuration/shared/tls/)

当前模板直接连接 VPS。REALITY 和 Hysteria 不适合直接套普通 HTTP 反向代理或普通 HTTP CDN；VMess 的 WS 方案若另接 CDN，需要结合其端口、域名和回源配置调整。

## 客户端使用与节点切换

默认选择 `vless-reality`。可以在启动前修改 `proxy` 出站的 `default`，也可以运行时通过本机 Clash API 切换：

```sh
# 将下面的 API 密码替换为你填写的值；选择 Hysteria 2
curl -X PUT 'http://127.0.0.1:9090/proxies/proxy' \
  -H 'Authorization: Bearer __CLASH_API_SECRET__' \
  -H 'Content-Type: application/json' \
  -d '{"name":"hy2"}'

# 选择自动延迟测试组
curl -X PUT 'http://127.0.0.1:9090/proxies/proxy' \
  -H 'Authorization: Bearer __CLASH_API_SECRET__' \
  -H 'Content-Type: application/json' \
  -d '{"name":"auto"}'
```

API 只监听 `127.0.0.1:9090`。切换可能中断已有连接；未启用选择缓存，重启后恢复 `default`。`auto` 定期比较可用节点的 HTTP 测试延迟，不能据此判断最高吞吐量，也不保证现有连接无缝恢复。[Selector](https://sing-box.sagernet.org/configuration/outbound/selector/)、[URLTest](https://sing-box.sagernet.org/configuration/outbound/urltest/)

普通客户端运行后，把应用的 SOCKS5 或 HTTP 代理设为 `127.0.0.1:2080`。SOCKS 应用优先使用代理端解析域名，例如 curl 的 `--socks5-hostname`。应用自身提前进行的本地 DNS 查询不受普通代理模板接管。

TUN 模板适用于具备相应权限的桌面环境，通常需要 root / 管理员权限。Linux 可按系统环境在 TUN inbound 中增加 `"auto_redirect": true`，需要可用的 nftables。Android / Apple 图形客户端还需结合应用的 VPN 权限及平台配置。TUN 的地址段如与现有网络冲突，应先修改。

客户端采用新版 DNS 配置：

- `dns-bootstrap` 通过直连 UDP `223.5.5.5` 解析代理服务器域名；如当前网络不可用，可改成可直连的 DNS IP。
- `dns-remote` 通过所选代理向 `1.1.1.1` 发起 DoH 查询。TUN 捕获的普通 DNS 请求走此服务。
- `route.default_domain_resolver` 保持指向 `dns-bootstrap`，避免解析代理服务器时依赖代理自身。
- TUN 使用 1.14 的 `dns_mode: "hijack"`；路由中也保留端口 53 的 DNS 接管规则。应用自带 DoH/DoT 不会被转换成上述 DNS 查询。
- 目的地址为私有 IP 时直连，其余流量使用 `proxy`；没有额外配置中国大陆域名/IP分流。

这是基础 DNS 策略，bootstrap 查询使用明文 UDP。通过代理传递的目标域名可以由 VPS 解析；客户端 DoH 并不意味着所有目标域名都会在客户端解析。[新版 DNS 格式](https://sing-box.sagernet.org/configuration/dns/server/https/)、[TUN DNS 行为](https://sing-box.sagernet.org/configuration/inbound/tun/)

## 检查与启动

确认实际执行的核心版本，并替换所用配置中的全部占位符：

```sh
sing-box version

# 在本目录检查是否还有占位符；有输出时继续填写
rg '__[A-Z0-9_]+__' server.json client.json client-tun.json

# 服务端所在设备
sing-box check -c server.json
sudo sing-box run -c server.json

# 普通客户端所在设备
sing-box check -c client.json
sing-box run -c client.json

# 或使用 TUN 客户端，勿与普通客户端同时启动
sing-box check -c client-tun.json
sudo sing-box run -c client-tun.json
```

只运行实际需要的一组启动命令。TCP/UDP 443 的绑定通常要求 root 或 `CAP_NET_BIND_SERVICE`；TUN 还需要网络管理权限。上面的命令用于前台运行，生产部署可将填写后的服务端文件放到现有 systemd 服务所读取的位置。

普通客户端运行后可检查 HTTP 请求：

```sh
curl --socks5-hostname 127.0.0.1:2080 https://example.com/
```

Hysteria 1 和 Hysteria 2 是不同协议，两端的 `type` 必须一致。Hysteria 1 的 `up_mbps` / `down_mbps` 暂设为 100，按各端实际带宽调整。Hysteria 2 没有设置带宽值，使用 BBR；`bbr_profile` 为 `standard`。混淆密码与认证密码是独立配置，必须分别与服务端匹配。[Hysteria 1](https://sing-box.sagernet.org/configuration/inbound/hysteria/)、[Hysteria 2](https://sing-box.sagernet.org/configuration/outbound/hysteria2/)

生成时已将三份模板中的占位符替换为临时生成的匹配凭据和 ECDSA 测试证书，并使用官方 Linux amd64 **sing-box 1.14.3** 执行 `check`，三份全部通过。这验证配置格式与初始化，未验证你的 VPS 网络、真实证书、握手目标、防火墙或 TUN 路由权限；原始模板在完成填写前不能直接运行。
