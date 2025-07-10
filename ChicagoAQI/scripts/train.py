"""Train DCRNN on AQI data."""
from pathlib import Path
import torch
from torch.utils.data import DataLoader, TensorDataset

from .model import DCRNN


def train(graph_path: Path, features: torch.Tensor, targets: torch.Tensor, epochs: int = 10):
    data = torch.load(graph_path)
    model = DCRNN(features.size(-1), 32, targets.size(-1))
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    dataset = TensorDataset(features, targets)
    loader = DataLoader(dataset, batch_size=32, shuffle=True)
    for _ in range(epochs):
        for x, y in loader:
            pred = model(x, data.edge_index, data.edge_attr)
            loss = torch.nn.functional.mse_loss(pred, y)
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()
    return model



