##
# Copyright 2009-2012 Stijn De Weirdt
# Copyright 2010 Dries Verdegem
# Copyright 2010-2012 Kenneth Hoste
# Copyright 2011 Pieter De Baets
# Copyright 2011-2012 Jens Timmerman
#
# This file is part of EasyBuild,
# originally created by the HPC team of the University of Ghent (http://ugent.be/hpc).
#
# http://github.com/hpcugent/easybuild
#
# EasyBuild is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation v2.
#
# EasyBuild is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with EasyBuild.  If not, see <http://www.gnu.org/licenses/>.
##
"""
EasyBuild support for building and installing MUMer, implemented as an easyblock
"""
import os
import shutil

from easybuild.easyblocks.generic.configuremake import ConfigureMake 
from easybuild.tools.filetools import run_cmd


class EB_MUMmer(ConfigureMake):
    """Support for building and installing MUMmer."""

    def __init__(self, *args, **kwargs):
        """Constructor, set to build in installdir"""
        super(EB_MUMmer, self).__init__(*args, **kwargs)
        self.build_in_installdir = True

    def configure_step(self):
        """Configure MUMmer build by running make check."""
        cmd = "%s make check %s" % (self.cfg['preconfigopts'], self.cfg['configopts'])
        run_cmd(cmd, log_all=True, simple=True, log_output=True)
        # build in installation directory

    def make_step(self):
        """Build MUMer"""
        makeopts = self.cfg['makeopts']
        # set all as default make argument
        makeopts = " ".join([makeopts, 'all'])
        super(EB_MUMmer, self).build_step()

    def make_module_extra(self):
        """Add the root to path, since this is where the binaries are located"""
        txt = super(self.__class__, self).make_module_extra()
        txt += self.moduleGenerator.prepend_paths("PATH", [self.cfg['start_dir']] )
        txt += self.moduleGenerator.prepend_paths("PERL5LIB", [os.path.join(self.cfg['start_dir'], "scripts")])
        return txt

    def sanity_check_step(self):
        """Custom sanity check for OpenFOAM"""

        custom_paths =   {'files': [os.path.join(self.cfg['start_dir'], x) for x in ['mapview', 'combineMUMs', 'mgaps',
                                                                                     'run-mummer3', 'show-coords',
                                                                                     'show-snps', 'show-aligns',  
                                                                                     'dnadiff', 'mummerplot',
                                                                                     'nucmer2xfig', 'annotate',
                                                                                     'promer', 'show-diff', 'nucmer',
                                                                                     'delta-filter', 'src',
                                                                                     'run-mummer1', 'gaps', 'mummer',
                                                                                     'repeat-match', 'show-tiling', 
                                                                                      'exact-tandems',
                                                                                     ]
                                    ],
                          'dirs': [os.path.join(self.cfg['start_dir'], x) for x in ['scripts', 'docs', 'aux_bin']]
                         }

        self.log.info("Customized sanity check paths: %s" % custom_paths)

        super(EB_MUMmer, self).sanity_check_step(custom_paths=custom_paths)
