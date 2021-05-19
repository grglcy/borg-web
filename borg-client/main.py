from borgclient import BorgClient
from sys import stdin
import argparse
from tables import Error, Repo, Archive, Cache
import json
from datetime import datetime
import urllib3


def main(args):
    borg_json, errors = get_json_and_errors(stdin.readlines())
    if not (args.label and args.username and args.password and args.url):
        raise Exception("Supply label, username, password and url")
    else:
        client = BorgClient(url=args.url, username=args.username, password=args.password)

        current_time = datetime.utcnow()
        for error in errors:
            error = Error(error, current_time)
            client.post_error(error.get_dict(args.label))

        if borg_json is not None:
            repo = Repo.from_json(borg_json['repository'])
            archive = Archive.from_json(borg_json['archive'])
            cache = Cache.from_json(borg_json['cache']['stats'])

            client.post_repo(repo.get_dict(args.label))
            archive_cache = archive.get_dict(args.label)
            archive_cache.update(cache.get_dict(args.label))
            client.post_archive_and_cache(archive_cache)


def get_json_and_errors(borg_output: list):
    errors = []
    borg_json = None
    for index in range(len(borg_output)):
        truncated_output = borg_output[index:]
        try:
            borg_json = json.loads(" ".join(truncated_output))
            break
        except json.JSONDecodeError:
            errors.append(truncated_output[0].strip())

    return borg_json, errors


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--label", help="Repo Label", type=str, required=True)
    parser.add_argument("-u", "--username", help="Username", type=str, required=True)
    parser.add_argument("-p", "--password", help="Password", type=str, required=True)
    parser.add_argument("-w", "--url", help="Server Url", type=str, required=True)
    return parser.parse_args()


if __name__ == "__main__":
    urllib3.disable_warnings()
    main(get_args())
