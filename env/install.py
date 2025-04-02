import subprocess
import sys

failed_packages = []

with open('requirements.txt') as f:
    for line in f:
        package = line.strip()
        if not package or package.startswith('#'):
            continue

        print(f"🔄 Installing: {package}")
        try:
            result = subprocess.run(
                [sys.executable, '-m', 'pip', 'install', package],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            print(f"✅ Successfully installed: {package}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install: {package}")
            print(f"🪵 Error message:\n{e.stderr.strip()}")
            failed_packages.append(package)

if failed_packages:
    with open('failed_packages.txt', 'w') as fail_log:
        fail_log.write('\n'.join(failed_packages))
    print(f"\n🚨 Some packages failed. See failed_packages.txt")
else:
    print("\n🎉 All packages installed successfully!")