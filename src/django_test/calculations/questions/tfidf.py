from calculations import util
from corpora.models import *
import math
from sklearn.feature_extraction.text import TfidfTransformer
import numpy as np
import re
import pandas as pd

class TFIDF:
    def url(self):
        return "tfidf"

    def name(self):
        # shown in the navigation
        return "TFIDF"
    
    def title(self):
        # title for the page
        return "What could this mean?"
    
    def tfidf(self, texts_df):
        result = {}
        for y_interval, text_df in texts_df.items():
            result[y_interval] = pd.DataFrame(data = TfidfTransformer().fit_transform(text_df).toarray(), index =text_df.index, columns = text_df.columns)
        return result
    
    def calc(self, parsed_request):
        # dict with possible calculations
        texts = util.get_texts_from_authors_in_timespan(parsed_request['authors'], parsed_request['timespan'])
        texts_dict = util.group_texts_by_interval(texts, 5)
        text_dfs = util.texts_to_data_frames(texts_dict, parsed_request['stem'])
    
        result = self.tfidf(text_dfs)
        words = parsed_request['words']
    
        for y_interval in result.keys():
            word_df = pd.DataFrame(index = words, columns = result[y_interval].keys()).fillna(0)
            result[y_interval] = pd.merge(result[y_interval], word_df, left_index=True, right_index=True)
            result[y_interval] = result[y_interval].mean().mean(axis = 1)
    
        x = []
        y = []
        for period in sorted(result.keys()):
            x.append(str(period[0]+(period[1]-period[0])/2))
            if not np.isnan(result[period]):
                y.append(str(result[period]))
            else:
                print("ERROR: NAN VALUES")
                y.append("0")
    
        x = '[' + ','.join(x) + ']'
        y = '[' + ','.join(y) + ']'
    
        return {
                'text_list': "",
                'x': x,
                'y': y
                }