#!/usr/bin/env python3
"""Interactive sing-box 1.12/1.13/1.14 configuration generator (stdlib only)."""

import argparse
import base64
import copy
from dataclasses import dataclass, field
from datetime import datetime
import getpass
import ipaddress
import json
import os
from pathlib import Path
import re
import secrets
import shutil
import subprocess
import sys
import uuid


FAMILIES = ("1.12", "1.13", "1.14")
# tag, display name, inbound type, default port, listening transports
PROTOCOLS = (
    ("vless-reality", "VLESS + REALITY + Vision", "vless", 443, ("tcp",)),
    ("vless-tls", "VLESS + TLS + Vision", "vless", 8444, ("tcp",)),
    ("vmess-ws-tls", "VMess + WebSocket + TLS", "vmess", 8443, ("tcp",)),
    ("trojan-tls", "Trojan + TLS", "trojan", 9443, ("tcp",)),
    ("hy2", "Hysteria 2 + Salamander", "hysteria2", 443, ("udp",)),
    ("hy1", "Hysteria 1", "hysteria", 8443, ("udp",)),
    ("ss2022", "Shadowsocks 2022 AES-128", "shadowsocks", 8388, ("tcp", "udp")),
)
BY_TAG = {item[0]: item for item in PROTOCOLS}
APP_MATCHERS = {
    "linux": [{"process_name": ["REPLACE_APP"]}, {"process_path": ["/REPLACE/APP/PATH"]}],
    "windows": [{"process_name": ["REPLACE_APP.exe"]},
                {"process_path": [r"C:\REPLACE\APP\PATH.exe"]}],
    "macos": [{"process_name": ["REPLACE_APP"]},
              {"process_path": ["/Applications/REPLACE.app/Contents/MacOS/REPLACE"]}],
    "android": [{"package_name": ["invalid.example.replace_app"]}],
}
SITE_MATCHER = {"domain_suffix": ["replace-site.example.invalid"]}


def version_family(value):
    match = re.fullmatch(r"v?(1\.(?:12|13|14))(?:\.\d+)?(?:[-+][0-9A-Za-z.-]+)?", value)
    if not match:
        raise ValueError("请输入 1.12、1.13、1.14，或对应完整版本号，如 1.14.3")
    return match.group(1)


def target_version(value):
    version_family(value)
    return value


def detect_version(binary):
    if not binary:
        return None
    try:
        result = subprocess.run([binary, "version"], capture_output=True, text=True,
                                check=True, timeout=10)
    except (OSError, subprocess.SubprocessError):
        return None
    match = re.search(r"sing-box version\s+(\S+)", result.stdout)
    return match.group(1) if match else None


def ask(label, default=None, validate=None, hidden=False):
    while True:
        suffix = f" [{default}]" if default is not None else ""
        raw = (getpass.getpass if hidden else input)(f"{label}{suffix}: ").strip()
        value = str(default) if not raw and default is not None else raw
        if not value and default is None:
            print("此项不能为空。")
            continue
        try:
            return validate(value) if validate else value
        except ValueError as error:
            print(f"输入无效：{error}")


def port_number(value):
    try:
        number = int(value)
    except ValueError:
        raise ValueError("端口必须是 1–65535 的整数") from None
    if not 1 <= number <= 65535:
        raise ValueError("端口必须是 1–65535 的整数")
    return number


def ip_address(value):
    value = value.removeprefix("[").removesuffix("]")
    return str(ipaddress.ip_address(value))


def domain_name(value):
    try:
        normalized = value.rstrip(".").encode("idna").decode("ascii").lower()
    except UnicodeError:
        raise ValueError("请输入有效域名，不带协议、端口或路径") from None
    if len(normalized) > 253 or "." not in normalized or any(
        not re.fullmatch(r"[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?", label)
        for label in normalized.split(".")
    ):
        raise ValueError("请输入有效域名，不带协议、端口或路径")
    try:
        ipaddress.ip_address(normalized)
    except ValueError:
        return normalized
    raise ValueError("此处填写域名，不能使用 IP 地址")


