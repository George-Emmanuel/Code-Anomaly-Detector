## Suggested upgrades for production
- Replace TF-IDF + OneHot with code embeddings (CodeBERT / OpenAI) to capture semantic changes.
- Use an autoencoder or deep representation-based detector for higher fidelity.
- Add behavioral features: time-of-day, repo ownership, PR size, changed dependency list.
- Store models & features in a feature store; version via MLflow or similar.
- Add explainability (SHAP) for alerts and integrate with SIEM/IR workflows.
