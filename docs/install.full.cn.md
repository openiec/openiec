## 安装指南

### 安装Anaconda

访问[Anaconda](https://www.anaconda.com/download)，或者国内的镜像源进行Anaconda下载，例如[清华镜像](https://mirrors.tuna.tsinghua.edu.cn/help/anaconda/)。

### 创建安装所需的Python虚拟环境
```bash
conda create -n py37 python=3.7
conda activate py37
```

### 安装pycalphad

```bash
pip install -U pip setuptools
pip install -U pycalphad
```

### 安装OpenIEC

下载OpenIEC源代码，解压后，切换到源代码目录，执行：

```
python setup.py install
```

对于开发者可以使用，
```
pip install -e .
```
