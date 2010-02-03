"""
Mount resource configuration class.

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

module for configuring mount resources on RedHat based distros.
requires the python-augeas module
"""

import augeas
import os
import time

class ConfigureMounts:
    def __init__(self, mounts):
        self.mounts  = mounts
        self.in_sync = 0
        self.oo_sync = 0
        self.failed  = 0
        self.augeas = augeas.Augeas('/')

    def configure(self):
        print "\033[1;36m- Configuring Mounts\033[1;m"
        runtime_start = time.time()
        mounts = self.mounts
        matches = self.augeas.match('/files/etc/fstab/*/file')
        current_mount_points = list([self.augeas.get(match) for match in matches])
        # Get a list for nodes in to a list
        nodes = self.augeas.match('/files/etc/fstab/*')
        node_list = list([os.path.basename(node) for node in nodes])
        for mount in mounts:
            mount_point = mounts[mount]['mount-point']
            spec        = mounts[mount]['device-name']
            vfstype     = mounts[mount]['fs-type']
            opts        = mounts[mount]['options']
            dump        = mounts[mount]['dump-freq']
            passno      = mounts[mount]['pass-num']
            action      = mounts[mount]['action']
            if mount_point in current_mount_points:
                if action == 'create':
                    # Compare new and existing mount attributes
                    # Resolve any differences.
                    self.in_sync += 1
                if action == 'remove':
                    node = current_mount_points.index(mount_point) + 1
                    self.remove(node)
            if not mount_point in current_mount_points:
                if action == 'create':
                    self.create(node_list,spec,mount_point,vfstype,opts,dump,passno)
                if action == 'remove':
                    self.in_sync += 1
        self.augeas.save()
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

    def create(self,node_list,spec,mount_point,vfstype,opts,dump,passno):
        print "%s does not exist..creating" % mount_point
        # Get the a new node number. Must get the highest node
        # currently in the tree + 1. Used when create a new node
        # in the tree.
        node = (int(max(node_list)) + 1)
        self.augeas.set('/files/etc/fstab/%s/spec' % str(node), spec)
        self.augeas.set('/files/etc/fstab/%s/file' % str(node), mount_point)
        self.augeas.set('/files/etc/fstab/%s/vfstype' % str(node), vfstype)

        # Split, then assign each option to a different opts index
        # assigning "opt1,opt2" is in error for augeas
        opts = opts.split(',')
        opt_count = 0
        for opt in opts:
            self.augeas.set('/files/etc/fstab/%s/opt[%s]' % (str(node), opt_count), opt)
            opt_count = opt_count + 1
        # Configure the remaning options
        self.augeas.set('/files/etc/fstab/%s/dump' % str(node), dump)
        self.augeas.set('/files/etc/fstab/%s/passno' % str(node), passno)
        self.oo_sync += 1

    def remove(self,node):
        path = '/files/etc/fstab/%s' % node
        self.augeas.remove(path)
        self.oo_sync += 1

    def sync(self,spec,mount_point,vfstype,opts,dump,passno):
        pass
