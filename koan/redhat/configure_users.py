"""
User resource configuration class.

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

module for configuring user resources on RedHat based distros.
"""

import pwd
import subprocess
import time

class ConfigureUsers:
    def __init__(self, users):
        self.users = users
        self.in_sync = 0
        self.oo_sync = 0
        self.failed  = 0

    def configure(self):
        print "\033[1;36m- Configuring Users\033[1;m"
        runtime_start = time.time()
        users = self.users

        for user in users:
            action     = users[user]['action']
            username   = user
            if action == 'create':
                new_shell  = users[user]['shell']
                new_gid    = users[user]['gid']
                new_groups = users[user]['groups']
                # Does the user exist?
                try:
                    user_info= pwd.getpwnam(username)
                    old_uid   = user_info[2]
                    old_gid   = user_info[3]
                    old_home  = user_info[5]
                    old_shell = user_info[6]
                    # User resource in sync?
                    if old_shell != new_shell or old_gid != int(new_gid):
                        self.sync(username,new_gid,new_shell,new_groups)
                    else:
                        self.in_sync += 1
                except KeyError:
                    self.create(username,new_groups,new_shell)
            elif action == 'remove':
                try:
                    user_info= pwd.getpwnam(username)
                    self.remove(username)
                except KeyError:
                    self.in_sync += 1
            else:
                # This should never happen.
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

    def create(self,username,groups,shell):
        print "  %s does not exsit, creating..." % username
        subprocess.call(['/usr/sbin/useradd', '-s', shell, '-G', groups, username])
        self.oo_sync += 1

    def remove(self,username):
        print "  removing user: %s" % username
        subprocess.call(['/usr/sbin/userdel', '-r', username])
        self.oo_sync += 1

    def sync(self,username,gid,shell,groups):
        subprocess.call(['/usr/sbin/usermod', '-s', shell, '-g', gid, '-G', groups, username])
        self.oo_sync += 1
