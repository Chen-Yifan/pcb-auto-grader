import os, sys
from zip_handling import *
from render_gerber import *
from grade_ground_plane import *
from grade_components import *

def grade_main(zip_file):
    score = 0
    explanation = ""

    try:
        basedir = unzip(zip_file, "workdir")
    except Exception as e:
        return score, "".join([explanation, "\n", str(e)])

    try:
        render_gerber(basedir)
    except Exception as e:
        return score, "".join(["Missing gerber file", "\n", str(e)])

    print("Started grading, Prepared all files at :", basedir)

    score_gp, explanation_gp = grade_ground_plane(basedir)

    score += score_gp
    explanation = "".join([explanation, "\n", explanation_gp, "\n"])

    score_cp, explanation_cp, labels, boxes, scores = grade_components(basedir)

    score += score_cp
    explanation += explanation_cp

    return score, explanation

if __name__ == "__main__":
    FILE = "upload/student.zip"
    print(grade_main(FILE))
