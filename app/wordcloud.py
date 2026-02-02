from wordcloud import WordCloud
import os
from typing import Dict, Optional
try:
    import numpy as np
    from PIL import Image
except ImportError:
    np = None
    Image = None


def generate_wordcloud(
    word_count: Dict[str, int],
    output_path: str,
    max_word_number: int,
    width: int = 800,
    height: int = 400,
    background_color: str = "white",
    shape_path: Optional[str] = None,
    font_path: Optional[str] = None,
    palette: Optional[str] = None,
):
    # Limit the number of words to max_word_number
    limited_word_count = dict(
        sorted(word_count.items(), key=lambda item: item[1], reverse=True)[
            : max_word_number
        ]
    )

    mask = None
    if shape_path:
        if np is None or Image is None:
            print(
                "Shape path provided but numpy/PIL not available. Proceeding without mask."
            )
        elif not os.path.exists(shape_path):
            print(f"Shape file not found: {shape_path}. Proceeding without mask.")
        else:
            try:
                # Convert image to grayscale array for mask
                mask = np.array(Image.open(shape_path).convert("L"))
            except Exception as e:
                print(f"Failed to load shape mask from {shape_path}: {e}")

    # Determine color function based on palette input
    color_func = None
    if palette:
        def _resolve_colors(pal: str):
            presets = {
                "base": ["#BB0404", "#FF8800", "#A510A5","#800000", "#008000", "#090961", "#3C0085"],
                "pastel": ["#AEC6CF", "#FFD1DC", "#FFB347", "#B39EB5", "#77DD77", "#CFCFC4", "#F49AC2", "#CB99C9", "#FDFD96", "#CDEAC0"],
                "vibrant": ["#E6194B", "#3CB44B", "#FFE119", "#0082C8", "#F58231", "#911EB4", "#46F0F0", "#F032E6", "#FABEBE", "#008080"],
                "cool": ["#0E6CFF", "#3A86FF", "#48BFE3", "#56CFE1", "#72EFDD", "#80FFDB", "#64DFDF", "#4EA8DE"],
                "warm": ["#FF595E", "#FF924C", "#FFCA3A", "#FB5607", "#FF7B00", "#FF006E", "#E85D04", "#DC2F02"],
                "earth": ["#7F5539", "#9C6644", "#B08968", "#DDB892", "#EDE0D4", "#CCD5AE", "#A3B18A", "#588157"],
            }
            p = pal.strip()
            low = p.lower()
            if low in presets:
                return presets[low]
            if low.startswith("mono-"):
                color = p.split("-", 1)[1].strip()
                if not color.startswith("#"):
                    color = "#" + color
                return [color] * 10
            if "," in p:
                cols = []
                for c in p.split(","):
                    c = c.strip()
                    if not c:
                        continue
                    if not c.startswith("#"):
                        c = "#" + c
                    cols.append(c)
                return cols
            if p.startswith("#"):
                return [p]
            return None

        colors = _resolve_colors(palette)
        if colors:
            import random as _random
            def color_func(*args, **kwargs):
                return _random.choice(colors)

    # Build kwargs to avoid passing None-typed color_func when unset (type-checker friendly)
    kwargs = dict(width=width, height=height, background_color=background_color, font_path=font_path)
    if mask is not None:
        kwargs["mask"] = mask
    if color_func is not None:
        kwargs["color_func"] = color_func
    wc = WordCloud(**kwargs)

    wordcloud = wc.generate_from_frequencies(limited_word_count)

    # Ensure output directory exists
    out_dir = os.path.dirname(output_path) or "."
    os.makedirs(out_dir, exist_ok=True)

    wordcloud.to_file(output_path)
    print(f"Word cloud saved to {output_path}")
