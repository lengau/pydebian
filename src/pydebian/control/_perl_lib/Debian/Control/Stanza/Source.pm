package Debian::Control::Stanza::Source;

use strict;
use warnings;

use base 'Debian::Control::Stanza';

sub fields {
    return qw(
      Source
      Section
      Priority
      Maintainer
      Uploaders
      DM_Upload_Allowed
      Build_Conflicts
      Build_Conflicts_Indep
      Build_Depends
      Build_Depends_Indep
      Standards_Version
      Vcs_Browser
      Vcs_Bzr
      Vcs_CVS
      Vcs_Git
      Vcs_Svn
      Homepage
      XS_Autobuild
      Testsuite
    );
}

1;
