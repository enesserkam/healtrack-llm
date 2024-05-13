import pandas as pd
import os

class DatasetPrep:
    def __init__(self, data_path):
        self.path = data_path
        self.data = None
        self.text_data = []

    def readData(self):
        if os.path.exists(self.path):
            self.data = pd.read_csv(self.path)
        else:
            raise FileNotFoundError(f"No file found at {self.path}")

    def process_data(self):
        if self.data is not None:
            self.data = self.data.drop(columns=['qtype'])

            for index, row in self.data.iterrows():
                formatted_text = f"<s>[INST] {row['Question']} [/INST] {row['Answer']}</s>"
                self.text_data.append(formatted_text)
        else:
            print("Data not loaded. Please load the data first.")

    def save_csv_data(self, data, filename):
        df = pd.DataFrame(data, columns=['text'])
        file_path = os.path.join(os.path.dirname(self.path), filename)
        df.to_csv(file_path, index=False)
        print(f"Data saved to {file_path}")

    def save_sample_data(self, sample_size=1000):
        if len(self.text_data) >= sample_size:
            sample_data = self.text_data[:sample_size]
            self.save_csv_data(sample_data, 'trial_data.csv')
        else:
            print("Not enough data to create a sample of the specified size.")

    def save_full_data(self):
        self.save_csv_data(self.text_data, 'full_data.csv')


# Usage
d_path = "../datasets/medDataset_processed.csv"
prepare = DatasetPrep(d_path)
prepare.readData()
prepare.process_data()
prepare.save_sample_data()
prepare.save_full_data()
