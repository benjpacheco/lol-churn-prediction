#importing packages
import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import RobustScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import make_pipeline
from sklearn.metrics import (accuracy_score, f1_score, recall_score, precision_score)
import pickle as pickle
import logging
import warnings
import os
warnings.filterwarnings("ignore")

class Preprocessing:

    def __init__(self):
        self.CURRENT_DIR = os.path.dirname(__file__)
        self.EXTRA_FEATURES = ['summoner_name', 'game_end_timestamp', 'game_start_timestamp', 'days_since_last_match',
                    'match_id', 'last_match']
        self.dc = pd.Timestamp("2022-05-17")
      
    def get_date_diff(self, date , dc):
        return (dc - date).days

    def feature_eng(self):
        df = pd.read_csv(os.path.abspath(os.path.join(self.CURRENT_DIR, "..", "../data/processed/master_lol_churn_prediction.csv")))
        df['last_match'] = pd.to_datetime(df['last_match'])
        df['days_since_last_match'] = df.apply(lambda row: self.get_date_diff(row['last_match'], self.dc), axis=1)
        df['churn'] = df['days_since_last_match']>30

        df['deaths'] = df['deaths'].replace(0, 0.1)
        df['KDA'] = (df['kills'] + df['assists'])/df['deaths']
        df['WL'] = df['wins']/df['losses']
        df['gold_earned_per_min'] = (df['gold_earned']/df['time_played'])/60
        df = df.drop(columns=self.EXTRA_FEATURES, axis=1)

        X = df.loc[:, df.columns != 'churn']
        y = df['churn']

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.2, train_size=0.8)


class Train:

    def __init__(self, X_train, X_test, y_train, y_test):
        self.X_train = X_train
        self.X_test = X_test
        self.y_train = y_train
        self.y_test = y_test
        self.CURRENT_DIR = os.path.dirname(__file__)
        self.seed = np.random.seed(42)
        self.COLUMNS_TO_TRANSFORM = ['rank', 'tier', 'game_version', 'lane', 'champion_name']

    def summary(self, y_predicted, y_test):

        self.accuracy = accuracy_score(y_predicted, y_test)
        self.recall = recall_score(y_predicted, y_test)
        self.precision = precision_score(y_predicted, y_test)
        self.f1 = f1_score(y_predicted, y_test)

        summary_output = f'''
            accuracy = {self.accuracy : .2f}
            f1 = {self.f1 : .2f}
            recall = {self.recall : .2f}
            precision =  {self.precision : .2f}
        '''
        print(summary_output)

    def train_model(self):

        ct = ColumnTransformer([('categ', OneHotEncoder(handle_unknown='ignore'), self.COLUMNS_TO_TRANSFORM)], remainder='passthrough')
        scaler = RobustScaler(with_centering=False)

        xgb_clf = xgb.XGBClassifier(max_depth=20, learning_rate=0.00719580052831331, n_estimators=198, seed=self.seed)

        pipeline = make_pipeline(ct, scaler, xgb_clf)
        pipeline.fit(self.X_train, self.y_train)

        #saving model to backend
        with open(os.path.abspath(os.path.join(self.CURRENT_DIR, '..', '../backend/model_pkl')), 'wb') as pickle_file:
            pickle.dump(pipeline, pickle_file)

        y_predicted = pipeline.predict(self.X_test)
        self.summary(y_predicted, self.y_test)

    
def main():
    """ trains model and saves pickle file to same directory
    """
    logger = logging.getLogger(__name__)
    logger.info('training model from master_df')


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    preprocess_model = Preprocessing()
    preprocess_model.feature_eng()

    train_model = Train(preprocess_model.X_train, preprocess_model.X_test, preprocess_model.y_train, preprocess_model.y_test)
    train_model.train_model()

    main()