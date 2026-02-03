# word_cloud

[![CI](https://github.com/jo-hoe/word_cloud/actions/workflows/ci.yml/badge.svg)](https://github.com/jo-hoe/word_cloud/actions/workflows/ci.yml)
[![Dependabot](https://img.shields.io/badge/Dependabot-enabled-brightgreen?logo=dependabot)](https://github.com/jo-hoe/word_cloud/security/dependabot)
[![Lint: flake8](https://img.shields.io/badge/lint-flake8-blueviolet)](https://github.com/jo-hoe/word_cloud/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.12-blue)

Generate word clouds from source files (e.g. whatsapp chat backup files)

## Installation

- Python 3.12 (as used in CI)
- pip install -r requirements.txt

## Usage

Basic:
- PowerShell (Windows)
  ```powershell
  python .\main.py "input\my_backup_xhst_file.txt" --blocklist_word_file "input\word_blocklist.txt" --palette pastel
  ```

