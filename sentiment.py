from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

import torch

from tqdm import tqdm

class Sentiment_classification():
    def __init__(self,
                 model_checkpoint="MonoHime/rubert-base-cased-sentiment-new"):

        self.tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_checkpoint)

        self.classifier = pipeline('text-classification',
                                   model=self.model,
                                   tokenizer=self.tokenizer)

    def classify_text(self, text):
        '''
        Classifies just one string of text

        :param text: just a string
        :return: sentiment label
        '''

        return str(self.classifier(text)[0]['label'])


    def predict_dataset(self):
        pass



class Emotion_detection():
    def __init__(self,
                 model_checkpoint="cointegrated/rubert-tiny2-cedr-emotion-detection"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_checkpoint)

        self.classifier = pipeline('text-classification',
                                   model=self.model,
                                   tokenizer=self.tokenizer)


    def classify_text(self, text):
        '''
        Classifies just one string of text

        :param text: just a string
        :return: sentiment label
        '''

        return str(self.classifier(text)[0]['label'])


    def predict_dataset(self):
        pass



class Toxicity_detection():
    def __init__(self,
                 model_checkpoint="cointegrated/rubert-tiny-toxicity"):

        self.tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_checkpoint)

        if torch.cuda.is_available():
            self.model.cuda()

    def text2toxicity(self, text, aggregate=True):
        """ Calculate toxicity of a text (if aggregate=True) or a vector of toxicity aspects (if aggregate=False)"""

        with torch.no_grad():
            inputs = self.tokenizer(text, return_tensors='pt', truncation=True, padding=True).to(self.model.device)
            proba = torch.sigmoid(self.model(**inputs).logits).cpu().numpy()
        if isinstance(text, str):
            proba = proba[0]
        if aggregate:
            return 1 - proba.T[0] * (1 - proba.T[-1])
        return proba


    def classify_text(self, text):
        '''Prints result  '''

        pred = self.text2toxicity(text)
        pred = round(pred)

        if pred == 0:
            return 'NOT TOXIC! Это сообщение не является грубым или токсичным.'
        else:
            return 'TOXIC! Внимание, перед Вами токсичное сообщение!'

