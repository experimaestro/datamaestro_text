from datamaestro.data.csv import Generic
from datamaestro.definitions import data, argument, datatasks, datatags, dataset
from datamaestro.download.archive import zipdownloader
from datamaestro.data.ml import Supervised
from datamaestro.utils import HashCheck

# name: Sentiment140
# web: http://help.sentiment140.com/for-students/

# description: |


@zipdownloader(
    "dir",
    "http://cs.stanford.edu/people/alecmgo/trainingandtestdata.zip",
    checker=HashCheck("1647eb110dd2492512e27b9a70d5d1bc"),
)
@datatasks("sentiment analysis")
@datatags("english", "sentiment", "text")
@dataset(Supervised, url="http://help.sentiment140.com/for-students/", size="228M")
def english(dir):
    """Sentiment analysis dataset 140

  The data is a CSV with emoticons removed. Data file format has 6 fields:
  0 - the polarity of the tweet (0 = negative, 2 = neutral, 4 = positive)
  1 - the id of the tweet (2087)
  2 - the date of the tweet (Sat May 16 23:58:44 UTC 2009)
  3 - the query (lyx). If there is no query, then this value is NO_QUERY.
  4 - the user that tweeted (robotickilldozr)
  5 - the text of the tweet (Lyx is cool)

  If you use this data, please cite Sentiment140 as your source.
  """
    return {
        "train": Generic(path=dir / "training.1600000.processed.noemoticon.csv"),
        "test": Generic(path=dir / "testdata.manual.2009.06.14.csv"),
    }
