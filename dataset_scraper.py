import json
from dataclasses import dataclass, InitVar
from pathlib import Path
from pprint import pprint
from typing import List, Dict

from piazza_api import Piazza
from piazza_api.network import Network
import os


@dataclass
class PostDC:
    id: str
    created: str
    unique_views: int
    folders: List[str]
    type: str
    change_log: List[Dict]
    history: List[Dict]

    def __post_init__(self):
        assert self.change_log[0]['type'] == "create"
        self.anon: str = self.change_log[0]['anon']
        self.subject: str = self.history[0]['subject']


@dataclass
class NetworkDC:
    _root: InitVar[Piazza]

    id: str
    course_number: str
    name: str
    topics: List[str]
    user_count: int

    def __post_init__(self, _root):
        self.api: Network = _root.network(self.id)


def get_dataset(_root: Piazza) -> Dict:
    networks = [NetworkDC(_root, **_clean_data(i, NetworkDC)) for i in _root.get_user_status()["networks"]]
    data = {
        i.id: {
            "name"         : i.name,
            "course_number": i.course_number,
            "topics"       : i.topics,
            "user_count"   : i.user_count,
            "posts"        : [
                {
                    "id"     : b.id,
                    "created": b.created,
                    "type"   : b.type,
                    "anon"   : b.anon,
                    "subject": b.subject,
                    "folders": b.folders,
                    "views"  : b.unique_views,
                } for b in get_posts(i)
            ]
        } for i in networks
    }
    return data


def get_posts(network: NetworkDC) -> List[PostDC]:
    a = []
    for i in network.api.iter_all_posts():
        post = PostDC(**_clean_data(i, PostDC))
        print(post.subject)
        a.append(post)
    return a


def _clean_data(data: Dict, _dataclass) -> Dict:
    valid_ids = filter(lambda key: key in _dataclass.__dataclass_fields__.keys(), data)
    return {i: data[i] for i in valid_ids}


def save_data(data, path: Path):
    with path.open("w") as fp:
        json.dump(data, fp)


if __name__ == "__main__":
    root = Piazza()
    root.user_login(os.environ["PIAZZA-EMAIL"], os.environ["PIAZZA-PASSWORD"])
    data = get_dataset(root)
    save_data(data, Path("dataset.json"))
