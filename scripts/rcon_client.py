"""RCON client for Minecraft server remote control.

Usage:
    from scripts.rcon_client import RconClient
    with RconClient("localhost", 25575, "particlefactory") as rcon:
        response = rcon.command("say Hello")
        print(response)
"""
import socket
import struct


class RconClient:
    """Minimal RCON client for Minecraft servers."""

    def __init__(self, host="localhost", port=25575, password=""):
        self.host = host
        self.port = port
        self.password = password
        self.sock = None
        self.request_id = 0

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(5)
        self.sock.connect((self.host, self.port))
        # Authenticate
        self._send(3, self.password)  # type 3 = login
        resp = self._recv()
        if resp[0] != self.request_id:
            raise ConnectionError("RCON authentication failed")
        return self

    def command(self, cmd):
        self.request_id += 1
        self._send(2, cmd)  # type 2 = command
        resp = self._recv()
        return resp[1]

    def _send(self, pkt_type, payload):
        data = struct.pack("<ii", self.request_id, pkt_type) + payload.encode("utf-8") + b"\x00\x00"
        self.sock.sendall(struct.pack("<i", len(data)) + data)

    def _recv(self):
        size = struct.unpack("<i", self.sock.recv(4))[0]
        data = self.sock.recv(size)
        req_id, pkt_type = struct.unpack("<ii", data[:8])
        payload = data[8:-2].decode("utf-8", errors="replace")
        return req_id, payload

    def close(self):
        if self.sock:
            self.sock.close()
            self.sock = None

    def __enter__(self):
        return self.connect()

    def __exit__(self, *args):
        self.close()


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Send RCON command")
    parser.add_argument("command", nargs="+", help="Command to send")
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", type=int, default=25575)
    parser.add_argument("--password", default="particlefactory")
    args = parser.parse_args()

    cmd = " ".join(args.command)
    try:
        with RconClient(args.host, args.port, args.password) as rcon:
            resp = rcon.command(cmd)
            print(resp)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    import sys
    main()
