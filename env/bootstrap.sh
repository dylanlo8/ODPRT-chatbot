#!/bin/bash

install_conda_and_create_env() {
    local miniconda_dir="$HOME/miniconda3"
    local conda_exe="$miniconda_dir/bin/conda"

    if [ ! -d "$miniconda_dir" ] || [ ! -f "$conda_exe" ]; then
        echo "installing miniconda..."
        rm -rf "$miniconda_dir"
        mkdir -p "$miniconda_dir"
        wget -q https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh -O "$miniconda_dir/miniconda.sh"
        bash "$miniconda_dir/miniconda.sh" -b -u -p "$miniconda_dir"
        rm -f "$miniconda_dir/miniconda.sh"
    else
        echo "miniconda already installed."
    fi

    eval "$($conda_exe shell.bash hook)"
    
    if ! command -v conda &> /dev/null; then
        echo "failed to initialize conda. exiting."
        exit 1
    fi

    if conda info --envs | grep -q odprt; then
        echo "conda environment 'odprt' exists. activating..."
        conda activate odprt
    else
        echo "creating conda environment 'odprt'"
        conda env create -n odprt -f environment.yml
        conda activate odprt
        conda install ipykernel -y
    fi
}

install_conda_and_create_env
ipython kernel install --user --name=odprt --display-name "(odprt)"
git clone https://github.com/FlagOpen/FlagEmbedding.git
cd FlagEmbedding/research/visual_bge
pip install -e .