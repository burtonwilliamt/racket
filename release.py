import subprocess


def capture_output(command: list[str]) -> list[str]:
    res = subprocess.run(command,
                         capture_output=True,
                         check=True)
    if res.stderr != b'':
        raise RuntimeError('Unexpected command output:\n' + res.stderr)
    return res.stdout.decode('utf-8').splitlines()


def main():
    print('Checking for uncommited changes...')
    uncommited = capture_output(['git', 'status', '--porcelain=v1'])
    if len(uncommited) != 0:
        print('Uncommited changes found:')
        print('\n'.join(uncommited))
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
    old_version, new_version = capture_output(['hatch version micro'])
    print(f'Migrated: {old_version}->{new_version}')



if __name__ == '__main__':
    main()