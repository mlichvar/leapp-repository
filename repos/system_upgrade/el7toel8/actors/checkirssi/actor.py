from leapp.actors import Actor
from leapp.libraries.common.reporting import report_with_remediation
from leapp.libraries.common.rpms import has_package
from leapp.models import InstalledRedHatSignedRPM
from leapp.tags import ChecksPhaseTag, IPUWorkflowTag
from leapp.reporting import Report


class CheckIrssi(Actor):
    """
    Check if irssi is installed. If yes, write information about non-compatible changes.
    """

    name = 'checkirssi'
    consumes = (InstalledRedHatSignedRPM,)
    produces = (Report,)
    tags = (ChecksPhaseTag, IPUWorkflowTag)

    def process(self):
        if has_package(InstalledRedHatSignedRPM, 'irssi'):
            report_with_remediation(
                title='Irssi incompatible changes in the next major version',
                summary='Disabled support for the insecure SSLv2 protocol.\n'
                        'Disabled SSLv3 due to the POODLE vulnerability.\n'
                        'Removing networks will now remove all attached servers and channels.\n'
                        'Removed --disable-ipv6 option.\n',
                remediation='Please update your scripts to be compatible with the changes.',
                severity='low')
