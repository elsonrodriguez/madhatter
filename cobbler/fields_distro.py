# FIXME: header

def get_fields():
   return {
     'name': {
       'type'    :'text',
       'valtype' :'str',
       'label'   :'Name',
       'example' :'Example: RHEL-5-i386',
       'size'    :'128',
       'width'   :'150px',
       'value'   :'',
       'default' :'',
       'opts'    :'',
       'setopts' :'disabled="true"',
       'editable':True,
     },
     'ctime': {
       'type'    :'label',
       'valtype' :'str',
       'label'   :'Created',
       'value'   :'',
       'default' :'',
       'editable':False,
     },
     'mtime': {
       'type'    :'label',
       'valtype' :'str',
       'label'   :'Last Modified',
       'value'   :'',
       'default' :'',
       'editable':False,
     },
     'kernel': {
       'type'    :'text',
       'valtype' :'str',
       'label'   :'Kernel',
       'example' :'Absolute filesystem path to a kernel file',
       'size'    :'255',
       'width'   :'400px',
       'value'   :'',
       'default' :'',
       'opts'    :'',
       'setopts' :'',
       'editable':True,
     },
     'initrd': {
       'type'    :'text',
       'valtype' :'str',
       'label'   :'Initrd',
       'example' :'Absolute filesystem path to an initrd file',
       'size'    :'255',
       'width'   :'400px',
       'value'   :'',
       'default' :'',
       'opts'    :'',
       'setopts' :'',
       'editable':True,
    },
     'kernel_options': {
       'type'    :'text',
       'valtype' :'str',
       'label'   :'Kernel Options',
       'example' :'Example: noipv6 magic=foo',
       'size'    :'255',
       'width'   :'400px',
       'value'   :'',
       'default' :'',
       'opts'    :'',
       'setopts' :'',
       'editable':True,
     },
     'kernel_options_post': {
       'type'    :'text',
       'valtype' :'str',
       'label'   :'Kernel Options Post',
       'example' :'Example: clocksource=pit nosmp noapic nolapic',
       'size'    :'255',
       'width'   :'400px',
       'value'   :'',
       'default' :'',
       'opts'    :'',
       'setopts' :'',
       'editable':True,
     },
     'arch': {
       'type'    :'radio',
       'valtype' :'str',
       'label'   :'Architecture',
       'example' :'What architecture is the distro?',
       'value'   :'',
       'default' :'',
       'list'    :(('i386','i386'),('x86','x86'),('x86_64','x86_64'),('ppc','ppc'),('ppc64','ppc64'),('s390','s390'),('s390x','s390x'),('ia64','ia64')),
       'opts'    :'',
       'setopts' :'',
       'editable':True,
     },
     'ks_meta': {
       'type'    :'text',
       'valtype' :'str',
       'label'   :'Kickstart Metadata',
       'example' :'Example: dog=fido gnome=yes foo bar',
       'size'    :'255',
       'width'   :'400px',
       'value'   :'',
       'default' :'',
       'opts'    :'',
       'setopts' :'',
       'editable':True,
     },
     'breed': {
       'type'    :'radio',
       'valtype' :'str',
       'label'   :'Breed',
       'example' :'This option determines how kernel options are prepared',
       'value'   :'',
       'default' :'',
       'list'    :(('redhat','Red Hat Based'), ('debian','Debian'), ('ubuntu','Ubuntu'), ('suse','SuSE')),
       'opts'    :'',
       'setopts' :'',
       'editable':True,
     },
     'os_version': {
       'type'    :'text',
       'valtype' :'str',
       'label'   :'OS Version',
       'example' :'Example: rhel2.1, rhel4, fedora8',
       'size'    :'255',
       'width'   :'400px',
       'value'   :'',
       'default' :'',
       'opts'    :'',
       'setopts' :'',
       'editable':True,
     },
     'owners': {
       'type'    :'text',
       'valtype' :'list',
       'label'   :'Access Allowed For',
       'example' :'Applies only if using authz_ownership module, space delimited',
       'size'    :'255',
       'width'   :'400px',
       'value'   :'',
       'default' :'',
       'opts'    :'',
       'setopts' :'',
       'editable':True,
     },
     'mgmt_classes': {
       'type'    :'text',
       'valtype' :'list',
       'label'   :'Management Classes',
       'example' :'Management classes (space delimited) for use with external configuration management system',
       'size'    :'255',
       'width'   :'400px',
       'value'   :'',
       'default' :'',
       'opts'    :'',
       'setopts' :'',
       'editable':True,
     },
     'template_files': {
       'type'    :'text',
       'valtype' :'str',
       'label'   :'Templated Files',
       'example' :'Files that can be downloaded to the system during kickstart and with koan, using internal templating',
       'size'    :'255',
       'width'   :'400px',
       'value'   :'',
       'default' :'',
       'opts'    :'',
       'setopts' :'',
       'editable':True,
     },
     'comment': {
       'type'    :'textarea',
       'valtype' :'str',
       'label'   :'Comment',
       'example' :'This is a free-form description field',
       'rows'    :'5',
       'cols'    :'30',
       'width'   :'400px',
       'value'   :'',
       'default' :'',
       'opts'    :'',
       'setopts' :'',
       'editable':True,
     },
     'redhat_management_key': {
       'type'    :'text',
       'valtype' :'str',
       'label'   :'Management Key',
       'example' :'Registration key for RHN, Satellite, or Spacewalk',
       'size'    :'255',
       'width'   :'400px',
       'value'   :'',
       'default' :'',
       'opts'    :'',
       'setopts' :'',
       'editable':True,
     },
     'redhat_management_server': {
       'type'    :'text',
       'valtype' :'str',
       'label'   :'Management Server',
       'example' :'RHN, Satellite, or Spacewalk server',
       'size'    :'255',
       'width'   :'400px',
       'value'   :'',
       'default' :'',
       'opts'    :'',
       'setopts' :'',
       'editable':True,
     },
   }