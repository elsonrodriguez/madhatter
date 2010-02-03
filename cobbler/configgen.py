"""
Configuration generation class.

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

module for generating configuration manifest using ksmeta data,
mgmtclasses, resources, and templates for a given system (hostname)
"""

from Cheetah.Template import Template
from ConfigParser import RawConfigParser
import cobbler.utils
import cobbler.api as capi
import pprint
import simplejson as json

class GenConfig:

    def __init__(self,hostname):
        self.hostname    = hostname
        self.handle      = capi.BootAPI()
        self.system      = self.handle.find_system(hostname=self.hostname)
        self.mgmtclasses = self.get_host_mgmtclasses()
        self.resources   = self.get_resources()

    def get_host_vars(self):
        handle = self.handle
        system = self.system
        return cobbler.utils.blender(handle, False, system)['ks_meta']

    def get_host_mgmtclasses(self):
        handle = self.handle
        system = self.system
        return cobbler.utils.blender(handle, False, system)['mgmt_classes']

    def get_repositories(self):
        return self.resources['repositories']
    def get_groups(self):
        return self.resources['groups']
    def get_users(self):
        return self.resources['users']
    def get_mounts(self):
        return self.resources['mounts']
    def get_packages(self):
        return self.resources['packages']
    def get_directories(self):
        return self.resources['directories']
    def get_files(self):
        return self.resources['files']

    def get_resources(self):
        handle = self.handle
        mgmtclasses = self.mgmtclasses
        repository_set   = set()
        group_set        = set()
        user_set         = set()
        mount_set        = set()
        package_set      = set()
        directory_set    = set()
        file_set         = set()
        # Construct the resources dictionary
        for mgmtclass in mgmtclasses:
            _mgmtclass = handle.find_mgmtclass(name=mgmtclass)
            for repo in _mgmtclass.repositories:
                repository_set.add(repo)
            for group in _mgmtclass.groups:
                group_set.add(group)
            for user in _mgmtclass.users:
                user_set.add(user)
            for mount in _mgmtclass.mounts:
                mount_set.add(mount)
            for package in _mgmtclass.packages:
                package_set.add(package)
            for directory in _mgmtclass.directories:
                directory_set.add(directory)
            for file in _mgmtclass.files:
                file_set.add(file)
        resources = {
            'repositories' : repository_set,
            'groups'       : group_set,
            'users'        : user_set,
            'mounts'       : mount_set,
            'packages'     : package_set,
            'directories'  : directory_set,
            'files'        : file_set,
        } 
        print resources
        return resources

    def gen_repository_data(self):
        """
        Generate repository resources dictionary.
        """
        repository_resources = RawConfigParser()
        repository_resources.read('/etc/cobbler/resources/repositories')
        repository_list = self.get_repositories()
        repository_data = {}
        for repo in repository_list:
            options = repository_resources.options(repo)
            repository_data[repo] = dict([(k, repository_resources.get(repo, k)) for k in options])
            if 'action' in repository_data[repo]:
                pass # validate action
            else:
                repository_data[repo]['action'] = 'create'
            repo_data = {}
            repo_data['repo'] = repo
            repo_data['repodata'] = repository_data[repo]
            # Use options to fill in default repo.template
            t = Template(file='/etc/cobbler/repo.template', searchList=[repo_data])
            repository_data[repo]['content'] = t.respond()
            repository_data[repo]['path'] = '/etc/yum.repos.d/%s.repo' % repo
        return repository_data

    def gen_group_data(self):
        """
        Generate group resources dictionary.
        """
        group_resources = RawConfigParser()
        group_resources.read('/etc/cobbler/resources/groups')
        group_list = self.get_groups()
        group_data = {}
        for group in group_list:
            options = group_resources.options(group)
            group_data[group] = dict([(k, group_resources.get(group, k)) for k in options])
            if 'action' in group_data[group]:
                pass # validate action
            else:
                group_data[group]['action'] = 'create'
        return group_data

    def gen_user_data(self):
        """
        Generate user resources dictionary.
        """
        user_resources = RawConfigParser()
        user_resources.read('/etc/cobbler/resources/users')
        user_list = self.get_users()
        user_data = {}
        for user in user_list:
            options = user_resources.options(user)
            user_data[user] = dict([(k, user_resources.get(user, k)) for k in options])
            if 'action' in user_data[user]:
                pass # validate action
            else:
                user_data[user]['action'] = 'create'
        return user_data

    def gen_mount_data(self):
        """
        Generate mount resources dictionary.
        """
        mount_resources = RawConfigParser()
        mount_resources.read('/etc/cobbler/resources/mounts')
        mount_list = self.get_mounts()
        mount_data = {}
        for mount in mount_list:
            options = mount_resources.options(mount)
            mount_data[mount] = dict([(k, mount_resources.get(mount, k)) for k in options])
            if 'action' in mount_data[mount]:
                pass # validate action
            else:
                mount_data[mount]['action'] = 'create'
        return mount_data

    def gen_package_data(self):
        """
        Generate package resources dictionary.
        """
        package_resources = RawConfigParser()
        package_resources.read('/etc/cobbler/resources/packages')
        package_list = self.get_packages()
        pkg_data = {}
        for package in package_list:
            options = package_resources.options(package)
            pkg_data[package] = dict([(k, package_resources.get(package, k)) for k in options])
            pkg_data[package]['name'] = package
            if 'action' in pkg_data[package]:
                pass # validate action
            else:
                pkg_data[package]['action'] = 'create'
        return pkg_data

    def gen_directory_data(self):
        """
        Generate directory resources dictionary.
        """
        directory_resources = RawConfigParser()
        directory_resources.read('/etc/cobbler/resources/directories')
        directory_list = self.get_directories()
        directory_data = {}
        for directory in directory_list:
            options = directory_resources.options(directory)
            directory_data[directory] = dict([(k, directory_resources.get(directory, k)) for k in options])
            if 'action' in directory_data[directory]:
                pass # validate action
            else:
                directory_data[directory]['action'] = 'create'
        return directory_data

    def gen_file_data(self):
        """
        Generate file resources dictionary.
        """
        file_resources = RawConfigParser()
        file_resources.read('/etc/cobbler/resources/files')
        file_list = self.get_files()
        file_data = {}
        for file in file_list:
            options = file_resources.options(file)
            file_data[file] = dict([(k, file_resources.get(file, k)) for k in options])
            if 'action' in file_data[file]:
                pass # validate action
            else:
                file_data[file]['action'] = 'create'
            if 'template' in file_data[file]:
                template_vars = self.get_host_vars()
                t = Template(file=file_data[file]['template'], searchList=[template_vars])
                file_data[file]['content'] = t.respond()
                del file_data[file]['template']
        return file_data

    def gen_config_data(self):
        """
        Generate configuration data.
        """
        config_data = {
            'repositories': self.gen_repository_data(),
            'groups': self.gen_group_data(),
            'users': self.gen_user_data(),
            'mounts': self.gen_mount_data(),
            'packages': self.gen_package_data(),
            'directories': self.gen_directory_data(),
            'files': self.gen_file_data(),
        }
        return config_data

    def gen_config_data_for_koan(self):
        """
        Encode configuration data. Return json object for Koan.
        """
        json_config_data = json.JSONEncoder(sort_keys=True, indent=4).encode(self.gen_config_data())
        return json_config_data
