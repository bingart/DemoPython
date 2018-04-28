##Example
"""
Suppose you have some texts of news and know their categories.
You want to train a system with this pre-categorized/pre-classified
texts. So, you have better call this data your training set.
"""
from naiveBayesClassifier import tokenizer
from naiveBayesClassifier.trainer import Trainer
from naiveBayesClassifier.classifier import Classifier

newsTrainer = Trainer(tokenizer)

# You need to train the system passing each text one by one to the trainer module.
newsSet =[
{'text': 'not to eat too much is not enough to lose weight', 'category': 'health'},
{'text': 'Russia is trying to invade Ukraine', 'category': 'politics'},
{'text': 'do not neglect exercise', 'category': 'health'},
{'text': 'Syria is the main issue, Obama says', 'category': 'politics'},
{'text': 'eat to lose weight', 'category': 'health'},
{'text': 'you should not eat much', 'category': 'health'}
]

for news in newsSet:
    newsTrainer.train(news['text'], news['category'])

# When you have sufficient trained data, you are almost done and can start to use
# a classifier.
newsClassifier = Classifier(newsTrainer.data, tokenizer)

# Now you have a classifier which can give a try to classifiy text of news whose
# category is unknown, yet.
unknownInstance = "Even if I eat too much, is not it possible to lose some weight"
classification = newsClassifier.classify(unknownInstance)

# the classification variable holds the possible categories sorted by
# their probablity value
print (classification)