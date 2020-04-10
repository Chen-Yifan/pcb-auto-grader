#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2015 Hamilton Kibbe <ham@hamiltonkib.be>

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

"""
This example demonstrates the use of pcb-tools with cairo to render a composite
image from a set of gerber files. Each layer is loaded and drawn using a
GerberCairoContext. The color and opacity of each layer can be set individually.
Once all thedesired layers are drawn on the context, the context is written to
a .png file.
"""

import os
from gerber import load_layer
from gerber.render import RenderSettings, theme
from gerber.render.cairo_backend import GerberCairoContext

GERBER_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), 'Archive'))


# Open the gerber files
copper = load_layer(os.path.join(GERBER_FOLDER, 'TPS799.GTL'))
mask = load_layer(os.path.join(GERBER_FOLDER, 'TPS799.GTS'))
silk = load_layer(os.path.join(GERBER_FOLDER, 'TPS799.GTO'))
drill = load_layer(os.path.join(GERBER_FOLDER, 'TPS799.TXT'))
placement = load_layer(os.path.join(GERBER_FOLDER, 'TPS799.GTP'))

# Create a new drawing context
ctx = GerberCairoContext()

# Draw the copper layer. render_layer() uses the default color scheme for the
# layer, based on the layer type. Copper layers are rendered as
# Draw the soldermask layer
ctx.render_layer(copper)
ctx.render_layer(mask)
ctx.render_layer(silk, settings=RenderSettings(color=theme.COLORS['white'], alpha=0.85))
ctx.render_layer(drill)

# Write output to png file
ctx.dump(os.path.join(os.path.dirname(__file__), 'top.png'))









# Load the bottom layers
copper_top = load_layer(os.path.join(GERBER_FOLDER, 'TPS799.GTL'))
copper = load_layer(os.path.join(GERBER_FOLDER, 'TPS799.GBL'))
mask = load_layer(os.path.join(GERBER_FOLDER, 'TPS799.GBS'))

# Clear the drawing
ctx.clear()

# Render bottom layers
ctx.render_layer(copper, bounds = copper_top.bounds)
ctx.render_layer(mask)
ctx.render_layer(drill, settings=RenderSettings(mirror=True))

# Write png file
ctx.dump(os.path.join(os.path.dirname(__file__), 'cairo_bottom.png'))

