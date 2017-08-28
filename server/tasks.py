"""Task Runners for TinyLog Server"""

import invoke

@invoke.task
def venv(ctx):
	ctx.run('virtualenv venv')
	ctx.run('venv/bin/pip3 install -Ur requirements.txt')
	ctx.run('venv/bin/pip3 install -Ur dev_requirements.txt')
