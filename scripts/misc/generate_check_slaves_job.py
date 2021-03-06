#!/usr/bin/env python3

import argparse
import sys

from ros_buildfarm.argument import add_argument_config_url
from ros_buildfarm.argument import add_argument_dry_run
from ros_buildfarm.config import get_index
from ros_buildfarm.jenkins import configure_job
from ros_buildfarm.jenkins import configure_management_view
from ros_buildfarm.jenkins import connect
from ros_buildfarm.templates import expand_template


def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser(
        description="Generate the 'check_slaves' job on Jenkins")
    add_argument_config_url(parser)
    add_argument_dry_run(parser)
    args = parser.parse_args(argv)

    config = get_index(args.config_url)
    job_config = get_job_config(config.notify_emails)

    jenkins = connect(config.jenkins_url)

    configure_management_view(jenkins, dry_run=args.dry_run)

    job_name = 'check_slaves'
    configure_job(jenkins, job_name, job_config, dry_run=args.dry_run)


def get_job_config(notification_emails):
    template_name = 'misc/check_slaves_job.xml.em'
    job_data = {
        'notification_emails': notification_emails,
    }
    job_config = expand_template(template_name, job_data)
    return job_config


if __name__ == '__main__':
    main()
