Vagrant.configure("2") do |config|

  
  config.vm.define "firewall" do |fw|
    fw.vm.hostname = "firewall"
  $opnsense_box = 'punktde/freebsd-130-ufs'
  
  # Which OPNsense release to install
  $opnsense_release = '22.1'

  # IP address of the firewall in the host-only network
  # config.ssh.private_key_path = "C:/Users/juans/.ssh/id_ed25519.pub"
  # config.ssh.forward_agent = true
  
  # Enable SSH keepalive to work around https://github.com/hashicorp/vagrant/issues/516
  fw.ssh.keep_alive = true

  # Configure proper shell for FreeBSD
  fw.ssh.shell = '/bin/sh'

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://atlas.hashicorp.com/search
  fw.vm.box = $opnsense_box

  # Create a private network, which allows host-only access to the machine
  # using a specific IP
  fw.vm.network 'private_network', ip: "192.168.56.111"
  fw.vm.network "private_network", ip: "192.168.100.111"

  # Customize build VB settings
  fw.vm.provider 'virtualbox' do |vb|
    vb.gui = true
    vb.name = "firewall"
    vb.memory = 512
    vb.cpus = 1

  end
  
  # Transfer config file snippets into VM
  fw.vm.provision "file", source: "files", destination: "files"
  config.vm.synced_folder ".", "/vagrant", disabled: true

  # Bootstrap OPNsense
  fw.vm.provision 'shell', inline: <<-SHELL

  #Configure      
    

    # Download the OPNsense bootstrap script
    fetch -o opnsense-bootstrap.sh https://raw.githubusercontent.com/opnsense/update/master/src/bootstrap/opnsense-bootstrap.sh.in
    # Remove reboot command from bootstrap script
    sed -i '' -e '/reboot$/d' opnsense-bootstrap.sh
    # Start bootstrap
    sh ./opnsense-bootstrap.sh -r #{$opnsense_release} -y
    
    
    # Enable SSH by default
    sed -i '' -e '/<group>admins<\\/group>/r files/ssh.xml' /usr/local/etc/config.xml
    # Allow SSH on all interfaces
   sed -i '' -e '/<filter>/r files/filter.xml' /usr/local/etc/config.xml
    # Do not block private networks on WAN
   sed -i '' -e '/<blockpriv>1<\\/blockpriv>/d' /usr/local/etc/config.xml
    # # Create XML config for Vagrant user
    key=$(b64encode -r dummy <.ssh/authorized_keys | tr -d '\n')
    echo "      <authorizedkeys>${key}</authorizedkeys>" >files/vagrant2.xml
    cat files/vagrant[123].xml >files/vagrant.xml
    # # Add Vagrant user - OPNsense style
    sed -i '' -e '/<\\/member>/r files/admins.xml' /usr/local/etc/config.xml
    sed -i '' -e '/<\\/user>/r files/vagrant.xml' /usr/local/etc/config.xml
    # # Change home directory to group nobody
    chgrp -R nobody /usr/home/vagrant
    # # Change sudoers file to reference user instead of group
    sed -i '' -e 's/^%//' /usr/local/etc/sudoers.d/vagrant
    # # Reboot the system

    cp -f files/config2.xml /usr/local/etc/config.xml

    shutdown -r now

  SHELL
  
end
config.vm.define "logger" do |cfg|
  cfg.vm.box = "bento/ubuntu-20.04"
  cfg.vm.hostname = "logger"
  cfg.vm.provision :shell, path: "logger_bootstrap.sh"
  cfg.vm.network :private_network, ip: "192.168.56.105", gateway: "192.168.56.111", dns: "8.8.8.8" 
  cfg.vm.provider "virtualbox" do |vb, override|
    vb.gui = false
    vb.name = "logger"
    vb.customize ["modifyvm", :id, "--memory", 2048]
    vb.customize ["modifyvm", :id, "--cpus", 2]
    vb.customize ["modifyvm", :id, "--vram", "32"]
    vb.customize ["modifyvm", :id, "--nicpromisc2", "allow-all"]
    vb.customize ["modifyvm", :id, "--clipboard", "bidirectional"]
    vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
    vb.customize ["setextradata", "global", "GUI/SuppressMessages", "all" ]
  end
 
  cfg.vm.provision 'shell',run: "always", inline: <<-SHELL
  sudo ip route del default via 10.0.2.2
  sudo ip route add default via 192.168.56.111
