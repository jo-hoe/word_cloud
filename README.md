# word_cloud

[![CI](https://github.com/jo-hoe/word_cloud/actions/workflows/ci.yml/badge.svg)](https://github.com/jo-hoe/word_cloud/actions/workflows/ci.yml)
[![Dependabot](https://img.shields.io/badge/Dependabot-enabled-brightgreen?logo=dependabot)](https://github.com/jo-hoe/word_cloud/security/dependabot)
[![Lint: flake8](https://img.shields.io/badge/lint-flake8-blueviolet)](https://github.com/jo-hoe/word_cloud/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.12-blue)

Generate word clouds from chat exports (e.g., WhatsApp). Supports:
- Emoji tokenization and rendering (auto-detected emoji-capable font)
- Word and regex blocklists (including emojis)
- Optional shape mask (PNG recommended)
- Custom color palettes

Note on image size:

## Installation

- Python 3.12 (as used in CI)
- pip install -r requirements.txt

## Usage

Basic:
- PowerShell (Windows)
  ```powershell
  python .\main.py "input\WhatsApp Chat with Elektra.txt" --blocklist_word_file "input\word_blocklist.txt"
  ```

With a color palette:
- Preset palette (e.g., pastel):
  ```powershell
  python .\main.py "input\WhatsApp Chat with Elektra.txt" --blocklist_word_file "input\word_blocklist.txt" --palette pastel
  ```
- Custom colors (comma-separated hex):
  ```powershell
  python .\main.py "input\WhatsApp Chat with Elektra.txt" --palette "#ff0000,#00ff00,#0000ff"
  ```
- Single color (monochrome):
  ```powershell
  python .\main.py "input\WhatsApp Chat with Elektra.txt" --palette mono-#333333
  ```

With a shape/mask (PNG recommended):
- A sample heart mask is provided: `input/heart.png`
  ```powershell
  python .\main.py "input\WhatsApp Chat with Elektra.txt" --shape_path "input\heart.png" --palette pastel
  ```

Output is saved to `output/output.png` by default.

## CLI Options

- `--input_type` (default: whatsapp)
- `--blocklist_word_file` Path to a plain word blocklist (tokens + emojis supported)
- `--blocklist_regex_file` Path to a regex blocklist (one regex per line)
- `--output` Path to save the PNG (default: output/output.png)
- `--max_word_number` Maximum words in the output (default: 124)
- `--background_color` Background color (default: white)
- `--min_word_length` Minimum token length for words (emojis bypass this)
- `--shape_path` Path to a raster image (PNG) used as a mask/shape
- `--font_path` Path to a TTF/OTF font file (emoji-capable font recommended)
- `--palette` Color palette for words:
  - Presets: `pastel`, `redvsblue`, `orange`
  - Comma-separated hex list: `"#ff0000,#00ff00,#0000ff"` (leading `#` optional)
  - Monochrome: `mono-#RRGGBB` (e.g., `mono-#333333`)

## Emoji Rendering

- If `--font_path` is omitted, the app auto-detects an emoji-capable font:
  - Windows: `C:\Windows\Fonts\seguiemj.ttf` (Segoe UI Emoji)
  - Ubuntu/Linux: tries Symbola/NotoEmoji in common locations
- Note: WordCloud/Pillow typically render monochrome glyphs for color emoji fonts.

## Blocklists

- Word blocklist (`--blocklist_word_file`): Uses the same tokenizer as the analyzer, so emojis in the blocklist are supported.
- Regex blocklist (`--blocklist_regex_file`): One regex per non-empty, non-comment line.

## Development

- Tests and linting:
  - CI runs on Windows and Linux (GitHub Actions)
  - Linting uses flake8
- Dependabot:
  - Weekly updates for GitHub Actions and pip dependencies

Run tests locally:
```bash
pip install pytest flake8
pytest -q
flake8 .
## Installation

- Python 3.12 (as used in CI)
- pip install -r requirements.txt

## Usage

Basic:
- PowerShell (Windows)
  ```powershell
  python .\main.py "input\WhatsApp Chat with Elektra.txt" --blocklist_word_file "input\word_blocklist.txt"
  ```

With a color palette:
- Preset palette (e.g., pastel):
  ```powershell
  python .\main.py "input\WhatsApp Chat with Elektra.txt" --blocklist_word_file "input\word_blocklist.txt" --palette pastel
  ```
- Custom colors (comma-separated hex):
  ```powershell
  python .\main.py "input\WhatsApp Chat with Elektra.txt" --palette "#ff0000,#00ff00,#0000ff"
  ```
- Single color (monochrome):
  ```powershell
  python .\main.py "input\WhatsApp Chat with Elektra.txt" --palette mono-#333333
  ```

With a shape/mask (PNG recommended):
- A sample heart mask is provided: `input/heart.png`
  ```powershell
  python .\main.py "input\WhatsApp Chat with Elektra.txt" --shape_path "input\heart.png" --palette pastel
  ```

Output is saved to `output/output.png` by default.

## CLI Options

- `--input_type` (default: whatsapp)
- `--blocklist_word_file` Path to a plain word blocklist (tokens + emojis supported)
- `--blocklist_regex_file` Path to a regex blocklist (one regex per line)
- `--output` Path to save the PNG (default: output/output.png)
- `--max_word_number` Maximum words in the output (default: 124)
- `--background_color` Background color (default: white)
- `--min_word_length` Minimum token length for words (emojis bypass this)
- `--shape_path` Path to a raster image (PNG) used as a mask/shape
- `--font_path` Path to a TTF/OTF font file (emoji-capable font recommended)
- `--palette` Color palette for words:
  - Presets: `pastel`, `redvsblue`, `orange`
  - Comma-separated hex list: `"#ff0000,#00ff00,#0000ff"` (leading `#` optional)
  - Monochrome: `mono-#RRGGBB` (e.g., `mono-#333333`)

## Emoji Rendering

- If `--font_path` is omitted, the app auto-detects an emoji-capable font:
  - Windows: `C:\Windows\Fonts\seguiemj.ttf` (Segoe UI Emoji)
  - Ubuntu/Linux: tries Symbola/NotoEmoji in common locations
- Note: WordCloud/Pillow typically render monochrome glyphs for color emoji fonts.

## Blocklists

- Word blocklist (`--blocklist_word_file`): Uses the same tokenizer as the analyzer, so emojis in the blocklist are supported.
- Regex blocklist (`--blocklist_regex_file`): One regex per non-empty, non-comment line.

## Development

- Tests and linting:
  - CI runs on Windows and Linux (GitHub Actions)
  - Linting uses flake8
- Dependabot:
  - Weekly updates for GitHub Actions and pip dependencies

Run tests locally:
```bash
pip install pytest flake8
pytest -q
