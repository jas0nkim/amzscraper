"""
run.py

features

- add new job to discover new product/listing
    accept variables:
        - domain
        - urls
- add new job to track existing products/listings
    accept variables:
        - domain
        - urls
        - asins
- monitor jobs
"""

import sys
import getopt
from pwbot_schedular import Runner
from pwbot_schedular import settings


def main(func, argv):
    """ main function
    """
    if func not in ['discover', 'track', 'jobs',]:
        print(settings.HELP_MESSAGE)
        sys.exit(2)
    try:
        opts, _ = getopt.getopt(argv, "hda:", ["help", "deploy"])
    except getopt.GetoptError as e:
        print(e)
        print("")
        print(settings.HELP_MESSAGE)
        sys.exit(2)
    add_version = False
    project = None
    version = None
    spider = None
    kwargs = {}
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print(settings.HELP_MESSAGE)
            sys.exit()
        elif opt in ('-d', '--deploy'):
            add_version = True
        elif opt in ('-p', '--project'):
            project = arg
        elif opt in ('-v', '--version'):
            version = arg
        elif opt in ('-s', '--spider'):
            spider = arg
        elif opt == '-a':
            name, value = arg.split('=', 1)
            kwargs[name] = value
    runner = Runner()
    if func == 'jobs':
        getattr(runner, func)()
    else:
        getattr(runner, func)(add_version=add_version,
                              project=project,
                              version=version,
                              spider=spider,
                              **kwargs)


if __name__ == "__main__":
    try:
        main(sys.argv[1], sys.argv[2:])
    except IndexError:
        print(settings.HELP_MESSAGE)
        sys.exit(2)
