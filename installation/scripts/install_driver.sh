#!/bin/bash 

echo INSTALLING DRIVER
echo ==================================================================

set -e

# Docker swarm installation
docker swarm init --advertise-addr $1 --listen-addr $1
docker swarm join-token -q worker > /vagrant/.join-token-worker

# Java installation
apt install -y openjdk-8-jdk ant 
echo JAVA_HOME="/usr/lib/jvm/java-8-openjdk-amd64/" >> /etc/environment

# Making sure python works
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.6 1
sudo update-alternatives --set python /usr/bin/python3.6

# Installion of Jupyter Notebook
cd ~
wget https://repo.anaconda.com/archive/Anaconda3-2020.02-Linux-x86_64.sh -O ~/Anaconda3-2020.02-Linux-x86_64.sh
bash ~/Anaconda3-2020.02-Linux-x86_64.sh -b -p $HOME/anaconda

echo export PATH=/home/vagrant/anaconda/bin:$PATH >> ~/.bashrc
source ~/.bashrc

eval "$(/home/vagrant/anaconda/bin/conda shell.bash hook)"
conda init

# jupyter notebook --generate-config
# jupyter notebook password (Define your jupyter password, or type ENTER twice for an empty password)


# 2. Update the following values in/home/user/.jupyter/jupyter_notebook_config.py:
#    - c.NotebookApp.allow_remote_access = True
#    - c.NotebookApp.ip = '*'
#    - c.NotebookApp.open_browser = False
# 3. Then, execute:
#    - conda install -c r r-essentials (answer y)
#    - conda deactivate
#    - mkdir ~/notebooks
#    - cd ~/notebooks
#    - conda create -n pptam python anaconda r-essentials (see https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-with-commands)
#    - conda activate pptam
#    - jupyter notebook (now http://localhost:8888/ should be reachable)
# 4. Then, copy the files of the [analyzer](analyzer) folder into the notebooks folder created above (I used [Cyberduck](https://cyberduck.io/)). 
