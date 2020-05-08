import os
from gerber import load_layer
from gerber.render import RenderSettings, theme
from gerber.render.cairo_backend import GerberCairoContext

def render_gerber(basedir):
    files = os.listdir(basedir)
    for fname in files:
        full_name = os.path.join(basedir, fname)
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

    combine(gtl_file, gts_file, gto_file, txt_file, gtp_file, gbl_file, gbs_file, basedir)

def combine(gtl_file, gts_file, gto_file, txt_file, gtp_file, gbl_file, gbs_file, basedir):
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
    ctx.dump(os.path.join(basedir, "top.png"))


    # Load the bottom layers
    copper = load_layer(gbl_file)
    copper_top = load_layer(gtl_file)
    mask = load_layer(gbs_file)

    # Clear the drawing
    ctx = GerberCairoContext()
    from gerber.rs274x import read, GerberFile

    # Render bottom layers
    ctx.render_layer(copper, bounds = copper_top.bounds)
    ctx.render_layer(mask)
    ctx.render_layer(drill, settings = RenderSettings(mirror=True))

    # Write png file
    ctx.dump(os.path.join(basedir, "bottom.png"))

    copper = load_layer(gtl_file)
    ctx = GerberCairoContext()
    ctx.render_layer(copper)

    ctx.dump(os.path.join(basedir, "top-copper.png"))
    ctx = GerberCairoContext()
    copper_bottom = load_layer(gbl_file)
    ctx.render_layer(copper_bottom, bounds = copper.bounds)
    ctx.dump(os.path.join(basedir, "bottom-copper.png"))