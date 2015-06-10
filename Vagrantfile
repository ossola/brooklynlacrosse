Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.hostname = "dev"
  config.vm.network "forwarded_port", guest: 80, host: 2828 
  config.vm.provision :puppet do |puppet|
    puppet.options = "--verbose --debug"
  end
end
