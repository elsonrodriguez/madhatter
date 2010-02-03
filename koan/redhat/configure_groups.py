"""
Group resource configuration class.

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

module for configuring group resources on RedHat based distros.
"""

import grp
import subprocess
import time

class ConfigureGroups:
    def __init__(self, groups):
        self.groups  = groups
        self.in_sync = 0
        self.oo_sync = 0
        self.failed  = 0

    def configure(self):
        """
        Configure group resources.
        """
        print "\033[1;36m- Configuring Groups\033[1;m"
        runtime_start = time.time()
        groups = self.groups
        for group in groups:
            action  = groups[group]['action']
            new_gid = int(groups[group]['gid'])
            if action == 'create':
                try:
                    group_info = grp.getgrnam(group)
                    old_gid = group_info[2]
                    if old_gid != new_gid:
                        self.sync(group,new_gid)
                    else:
                        self.in_sync += 1
                except KeyError:
                    self.create(group,str(new_gid))
            elif action == 'remove':
                try:
                    group_info = grp.getgrnam(group)
                    self.remove(group)
                except KeyError:
                    self.in_sync += 1
            else:
                # This should never happen
                pass
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

    def create(self,group,gid):
        print "  %s group does not exist. Creating..." % group
        subprocess.call(['/usr/sbin/groupadd', group, '-g', gid])
        self.oo_sync += 1

    def remove(self,group):
        print "  Removing %s group" % (group)
        subprocess.call(['/usr/sbin/groupdel', group])
        self.oo_sync += 1

    def sync(self,group,gid):
        print "  %s has the wrong gid: changing to %s" % (group, gid)
        # Convert gid to string for subprocess call.
        subprocess.call(['/usr/sbin/groupmod', group, '-g', str(gid)])
        self.oo_sync += 1
