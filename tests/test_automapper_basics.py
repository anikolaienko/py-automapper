from dataclasses import dataclass

from automapper import mapper


class BasicUser:
    def __init__(self, name: str, city: str):
        self.name = name
        self.city = city

    def __repr__(self):
        return f"BasicUser(name={self.name}, city={self.city})"


class AdvancedUser:
    def __init__(self, user: BasicUser, job: str, salary: int):
        self.user = user
        self.job = job
        self.salary = salary


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


@dataclass
class Address:
    street: str
    number: int
    zip_code: int
    city: str


class PersonInfo:
    def __init__(self, name: str, age: int, address: Address):
        self.name = name
        self.age = age
        self.address = address


class PublicPersonInfo:
    def __init__(self, name: str, address: Address):
        self.name = name
        self.address = address


def test_map__field_with_same_name():
    user_info = UserInfo("John Malkovich", 35, "engineer")
    public_user_info = mapper.to(PublicUserInfo).map(
        user_info, fields_mapping={"full_name": user_info.name}
    )

    assert public_user_info.name == "John Malkovich"
    assert public_user_info.profession == "engineer"


def test_map__chained_attributes():
    try:
        mapper.add(
            AdvancedUser,
            BasicUser,
            fields_mapping={
                "name": "AdvancedUser.user.name",
                "city": "AdvancedUser.user.city",
            },
        )

        user = BasicUser(name="John Malkovich", city="USA")
        advanced_user = AdvancedUser(user=user, job="Engineer", salary=100)

        mapped_basic_user: BasicUser = mapper.map(advanced_user)

        assert mapped_basic_user.name == advanced_user.user.name
        assert mapped_basic_user.city == advanced_user.user.city
    finally:
        mapper._mappings.clear()


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


def test_map__check_deepcopy_not_applied_if_use_deepcopy_false():
    address = Address(street="Main Street", number=1, zip_code=100001, city="Test City")
    info = PersonInfo("John Doe", age=35, address=address)

    public_info = mapper.to(PublicPersonInfo).map(info)
    assert address is not public_info.address

    public_info = mapper.to(PublicPersonInfo).map(info, use_deepcopy=False)
    assert address is public_info.address
