exec { 'apt-get update':
    path => '/usr/bin',
}
file { ['/data', '/data/web',]:
    ensure => 'directory',
}
file { '/data/web/brooklynlacrosse/':
   ensure => 'link',
   target => '/vagrant/brooklynlacrosse/',
   force  => true,
}
file {'/etc/apache2/sites-enabled/000-default.conf':
	ensure => absent,
}
file {'/var/www/html/index.html':
	ensure => absent,
}
file {'/etc/apache2/sites-available/brooklynlacrosse.conf':
   ensure => file,
   content => 'NameVirtualHost *.80
<VirtualHost *:80>
        ServerAdmin info@brooklynlacrosse.com
        ServerName brooklynlacrosse.com
        ServerAlias www.brooklynlacrosse.com
        WSGIDaemonProcess brooklynlacrosse
        WSGIScriptAlias / /data/web/brooklynlacrosse/bk.wsgi

        <Directory /data/web/brooklynlacrosse>
                Options All
                AllowOverride All
                Require all granted
        </Directory>

        <Directory /data/web/brooklynlacrosse>
                WSGIProcessGroup brooklynlacrosse
                WSGIApplicationGroup %{GLOBAL}
                Order allow,deny
                Allow from all
        </Directory>
</VirtualHost>
',
   require => Package['apache2'],
}  
file { '/etc/apache2/sites-enabled/brooklynlacrosse.conf':
   ensure => 'link',
   target => '/etc/apache2/sites-available/brooklynlacrosse.conf',
   force  => true,
}
package { 'apache2':
    ensure  => present,
    require => Exec['apt-get update'],
}
package { 'libapache2-mod-wsgi':
    ensure  => present,
    require => Exec['apt-get update'],
}
package { 'python-pip':
    ensure  => present,
    require => Exec['apt-get update'],
}
package { 'flask':
    ensure   => present,
    provider => pip,
}
package { 'gdata':
    ensure   => present,
    provider => pip,
}
package { 'oauth2client':
    ensure   => present,
    provider => pip,
}
service { 'apache2':
    ensure  => 'running',
    require => Package['apache2'],
}