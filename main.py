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
    parser.add_argument("input_source", type=str, help="Path to the source file.")
    parser.add_argument(
        "input_type", type=str, help="Type of input source (e.g., 'whatsapp')."
    )
    parser.add_argument(
        "--blocklist_word_file", type=str, help="Path to the word blocklist file."
    )
    parser.add_argument(
        "--blocklist_regex_file", type=str, help="Path to the regex blocklist file."
    )
    parser.add_argument(
        "--output",
        type=str,
        default="output",
        help="Directory to save the generated word clouds.",
    )
    parser.add_argument(
        "--min_word_length",
        type=int,
        default=3,
        help="Minimum length of words to consider.",
    )
    parser.add_argument(
        "--max_word_number",
        type=int,
        default=45,
        help="Maximum number of words to be in the output.",
    )

    args = parser.parse_args()

    input_source = args.input_source
    input_type = args.input_type
    output_dir = args.output

    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    # Resolve strategy for the given input type
    strategy = get_strategy(input_type)

    print(f"Processing input source: {input_source}")
    print(f"Input type: {input_type}")

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
    generate_wordcloud(counts, output_dir, args.max_word_number)
    print(f"Word clouds will be saved to: {output_dir}")


if __name__ == "__main__":
    main()