def select_protocols(value):
    if value.lower() == "all":
        return [item[0] for item in PROTOCOLS]
    selected = set()
    for token in re.split(r"[,，\s]+", value.lower()):
        if not token:
            continue
        if token.isdecimal() and 1 <= int(token) <= len(PROTOCOLS):
            selected.add(PROTOCOLS[int(token) - 1][0])
        elif token in BY_TAG:
            selected.add(token)
        else:
            raise ValueError(f"未知协议 {token}；请输入编号、节点 tag，或 all")
    if not selected:
        raise ValueError("至少选择一个协议")
    return [item[0] for item in PROTOCOLS if item[0] in selected]


def choice(value, options):
    if value not in options:
        raise ValueError("请选择 " + " / ".join(options))
    return value


def reality_key(value):
    try:
        decoded = base64.b64decode(value + "=" * (-len(value) % 4), altchars=b"-_", validate=True)
    except ValueError:
        raise ValueError("REALITY 密钥必须是 32 字节的 URL-safe Base64") from None
    if len(decoded) != 32:
        raise ValueError("REALITY 密钥必须是 32 字节的 URL-safe Base64")
    return value


def generate_credentials(tags, binary):
    result = {
        "uuids": {tag: str(uuid.uuid4()) for tag in tags},
        "passwords": {tag: secrets.token_urlsafe(32) for tag in tags},
        "hy1_obfs": secrets.token_urlsafe(32), "hy2_obfs": secrets.token_urlsafe(32),
        "ss_key": base64.b64encode(secrets.token_bytes(16)).decode(),
        "short_id": secrets.token_hex(4), "ws_path": "/" + secrets.token_hex(12),
        "api_secret": secrets.token_urlsafe(32),
    }
    if "vless-reality" in tags:
        if binary:
            try:
                output = subprocess.run([binary, "generate", "reality-keypair"],
                    capture_output=True, text=True, check=True, timeout=10).stdout
                result["private_key"] = reality_key(re.search(r"PrivateKey:\s*(\S+)", output).group(1))
                result["public_key"] = reality_key(re.search(r"PublicKey:\s*(\S+)", output).group(1))
                return result
            except (OSError, subprocess.SubprocessError, AttributeError, ValueError):
                print("本机核心未能生成 REALITY 密钥，请输入一对已有密钥。")
        else:
            print("未找到 sing-box；启用 REALITY 时，需要输入一对已有密钥。")
        result["private_key"] = ask("REALITY 私钥（隐藏输入）", validate=reality_key, hidden=True)
        result["public_key"] = ask("配对的 REALITY 公钥", validate=reality_key)
    return result


@dataclass
class Settings:
    version: str
    server: str
    tags: list
    ports: dict
    platform: str = "linux"
    listen: str = "0.0.0.0"
    tls_domain: str = "proxy.example.com"
    certificate: str = "/etc/sing-box/cert/fullchain.pem"
    key: str = "/etc/sing-box/cert/privkey.pem"
    reality_sni: str = "www.microsoft.com"
    mixed_port: int = 2080
    api_port: int = 9090
    bootstrap_dns: str = "223.5.5.5"
    hy1_mbps: int = 100
    default_node: str = ""
    credentials: dict = field(default_factory=dict, repr=False)

    @property
    def family(self):
        return version_family(self.version)


