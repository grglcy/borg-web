from borgclient import BorgClient
from sys import stdin
import argparse
from tables import Error, Repo, Archive, Cache
import json
from datetime import datetime


def main(args):
    borg_output = " ".join(stdin.readlines())
    if not (args.label and args.username and args.password and args.url):
        raise Exception("Supply label, username, password and url")
    else:
        client = BorgClient(url=args.url, username=args.username, password=args.password)
        try:
            borg_json = json.loads(borg_output)
            repo = Repo.from_json(borg_json['repository'])
            archive = Archive.from_json(borg_json['archive'])
            cache = Cache.from_json(borg_json['cache']['stats'])

            client.post_repo(repo.get_dict(args.label))
            archive_cache = archive.get_dict(args.label)
            archive_cache.update(cache.get_dict(args.label))
            client.post_archive_and_cache(archive_cache)
        except json.JSONDecodeError:
            error = Error(borg_output, datetime.utcnow())
            client.post_error(error.get_dict(args.label))


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--label", help="Repo Label", type=str, required=True)
    parser.add_argument("-u", "--username", help="Username", type=str, required=True)
    parser.add_argument("-p", "--password", help="Password", type=str, required=True)
    parser.add_argument("-w", "--url", help="Server Url", type=str, required=True)
    return parser.parse_args()


if __name__ == "__main__":
    main(get_args())
