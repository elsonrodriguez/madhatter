"""
Copyright 2010, Kelsey Hightower
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

import utils
import item

from utils import _


FIELDS = [
  ["name","",0,"Name",True,"Ex: F10-i386-webserver",0,"str"],
  ["owners","SETTINGS:default_ownership","SETTINGS:default_ownership","Owners",True,"Owners list for authz_ownership (space delimited)",0,"list"],
  ["comment","",0,"Comment",True,"Free form text description",0,"str"],
  ["ctime",0,0,"",False,"",0,"int"],
  ["mtime",0,0,"",False,"",0,"int"],
  ["packages",[],0,"Packages",True,"Package resources",0,"list"],
  ["repositories",[],0,"Repositories",True,"Repo resources",0,"list"],
  ["mounts",[],0,"Mounts",True,"Mount resources",0,"list"],
  ["users",[],0,"Users",True,"User resources",0,"list"],
  ["groups",[],0,"Groups",True,"Group resources",0,"list"],
  ["files",[],0,"Files",True,"File resources",0,"list"],
  ["directories",[],0,"Directories",True,"Directory resources",0,"list"],
]

class Mgmtclass(item.Item):

    TYPE_NAME = _("mgmtclass")
    COLLECTION_TYPE = "mgmtclass"

    def make_clone(self):
        ds = self.to_datastruct()
        cloned = Mgmtclass(self.config)
        cloned.from_datastruct(ds)
        return cloned

    def get_fields(self):
        return FIELDS

    def set_packages(self,packages):
        self.packages = utils.input_string_or_list(packages)
        return True

    def set_repositories(self,repositories):
        self.repositories = utils.input_string_or_list(repositories)
        return True

    def set_mounts(self,mounts):
        self.mounts = utils.input_string_or_list(mounts)
        return True

    def set_users(self,users):
        self.users = utils.input_string_or_list(users)
        return True

    def set_groups(self,groups):
        self.groups = utils.input_string_or_list(groups)
        return True

    def set_files(self,files):
        self.files = utils.input_string_or_list(files)
        return True

    def set_directories(self,directories):
        self.directories = utils.input_string_or_list(directories)
        return True

    def get_parent(self):
        """
        currently the Cobbler object space does not support subobjects of mgmtclass
        as it is conceptually not useful.
        """
        return None

    def check_if_valid(self):
        if self.name is None or self.name == "":
            raise CX("name is required")
