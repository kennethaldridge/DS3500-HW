"""
File: text_analysis.py
Description: A reusable library for text analysis and comparison
"""
import matplotlib.pyplot as plt
from collections import Counter, defaultdict
import sankey as sk
import pandas as pd
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import seaborn as sns
from wordcloud import WordCloud

nltk.download('vader_lexicon')

class TextAnalysis:
    def __init__(self):
        """Constructor"""
        self.data = defaultdict(dict)

    @staticmethod
    def _default_parser(filename, stopwords_file):
        """this should probably be a default text parser for processing simple
        unformatted text files."""

        # Get the stop words
        stopwords = TextAnalysis._load_stop_words(stopwords_file)

        with open(filename, 'r') as file:
            text = file.read()

        # Remove puncuation, digits, \n's, etc and also lowercase everything
        cleaned_text = ''.join(filter(lambda x: x.isalpha() or x.isdigit() or x.isspace(), text))
        cleaned_text = cleaned_text.replace('\n', ' ').lower()

        # Get the list of words for the text
        words = [word for word in cleaned_text.split() if word not in stopwords]

        # Get sentiment
        sia = SentimentIntensityAnalyzer()
        sentiment_score = sia.polarity_scores(text)

        results = {
            'wordcount': Counter(words),
            'total_words': len(words),
            'cleaned text': ' '.join(words),
            'sentiment': sentiment_score
        }

        return results

    @staticmethod
    def _load_stop_words(filename):
        """Loads the stop words from a file into a list"""
        stop_words = []
        with open(filename, 'r') as file:
            for line in file:
                word = line.strip()
                stop_words.append(word)

        return stop_words

    def load_text(self, filename, stopwords_file, label=None, parser=None):  # customize parser for dataset
        # default takes normal text file without any special formatting
        if parser is None:
            results = TextAnalysis._default_parser(filename, stopwords_file)
        else:
            results = parser(filename)

        if label is None:
            label = filename

        for k, v in results.items():
            self.data[k][label] = v

    def wordcount_sankey(self, word_list=None, k=5, save=False):
        """Creates a sankey diagram of the most common words for the text files"""
        wordcounts_dict = self.data['wordcount']

        if word_list is None:
            sorting_df = pd.DataFrame(
                wordcounts_dict)

            # Sum the word counts across all songs
            total_word_counts = sorting_df.sum(axis=1)

            # Sort the word counts in descending order and get the k most common
            sorted_word_counts = total_word_counts.sort_values(ascending=False)
            most_common = list(sorted_word_counts[:k].index)
        else:
            most_common = word_list

        # Initialize a dictionary to store the data, will be used in a dataframe
        data = {'label': [], 'word': [], 'count': []}

        # Go through each word in the most common words and add the number of time it's in each song to data
        for word in most_common:
            for label in wordcounts_dict.keys():
                label_word_counts = wordcounts_dict[label]

                if word in label_word_counts.keys():
                    data['label'].append(label)
                    data['word'].append(word)
                    data['count'].append(label_word_counts[word])

        song_word_counts_df = pd.DataFrame(data)
        sk.make_sankey(song_word_counts_df, 'label', 'word', vals='count')


    def generate_wordclouds(self, rows=None, cols=None, save=False):
        """Generates a subplot grid of word clouds for each text file"""
        wordcounts_dict = self.data['wordcount']
        num_files = len(wordcounts_dict)

        if rows is None and cols is None:
            # Define reasonable defaults for the subplot grid dimensions
            if num_files <= 4:
                rows = 2
                cols = 2
            elif num_files <= 6:
                rows = 2
                cols = 3
            else:
                rows = 3
                cols = 4

        fig, axes = plt.subplots(rows, cols, figsize=(15, 10))

        # Flatten the axes array for easier iteration
        axes = axes.flatten()

        for ax, (label, wordcounts) in zip(axes, wordcounts_dict.items()):
            wordcloud = WordCloud(width=400, height=200, background_color='white').generate_from_frequencies(wordcounts)
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.set_title(f'Word Cloud for {label}')
            ax.axis('off')

        # Hide any remaining empty subplots
        for ax in axes[num_files:]:
            ax.axis('off')

        plt.tight_layout()

        if save:
            plt.savefig('wordcloud.png')
        else:
            plt.show()

    def sentiment_scores_heatmap(self, size=(10, 7), save=False):
        """Creates a heatmap showing the sentiment scores for each text file"""

        # Create a dataframe of the sentiment scores
        sentiment_dict = self.data['sentiment']
        df = pd.DataFrame(sentiment_dict).T

        # Create heatmap
        plt.figure(figsize=size)
        sns.heatmap(df, annot=True, cmap='coolwarm', linewidths=.5)
        plt.title('Sentiment Scores Heatmap')
        plt.xlabel('Sentiment')
        plt.ylabel('Text')
        plt.tight_layout(rect=(0.0, 0.0, 1.0, 1.0))

        if save:
            plt.savefig('sentiment_heatmap.png')
        else:
            plt.show()
