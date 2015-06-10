## brooklynlacrosse.com

Small Flask WebApp for a Club Lacrosse team based out of Brooklyn N.Y. (http://www.brooklynlacrosse.com)

Production code lives on a AWS t1 micro EC2 instance running Ubuntu Linux.
Apache serves the Python/HTML/Javascript/CSS via WSGI. The gdata library is imported to allow the rosters and schedules to be read in from google spreadsheets.

Development is done locally by spinning up a Vagrant VM instance, which is provsioned to mimic the production AWS instance using Puppet. Code is written using Sublime Text 3 on both a Windows Desktop or MacBook. Changes are checked in to the local repo, pushed to github, and deployed to production via a githook (seen below)


### post-commit
```
#!/bin/bash
git push -u origin master
rsync -avr -e 'ssh -i /home/matt/aws.pem' /home/matt/vagrant/trusty/brooklynlacrosse/ ubuntu@brooklynlacrosse.com:/data/web/brooklynlacrosse/
ssh -i /home/matt/aws.pem ubuntu@brooklynlacrosse.com 'sudo /etc/init.d/apache2 restart'
echo "COMPLETE!"
```