import os
import joblib
from server.models.article import Article
from server.interfaces.i_category_predictor import ICategoryPredictor


class MLCategoryPredictor(ICategoryPredictor):
    def __init__(self):
        model_path = os.path.join("docs", "trained_category_model.joblib")
        if not os.path.exists(model_path):
            raise FileNotFoundError("Trained model not found. Run train_category_model.py first.")
        self.model, self.vectorizer = joblib.load(model_path)

    def predict(self, article: Article) -> str:
        combined_text = f"{article.title} {article.content}".lower()
        X = self.vectorizer.transform([combined_text])
        return self.model.predict(X)[0]
