from typing import Optional

from automapper import mapper
from pydantic import BaseModel


class Address(BaseModel):
    street: Optional[str]
    number: Optional[int]
    zip_code: Optional[int]
    city: Optional[str]


class PersonInfo(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    address: Optional[Address] = None


class PublicPersonInfo(BaseModel):
    name: Optional[str] = None
    address: Optional[Address] = None


def test_map__without_deepcopy_mapped_objects_should_be_the_same():
    address = Address(street="Main Street", number=1, zip_code=100001, city="Test City")
    info = PersonInfo(name="John Doe", age=35, address=address)

    # default deepcopy behavior
    public_info = mapper.to(PublicPersonInfo).map(info)
    assert (
        public_info.address is not address
    ), "Address mapped object is same as origin."

    # disable deepcopy
    public_info = mapper.to(PublicPersonInfo).map(info, use_deepcopy=False)
    assert (
        public_info.address is info.address
    ), "Address mapped object is not same as origin."
