echo INSTALLING PPTAM
echo ==================================================================

cd ~
sudo rm -rf pptam-tool
git clone https://github.com/pptam/pptam-tool.git
\cp /vagrant/scripts/configuration.ini ~/pptam-tool/ini2json/configuration.ini
cd ~/pptam-tool/ini2json
./ini2json.sh 
