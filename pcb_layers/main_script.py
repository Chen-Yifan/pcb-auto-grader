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



def combine(gtl_file, gts_file, gto_file, txt_file, gtp_file, gbl_file, gbs_file, out_top, out_bottom):
    # Open the gerber files
    copper = load_layer(gtl_file)
    mask = load_layer(gts_file)
    silk = load_layer(gto_file)
    drill = load_layer(txt_file)
    placement = load_layer(gtp_file)

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
    ctx.dump(os.path.join(os.path.dirname(__file__), out_top))


    # Load the bottom layers
    copper_top = load_layer(gtl_file)
    copper = load_layer(gbl_file)
    mask = load_layer(gbs_file)

    # Clear the drawing
    ctx.clear()

    # Render bottom layers
    ctx.render_layer(copper, bounds = copper_top.bounds)
    ctx.render_layer(mask)
    ctx.render_layer(drill, settings = RenderSettings(mirror=True))

    # Write png file
    ctx.dump(os.path.join(os.path.dirname(__file__), out_bottom))



def combine_copper_only(gtl_file, out_copper_only_top, out_copper_only_bottom):
    copper = load_layer(gtl_file)
    ctx = GerberCairoContext()
    ctx.render_layer(copper)
    ctx.dump(os.path.join(os.path.dirname(__file__), out_copper_only_top))
    ctx.clear()
    copper_top = load_layer(gtl_file)
    ctx.render_layer(copper, bounds = copper_top.bounds)
    ctx.dump(os.path.join(os.path.dirname(__file__), out_copper_only_bottom))


def combine_folder(root_in, out_top, out_bottom, out_copper_only_top, out_copper_only_bottom):
    files = os.listdir(root_in)
    for fname in files:
        full_name = os.path.join(root_in, fname)
        suffix = fname[-3:].upper()
        if suffix == 'GTL':
            gtl_file = full_name
        elif suffix == 'GTS':
            gts_file = full_name
        elif suffix == 'GTO':
            gto_file = full_name
        elif suffix == 'TXT':
            txt_file = full_name
        elif suffix == 'GTP':
            gtp_file = full_name
        elif suffix == 'GBL':
            gbl_file = full_name
        elif suffix == 'GBS':
            gbs_file = full_name
    print('combining', root_in, out_top, out_bottom)
    combine(gtl_file, gts_file, gto_file, txt_file, gtp_file, gbl_file, gbs_file, out_top, out_bottom)
    print('combining', root_in, out_copper_only_top, out_copper_only_bottom)
    combine_copper_only(gtl_file, out_copper_only_top, out_copper_only_bottom)



if __name__ == '__main__':
    folders = []
    for prefix in ('dataset', 'additional-data'):
        for f in os.listdir(prefix):
            if f[0] == '.':
                continue
            root_in = os.path.join(prefix, f)
            combine_folder(root_in, os.path.join('processed', f+'-top.png'), os.path.join('processed', f+'-bottom.png')
                , os.path.join('processed', f+'-top-copper.png'), os.path.join('processed', f+'-bottom-copper.png'))