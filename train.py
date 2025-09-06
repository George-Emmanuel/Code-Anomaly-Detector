import argparse
import pandas as pd
import joblib
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import IsolationForest
from sklearn.pipeline import make_pipeline
from sklearn.compose import ColumnTransformer

def build_and_train(df, out_model):
    # Features: TF-IDF on diffs, OneHot on author (simple)
    tfidf = TfidfVectorizer(max_features=512, token_pattern=r"(?u)\\b\\w+\\b")
    ohe = OneHotEncoder(handle_unknown='ignore', sparse=False)

    pre = ColumnTransformer(transformers=[
        ('diff', tfidf, 'diff'),
        ('author', ohe, ['author'])
    ], remainder='drop')

    # Prepare text for author column: must be 2D for ColumnTransformer
    # Build pipeline: transform -> IsolationForest
    iso = IsolationForest(n_estimators=200, contamination=0.02, random_state=42)
    pipeline = make_pipeline(pre, iso)

    # Fit on diffs + authors (unsupervised)
    X = df[['diff','author']]
    pipeline.fit(X)
    os.makedirs(os.path.dirname(out_model), exist_ok=True)
    joblib.dump(pipeline, out_model)
    print(f'Model saved to {out_model}')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', default='sample_commits.csv')
    parser.add_argument('--model', default='out/model.joblib')
    args = parser.parse_args()
    df = pd.read_csv(args.input)
    build_and_train(df, args.model)

if __name__ == '__main__':
    main()
