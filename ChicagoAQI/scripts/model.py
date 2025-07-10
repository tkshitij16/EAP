"""Minimal DCRNN implementation using PyTorch Geometric."""

import torch
from torch import nn
from torch_geometric.nn import MessagePassing


class DCGRU(MessagePassing):
    def __init__(self, in_channels: int, out_channels: int):
        super().__init__(aggr="add")
        self.gru = nn.GRUCell(in_channels, out_channels)

    def forward(self, x, edge_index, edge_weight):
        out = self.propagate(edge_index, x=x, edge_weight=edge_weight)
        return out

    def message(self, x_j, edge_weight):
        return x_j * edge_weight

    def update(self, aggr_out, x):
        return self.gru(aggr_out, x)


class DCRNN(nn.Module):
    def __init__(self, in_channels: int, hidden: int, out_channels: int):
        super().__init__()
        self.dcgru1 = DCGRU(in_channels, hidden)
        self.dcgru2 = DCGRU(hidden, out_channels)

    def forward(self, x, edge_index, edge_weight):
        h = self.dcgru1(x, edge_index, edge_weight)
        out = self.dcgru2(h, edge_index, edge_weight)
        return out
