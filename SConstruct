# -*- mode: python; -*-
import os

env = Environment(HOME=os.environ['HOME'])

SCRIPTS = Glob('scripts/*.py')
UNITS = [Glob('units/*.%s' % type) for type in 'service timer'.split()]

SCRIPTS_DIR = "$HOME/.web-plumbing"
UNITS_DIR = "$HOME/.config/systemd/user"

env.Install(SCRIPTS_DIR, SCRIPTS + ['requirements.txt'])
env.Install(UNITS_DIR, UNITS)

env.Alias('install', [SCRIPTS_DIR, UNITS_DIR])
env.Default('install')
