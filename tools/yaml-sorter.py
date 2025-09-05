import glob
import subprocess
import sys
import logging


logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger("yaml-sorter")


command_lint = "yq eval 'sortKeys(..)' {file}"
command_fmt = "yq eval 'sortKeys(..)' -i {file}"


def lint():
    yaml_files = [
        file for file in glob.glob("**/*.yaml", recursive=True)
        if '/templates/' not in file
    ]
    failed = False
    for file in yaml_files:
        cmd = command_lint.format(file=file)
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            logger.error(f"Lint error in {file}: {result.stderr}")
            failed = True
        else:
            with open(file, "r") as f:
                original = f.read()
            if result.stdout.strip() != original.strip():
                logger.error(f"Lint failed: {file} is not sorted.")
            else:
                logger.debug(f"Linted: {file} (OK)")
    if failed:
        sys.exit(1)


def fmt():
    yaml_files = [
        file for file in glob.glob("**/*.yaml", recursive=True)
        if '/templates/' not in file
    ]
    for file in yaml_files:
        cmd = command_fmt.format(file=file)
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            logger.error(f"Format error in {file}: {result.stderr}")
        else:
            logger.debug(f"Formatted: {file}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python yaml-sorter.py [lint|fmt]")
        sys.exit(1)
    if sys.argv[1] == "lint":
        lint()
    elif sys.argv[1] == "fmt":
        fmt()
    else:
        print("Unknown command. Use 'lint' or 'fmt'.")
        sys.exit(1)
