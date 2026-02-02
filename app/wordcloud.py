from wordcloud import WordCloud
import os
from typing import Dict, Optional, Any, Callable
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
    background_color: str,
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
    color_func: Optional[Callable[..., str]] = None
    if palette:
        def _resolve_colors(pal: str):
            presets = {
                "redvsblue": ["#051e3e", "#251e3e", "#451e3e", "#651e3e", "#851e3e"],
                "pastel": ["#5A9CB5", "#FACE68", "#FAAC68", "#FA6868", "#A3D39C"],
                "orange": ["#7C444F", "#9F5255", "#E16A54", "#F39E60"],
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

            def _color_func(*args, **kwargs):
                return _random.choice(colors)
            color_func = _color_func

    # Build kwargs to avoid passing None-typed values when unset (type-checker friendly)
    kwargs: Dict[str, Any] = {"background_color": background_color}
    if font_path is not None:
        kwargs["font_path"] = font_path
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
