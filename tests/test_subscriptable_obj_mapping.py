from automapper import mapper

class PublicUserInfo(object):
    def __init__(self, name: str, profession: str):
        self.name = name
        self.profession = profession


def test_map__dict_to_object():
    original = {
        "name": "John Carter",
        "age": 35,
        "profession": "hero"
    }
    
    public_info = mapper.to(PublicUserInfo).map(original)

    assert hasattr(public_info, "name") and public_info.name == "John Carter"
    assert hasattr(public_info, "profession") and public_info.profession == "hero"
    assert not hasattr(public_info, "age")
