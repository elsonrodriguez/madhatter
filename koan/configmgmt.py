"""
Configuration wrapper class.

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
"""

import simplejson as json

from redhat.configure_repositories import ConfigureRepositories
from redhat.configure_groups       import ConfigureGroups
from redhat.configure_users        import ConfigureUsers
from redhat.configure_packages     import ConfigurePackages
from redhat.configure_directories  import ConfigureDirectories
from redhat.configure_files        import ConfigureFiles
from redhat.configure_mounts       import ConfigureMounts

#=======================================================

class Configure:
    def __init__(self, data):
        self.data     = json.JSONDecoder().decode(data)
        self.repos    = self.data['repositories']
        self.groups   = self.data['groups']
        self.users    = self.data['users']
        self.pkgs     = self.data['packages']
        self.dirs     = self.data['directories']
        self.files    = self.data['files']
        self.mounts   = self.data['mounts']
        self.services = self.data['services']

    def configure_repositories(self):
        repos = ConfigureRepositories(self.repos)
        stats = repos.configure()
        return stats
    def configure_groups(self):
        groups = ConfigureGroups(self.groups)
        stats = groups.configure()
        return stats
    def configure_users(self):
        users = ConfigureUsers(self.users)
        stats = users.configure()
        return stats
    def configure_packages(self):
        packages = ConfigurePackages(self.pkgs)
        stats = packages.configure()
        return stats
    def configure_directories(self):
        directories = ConfigureDirectories(self.dirs)
        stats = directories.configure()
        return stats
    def configure_files(self):
        files = ConfigureFiles(self.files)
        stats = files.configure()
        return stats
    def configure_mounts(self):
        mounts = ConfigureMounts(self.mounts)
        stats = mounts.configure()
        return stats
