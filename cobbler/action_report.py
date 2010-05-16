"""
Report from a cobbler master.
FIXME: reinstante functionality for 2.0

Copyright 2007-2009, Red Hat, Inc
Anderson Silva <ansilva@redhat.com>
Michael DeHaan <mdehaan@redhat.com>

This software may be freely redistributed under the terms of the GNU
general public license.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
"""

import re
from cexceptions import *
import utils
import clogger

class Report:

    def __init__(self, config, logger=None):
        """
        Constructor
        """
        self.config = config
        self.settings = config.settings()
        self.api = config.api
        self.report_type = None
        self.report_what = None
        self.report_name = None
        self.report_fields = None
        self.report_noheaders = None
        self.array_re = re.compile('([^[]+)\[([^]]+)\]')
        if logger is None:
            logger       = clogger.Logger()
        self.logger      = logger


    def fielder(self, structure, fields_list):
        """
        Return data from a subset of fields of some item
        """
        item = {}

        for field in fields_list:
            
            internal = self.array_re.search(field)
            # check if field is primary field
            if field in structure.keys():
                item[field] = structure[field]
            # check if subfield in 'interfaces' field
            elif internal and internal.group(1) in structure.keys():
                outer = internal.group(1)
                inner = internal.group(2)
                if type(structure[outer]) is type({}) and inner in structure[outer]:
                    item[field] = structure[outer][inner]
            elif "interfaces" in structure.keys():
                for device in structure['interfaces'].keys():
                    if field in structure['interfaces'][device]:
                        item[field] = device + ': ' + structure['interfaces'][device][field]                    
        return item

    def reporting_csv(self, info, order, noheaders):
        """
        Formats data on 'info' for csv output
        """
        outputheaders = ''
        outputbody = ''
        sep = ','

        info_count = 0
        for item in info:

            item_count = 0
            for key in order:

                if info_count == 0:
                    outputheaders += str(key) + sep

                if key in item.keys():
                    outputbody += str(item[key]) + sep
                else:
                    outputbody += '-' + sep

                item_count = item_count + 1

            info_count = info_count + 1
            outputbody += '\n'

        outputheaders += '\n'

        if noheaders:
            outputheaders = '';

        return outputheaders + outputbody
 
    def reporting_trac(self, info, order, noheaders):
        """
        Formats data on 'info' for trac wiki table output
        """        
        outputheaders = ''
        outputbody = ''
        sep = '||'

        info_count = 0
        for item in info:
            
            item_count = 0
            for key in order:


                if info_count == 0:
                    outputheaders += sep + str(key)

                if key in item.keys():
                    outputbody += sep + str(item[key])
                else:
                    outputbody += sep + '-'

                item_count = item_count + 1

            info_count = info_count + 1
            outputbody += '||\n'

        outputheaders += '||\n'
        
        if noheaders:
            outputheaders = '';
        
        return outputheaders + outputbody

    def reporting_doku(self, info, order, noheaders):
        """
        Formats data on 'info' for doku wiki table output
        """      
        outputheaders = ''
        outputbody = ''
        sep1 = '^'
        sep2 = '|'


        info_count = 0
        for item in info:
            
            item_count = 0
            for key in order:

                if info_count == 0:
                    outputheaders += sep1 + key

                if key in item.keys():
                    outputbody += sep2 + item[key]
                else:
                    outputbody += sep2 + '-'

                item_count = item_count + 1

            info_count = info_count + 1
            outputbody += sep2 + '\n'

        outputheaders += sep1 + '\n'
        
        if noheaders:
            outputheaders = '';
        
        return outputheaders + outputbody

    def reporting_mediawiki(self, info, order, noheaders):
        """
        Formats data on 'info' for mediawiki table output
        """
        outputheaders = ''
        outputbody = ''
        opentable = '{| border="1"\n'
        closetable = '|}\n'
        sep1 = '||'
        sep2 = '|'
        sep3 = '|-'


        info_count = 0
        for item in info:

            item_count = 0
            for key in order:

                if info_count == 0 and item_count == 0:
                    outputheaders += sep2 + key
                elif info_count == 0:
                    outputheaders += sep1 + key

                if item_count == 0:
                    if key in item.keys():
                        outputbody += sep2 + str(item[key])
                    else:
                        outputbody += sep2 + '-'
                else:
                    if key in item.keys():
                        outputbody += sep1 + str(item[key])
                    else:
                        outputbody += sep1 + '-'

                item_count = item_count + 1

            info_count = info_count + 1
            outputbody += '\n' + sep3 + '\n'

        outputheaders += '\n' + sep3 + '\n'

        if noheaders:
            outputheaders = '';

        return opentable + outputheaders + outputbody + closetable
    
    def print_formatted_data(self, data, order, report_type, noheaders):
        """
        Used for picking the correct format to output data as
        """
        if report_type == "csv":
            self.logger.flat(self.reporting_csv(data, order, noheaders))
        if report_type == "mediawiki":
            self.logger.flat(self.reporting_mediawiki(data, order, noheaders))
        if report_type == "trac":
            self.logger.flat(self.reporting_trac(data, order, noheaders))
        if report_type == "doku":
            self.logger.flat(self.reporting_doku(data, order, noheaders))

        return True

    def reporting_sorter(self, a, b):
        """
        Used for sorting cobbler objects for report commands
        """
        return cmp(a.name, b.name)

    def reporting_print_sorted(self, collection):
        """
        Prints all objects in a collection sorted by name
        """
        collection = [x for x in collection]
        collection.sort(self.reporting_sorter)
        for x in collection:
            self.logger.flat(x.printable())
        return True

    def reporting_list_names2(self, collection, name):
        """
        Prints a specific object in a collection.
        """
        obj = collection.get(name)
        if obj is not None:
            self.logger.flat(obj.printable())
        return True
    
    def reporting_print_all_fields(self, collection, report_name, report_type, report_noheaders):
        """
        Prints all fields in a collection as a table given the report type
        """
        # per-item hack
        if report_name:
            collection = collection.find(name=report_name)
            if collection:
                collection = [collection]
            else:
                return

        collection = [x for x in collection]
        collection.sort(self.reporting_sorter)
        data = []
        out_order = []
        count = 0
        for x in collection:
            item = {}
            structure = x.to_datastruct()
           
            for (key, value) in structure.iteritems():

                # exception for systems which could have > 1 interface
                if key == "interfaces":
                    for (device, info) in value.iteritems():
                        for (info_header, info_value) in info.iteritems():
                            item[info_header] = str(device) + ': ' + str(info_value)
                            # needs to create order list for print_formatted_fields
                            if count == 0:
                                out_order.append(info_header)
                else: 
                    item[key] = value
                    # needs to create order list for print_formatted_fields
                    if count == 0:
                        out_order.append(key)                  

            count = count + 1
  
            data.append(item) 

        self.print_formatted_data(data = data, order = out_order, report_type = report_type, noheaders = report_noheaders)
        
        return True
    
    def reporting_print_x_fields(self, collection, report_name, report_type, report_fields, report_noheaders):
        """
        Prints specific fields in a collection as a table given the report type
        """
        # per-item hack
        if report_name:
            collection = collection.find(name=report_name)
            if collection:
                collection = [collection]
            else:
                return

        collection = [x for x in collection]
        collection.sort(self.reporting_sorter)
        data = []
        fields_list = report_fields.replace(' ', '').split(',')
        
        for x in collection:
            structure = x.to_datastruct()
            item = self.fielder(structure, fields_list)
            data.append(item)
         
        self.print_formatted_data(data = data, order = fields_list, report_type = report_type, noheaders = report_noheaders)
                        
        return True
        
    # -------------------------------------------------------

    def run(self, report_what = None, report_name = None, report_type = None, report_fields = None, report_noheaders = None):
        """
        Get remote profiles and distros and sync them locally
        """
               
        """
        1. Handles original report output
        2. Handles all fields of report outputs as table given a format
        3. Handles specific fields of report outputs as table given a format
        """        
        

        if report_type == 'text' and report_fields == 'all':

            for collection_name in ["distro","profile","system","repo","network","image","mgmtclass"]:
                if report_what=="all" or report_what==collection_name or report_what=="%ss"%collection_name:
                    if report_name:
                        self.reporting_list_names2(self.api.get_items(collection_name), report_name)
                    else:
                        self.reporting_print_sorted(self.api.get_items(collection_name))

        elif report_type == 'text' and report_fields != 'all':
            utils.die(self.logger,"The 'text' type can only be used with field set to 'all'")
 
        elif report_type != 'text' and report_fields == 'all':

            for collection_name in ["distro","profile","system","repo","network","image","mgmtclass"]:
                if report_what=="all" or report_what==collection_name or report_what=="%ss"%collection_name:
                    self.reporting_print_all_fields(self.api.get_items(collection_name), report_name, report_type, report_noheaders)
        
        else:

            for collection_name in ["distro","profile","system","repo","network","image","mgmtclass"]:
                if report_what=="all" or report_what==collection_name or report_what=="%ss"%collection_name:
                    self.reporting_print_x_fields(self.api.get_items(collection_name), report_name, report_type, report_fields, report_noheaders)

