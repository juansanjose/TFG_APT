#!/bin/bash
caldera1(){
sudo apt update

sudo DEBIAN_FRONTEND=noninteractive apt-get -y -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confnew" install git

#get golang 1.9.1
curl -O https://storage.googleapis.com/golang/go1.17.7.linux-amd64.tar.gz

#unzip the archive 
tar -xvf go1.17.7.linux-amd64.tar.gz

#move the go lib to local folder
mv go /usr/local

#delete the source file
rm  go1.17.7.linux-amd64.tar.gz

#only full path will work
touch /home/vagrant/.bash_profile

echo "export PATH=$PATH:/usr/local/go/bin" >> /home/vagrant/.bash_profile

echo `export GOPATH=/home/vagrant/workspace:$PATH` >> /home/vagrant/.bash_profile

export GOPATH=/home/vagrant/workspace

mkdir -p "$GOPATH/bin" 

sudo apt-get install -y python3-pip
sudo apt install -y upx
sudo git clone https://github.com/mitre/caldera.git --recursive

cd caldera
sudo pip3 install -r requirements.txt





}
caldera1