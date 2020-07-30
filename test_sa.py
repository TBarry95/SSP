# initialize afinn sentiment analyzer
from afinn import Afinn
af = Afinn()
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
nlp = spacy.load("en_core_web_sm")

corpus = ["hello", "great", "bye", "terrible", "good", "yes"]
# [i for i in processed_txt_token if i not in stopwords_list]


doc = nlp("Some text here no bye yes great")
filtered_sent2 = [i for i in doc if i.is_stop==False]


sentiment_scores = [af.score(article) for article in corpus]

sentiment_category = ['positive' if score > 0
                      else 'negative' if score < 0
                        else 'neutral'
                      for score in sentiment_scores]

# sentiment statistics per news category
df = pd.DataFrame([list(news_df['news_category']), sentiment_scores, sentiment_category]).T
df.columns = ['news_category', 'sentiment_score', 'sentiment_category']
df['sentiment_score'] = df.sentiment_score.astype('float')
df.groupby(by=['news_category']).describe()
