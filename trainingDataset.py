import torch
from torch.utils.data import Dataset
import numpy as np
class TrainDataset(Dataset):
    """MovieLens PyTorch Dataset for Training

    Args:
        ratings (pd.DataFrame): Dataframe containing the movie ratings
        all_feedIds (list): List containing all movieIds

    """

    def __init__(self, ratings, all_feedIds):
        self.users, self.items, self.labels = self.get_dataset(ratings, all_feedIds)

    def __len__(self):
        return len(self.users)

    def __getitem__(self, idx):
        return self.users[idx], self.items[idx], self.labels[idx]

    def get_dataset(self, df, all_feedIds):
        users, items, labels = [], [], []
        user_item_set = set(zip(df['user'], df['feed_id']))

        num_negatives = 2
        for u, i in user_item_set:
            users.append(u)
            items.append(i)
            labels.append(1)
            for _ in range(num_negatives):
                negative_item = np.random.choice(all_feedIds)
                while (u, negative_item) in user_item_set:
                    negative_item = np.random.choice(all_feedIds)
                users.append(u)
                items.append(negative_item)
                labels.append(0)

        return torch.tensor(users), torch.tensor(items), torch.tensor(labels)
