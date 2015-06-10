## brooklynlacrosse.com

Flask application using jinja templates.
This repo also includes a vagrant file provisioned with puppet.
My local workstation has a git post-update hook which rsyncs all code changes to a t1 micro EC2 instance and bounces apache to pick up on any changes to the python code.

Development is done locally using Sublime Text 3 on both a Windows Desktop or MacBook.
Changes are checked in to the local repo, pushed to git hub, and deployed to production via the hooks.