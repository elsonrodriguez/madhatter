"""
File resource configuration class.

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

module for configuring file resources on RedHat based distros.
"""

import filecmp
import shutil
import subprocess
import tempfile
import stat
import pwd
import grp
import os.path
import time

class ConfigureFiles:
    def __init__(self,files):
        self.files   = files
        self.in_sync = 0
        self.oo_sync = 0
        self.failed  = 0

    def configure(self):
        """
        Configure file resources.
        """
        print "\033[1;36m- Configuring Files\033[1;m"
        runtime_start = time.time()

        for file in self.files:
            action   = self.files[file]['action']
            old_file = self.files[file]['path'] + file
            if action == 'create':
                new_mode = int(self.files[file]['mode'],8)
                new_uid  = pwd.getpwnam(self.files[file]['owner'])[2]
                new_gid  = grp.getgrnam(self.files[file]['group'])[2]
               
                # Setup and write incoming file content to tempfile.
                t = tempfile.NamedTemporaryFile()
                t.write(self.files[file]['content'])
                t.flush()

                new_file = t.name

                # Check if the file exists
                if os.path.isfile(old_file):
                    stat_info = os.stat(old_file)
                    old_mode  = stat.S_IMODE(stat_info.st_mode)
                    old_uid   = pwd.getpwuid(stat_info.st_uid)[2]
                    old_gid   = grp.getgrgid(stat_info.st_gid)[2]
                    # Compare exsiting file and incoming changes
                    if not filecmp.cmp(old_file, new_file) or old_mode != new_mode or old_gid != new_gid or old_uid != new_uid:
                        self.sync(old_file,new_file,new_uid,new_gid,new_mode)
                    else:
                        self.in_sync += 1
                elif os.path.dirname(old_file):
                    self.create(old_file,new_file,new_uid,new_gid,new_mode)
                else:
                    print "%s not found, skipping." % (old_file)
                    self.failed += 1
                # Close temporary file.
                t.close()
            elif action == 'remove':
                if os.path.isfile(file):
                    self.remove(old_file)
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

    def create(self,old_file,new_file,uid,gid,mode):
        open(old_file,'w').close()
        self.diff_files(old_file, new_file)
        shutil.copy(new_file, old_file)
        os.chown(old_file,uid,gid)
        os.chmod(old_file,mode)
        self.oo_sync += 1

    def remove(self,file):
        os.remove(file)
        self.oo_sync += 1

    def sync(self,old_file,new_file,uid,gid,mode):
        self.diff_files(old_file, new_file)
        shutil.copy(new_file, old_file)
        os.chown(old_file,uid,gid)
        os.chmod(old_file,mode)
        self.oo_sync += 1

    def diff_files(self, file1, file2):
        """
        Diff two files by shelling out to local system diff command.
        Make this configurable?
        """
        subprocess.call(['/usr/bin/diff', file1, file2])
