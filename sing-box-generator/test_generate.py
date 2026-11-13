import base64
import copy
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import uuid

import generate as gen


def sample_settings(version="1.14", platform="linux", tags=None):
    tags = tags or [entry[0] for entry in gen.PROTOCOLS]
    credentials = gen.generate_credentials([tag for tag in tags if tag != "vless-reality"], None)
    # Test-only keys; native checks parse them but do not perform a handshake.
    credentials.update(private_key=base64.urlsafe_b64encode(bytes(range(32))).decode().rstrip("="),
                       public_key=base64.urlsafe_b64encode(bytes(range(32, 64))).decode().rstrip("="))
    credentials["uuids"]["vless-reality"] = str(uuid.uuid4())
    return gen.Settings(version, "2001:db8::1", tags,
                        {tag: gen.BY_TAG[tag][3] for tag in tags}, platform=platform,
                        listen="::", default_node=tags[0], credentials=credentials)


class GeneratorTests(unittest.TestCase):
    def test_local_version_is_default(self):
        answers = ["", "192.0.2.2", "", "7", "", "", "", "", "", ""]
        with patch("builtins.input", side_effect=answers), patch("builtins.print"):
            settings = gen.collect_settings(None, "1.12.13")
        self.assertEqual(settings.version, "1.12.13")
        self.assertEqual(settings.tags, ["ss2022"])

    def test_port_collisions_are_reprompted(self):
        answers = ["1.14", "192.0.2.2", "linux", "1,2", "443", "443", "8444",
                   "", "proxy.example.com", "", "", "", "2080", "2080", "9090", "", ""]
        with patch("builtins.input", side_effect=answers), patch("builtins.print"), \
                patch.object(gen, "generate_credentials", return_value={}):
            settings = gen.collect_settings(None, None)
        self.assertEqual(settings.ports, {"vless-reality": 443, "vless-tls": 8444})
        self.assertEqual(settings.api_port, 9090)

    def test_version_and_input_validation(self):
        for value, expected in [("1.12", "1.12"), ("1.13.0", "1.13"),
                                ("v1.14.3", "1.14"), ("1.14.0-rc.1", "1.14")]:
            self.assertEqual(gen.version_family(value), expected)
        for value in ("1.11", "1.15.0", "1.14oops", "2.14", "1.140"):
            with self.assertRaises(ValueError):
                gen.version_family(value)
        for value in ("0", "65536", "abc"):
            with self.assertRaises(ValueError):
                gen.port_number(value)
        self.assertEqual(gen.ip_address("[2001:db8::1]"), "2001:db8::1")
        self.assertEqual(gen.select_protocols("7,1,7"), ["vless-reality", "ss2022"])
        for value in ("https://example.com", "example.com:443", "127.0.0.1"):
            with self.assertRaises(ValueError):
                gen.domain_name(value)

    def test_protocol_credentials_and_ports_match(self):
        s = sample_settings()
        s.ports["vless-reality"] = 10443
        s.ports["hy2"] = 20443
        configs = gen.build_configs(s)
        outs = {item["tag"]: item for item in configs["client.json"]["outbounds"]}
        for inbound in configs["server.json"]["inbounds"]:
            tag = inbound["tag"].removesuffix("-in")
            outbound = outs[tag]
            self.assertEqual(inbound["listen_port"], outbound["server_port"])
            self.assertEqual(inbound["type"], outbound["type"])
            if inbound["type"] in ("vless", "vmess"):
                self.assertEqual(inbound["users"][0]["uuid"], outbound["uuid"])
            elif inbound["type"] in ("trojan", "hysteria2"):
                self.assertEqual(inbound["users"][0]["password"], outbound["password"])
            elif inbound["type"] == "hysteria":
                self.assertEqual(inbound["users"][0]["auth_str"], outbound["auth_str"])
            else:
                self.assertEqual(inbound["password"], outbound["password"])
                self.assertEqual(len(base64.b64decode(outbound["password"])), 16)
            if "obfs" in inbound:
                self.assertEqual(inbound["obfs"], outbound["obfs"])

    def test_version_gates_and_standalone_selection(self):
        for family in gen.FAMILIES:
            configs = gen.build_configs(sample_settings(family))
            for name in ("server.json", "client.json"):
                entries = configs[name].get("outbounds", []) + configs[name]["inbounds"]
                hy2 = next(item for item in entries if item["type"] == "hysteria2")
                self.assertEqual("bbr_profile" in hy2, family == "1.14")
            tun = configs["client-tun.json"]["inbounds"][0]
            self.assertEqual("dns_mode" in tun, family == "1.14")
        single = gen.build_configs(sample_settings("1.12", tags=["ss2022"]))
        self.assertEqual(len(single["server.json"]["inbounds"]), 1)
        self.assertNotIn('"type": "vless"', json.dumps(single))

    def test_independent_groups_and_platform_rules(self):
        for platform in gen.APP_MATCHERS:
            configs = gen.build_configs(sample_settings(platform=platform))
            client, tun = configs["client.json"], configs["client-tun.json"]
            self.assertEqual(client["outbounds"], tun["outbounds"])
            self.assertEqual(client["route"], tun["route"])
            outs = {item["tag"]: item for item in client["outbounds"]}
            for item in outs.values():
                for target in item.get("outbounds", []):
                    self.assertIn(target, outs)
            self.assertEqual(outs["site-proxy"]["default"], "site-node")
            self.assertEqual(outs["app-proxy"]["default"], "app-node")
            # Editing a dedicated node must not edit the default node or other node.
            original = copy.deepcopy(outs["vless-reality"])
            outs["site-node"]["tls"]["server_name"] = "other.example.com"
            self.assertEqual(outs["vless-reality"], original)
            self.assertEqual(outs["app-node"]["tls"], original["tls"])
            route_rules = client["route"]["rules"]
            self.assertEqual(route_rules[3]["outbound"], "site-proxy")
            for matcher in gen.APP_MATCHERS[platform]:
                for key, value in matcher.items():
                    self.assertTrue(any(rule.get(key) == value and rule.get("outbound") == "app-proxy"
                                        for rule in route_rules))
                    self.assertTrue(any(rule.get(key) == value and rule.get("server") == "dns-app"
                                        for rule in client["dns"]["rules"]))

    def test_cli_and_existing_directory_protection(self):
        with tempfile.TemporaryDirectory() as parent:
            output = Path(parent) / "result"
            # Explicit version, IPv6, platform, SS only, server port/listen,
            # mixed port/API port/bootstrap DNS/default node.
            answers = "\n".join(["1.13", "2001:db8::8", "linux", "7", "18388", "",
                                  "12080", "19090", "1.1.1.1", "", ""])
            command = [sys.executable, str(Path(gen.__file__)), "--output", str(output)]
            first = subprocess.run(command, input=answers, text=True, capture_output=True)
            self.assertEqual(first.returncode, 0, first.stderr + first.stdout)
            server = json.loads((output / "server.json").read_text())
            self.assertEqual(server["inbounds"][0]["listen_port"], 18388)
            self.assertEqual(server["inbounds"][0]["listen"], "::")
            before = (output / "server.json").read_bytes()
            second = subprocess.run(command, input=answers, text=True, capture_output=True)
            self.assertNotEqual(second.returncode, 0)
            self.assertEqual((output / "server.json").read_bytes(), before)
            if os.name == "posix":
                self.assertEqual(output.stat().st_mode & 0o777, 0o700)
                self.assertEqual((output / "server.json").stat().st_mode & 0o777, 0o600)

    def test_with_native_cores(self):
        binaries = {family: os.environ.get("SING_BOX_" + family.replace(".", "_"))
                    for family in gen.FAMILIES}
        binaries = {family: path for family, path in binaries.items() if path}
        if not binaries:
            self.skipTest("设置 SING_BOX_1_12 / SING_BOX_1_13 / SING_BOX_1_14 可执行真实核心校验")
        if not shutil.which("openssl"):
            self.skipTest("真实核心校验需要 openssl 生成临时证书")
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            certificate, key = root / "cert.pem", root / "key.pem"
            subprocess.run(["openssl", "req", "-x509", "-newkey", "ec", "-pkeyopt", "ec_paramgen_curve:P-256",
                "-nodes", "-keyout", str(key), "-out", str(certificate), "-days", "1",
                "-subj", "/CN=proxy.example.com"], check=True, capture_output=True)
            for family, binary in binaries.items():
                self.assertEqual(gen.version_family(gen.detect_version(binary)), family)
                for platform in gen.APP_MATCHERS:
                    settings = sample_settings(family, platform)
                    settings.certificate, settings.key = str(certificate), str(key)
                    for name, config in gen.build_configs(settings).items():
                        with self.subTest(family=family, platform=platform, config=name):
                            target = root / name
                            target.write_text(json.dumps(config))
                            result = subprocess.run([binary, "check", "-c", str(target)],
                                                    capture_output=True, text=True)
                            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)


if __name__ == "__main__":
    unittest.main()