SHELL

end

config.vm.define "caldera" do |trst|

  trst.vm.box = "bento/ubuntu-20.04"
  trst.vm.hostname = "caldera"
  trst.ssh.keep_alive = true

  
  trst.vm.network "private_network", ip: "192.168.100.100"
  
  trst.vm.provider "virtualbox" do |vb|
    # vb.gui = true
    vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]

   vb.name = "caldera"
   vb.cpus = 2
   vb.memory = 512
  end
  #instalación de caldera
  # trst.vm.provision "file", source: "app.py", destination: "/home/vagrant/app.py"

  # trst.vm.provision :shell, :inline => "python3 /home/vagrant/app.py"
  
  #ejecutar script de caldera
  trst.vm.provision "file",run: "always", source: "scriptcaldera1.py", destination: "/home/vagrant/scriptcaldera1.py"
  trst.vm.provision "file",run: "always", source: "windows.json", destination: "/home/vagrant/windows.json"

  

  trst.vm.provision :shell, :path => "caldera1.sh"




   trst.vm.provision 'shell',run: "always", inline: <<-SHELL
  


   sudo ip route del default via 10.0.2.2
   sudo ip route add default via 192.168.100.111
   

  


 SHELL

   
 end


   

  config.vm.define "dc" do |cfg|
    cfg.vm.box = "detectionlab/win2016"
    cfg.vm.hostname = "dc"
    cfg.vm.boot_timeout = 600
    cfg.winrm.transport = :plaintext
    cfg.vm.communicator = "winrm"
    cfg.winrm.basic_auth_only = true
    cfg.winrm.timeout = 300
    cfg.winrm.retry_limit = 20
    cfg.vm.network :private_network, ip: "192.168.56.102", gateway: "192.168.56.1", dns: "8.8.8.8"

    cfg.vm.provision "shell", path: "scripts/fix-second-network.ps1", privileged: true, args: "-ip 192.168.56.102 -dns 8.8.8.8 -gateway 192.168.56.1" 
    cfg.vm.provision "shell", path: "scripts/provision.ps1", privileged: false
    cfg.vm.provision "reload"
    cfg.vm.provision "shell", path: "scripts/provision.ps1", privileged: false
    cfg.vm.provision "shell", path: "scripts/download_palantir_wef.ps1", privileged: false
    cfg.vm.provision "shell", path: "scripts/install-utilities.ps1", privileged: false
    cfg.vm.provision "shell", path: "scripts/install-redteam.ps1", privileged: false
    cfg.vm.provision "shell", path: "scripts/install-choco-extras.ps1", privileged: false
    cfg.vm.provision "shell", path: "scripts/install-osquery.ps1", privileged: false
    cfg.vm.provision "shell", path: "scripts/install-sysinternals.ps1", privileged: false
    cfg.vm.provision "shell", path: "scripts/install-velociraptor.ps1", privileged: false
    cfg.vm.provision "shell", path: "scripts/configure-ou.ps1", privileged: false
    cfg.vm.provision "shell", path: "scripts/configure-wef-gpo.ps1", privileged: false
    cfg.vm.provision "shell", path: "scripts/configure-powershelllogging.ps1", privileged: false
    cfg.vm.provision "shell", path: "scripts/configure-AuditingPolicyGPOs.ps1", privileged: false
    cfg.vm.provision "shell", path: "scripts/configure-rdp-user-gpo.ps1", privileged: false
    cfg.vm.provision "shell", path: "scripts/configure-disable-windows-defender-gpo.ps1", privileged: false
    cfg.vm.provision "shell", path: "scripts/configure-taskbar-layout-gpo.ps1", privileged: false
    cfg.vm.provision "shell", path: "scripts/install-autorunstowineventlog.ps1", privileged: false
    cfg.vm.provision "shell", inline: 'wevtutil el | Select-String -notmatch "Microsoft-Windows-LiveId" | Foreach-Object {wevtutil cl "$_"}', privileged: false
    cfg.vm.provision "shell", inline: "Set-SmbServerConfiguration -AuditSmb1Access $true -Force", privileged: false
    cfg.vm.provision "shell", inline: "Write-Host 'DC Provisioning Complete!'", privileged: false


    cfg.vm.provider "virtualbox" do |vb, override|
      vb.gui = false
      vb.name = "dc.windomain.local"
      vb.default_nic_type = "82545EM"
      vb.customize ["modifyvm", :id, "--memory", 2048]
      vb.customize ["modifyvm", :id, "--cpus", 2]
      vb.customize ["modifyvm", :id, "--vram", "32"]
      vb.customize ["modifyvm", :id, "--clipboard", "bidirectional"]
      vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
      vb.customize ["setextradata", "global", "GUI/SuppressMessages", "all" ]
    end
    cfg.vm.provision 'shell',run: "always",privileged: false, inline: <<-SHELL
    route delete 0.0.0.0 
    route ADD 0.0.0.0 MASK 0.0.0.0 192.168.56.111
    
    SHELL

   
  end

  config.vm.define "wef" do |cfg|
    cfg.vm.box = "detectionlab/win2016"
    cfg.vm.hostname = "wef"
    cfg.vm.boot_timeout = 600
    cfg.vm.communicator = "winrm"
    cfg.winrm.basic_auth_only = true
    cfg.winrm.timeout = 300
    cfg.winrm.retry_limit = 20
    cfg.vm.network :private_network, ip: "192.168.56.103", gateway: "192.168.56.1", dns: "192.168.56.102"

    cfg.vm.provision "shell", path: "scripts/fix-second-network.ps1", privileged: true, args: "-ip 192.168.56.103 -dns 8.8.8.8 -gateway 192.168.56.1" 
    cfg.vm.provision "shell", path: "scripts/provision.ps1", privileged: false
    cfg.vm.provision "reload"
    cfg.vm.provision "shell", path: "scripts/provision.ps1", privileged: false
    cfg.vm.provision "shell", path: "scripts/download_palantir_wef.ps1", privileged: false
    cfg.vm.provision "shell", inline: 'wevtutil el | Select-String -notmatch "Microsoft-Windows-LiveId" | Foreach-Object {wevtutil cl "$_"}', privileged: false
    cfg.vm.provision "shell", path: "scripts/install-wefsubscriptions.ps1", privileged: false
    cfg.vm.provision "shell", path: "scripts/install-splunkuf.ps1", privileged: false
    cfg.vm.provision "shell", path: "scripts/install-windows_ta.ps1", privileged: false
    cfg.vm.provision "shell", path: "scripts/install-utilities.ps1", privileged: false
    cfg.vm.provision "shell", path: "scripts/install-redteam.ps1", privileged: false
    cfg.vm.provision "shell", path: "scripts/install-evtx-attack-samples.ps1", privileged: false
    cfg.vm.provision "shell", path: "scripts/install-choco-extras.ps1", privileged: false
    cfg.vm.provision "shell", path: "scripts/install-osquery.ps1", privileged: false
    cfg.vm.provision "shell", path: "scripts/install-sysinternals.ps1", privileged: false
    cfg.vm.provision "shell", path: "scripts/install-velociraptor.ps1", privileged: false
    cfg.vm.provision "shell", path: "scripts/configure-pslogstranscriptsshare.ps1", privileged: false
    cfg.vm.provision "shell", path: "scripts/install-autorunstowineventlog.ps1", privileged: false
    cfg.vm.provision "shell", inline: "Set-SmbServerConfiguration -AuditSmb1Access $true -Force", privileged: false
    cfg.vm.provision "shell", path: "scripts/install-microsoft-ata.ps1", privileged: false
    cfg.vm.provision "shell", inline: "Write-Host 'WEF Provisioning Complete!'", privileged: false

    

    cfg.vm.provider "virtualbox" do |vb, override|
      vb.gui = false
      vb.name = "wef.windomain.local"
      vb.default_nic_type = "82545EM"
      vb.customize ["modifyvm", :id, "--memory", 2048]
      vb.customize ["modifyvm", :id, "--cpus", 2]
      vb.customize ["modifyvm", :id, "--vram", "32"]
      vb.customize ["modifyvm", :id, "--clipboard", "bidirectional"]
      vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
      vb.customize ["setextradata", "global", "GUI/SuppressMessages", "all" ]
    end
    cfg.vm.provision 'shell',run: "always",privileged: false, inline: <<-SHELL
    route delete 0.0.0.0 
    route ADD 0.0.0.0 MASK 0.0.0.0 192.168.56.111
    
    SHELL
    
  end

  config.vm.define "win10" do |cfg|
    cfg.vm.box = "detectionlab/win10"
    cfg.vm.hostname = "win10"
    cfg.vm.boot_timeout = 1200
    cfg.vm.communicator = "winrm"
    cfg.winrm.basic_auth_only = true
    cfg.winrm.timeout = 1200
    cfg.winrm.retry_limit = 20
    cfg.vm.network :private_network, ip: "192.168.56.104", gateway: "192.168.56.1", dns: "192.168.56.102"

    cfg.vm.provision "shell", path: "scripts/fix-second-network.ps1", privileged: false, args: "-ip 192.168.56.104 -dns 8.8.8.8 -gateway 192.168.56.1" 
    cfg.vm.provision "shell", path: "scripts/MakeWindows10GreatAgain.ps1", privileged: false
    cfg.vm.provision "shell", path: "scripts/provision.ps1", privileged: false
    cfg.vm.provision "reload"
    cfg.vm.provision "shell", path: "scripts/provision.ps1", privileged: false
    cfg.vm.provision "shell", path: "scripts/download_palantir_wef.ps1", privileged: false
    cfg.vm.provision "shell", inline: 'wevtutil el | Select-String -notmatch "Microsoft-Windows-LiveId" | Foreach-Object {wevtutil cl "$_"}', privileged: false
    cfg.vm.provision "shell", path: "scripts/install-utilities.ps1", privileged: false
    cfg.vm.provision "shell", path: "scripts/install-redteam.ps1", privileged: false
    cfg.vm.provision "shell", path: "scripts/install-choco-extras.ps1", privileged: false
    cfg.vm.provision "shell", path: "scripts/install-osquery.ps1", privileged: false
    cfg.vm.provision "shell", path: "scripts/install-sysinternals.ps1", privileged: false
    cfg.vm.provision "shell", path: "scripts/install-velociraptor.ps1", privileged: false
    cfg.vm.provision "shell", path: "scripts/install-autorunstowineventlog.ps1", privileged: false


    cfg.vm.provision "shell", inline: "Write-Host 'Win10 Provisioning Complete!'", privileged: false
    
    # cfg.vm.provision "file",run: "always", source: "scripts/agente-windows.ps1", destination: "C:\Users\vagrant\Desktop\agente-windows.ps1"
    # cfg.vm.provision "shell",run:"always", path: "scripts/agente-windows.ps1",privileged:false
    
    #cfg.vm.provision "shell",path:"new_agent.ps1",powershell_elevated_interactive: "true",run: "always", privileged: true

    
    cfg.vm.provider "virtualbox" do |vb, override|
      vb.gui = false
      vb.name = "win10.windomain.local"
      vb.default_nic_type = "82545EM"
      vb.customize ["modifyvm", :id, "--memory", 2048]
      vb.customize ["modifyvm", :id, "--cpus", 2]
      vb.customize ["modifyvm", :id, "--vram", "32"]
      vb.customize ["modifyvm", :id, "--clipboard", "bidirectional"]
      vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
      vb.customize ["setextradata", "global", "GUI/SuppressMessages", "all" ]
    end
     cfg.vm.provision 'shell',run: "always",privileged: false, inline: <<-SHELL
     route delete 0.0.0.0 
     route ADD 0.0.0.0 MASK 0.0.0.0 192.168.56.111
      
     

     SHELL
   
   
    end
end
