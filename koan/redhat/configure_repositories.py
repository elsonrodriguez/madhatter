"""
Repository resource configuration class.

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

module for configuring repository resources on RedHat based distros.
"""

import filecmp
import shutil
import subprocess
import tempfile
import stat
import time
import os.path

class ConfigureRepositories:
    def __init__(self, repositories):
        self.repos   = repositories
        self.in_sync = 0
        self.oo_sync = 0
        self.failed  = 0

    def configure(self):
        """
        Configure repository resources.
        """
        print "\033[1;36m- Configuring Repositories\033[1;m"
        runtime_start = time.time()
        for repo in self.repos:
            action = self.repos[repo]['action']
            old_file = self.repos[repo]['path']
            if action == 'create':
                # Setup and write incoming file content to tempfile.
                t = tempfile.NamedTemporaryFile()
                t.write(self.repos[repo]['content'])
                t.flush()
                new_file = t.name
                # Check if the file resource exist on the client
                if os.path.isfile(old_file):
                    # Compare exsiting file and incoming changes
                    if not filecmp.cmp(old_file, new_file):
                        self.sync(old_file, new_file)
                    else:
                        self.in_sync += 1
                else:
                    self.create(old_file, new_file)
                # Close temporary file.
                t.close()
            elif action == 'remove':
                if os.path.isfile(old_file):
                    self.remove(old_file)
                else:
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
            'failed' : self.failed,
        }
        return stats

    def create(self,old_file,new_file):
        print "  %s not found, creating..." % (old_file)
        open(old_file, 'w').close()
        shutil.copy(new_file, old_file)
        os.chmod(old_file,644)
        os.chown(old_file,0,0)
        self.oo_sync += 1

    def remove(self,file):
        print "  removing %s" % file
        os.remove(file)
        self.oo_sync += 1

    def sync(self,old_file,new_file):
        # Show diff and overwrite exsiting file with temp
        self.diff_files(old_file, new_file)
        shutil.copy(new_file, old_file)
        os.chmod(old_file,644)
        os.chown(old_file,0,0)
        self.oo_sync += 1

    def diff_files(self, file1, file2):
        """
        Diff two files by shelling out to local system diff command.
        Make this configurable?
        """
        subprocess.call(['/usr/bin/diff', file1, file2])
