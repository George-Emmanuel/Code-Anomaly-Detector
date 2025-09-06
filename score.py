import argparse
import pandas as pd
import joblib
import os

def score(model_path, input_csv, out_csv):
    model = joblib.load(model_path)
    df = pd.read_csv(input_csv)
    X = df[['diff','author']]
    # IsolationForest.predict: -1 for anomaly, 1 for normal
    scores = model.named_steps['isolationforest'].decision_function(model.named_steps['columntransformer'].transform(X))
    # Higher negative => more anomalous; we invert to make 'anomaly_score' where higher = more anomalous
    anomaly_score = -scores
    df['anomaly_score'] = anomaly_score
    df.to_csv(out_csv, index=False)
    print(f'Wrote scores to {out_csv}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', default='out/model.joblib')
    parser.add_argument('--input', default='sample_commits.csv')
    parser.add_argument('--output', default='out/scores.csv')
    args = parser.parse_args()
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    score(args.model, args.input, args.output)
