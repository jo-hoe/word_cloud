import argparse
import os


def main():
    parser = argparse.ArgumentParser(
        description="Analyze input sources and generate word clouds.")
    parser.add_argument("input_source", type=str,
                        required=True, help="Path to the source file.")
    parser.add_argument("input_type", type=str, required=True,
                        help="Type of input source (e.g., 'whatsapp').")
    parser.add_argument("--blocklist_word_file", type=str,
                        help="Path to the blacklist file.")
    parser.add_argument("--blocklist_regex_file", type=str,
                        help="Path to the regex blacklist file.")
    parser.add_argument("--output", type=str, default="output",
                        help="Directory to save the generated word clouds.")
    parser.add_argument("--min_word_length", type=int,
                        default=3, help="Minimum length of words to consider.")
    parser.add_argument("--max_word_number", type=int,
                        default=45, help="Maximum number of words to be in the output.")

    args = parser.parse_args()

    backup_file = args.input_source
    input_type = args.input_type
    output_dir = args.output
    blocklist_word_file = args.blocklist_word_file
    blocklist_regex_file = args.blocklist_regex_file
    min_word_length = args.min_word_length
    max_word_number = args.max_word_number

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Here you would call the functions from WhatsAppConversationAnalyzer
    # to process the backup file and generate word clouds.
    print(f"Processing input source: {backup_file}")
    print(f"Input type: {input_type}")
    print(f"Word clouds will be saved to: {output_dir}")
