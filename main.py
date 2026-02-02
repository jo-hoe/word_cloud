import argparse
import os
from app.strategies import get_strategy
from app.blocklist import load_blocklist_words, load_blocklist_regex
from app.analyzer import word_counts_from_texts
from app.wordcloud import generate_wordcloud


def main():
    parser = argparse.ArgumentParser(
        description="Analyze input sources and generate word clouds."
    )
    parser.add_argument("input_source", type=str,
                        help="Path to the source file.")
    parser.add_argument("--input_type", type=str, default="whatsapp",
                        help="Type of input source (e.g., 'whatsapp').")
    parser.add_argument(
        "--blocklist_word_file", required=False, type=str, help="Path to the word blocklist file."
    )
    parser.add_argument(
        "--blocklist_regex_file", required=False, type=str, help="Path to the regex blocklist file."
    )
    parser.add_argument(
        "--output",
        type=str,
        default="output/output.png",
        help="Path to save the generated word cloud PNG (directory will be created if needed).",
    )
    parser.add_argument(
        "--max_word_number",
        type=int,
        default=124,
        help="Maximum number of words to be in the output.",
    )
    parser.add_argument(
        "--width",
        type=int,
        default=800,
        help="Width of the generated word cloud image.",
    )
    parser.add_argument(
        "--height",
        type=int,
        default=400,
        help="Height of the generated word cloud image.",
    )
    parser.add_argument(
        "--background_color",
        type=str,
        default="white",
        help="Background color of the generated word cloud image.",
    )
    parser.add_argument(
        "--min_word_length",
        type=int,
        default=3,
        help="Minimum length of words to consider.",
    )
    parser.add_argument(
        "--shape_path",
        type=str,
        help="Optional path to an image file used as a mask/shape for the word cloud.",
    )

    args = parser.parse_args()

    input_source = args.input_source
    input_type = args.input_type
    output_path = args.output

    # Ensure output directory exists (also handled in generate_wordcloud, but done here per requirement)
    out_dir = os.path.dirname(output_path) or "."
    if not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    # Resolve strategy for the given input type
    strategy = get_strategy(input_type)

    # Extract texts via strategy
    texts = strategy.extract_texts(input_source)

    # Load blocklists
    blocklist_words = load_blocklist_words(args.blocklist_word_file)
    blocklist_regex = load_blocklist_regex(args.blocklist_regex_file)

    # Compute word counts
    counts = word_counts_from_texts(
        texts, args.min_word_length, blocklist_words, blocklist_regex
    )

    # Generate and save word cloud
    generate_wordcloud(
        counts,
        output_path,
        args.max_word_number,
        width=args.width,
        height=args.height,
        background_color=args.background_color,
        shape_path=args.shape_path,
    )
    print(f"Word cloud will be saved to: {output_path}")


if __name__ == "__main__":
    main()
