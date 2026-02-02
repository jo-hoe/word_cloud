from wordcloud import WordCloud
import os

def generate_wordcloud(word_count, output_dir, max_word_number):
    # Limit the number of words to max_word_number
    limited_word_count = dict(sorted(word_count.items(), key=lambda item: item[1], reverse=True)[:max_word_number])

    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(limited_word_count)

    output_path = os.path.join(output_dir, 'wordcloud.png')
    wordcloud.to_file(output_path)
    print(f"Word cloud saved to {output_path}")