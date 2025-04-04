#  Copyright (c) Meta Platforms, Inc. and affiliates.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
"""
common module for conv_bias_act subgraph
"""

from aitemplate.compiler import ops
from aitemplate.frontend.nn.module import Module
from aitemplate.frontend.nn.parameter import Parameter

# pylint: disable=C0103


class Conv2dBiasAct(Module):
    """common functions for conv2d_bias_act"""

    def __init__(
        self,
        op_name,
        in_channels,
        out_channels,
        kernel_size,
        stride,
        padding=0,
        dilation=1,
        groups=1,
        dtype="float16",
    ):
        """Initialize the Conv2dBiasAct class

        Parameters
        ----------
        in_channel : [type]
            [description]
        out_channel : [type]
            [description]
        kernel_size : [type]
            [description]
        stride : [type]
            [description]
        pad : str, optional
            [description], by default 'SAME'
        dilate : int, optional
            [description], by default 1
        dtype : str, optional
            [description], by default "float16"

        Raises
        ------
        NotImplementedError
            [description]
        """
        super().__init__()
        self.weight = Parameter(
            shape=[out_channels, kernel_size, kernel_size, in_channels // groups],
            dtype=dtype,
        )
        self.bias = Parameter(shape=[out_channels], dtype=dtype)
        op_func = getattr(ops, op_name)
        self.op = op_func(stride=stride, pad=padding, dilate=dilation, group=groups)

    def forward(self, *args):
        assert len(args) == 1
        x = args[0]
        return self.op(x, self.weight.tensor(), self.bias.tensor())
