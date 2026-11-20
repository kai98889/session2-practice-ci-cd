import tempfile
import unittest
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from train_model import train


class TrainingTests(unittest.TestCase):
    def test_known_line_and_saved_model(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            data = root / "data.csv"
            data.write_text("YearsExperience,Salary\n1,5\n2,8\n3,11\n")
            model = train(data, root)
            self.assertAlmostEqual(model.coef_[0], 3)
            self.assertAlmostEqual(model.intercept_, 2)
            restored = joblib.load(root / "linear_model.pkl")
            prediction = restored.predict(pd.DataFrame({"YearsExperience": [4]}))
            self.assertAlmostEqual(prediction[0], 14)
            self.assertIn("Intercept:", (root / "linear_model.txt").read_text())

    def test_invalid_training_data_is_rejected(self):
        samples = [
            "Wrong,Salary\n1,5\n2,8\n",
            "YearsExperience,Salary\n1,5\n2,\n",
            "YearsExperience,Salary\n1,5\n",
            "YearsExperience,Salary\n1,5\n1,8\n",
        ]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for sample in samples:
                with self.subTest(sample=sample):
                    data = root / "data.csv"
                    data.write_text(sample)
                    with self.assertRaises(ValueError):
                        train(data, root)

    def test_assignment_dataset(self):
        with tempfile.TemporaryDirectory() as directory:
            model = train(Path(__file__).with_name("training_data.csv"), Path(directory))
            self.assertTrue(np.isfinite(model.coef_).all())
            self.assertGreater(model.coef_[0], 0)


if __name__ == "__main__":
    unittest.main()