def collect_settings(binary, local_version):
    print("sing-box 配置生成器：支持 1.12 / 1.13 / 1.14")
    default_version = None
    if local_version:
        print(f"检测到本机 sing-box {local_version}")
        try:
            version_family(local_version)
            default_version = local_version
        except ValueError:
            print("本机版本不在支持范围，请明确选择目标版本。")
    else:
        print("未能检测本机版本，请明确选择目标版本。")
    version = ask("目标 sing-box 版本", default_version, target_version)
    server = ask("服务器公网 IP（IPv4 / IPv6）", validate=ip_address)
    platform = ask("客户端平台 linux/windows/macos/android",
                   {"win32": "windows", "darwin": "macos"}.get(sys.platform, "linux"),
                   lambda value: choice(value, APP_MATCHERS))
    for number, (tag, name, _, port, transports) in enumerate(PROTOCOLS, 1):
        print(f"  {number}. {name} ({tag}), 默认 {port}/{' + '.join(transports)}")
    tags = ask("启用协议，多个编号用逗号分隔", "all", select_protocols)
    ports, used = {}, set()
    for tag in tags:
        _, name, _, default, transports = BY_TAG[tag]
        while True:
            port = ask(f"{name} 服务端端口", default, port_number)
            occupied = {(transport, port) for transport in transports}
            if occupied & used:
                print("此端口与已选协议在同一传输类型上冲突，请换一个端口。")
                continue
            ports[tag] = port
            used.update(occupied)
            break
    settings = Settings(version, server, tags, ports, platform=platform)
    settings.listen = ask("服务端监听地址", "::" if ":" in server else "0.0.0.0", ip_address)
    if set(tags) - {"vless-reality", "ss2022"}:
        settings.tls_domain = ask("普通 TLS 证书域名", validate=domain_name)
        settings.certificate = ask("服务端证书完整链路径", settings.certificate)
        settings.key = ask("服务端证书私钥路径", settings.key)
    if "vless-reality" in tags:
        settings.reality_sni = ask("REALITY 握手目标/SNI", settings.reality_sni, domain_name)
    if "hy1" in tags:
        settings.hy1_mbps = ask("Hysteria 1 上下行带宽 Mbps（之后可分别修改）", 100, positive_int)
    settings.mixed_port = ask("客户端本机 SOCKS5/HTTP 端口", 2080, port_number)
    while True:
        settings.api_port = ask("客户端本机 Clash API 端口", 9090, port_number)
        if settings.api_port != settings.mixed_port:
            break
        print("API 端口不能与本机代理端口相同。")
    settings.bootstrap_dns = ask("直连 bootstrap DNS IP", "223.5.5.5", ip_address)
    settings.default_node = ask("默认代理节点 tag", tags[0], lambda value: choice(value, tags))
    settings.credentials = generate_credentials(tags, binary)
    return settings


def positive_int(value):
    number = int(value)
    if number <= 0:
        raise ValueError("请输入大于 0 的整数")
    return number


