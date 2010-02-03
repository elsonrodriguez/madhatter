"""
Package resource configuration class.

Copyright 2010 Kelsey Hightower
Kelsey Hightower <kelsey.hightower@gmail.com>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
02110-1301  USA

module for configuring package resources on RedHat based distros.
requires the yum python module
"""

import subprocess
import sys
import time
import yum

class ConfigurePackages:
    def __init__(self, packages):
        self.packages = packages
        self.in_sync  = 0
        self.oo_sync  = 0
        self.failed   = 0

    def configure(self):
        print "\033[1;36m- Configuring Packages\033[1;m"
        runtime_start = time.time()
        # Setup YumBase
        yb = yum.YumBase()
        # Run in quite mode
        yb.preconf.debuglevel = 0
        yb.preconf.errorlevel = 0
        yb.doTsSetup()
        yb.doRpmDBSetup()
        # Setup YumCLI
        sys.path.append('/usr/share/yum-cli')
        import cli
        ybc = cli.YumBaseCli()
        # Run in quite mode
        ybc.preconf.debuglevel = 0
        ybc.preconf.errorlevel = 0
        # Assume yes to prevent Yum from prompting [Y/N]
        ybc.conf.assumeyes = True
        ybc.doTsSetup()
        ybc.doRpmDBSetup()
        pkg_list = list([package for package in self.packages])
        create_pkg_list = []
        remove_pkg_list = []
        for package in self.packages:
            if yb.isPackageInstalled(package):
                if self.packages[package]['action'] == 'create':
                    self.in_sync += 1
                if self.packages[package]['action'] == 'remove':
                    remove_pkg_list.append(package)
            if not yb.isPackageInstalled(package):
                if self.packages[package]['action'] == 'create':
                    create_pkg_list.append(package)
                if self.packages[package]['action'] == 'remove':
                    self.in_sync += 1
        doTransaction = False
        if create_pkg_list:
            self.create(ybc,create_pkg_list)
            doTransaction = True
        if remove_pkg_list:
            self.remove(ybc,remove_pkg_list)
            doTransaction = True
        if doTransaction:
            ybc.buildTransaction()
            ybc.doTransaction()
        # Collect Stats
        runtime_end = time.time()
        runtime = (runtime_end - runtime_start)
        stats = {
            'runtime': runtime,
            'in_sync': self.in_sync,
            'oo_sync': self.oo_sync,
            'failed' : self.failed
        }
        return stats

    def create(self,ybc,create_pkg_list):
        print "  Packages out of sync: %s" % create_pkg_list
        ybc.installPkgs(create_pkg_list)
        self.oo_sync += len(create_pkg_list)

    def remove(self,ybc,remove_pkg_list):
        ybc.erasePkgs(remove_pkg_list)
        self.oo_sync += len(remove_pkg_list)
