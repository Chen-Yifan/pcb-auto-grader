# PCB Auto Grader
This readme helps you use this autograder of ECE 445 EAGLE (pcb) assignment. 

## Prerequisites 

- Conda / pip
- Python3

## Packages
* torch == 1.5
* torchvision == 0.6
* pcb-tools
* detecto

**Install pytorch**

- OSX
```bash
# conda
conda install pytorch==1.5.1 torchvision==0.6.1 -c pytorch
# pip
pip install torch==1.5.1 torchvision==0.6.1
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

**Install other packages with pip.**
```bash
pip install pcb-tools
pip install detecto
```

## Download the code
This repo uses computer vision technique to autonomously grade the pcb assignment.  
```bash
git clone https://github.com/Chen-Yifan/pcb-auto-grader
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

2. Go to grader folder and run the code grade.py. You need to replace `path/to/zip/file` with the actual path to a submission for grading
```bash
cd pcb-auto-grader/grader
python grader.py path/to/zip/file
```

3. Done! Output is the final grade.
