#!/bin/bash
sudo apt-get install squashfs-tools genisoimage -y
sudo apt autoremove -y

mkdir ~/custom-img
mv *.iso ~/custom-img/
cd ~/custom-img
mkdir mnt
sudo mount -o loop *.iso mnt
mkdir extract
sudo rsync --exclude=/casper/filesystem.squashfs -a mnt/ extract

sudo unsquashfs mnt/casper/filesystem.squashfs

mv squashfs-root edit
sudo cp ../setEth0.py edit/home/guarani/.gcb/.

sudo cp /etc/resolv.conf edit/etc/
sudo cp ../google-chrome-stable_current_amd64.deb edit/home/guarani

sudo cp -r /certs edit/certs
sudo cp -r /etc/couchdb/ edit/etc/.

sudo mount --bind /dev/ edit/dev
sudo chroot edit
mount -t proc none /proc
mount -t sysfs none /sys
mount -t devpts none /dev/pts
export HOME=/root
export LC_ALL=C
dbus-uuidgen > /var/lib/dbus/machine-id
dpkg-divert --local --rename --add /sbin/initctl
ln -s /bin/true /sbin/initctl

dpkg --add-architecture i386
#______________________________________________________________________________________________________
# Preciso ter proxy no apt p/ baixar os pacotes, qdo terminar de configurar tudo deve ser apagado
scp root@10.67.125.203:/etc/apt/apt.conf /etc/apt/apt.conf

apt-get update
apt-get install vim git openssh-server build-essential -y

cd /tmp

git clone http://10.67.120.72/c2/c2db.git
git clone http://10.67.120.72/c2/pacificador_deploy_scripts.git
git clone http://10.67.120.72/c2/gcb_deploy_scripts.git



apt-get install libncurses5-dev openssl libssl-dev -y
wget http://erlang.org/download/otp_src_17.0.tar.gz
tar -xzf otp_src_17.0.tar.gz
cd otp_src_17.0
./configure
make
make install
# Instalou? 
erl -eval 'erlang:display(erlang:system_info(otp_release)), halt().'  -noshell

cd pacificador_deploy_scripts
./install-certs.sh
./atualizar-certs.sh
cd ..

cd c2db
apt-get install libcurl4-openssl-dev libicu-dev libmozjs185-1.0 libmozjs185-dev libtool autoconf-archive pkg-config -y --fix-missing

./bootstrap 
./configure 
make
make install

chmod 0770 -R /usr/local/etc/couchdb
chmod 0770 -R /usr/local/var/lib/couchdb var/log/couchdb var/run/couchdb etc/couchdb
chmod 0770 -R /usr/local/var/log/couchdb var/run/couchdb etc/couchdb
chmod 0770 -R /usr/local/var/run/couchdb etc/couchdb
chmod 0770 -R /usr/local/etc/couchdb

chown couchdb:couchdb -R /usr/local/etc/couchdb
chown couchdb:couchdb -R /usr/local/var/lib/couchdb var/log/couchdb var/run/couchdb etc/couchdb
chown couchdb:couchdb -R /usr/local/var/log/couchdb var/run/couchdb etc/couchdb
chown couchdb:couchdb -R /usr/local/var/run/couchdb etc/couchdb
chown couchdb:couchdb -R /usr/local/etc/couchdb

cd ..

cd /opt
git clone http://10.67.120.72/c2/pacificador_embarcado.git


# node
wget https://nodejs.org/download/release/v0.10.33/node-v0.10.33-linux-x64.tar.gz
tar zxf node-v0.10.33-linux-x64.tar.gz
ln -fs /opt/node-v0.10.33-linux-x64/bin/node /usr/bin/node
ln -fs /opt/node-v0.10.33-linux-x64/bin/npm /usr/bin/npm

# Criar o serviço do nodejs em /etc/systemd/system/nodejs.service
systemctl enable nodejs.service

# Configurando o proxy no npm p/ baixar as dependencias
export http_proxy=http://10.67.120.43:3128
npm config set proxy $http_proxy
npm set https-proxy $http_proxy
npm config set registry "http://registry.npmjs.org/"

