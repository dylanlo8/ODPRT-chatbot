#!/bin/bash

set -e  # exit if any command fails

install_conda_and_create_env() {
    local miniconda_dir="$HOME/miniconda3"
    local conda_exe="$miniconda_dir/bin/conda"

    # install Miniconda if not found
    if [ ! -x "$conda_exe" ]; then
        echo "Installing Miniconda..."
        rm -rf "$miniconda_dir"
        mkdir -p "$miniconda_dir"
        wget -q https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh -O "$miniconda_dir/miniconda.sh"

        if [ ! -f "$miniconda_dir/miniconda.sh" ]; then
            echo "Error: Failed to download Miniconda."
            exit 1
        fi

        bash "$miniconda_dir/miniconda.sh" -b -u -p "$miniconda_dir"
        rm -f "$miniconda_dir/miniconda.sh"
    else
        echo "Miniconda already installed."
    fi

    # init Conda in the current shell
    eval "$($conda_exe shell.bash hook)"

    if ! command -v conda &> /dev/null; then
        echo "Error: Conda initialization failed."
        exit 1
    fi

    # ensure the environment file exists
    ENV_FILE="env/environment.yml"
    if [ ! -f "$ENV_FILE" ]; then
        echo "Error: Environment file '$ENV_FILE' not found."
        exit 1
    fi

    # create or activate Conda environment
    if conda env list | grep -q "^odprt "; then
        echo "Activating existing Conda environment 'odprt'..."
        conda activate odprt
    else
        echo "Creating Conda environment 'odprt'..."
        conda env create -n odprt -f "$ENV_FILE"
        conda activate odprt
        conda install -y ipykernel
    fi
}

install_conda_and_create_env
ipython kernel install --user --name=odprt --display-name "(odprt)"

# clone the repository (shallow clone for speed)
if [ ! -d "FlagEmbedding" ]; then
    echo "Cloning FlagEmbedding repository..."
    git clone --depth=1 https://github.com/FlagOpen/FlagEmbedding.git
else
    echo "FlagEmbedding repository already exists."
fi

cd FlagEmbedding/research/visual_bge
pip install -e .

echo "Setup complete."