"""
File: song_lyrics_analysis.py
Description: Uses the TextAnalysis class to look at the 7 songs of To Pimp a Butterfly
"""
from text_analysis import TextAnalysis
import pprint as pp


def main():
    tt = TextAnalysis()
    stopwords = 'stopwords'
    tt.load_text('Songs/Alright Lyrics', stopwords, 'Alright')
    tt.load_text('Songs/Blacker the Berry Lyrics', stopwords, 'Blacker the Berry')
    tt.load_text('Songs/How Much a Dollar Cost Lyrics', stopwords, 'How Much a Dollar Cost')
    tt.load_text('Songs/i Lyrics', stopwords, 'i')
    tt.load_text('Songs/King Kunta Lyrics', stopwords, 'King Kunta')
    tt.load_text('Songs/u Lyrics', stopwords, 'u')
    tt.load_text("Songs/You Ain't Gotta Lie Lyrics", stopwords, "You Ain't Gotta Lie")

    pp.pprint(tt.data)

    tt.wordcount_sankey()

    tt.generate_wordclouds()

    tt.sentiment_scores_heatmap()


if __name__ == '__main__':
    main()
