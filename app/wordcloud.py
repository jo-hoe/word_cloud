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

    if mask is not None:
        wc = WordCloud(width=width, height=height, background_color=background_color, mask=mask, font_path=font_path)
    else:
        wc = WordCloud(width=width, height=height, background_color=background_color, font_path=font_path)

    wordcloud = wc.generate_from_frequencies(limited_word_count)

    # Ensure output directory exists
    out_dir = os.path.dirname(output_path) or "."
    os.makedirs(out_dir, exist_ok=True)

    wordcloud.to_file(output_path)
    print(f"Word cloud saved to {output_path}")