# Setar a versão do netroute p/ 1.0.2 no package.json

cd pacificador_embarcado
npm install --production

cd ..
rm *.tar.gz

# Apaga o amazon do dash do ubuntu
rm -rf /usr/share/applications/ubuntu-amazon-default.desktop

# Apaga o conteúdo de mídia que vem de exemplo com o ubuntu
unlink examples.desktop
rm -r /usr/share/example-content/

# Desabilita a tela de login:
echo "autologin-user=pacificador" >> /usr/share/lightdm/lightdm.conf.d/50-unity-greeter.conf

# Instalar o chrome
dpkg -i google-chrome-stable_current_amd64
apt-get -f install -y


# Configurando o crontab
crontab /tmp/gcb_deploy_scripts/conf/crontab

# Configurando o touch
cp /tmp/gcb_deploy_scripts/conf/99-calibration.conf /etc/X11/xorg.conf.d/

#______________________________________________________________________________________________________

#### calibrate.sh
wget http://ftp.br.debian.org/debian/pool/main/x/xinput-calibrator/xinput-calibrator_0.7.5+git20140201-1+b1_amd64.deb
mkdir -p /etc/X11/xorg.conf.d
cp /tmp/gcb_deploy_scripts/conf/99-calibration.conf /etc/X11/xorg.conf.d/

