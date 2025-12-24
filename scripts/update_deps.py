import subprocess
import shutil
import sys
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent

REQ_IN = ROOT / "requirements.in"
REQ_TXT = ROOT / "requirements.txt"
BACKUPS = ROOT / "requirements_backups"


def run(cmd: list[str]) -> None:
    print(f"→ {' '.join(cmd)}")
    subprocess.run(cmd, check=True)


def main():
    if not REQ_IN.exists():
        print("requirements.in not found")
        sys.exit(1)

    BACKUPS.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = BACKUPS / f"requirements_{timestamp}.txt"

    try:
        # Backup existing requirements.txt
        if REQ_TXT.exists():
            shutil.copy2(REQ_TXT, backup_file)
            print(f"✓ Backup created: {backup_file}")

        # Compile dependencies
        run([
            "pip-compile",
            str(REQ_IN),
            "--generate-hashes",
            
        ])

        # Sync environment
        run(["pip-sync", str(REQ_TXT)])

        # Sanity check
        run(["pip", "check"])

        print("✓ Dependencies updated successfully")

    except subprocess.CalledProcessError:
        print("✗ Dependency update failed")

        # Rollback
        if backup_file.exists():
            shutil.copy2(backup_file, REQ_TXT)
            print("↩ Rolled back requirements.txt")

            try:
                run(["pip-sync", str(REQ_TXT)])
                print("✓ Environment restored")
            except subprocess.CalledProcessError:
                print("⚠ Rollback sync failed — check manually")

        sys.exit(1)


if __name__ == "__main__":
    main()
