# word_cloud

[![CI](https://github.com/jo-hoe/word_cloud/actions/workflows/ci.yml/badge.svg)](https://github.com/jo-hoe/word_cloud/actions/workflows/ci.yml)
[![Dependabot](https://img.shields.io/badge/Dependabot-enabled-brightgreen?logo=dependabot)](https://github.com/jo-hoe/word_cloud/security/dependabot)
[![Lint: flake8](https://img.shields.io/badge/lint-flake8-blueviolet)](https://github.com/jo-hoe/word_cloud/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.12-blue)

Generate word clouds from chat exports (e.g., WhatsApp).

Example command:

```PowerShell
python .\main.py "input\<unzipped whatsapp backup file.txt>" --blocklist_word_file "input\word_blocklist.txt" --font_path "C:\Windows\Fonts\seguiemj.ttf" --shape_path "input\heart.png" --palette base
```
