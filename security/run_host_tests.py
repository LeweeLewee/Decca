"""Compile and execute production security headers on the host (no ESP32 emulation)."""
import argparse
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--zig', help='Path to portable zig executable; otherwise use c++')
args = parser.parse_args()
out = root / 'build' / 'security-host'
out.mkdir(parents=True, exist_ok=True)
exe = out / 'security_test.exe'
compiler = [args.zig, 'c++'] if args.zig else ['c++']
subprocess.run(compiler + ['-std=c++17', '-Wall', '-Wextra', '-Werror', '-I' + str(root / 'security/host'), '-I' + str(root / 'src'), str(root / 'security/host/security_test.cpp'), '-o', str(exe)], check=True)
subprocess.run([str(exe)], check=True)
