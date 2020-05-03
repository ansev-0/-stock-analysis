import torch
import torch.nn as nn

def CausalConv1d(in_channels, out_channels, kernel_size, dilation=1, **kwargs):
    pad = (kernel_size - 1) * dilation
    return nn.Conv1d(in_channels, out_channels,
                     kernel_size, padding=pad, dilation=dilation, **kwargs)

        
def ParallelCausalConv1D(in_channels, out_channels,
                         kernel_size, dilatation_ratios=None,
                          **kwargs):
    return nn.ModuleList(
        list(map(lambda dilatation : CausalConv1d(in_channels,
                                           out_channels,
                                           kernel_size,
                                           dilatation, **kwargs),
                     dilatation_ratios)))