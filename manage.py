#!/usr/bin/env python
from migrate.versioning.shell import main

if __name__ == '__main__':
    main(repository='concurs_migrate', debug='False', url='sqlite:///concurs_ash.sqlite')