#### disguise.sh
wget http://launchpadlibrarian.net/253336149/plymouth-theme-ubuntustudio_0.53_all.deb
dpkg -i plymouth-theme-ubuntustudio_0.53_all.deb
cp -f /tmp/gcb_deploy_scripts/images/ubuntu_logo.png /usr/share/plymouth/ubuntu_logo.png
cp -f /tmp/gcb_deploy_scripts/images/background.png /usr/share/plymouth/themes/ubuntus-logo/background.png
cp -f /tmp/gcb_deploy_scripts/images/logo.png /usr/share/plymouth/themes/ubuntu-logo/logo.png
cp -f /tmp/gcb_deploy_scripts/images/icon.png /usr/share/plymouth/themes/ubuntu-logo/icon.png
cp -f /tmp/gcb_deploy_scripts/images/progress_box.png /usr/share/plymouth/themes/ubuntu-logo/progress_box.png
chmod +x /usr/share/plymouth/themes/ubuntu-logo/*.png
sed 's/title\=Ubuntu 16\.04/title\=Pacificador Mec/' --in-place /usr/share/plymouth/themes/ubuntu-text/ubuntu-text.plymouth
update-initramfs -u

#### configure-autolauncher.sh

# -----------------------------------------
# 1. CRIAÇÃO DO USUÁRIO GUARANI
# -----------------------------------------
adduser guarani --gecos "guarani" --home /home/guarani --shell /bin/bash
# -----------------------------------------
# 2. INSTALAÇÃO DO XMONAD
# -----------------------------------------
wget http://ftp.cl.debian.org/debian/pool/main/libj/libjpeg-turbo/libjpeg62-turbo_1.5.1-2_amd64.deb
wget http://ftp.cl.debian.org/debian/pool/main/libp/libpng1.6/libpng16-16_1.6.28-1_amd64.deb

dpkg -i libjpeg62-turbo_1.5.1-2_amd64.deb
dpkg -i libpng16-16_1.6.28-1_amd64.deb

wget http://ftp.cl.debian.org/debian/pool/main/x/xmonad/xmonad_0.11-9_amd64.deb
wget http://ftp.br.debian.org/debian/pool/main/x/xloadimage/xloadimage_4.1-24_amd64.deb

dpkg -i xmonad_0.11-9_amd64.deb
dpkg -i xloadimage_4.1-24_amd64.deb

mkdir -p /home/guarani/.xmonad
cp -f /tmp/gcb_deploy_scripts/conf/xmonad.hs /home/guarani/.xmonad/
chown -R guarani:guarani /home/guarani/.xmonad

# NAO RODOU
su guarani -c 'xmonad --recompile' 
# NAO RODOU

# -----------------------------------------------------
# 3. CONFIGURAÇÃO DO DIRETÓRIO .GCB DO USUÁRIO GUARANI
# -----------------------------------------------------
mkdir -p /home/guarani/.gcb
cp -f /opt/pacificador_embarcado/package.json /home/guarani/.gcb/
cp -f /tmp/gcb_deploy_scripts/images/background.png /home/guarani/.gcb/
cp -f /tmp/gcb_deploy_scripts/conf/run_gcb.sh /home/guarani/.gcb/
chmod +x /home/guarani/.gcb/run_gcb.sh
chown -R guarani:guarani /home/guarani/.gcb
# --------------------------------------------------------
# 4. CONFIGURAÇÃO DO ARQUIVO .XSESSION DO USUÁRIO GUARANI
# --------------------------------------------------------
cp -f /tmp/gcb_deploy_scripts/conf/xsession.template /home/guarani/.xsession
sed "s/\#\#GCB_USER\#\#/guarani/g" --in-place /home/guarani/.xsession
chmod +x /home/guarani/.xsession
# --------------------------------------------------------
# 5. MUDANDO O DONO DO NODE-WEBKIT
# --------------------------------------------------------
# chown -R guarani:guarani /opt/webkit
# --------------------------------------------------------
# 6. CONFIGURAÇÃO DO LIGHTDM
# --------------------------------------------------------
cp -f /tmp/gcb_deploy_scripts/conf/gcb.desktop /usr/share/xsessions/gcb.desktop
cp -f /tmp/gcb_deploy_scripts/conf/lightdm.conf.template /etc/lightdm/lightdm.conf
sed "s/\#\#GCB_USER\#\#/guarani/g" --in-place /etc/lightdm/lightdm.conf
# -------------------------------------------------------------------------
# 7. CONFIGURAÇÃO DE PERMISSÃO PARA INICIALIZAÇÃO DO X A PARTIR DO CONSOLE
# -------------------------------------------------------------------------

# NAO RODOU
sed -e 's/allowed_users=console/allowed_users=anybody/' --in-place /etc/X11/Xwrapper.config
# NAO RODOU


echo "### Limpando a iso do ubuntu"
apt-get purge firefox* thunderbird* libreoffice* cups* hplib* printer-driver* remmina* rhythmbox* transmission* bluez* media-player* pulseaudio* simple-scan totem gnome-sudoku gnome-mines gnome-mahjongg aisleriot -y



gsettings set org.gnome.desktop.lockdown disable-lock-screen 'true'

apt-get autoremove -y
apt-get autoclean -y

rm -rf /tmp/* ~/.bash_history
rm /var/lib/dbus/machine-id
rm /sbin/initctl
dpkg-divert --rename --remove /sbin/initctl

umount /proc || umount -lf /proc
umount /sys
umount /dev/pts
exit
sudo umount edit/dev

sudo chmod +w extract/casper/filesystem.manifest
sudo chroot edit dpkg-query -W --showformat='${Package} ${Version}n' | sudo tee extract/casper/filesystem.manifest
sudo cp extract/casper/filesystem.manifest extract/casper/filesystem.manifest-desktop
sudo sed -i '/ubiquity/d' extract/casper/filesystem.manifest-desktop
sudo sed -i '/casper/d' extract/casper/filesystem.manifest-desktop

sudo mksquashfs edit extract/casper/filesystem.squashfs -b 1048576

printf $(du -sx --block-size=1 edit | cut -f1) | tee extract/casper/filesystem.size
cd extract
sudo rm md5sum.txt
find -type f -print0 | xargs -0 md5sum | grep -v isolinux/boot.cat | tee md5sum.txt
sudo genisoimage -D -r -V "$IMAGE_NAME" -cache-inodes -J -l -b isolinux/isolinux.bin -c isolinux/boot.cat -no-emul-boot -boot-load-size 4 -boot-info-table -o ../gcb-final04.iso .



ssh wendel@10.67.120.122 'xset -display :0.0 dpms force off'