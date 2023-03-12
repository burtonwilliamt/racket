import argparse
import subprocess

import pypi_settings

parser = argparse.ArgumentParser(
    description='Cut a new micro version and release it to pypi.org')
parser.add_argument('--ignore_uncommited',
                    action='store_true',
                    help='Ignore any uncommited changes.')


def capture_output(command: list[str]) -> list[str]:
    res = subprocess.run(command, capture_output=True, check=True)
    if res.returncode != 0:
        raise RuntimeError(f'Non-zero return code when running {command}')
    if res.stderr != b'':
        print(res.stderr.decode('utf-8'))
    return res.stdout.decode('utf-8').splitlines()


def main():
    args = parser.parse_args()
    if args.ignore_uncommited:
        print(
            'Ignoring any uncommited changes because --ignore_uncommited was provided.'
        )
    else:
        print('Checking for uncommited changes...')
        uncommited = capture_output(['git', 'status', '--porcelain=v1'])
        if len(uncommited) != 0:
            print('Uncommited changes found:')
            print('\n'.join(uncommited))
            print('To ignore this, include the --ignore_uncommited flag.')
            return
        del uncommited

    print('Checking for unpushed commits...')
    unpushed = capture_output(['git', 'cherry', '-v'])
    if len(unpushed) != 0:
        print('Unpushed commits found:')
        print('\n'.join(unpushed))
        return
    del unpushed

    print('Incrementing the micro version...')
    old_version, new_version = capture_output(['hatch', 'version', 'micro'])
    old_version = old_version.removeprefix('Old: ')
    new_version = new_version.removeprefix('New: ')
    print(f'Migrated: {old_version}->{new_version}')

    print('Creating a release commit...')
    capture_output(['git', 'add', 'racket/__about__.py'])
    capture_output(['git', 'commit', '-m', f'"Version {new_version}"'])
    capture_output(['git', 'push'])

    print('Building the release...')
    capture_output(['hatch', 'build'])

    print('Publishing...')
    publishing_output = capture_output([
        'hatch', 'publish', '--user=__token__', f'--auth={pypi_settings.TOKEN}'
    ])
    print(publishing_output)
    print('Done!')


if __name__ == '__main__':
    main()