#!/usr/bin/env python

import os
import subprocess
import socket
import sys
import json
import urllib2
import collections

SanityCheckResult = collections.namedtuple(
    'SanityCheckResult', ['is_ok', 'message']
)


def check_port(host, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(.1)
        s.connect((host, port))
        s.shutdown(socket.SHUT_RDWR)
        return True
    except socket.error:
        return False


def check_command(command):
    try:
        devnull = open(os.devnull, 'w')
        subprocess.check_call(
            command, shell=True, stdout=devnull, stderr=subprocess.STDOUT
        )
        return True
    except subprocess.CalledProcessError:
        return False


def get_free_percentage_on_mount(mount):
    stats = os.statvfs(mount)
    return stats.f_bavail / float(stats.f_blocks) * 100


def test_free_space_on_mount(mount, free_percentage_required):
    free_percentage = get_free_percentage_on_mount(mount)
    if free_percentage_required > free_percentage:
        message = "Not enough free space on {mount}. Free space is {percentage:.1f}%".format(
            mount=mount,
            percentage=free_percentage
        )
        return SanityCheckResult(False, message)
    message = "Enough free space {mount}. Free space is {percentage:.1f}%".format(
        mount=mount,
        percentage=free_percentage
    )
    return SanityCheckResult(True, message)


def send_message(recipient, subject, body):
    """
    While sending mail is not reliable, mail delivery is async, and mail always
    exits successfully.
    """
    process = subprocess.Popen(['mail', '-s', subject, recipient], stdin=subprocess.PIPE)
    process.communicate(body)


def test_global_free_percentage(default_free_space_percentage):
    # TODO: it would be very good to add test for this one
    response = []
    with open("/proc/mounts") as f:
        proc_mounts = f.read().strip()
    for line in proc_mounts.split("\n"):
        parts = line.split()
        device = parts[0]
        mount = parts[1]
        if device.startswith("/dev"):
            response.append(
                test_free_space_on_mount(mount, default_free_space_percentage))
    return response


def test_ports(ports):
    response = []
    for port in ports:
        if not check_port(port['host'], int(port['port'])):
            response.append(SanityCheckResult(False, port['message']))
        else:
            message = "Port {}:{} is getting connections".format(port['host'], int(port['port']))
            response.append(SanityCheckResult(True, message))
    return response


def test_commands(commands):
    response = []
    for command in commands:
        if not check_command(command['command']):
            response.append(SanityCheckResult(False, command['message']))
        else:
            message = format("Command {} returned exit status 0".format(
                command['command']
            ))
            response.append(SanityCheckResult(True, message))
    return response


def report_is_ok(report):
    return all(check.is_ok for check in report)


def format_report(report):
    lines = []
    report = sorted(report, key= lambda check: check.is_ok)
    for check in report:
        status = "OK" if check.is_ok else "ERROR"
        lines.append("#. {status} {message}".format(status=status, message=check.message))
    return "\n".join(lines)


def sanity_check(json_data):
    report = []
    report.extend(
        test_global_free_percentage(float(json_data['free_percentage']))
    )
    report.extend(
        test_ports(json_data['ports'])
    )
    report.extend(
        test_commands(json_data['commands'])
    )

    if report_is_ok(report):
        if 'snitch' in json_data and json_data['snitch']:
            if not check_heartbeat_url(json_data['snitch']):
                report.append(SanityCheckResult(False, "Couldn't send snitch"))

    if not report_is_ok(report):
        report_text = format_report(report)
        send_message(json_data['send_report_to'], json_data['subject'], report_text)

    with open(json_data['report_file'], 'w') as f:
        report_text = format_report(report)
        f.write(report_text)


def check_heartbeat_url(url):
    try:
        response = urllib2.urlopen(url, timeout=1)
        code = response.getcode()
        return 200 <= code < 300
    except (urllib2.URLError, urllib2.HTTPError) as e:
        return False


if __name__ == "__main__":
    data_file = sys.argv[1]
    with open(data_file, 'r') as f:
        json_data = json.load(f)
    sanity_check(json_data)