def build_configs(settings):
    s, creds = settings, settings.credentials
    new_fields = s.family == "1.14"

    def tls(server=False, alpn=None):
        value = {"enabled": True, "server_name": s.tls_domain}
        if server:
            value.update(certificate_path=s.certificate, key_path=s.key)
        else:
            value["insecure"] = False
        if alpn:
            value["alpn"] = alpn
        return value

    inbounds, nodes = [], []
    for tag in s.tags:
        kind = BY_TAG[tag][2]
        inbound = {"type": kind, "tag": tag + "-in", "listen": s.listen, "listen_port": s.ports[tag]}
        outbound = {"type": kind, "tag": tag, "server": s.server, "server_port": s.ports[tag]}
        if kind == "vless":
            inbound["users"] = [{"name": "user1", "uuid": creds["uuids"][tag], "flow": "xtls-rprx-vision"}]
            outbound.update(uuid=creds["uuids"][tag], flow="xtls-rprx-vision")
            if tag == "vless-reality":
                inbound["tls"] = {"enabled": True, "server_name": s.reality_sni,
                    "reality": {"enabled": True,
                        "handshake": {"server": s.reality_sni, "server_port": 443},
                        "private_key": creds["private_key"], "short_id": [creds["short_id"]]}}
                outbound["tls"] = {"enabled": True, "server_name": s.reality_sni,
                    "utls": {"enabled": True, "fingerprint": "chrome"},
                    "reality": {"enabled": True, "public_key": creds["public_key"], "short_id": creds["short_id"]}}
            else:
                inbound["tls"] = dict(tls(True), min_version="1.3")
                outbound["tls"] = dict(tls(), min_version="1.3")
        elif kind == "vmess":
            inbound.update(users=[{"name": "user1", "uuid": creds["uuids"][tag], "alterId": 0}],
                           tls=tls(True, ["http/1.1"]),
                           transport={"type": "ws", "path": creds["ws_path"]})
            outbound.update(uuid=creds["uuids"][tag], security="auto", alter_id=0,
                            tls=tls(False, ["http/1.1"]), transport={"type": "ws", "path": creds["ws_path"],
                                "headers": {"Host": s.tls_domain}})
        elif kind in ("trojan", "hysteria2"):
            alpn = ["h3"] if kind == "hysteria2" else None
            inbound.update(users=[{"name": "user1", "password": creds["passwords"][tag]}], tls=tls(True, alpn))
            outbound.update(password=creds["passwords"][tag], tls=tls(False, alpn))
            if kind == "hysteria2":
                for item in (inbound, outbound):
                    item["obfs"] = {"type": "salamander", "password": creds["hy2_obfs"]}
                    if new_fields:
                        item["bbr_profile"] = "standard"
        elif kind == "hysteria":
            for item in (inbound, outbound):
                item.update(up_mbps=s.hy1_mbps, down_mbps=s.hy1_mbps, obfs=creds["hy1_obfs"])
            inbound.update(users=[{"name": "user1", "auth_str": creds["passwords"][tag]}], tls=tls(True, ["hysteria"]))
            outbound.update(auth_str=creds["passwords"][tag], tls=tls(False, ["hysteria"]))
        else:
            for item in (inbound, outbound):
                item.update(method="2022-blake3-aes-128-gcm", password=creds["ss_key"])
        inbounds.append(inbound)
        nodes.append(outbound)

    server = {"log": {"level": "info", "timestamp": True},
        "dns": {"servers": [{"type": "local", "tag": "dns-local"}], "final": "dns-local"},
        "inbounds": inbounds, "outbounds": [{"type": "direct", "tag": "direct"}],
        "route": {"final": "direct", "default_domain_resolver": "dns-local"}}
    default_node = s.default_node or s.tags[0]
    base = next(node for node in nodes if node["tag"] == default_node)
    special_nodes = []
    for tag in ("site-node", "app-node"):
        node = copy.deepcopy(base)
        node["tag"] = tag
        special_nodes.append(node)

    def selector(tag, candidates, default):
        return {"type": "selector", "tag": tag, "outbounds": candidates,
                "default": default, "interrupt_exist_connections": True}

    def doh(tag, detour):
        return {"type": "https", "tag": tag, "server": "1.1.1.1", "server_port": 443,
                "path": "/dns-query", "tls": {"enabled": True, "server_name": "cloudflare-dns.com"}, "detour": detour}

    # Matchers are separate rules: process_name and process_path are alternatives.
    # Site rules precede app rules, so a site match wins when both match.
    matchers = [(SITE_MATCHER, "site-proxy", "dns-site")]
    matchers += [(matcher, "app-proxy", "dns-app") for matcher in APP_MATCHERS[s.platform]]
    dns_rules = [dict(copy.deepcopy(matcher), action="route", server=dns)
                 for matcher, _, dns in matchers]
    route_rules = [{"port": 53, "action": "hijack-dns"},
                   {"ip_is_private": True, "action": "route", "outbound": "direct"},
                   {"action": "sniff"}]
    route_rules += [dict(copy.deepcopy(matcher), action="route", outbound=outbound)
                    for matcher, outbound, _ in matchers]
    client = {"log": {"level": "info", "timestamp": True},
        "dns": {"servers": [
            {"type": "udp", "tag": "dns-bootstrap", "server": s.bootstrap_dns, "server_port": 53},
            doh("dns-remote", "proxy"), doh("dns-site", "site-proxy"), doh("dns-app", "app-proxy")],
            "rules": dns_rules, "final": "dns-remote"},
        "inbounds": [{"type": "mixed", "tag": "mixed-in", "listen": "127.0.0.1", "listen_port": s.mixed_port}],
        "outbounds": [
            selector("proxy", ["auto"] + s.tags, default_node),
            selector("site-proxy", ["site-node", "direct"] + s.tags, "site-node"),
            selector("app-proxy", ["app-node", "direct"] + s.tags, "app-node"),
            {"type": "urltest", "tag": "auto", "outbounds": s.tags,
             "url": "https://www.gstatic.com/generate_204", "interval": "3m", "tolerance": 50},
            *nodes, *special_nodes, {"type": "direct", "tag": "direct"}],
        "route": {"rules": route_rules, "final": "proxy", "default_domain_resolver": "dns-bootstrap",
                  "auto_detect_interface": True},
        "experimental": {"clash_api": {"external_controller": f"127.0.0.1:{s.api_port}",
                                       "secret": creds["api_secret"]}}}
    tun = copy.deepcopy(client)
    tun_inbound = {"type": "tun", "tag": "tun-in", "address": ["172.19.0.1/30", "fdfe:dcba:9876::1/126"],
                   "mtu": 1500, "auto_route": True, "strict_route": True}
    if new_fields:
        tun_inbound["dns_mode"] = "hijack"
    tun["inbounds"].insert(0, tun_inbound)
    return {"server.json": server, "client.json": client, "client-tun.json": tun}


