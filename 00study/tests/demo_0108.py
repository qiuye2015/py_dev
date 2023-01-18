from datetime import date
import pydantic
from pydantic import BaseModel, Field, Extra, constr, validator

print('compiled:', pydantic.compiled)


class Person(BaseModel):
    first_name: str = Field(alias='firstName', default=None)
    last_name: str = Field(alias='lastName')
    dob: date = None

    class Config:
        allow_population_by_field_name = True  # 是否可以根据model属性给定的名称以及别名填充别名字段（默认值：False）
        extra = Extra.allow  # extra=Extra.forbid 是否允许额外字段填充model


p = Person(first_name='Isaac', lastName='Newton')
print(p)
print(p.json(by_alias=True, indent=2))
print(p.dict(by_alias=True))


def snake_to_camel_case(value: str) -> str:
    if not isinstance(value, str):
        raise ValueError("Value must be a string.")
    words = value.split('_')
    value = "".join(word.title() for word in words if word)
    return f"{value[0].lower()}{value[1:]}"


print(snake_to_camel_case("__first_name"))


class CustomBaseModel(BaseModel):
    class Config:
        alias_generator = snake_to_camel_case
        extra = Extra.forbid  # 是否允许额外字段填充model
        allow_population_by_field_name = True  # 是否可以根据model属性给定的名称以及别名填充别名字段（默认值：False）


class Person(CustomBaseModel):
    first_name: str = None
    last_name: str
    dob: date = None


p = Person(first_name='Isaac', lastName='Newton')
print(p)


class Author(CustomBaseModel):
    first_name: constr(min_length=1, max_length=20, strip_whitespace=True)
    last_name: constr(min_length=1, max_length=20, strip_whitespace=True)
    display_name: constr(min_length=1, max_length=25) = None

    # always = True forces the validator to run, even if display_name is None, this
    # is how we can set a dynamic default value
    @validator("display_name", always=True)
    def validate_display_name(cls, value, values):
        # validator runs, even if previous fields did not validate properly - so
        # we will need to run our code only if prior fields validated OK.
        if not value and 'first_name' in values and 'last_name' in values:
            first_name = values['first_name']
            last_name = values['last_name']
            return f"{first_name} {(last_name[0]).upper()}"
        return value


print(Author(first_name="Gottfried", last_name="Leibniz"))

import tracemalloc

tracemalloc.start()
# ...
snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics("filename")
for stat in top_stats[:10]: print(stat)
