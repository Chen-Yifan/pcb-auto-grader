# PCB Auto Grader
The readme helps you get started with this autograder of ECE 445 EAGLE (pcb) assignment. 

## Prerequisites 

- Conda / pip
- Python3

## Packages
* torch = 1.5
* torchvision = 0.6
* pcb-tools
* detecto

**Install pytorch**

- OSX
```bash
# conda
conda install pytorch==1.5.1 torchvision==0.6.1 -c pytorch
# pip
pip install torch==1.5.1 torchvision==0.6.1  # use pip3 if needed
```

- Linux and Windows

Commands for CPU only 

```bash
# conda 
conda install pytorch==1.5.1 torchvision==0.6.1 cpuonly -c pytorch
# pip
pip install torch==1.5.1+cpu torchvision==0.6.1+cpu -f https://download.pytorch.org/whl/torch_stable.html
```
If you have CUDA, check this out for how to install pytorch on your machine: https://pytorch.org/get-started/previous-versions/

**Verify your Pytorch**
```bash
python -c "import torch; print(torch.__version__)" # 1.5.1
python -c "import torchvision; print(torchvision.__version__)" # 0.6.1
```

**Install other packages with pip.**
```bash
pip install pcb-tools
pip install detecto
```

## Download the code and model
1. Download the code: this repo uses computer vision technique to autonomously grade the pcb assignment.  
```bash
git clone https://github.com/Chen-Yifan/pcb-auto-grader
```
2. Download the model from https://drive.google.com/file/d/11-3x2Ob_R04PLv5ZYVx7f6IT7jPnmjz-/view?usp=sharing

3. Put ComponentDetectionModel.pth in `pcb-auto-grader/grader/` folder
```bash
mv ComponentDetectionModel.pth pcb-auto-grader/grader/
```

## How to grade
1. Put a ZIP file containing the student submissions in `pcb-auto-grader/grader/upload` folder. The zip file should include the following files at least:
```bash
ECE445_EagleHW.brd
ECE445_EagleHW.dri
ECE445_EagleHW.GBL
ECE445_EagleHW.GBO
ECE445_EagleHW.GBS
ECE445_EagleHW.GML
ECE445_EagleHW.gpi
ECE445_EagleHW.GTL
ECE445_EagleHW.GTO
ECE445_EagleHW.GTP
ECE445_EagleHW.GTS
ECE445_EagleHW.TXT
```
The student may not submit all these, then you'll need to generate these files using EAGLE and zip these together.

2. Go to grader folder and run the code grade.py. You need to replace `path/to/zip/file` with the actual path to a submission for grading
```bash
cd pcb-auto-grader/grader
python3 grader.py path/to/zip/file
```

3. Done! Output is the final grade.
