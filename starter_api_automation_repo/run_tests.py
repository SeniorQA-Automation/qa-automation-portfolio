"""
run_tests.py
Simple runner that executes pytest.
"""
import subprocess
import sys

def main():
    cmd = [sys.executable, "-m", "pytest", "-q"]
    result = subprocess.run(cmd)
    raise SystemExit(result.returncode)

if __name__ == "__main__":
    main()