def generated_readme(s):
    ports = "\n".join(f"| {tag} | {s.ports[tag]} | {' / '.join(BY_TAG[tag][4])} |" for tag in s.tags)
    return f"""# 本次生成的 sing-box 配置

- 目标版本：{s.version}，配置系列：{s.family}
- 服务器：{s.server}，监听：{s.listen}
- 客户端平台：{s.platform}，默认节点：{s.default_node or s.tags[0]}
- 本机代理：127.0.0.1:{s.mixed_port}，Clash API：127.0.0.1:{s.api_port}
- 普通客户端与 TUN 客户端各自完整，选择一份运行。

| 节点 | 端口 | 传输 |
| --- | --- | --- |
{ports}

UUID、密码、REALITY 密钥对、SS 2022 密钥、WS 路径与 API 密码已生成并填入配置。
API 密码位于客户端 experimental.clash_api.secret。文件包含真实私钥和密码。
普通 TLS 节点需要准备覆盖 {s.tls_domain} 的证书：
证书链 `{s.certificate}`，私钥 `{s.key}`。建议使用 ECDSA/RSA 证书。
REALITY 握手目标为 `{s.reality_sni}:443`，需要从服务器可达。

## 手动替换站点和 App 模板

直接编辑你要使用的 client.json 或 client-tun.json；两份文件不会自动同步。

1. 搜索 `replace-site.example.invalid`，替换成需要独立出口的域名，不带协议和路径。
   domain_suffix 匹配该域名及其子域名。route.rules 和 dns.rules 中都要替换。
2. 搜索 `REPLACE_APP` 或 `invalid.example.replace_app`，替换成进程名、完整可执行文件路径，
   或 Android 包名。route.rules 和 dns.rules 中都要替换。
   进程名和路径使用分开的规则，表示任选一个匹配即可；不要合成一个需要同时匹配的规则。
3. 编辑 outbounds 中 tag 为 `site-node`、`app-node` 的节点，填写各自服务器、端口和认证/TLS 信息。
   它们初始是默认节点的副本，因此当前出口仍是同一台 VPS。获得不同出口 IP 需要真正不同的上游节点。
   更换协议时替换整个 outbound 对象，并保留原 tag；对应服务器需另行配置，不会自动生成第二台服务器。
4. `site-proxy`、`app-proxy` 是两个独立选择组，分别默认使用 site-node、app-node。
   要让指定流量直连，可把对应组的 default 改成 `direct`，或使用 API 运行时切换。

规则顺序：DNS 接管 → 私有 IP 直连 → 嗅探域名 → 站点规则 → App 规则 → 默认 proxy。
同一请求同时命中站点和 App 时，站点规则优先。站点匹配需要域名可见：
使用 TUN DNS、SOCKS5 代理解析域名或可嗅探的域名。只提供 IP、使用 ECH 等情况可能无法恢复域名。
桌面 process_name/process_path 规则需要系统权限及可识别的本机进程，App 分流优先使用 TUN。
Android 使用 package_name，需要图形客户端提供应用识别能力；iOS 不支持此处的任意 App 进程分流。
设备作为其他设备的网关时，不能据此识别远端设备的应用进程。

DNS 模板给站点和 App 分别预留了 dns-site、dns-app，经对应出口组发起 DoH。
操作系统 DNS 服务可能代应用查询，使 App DNS 无法匹配原应用；应用自带 DoH 也不会命中这些 DNS 规则。
bootstrap DNS `{s.bootstrap_dns}` 使用直连明文 UDP，用来解析未来手动填写的上游服务器域名。
路由 default_domain_resolver 保持 dns-bootstrap，避免上游域名解析回环。

## 运行

```sh
sing-box version
sing-box check -c server.json
sing-box check -c client.json
sing-box check -c client-tun.json

# VPS 上运行；需已准备证书并放行端口
sudo sing-box run -c server.json

# 客户端选择一项
sing-box run -c client.json
# 或：sudo sing-box run -c client-tun.json
```

修改后使用目标系列核心重新执行 check。生成器不会安装、升级、启动核心或修改防火墙。
1.12/1.13 的 TUN 未使用 1.14 的 dns_mode，必要时手动将系统 DNS 设为 172.19.0.2。
TUN 需要网络管理权限；Linux 可按环境增加 auto_redirect: true，需要 nftables。
Android 图形客户端需授予 VPN 权限。TUN 地址如与现有网段冲突，先修改。

运行时切换示例（替换 API_SECRET；组名也可以改成 proxy 或 app-proxy）：

```sh
curl -X PUT http://127.0.0.1:{s.api_port}/proxies/site-proxy \\
  -H 'Authorization: Bearer API_SECRET' \\
  -H 'Content-Type: application/json' -d '{{"name":"direct"}}'
```

未启用选择缓存，重启后恢复各组 default；切换可能中断现有连接。
"""


