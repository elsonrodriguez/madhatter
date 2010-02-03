"""
Directory resource configuration class.

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

module for configuring directory resources on RedHat based distros.
"""

import shutil
import stat
import pwd
import grp
import os.path
import time

class ConfigureDirectories:

    def __init__(self, directories):
        self.directories = directories
        self.in_sync     = 0
        self.failed      = 0
        self.oo_sync     = 0

    def configure(self):
        """
        Configure directory resources.
        """
        print "\033[1;36m- Configuring Directories\033[1;m"
        runtime_start = time.time()
        for directory in self.directories:
            action    = self.directories[directory]['action']
            old_dir   = self.directories[directory]['path']
            if action == 'create':
                new_mode  = int(self.directories[directory]['mode'],8)
                new_uid   = pwd.getpwnam(self.directories[directory]['owner'])[2]
                new_gid   = grp.getgrnam(self.directories[directory]['group'])[2]
                # Check if the directory resource exist.
                if os.path.isdir(old_dir):
                    stat_info = os.stat(old_dir)
                    old_mode  = stat.S_IMODE(stat_info.st_mode)
                    old_uid   = pwd.getpwuid(stat_info.st_uid)[2]
                    old_gid   = grp.getgrgid(stat_info.st_gid)[2]
                    # Is the resource in sync?
                    if old_mode != new_mode or old_uid != new_uid or old_gid != new_gid:
                        self.sync(old_dir, new_mode, new_uid, new_gid)
                    else:
                        self.in_sync += 1
                else:
                    self.create(old_dir,new_mode,new_uid,new_gid)
            elif action == 'remove':
                if os.path.isdir(old_dir):
                    self.remove(old_dir)
                else:
                    self.in_sync += 1
            else:
                # This should never happen.
                pass
        runtime_end = time.time()
        runtime = (runtime_end - runtime_start)
        stats = {
            'runtime': runtime,
            'in_sync': self.in_sync,
            'oo_sync': self.oo_sync,
            'failed' : self.failed
        }
        return stats

    def create(self,directory,mode,uid,gid):
        """
        Create directory resources.
        """
        print "  Directory out of sync, creating %s" % directory
        os.makedirs(directory,mode)
        os.chown(directory,uid,gid)
        self.oo_sync += 1

    def remove(self,directory):
        """
        Remove directory resources.
        """
        print "  Directory out of sync, removing %s" % directory
        shutil.rmtree(directory)
        self.oo_sync += 1

    def sync(self,directory,mode,uid,gid):
        """
        Sync directory resources.
        """
        os.chmod(directory,mode)
        os.chown(directory,uid,gid)
        self.oo_sync += 1
