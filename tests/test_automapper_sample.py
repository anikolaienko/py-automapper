from automapper import mapper


class UserInfo:
    def __init__(self, name: str, age: int, profession: str):
        self.name = name
        self.age = age
        self.profession = profession


class PublicUserInfo:
    def __init__(self, name: str, profession: str):
        self.name = name
        self.profession = profession


class PublicUserInfoDiff:
    def __init__(self, full_name: str, profession: str):
        self.full_name = full_name
        self.profession = profession


def test_map__field_with_same_name():
    user_info = UserInfo("John Malkovich", 35, "engineer")
    public_user_info = mapper.to(PublicUserInfo).map(
        user_info, fields_mapping={"full_name": user_info.name}
    )

    assert public_user_info.name == "John Malkovich"
    assert public_user_info.profession == "engineer"


def test_map__field_with_different_name():
    user_info = UserInfo("John Malkovich", 35, "engineer")
    public_user_info: PublicUserInfoDiff = mapper.to(PublicUserInfoDiff).map(
        user_info, fields_mapping={"full_name": user_info.name}
    )

    assert public_user_info.full_name == "John Malkovich"
    assert public_user_info.profession == "engineer"


def test_map__field_with_different_name_register():
    try:
        mapper.add(
            UserInfo, PublicUserInfoDiff, fields_mapping={"full_name": "UserInfo.name"}
        )

        user_info = UserInfo("John Malkovich", 35, "engineer")
        public_user_info: PublicUserInfoDiff = mapper.map(user_info)

        assert public_user_info.full_name == "John Malkovich"
        assert public_user_info.profession == "engineer"
    finally:
        mapper._mappings.clear()


def test_map__override_field_value():
    try:
        user_info = UserInfo("John Malkovich", 35, "engineer")
        public_user_info = mapper.to(PublicUserInfo).map(
            user_info, fields_mapping={"name": "John Cusack"}
        )

        assert public_user_info.name == "John Cusack"
        assert public_user_info.profession == "engineer"
    finally:
        mapper._mappings.clear()


def test_map__override_field_value_register():
    try:
        mapper.add(UserInfo, PublicUserInfo, fields_mapping={"name": "John Cusack"})

        user_info = UserInfo("John Malkovich", 35, "engineer")
        public_user_info: PublicUserInfo = mapper.map(user_info)

        assert public_user_info.name == "John Cusack"
        assert public_user_info.profession == "engineer"
    finally:
        mapper._mappings.clear()
