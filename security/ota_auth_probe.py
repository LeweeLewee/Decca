"""Bounded ArduinoOTA authentication probe. Never opens a firmware server.

Run only against the owner's controller. No secrets or firmware are used.
A timeout is inconclusive, never a passing rejection test.
"""
import argparse
import json
import re
import socket


def probe(host, port=3232, timeout=5):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(timeout)
        sock.connect((host, port))
        # A minimal invitation; no TCP listener and no firmware payload exist.
        sock.send(b"0 9 1 d41d8cd98f00b204e9800998ecf8427e\n")
        reply = sock.recv(256)
        if reply == b"OK":
            return {"status": "FAIL", "reason": "Update invitation accepted without authentication"}
        if not re.fullmatch(rb"AUTH [0-9a-fA-F]{32}", reply):
            return {"status": "INCONCLUSIVE", "reason": "Unexpected challenge response"}
        # Deliberately invalid proof. No real password is loaded or guessed.
        sock.send(b"200 " + b"0" * 32 + b" " + b"0" * 32 + b"\n")
        reply = sock.recv(256)
        if reply == b"Authentication Failed":
            return {"status": "PASS", "reason": "Authentication required; invalid proof rejected"}
        return {"status": "FAIL" if reply == b"OK" else "INCONCLUSIVE",
                "reason": "Invalid proof accepted" if reply == b"OK" else "Unexpected rejection response"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("host")
    args = parser.parse_args()
    try:
        result = probe(args.host)
    except OSError as error:
        result = {"status": "INCONCLUSIVE", "reason": type(error).__name__}
    print(json.dumps(result))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