def write_output(directory, configs, readme):
    # A fresh directory prevents silent credential replacement on repeated runs.
    directory.mkdir(mode=0o700, parents=True, exist_ok=False)
    for name, content in {**configs, "README.md": readme}.items():
        path = directory / name
        with path.open("x", encoding="utf-8") as handle:
            if os.name == "posix":
                os.fchmod(handle.fileno(), 0o600)
            handle.write(content if isinstance(content, str) else json.dumps(content, ensure_ascii=False, indent=2) + "\n")


def main():
    parser = argparse.ArgumentParser(description="交互生成 sing-box 1.12/1.13/1.14 服务端和客户端配置")
    parser.add_argument("--sing-box", metavar="PATH", help="用于检测本机版本、生成 REALITY 密钥的核心路径")
    parser.add_argument("--output", type=Path, help="新的输出目录；已存在时拒绝覆盖")
    args = parser.parse_args()
    binary = args.sing_box or shutil.which("sing-box")
    if args.sing_box and not detect_version(binary):
        parser.error("--sing-box 指定的核心不能执行 version，请检查路径")
    settings = collect_settings(binary, detect_version(binary))
    default_path = Path(__file__).resolve().parent / "output" / (
        settings.family + "-" + datetime.now().strftime("%Y%m%d-%H%M%S-%f"))
    directory = args.output if args.output is not None else Path(ask("输出目录（必须是新目录）", default_path))
    directory = directory.expanduser().resolve()
    configs = build_configs(settings)
    write_output(directory, configs, generated_readme(settings))
    print(f"\n已生成：{directory}")
    print("  server.json / client.json / client-tun.json / README.md")
    print("认证信息已填入；请准备服务端证书，并按 README 替换站点和 App 分流模板。")
    print("site-node/app-node 初始使用当前服务器，独立出口需手动换成相应上游。")
    print("请使用目标版本 sing-box check 校验，再启动。")


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\n已取消。", file=sys.stderr)
        sys.exit(130)
    except (OSError, ValueError) as error:
        print(f"错误：{error}", file=sys.stderr)
        sys.exit(1)
