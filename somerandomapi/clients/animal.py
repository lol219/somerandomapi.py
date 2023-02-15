from __future__ import annotations
from typing import TYPE_CHECKING, Tuple, Union

from ..internals.endpoints import Animal as AnimalEndpoint, Facts as AnimalFactsEndpoint, Img as AnimalImgEndpoint
from ..enums import FactAnimal as AnimalFactsEnum, Animal as AnimalEnum, ImgAnimal as AnimalImgEnum
from ..models.animal_fact import AnimalImageFact


if TYPE_CHECKING:
    from ..internals.http import HTTPClient

    from ..types.animal import Animals as AnimalsLiterals
    from ..types.facts import Animals as FactsAnimalsLiterals
    from ..types.img import Images as ImgAnimalsLiterals


__all__: Tuple[str, ...] = ("Animal",)


class Animal:
    """Represents the "Animal" endpoint.

    This class is not meant to be instantiated by the user. Instead, access it through the `animal` attribute of the `Client` class.
    """

    def __init__(self, http: HTTPClient) -> None:
        self.__http: HTTPClient = http

    async def get_image_and_fact(self, animal: Union[AnimalEnum, AnimalsLiterals]) -> AnimalImageFact:
        """Get a random animal.

        Parameters
        ----------
        animal: Union[:class:`Animal`, :class:`str`]
            The animal to get.

        Returns
        -------
        :class:`Animal`
            Object representing the requested animal. It has attributes such as ``image`` and ``link`` that can be accessed.
        """
        _animal: AnimalEnum = animal  # type: ignore
        if not isinstance(animal, AnimalEnum):
            valid_animals = list(map(str, list(AnimalEnum)))
            if animal not in valid_animals:
                raise ValueError(
                    f"'animal' must be an instance of `Animal` or one of {', '.join(valid_animals)}, not {animal!r}"
                )

            _animal = AnimalEnum(animal.upper())

        _endpoint: AnimalEndpoint = AnimalEndpoint._from_enum(_animal)  # type: ignore
        response = await self.__http.request(_endpoint)
        return AnimalImageFact(**response)

    async def get_image(self, animal: Union[AnimalImgEnum, ImgAnimalsLiterals]) -> str:
        """Get a random image of an animal.

        Parameters
        ----------
        animal: Union[:class:`ImgAnimal`, :class:`str`]
            The animal to get an image of.


        Returns
        -------
        :class:`str`
            The image URL.
        """
        _animal: AnimalImgEnum = animal  # type: ignore
        if not isinstance(animal, AnimalImgEnum):
            if not isinstance(animal, str):
                raise TypeError(f"'animal' must be either an instance of `ImgAnimal` or `str`, not {type(animal)}")

            valid_animals = list(map(str, list(AnimalImgEnum)))
            if animal not in valid_animals:
                raise ValueError(
                    f"'animal' must be an instance of `ImgAnimal` or one of {', '.join(valid_animals)}, not {animal!r}"
                )

            _animal = AnimalImgEnum(animal.upper())

        _endpoint: AnimalImgEndpoint = AnimalImgEndpoint._from_enum(_animal)  # type: ignore
        response = await self.__http.request(_endpoint)
        return response["link"]

    async def get_fact(self, animal: Union[AnimalFactsEnum, FactsAnimalsLiterals]) -> str:
        """Get a random fact about an animal.

        Parameters
        ----------
        animal: Union[:class:`FactAnimal`, :class:`str`]
            The animal to get a fact about.


        Returns
        -------
        :class:`str`
            The fact.
        """
        _animal: AnimalFactsEnum = animal  # type: ignore
        if not isinstance(animal, AnimalFactsEnum):
            if not isinstance(animal, str):
                raise TypeError(f"'animal' must be either an instance of `FactAnimal` or `str`, not {type(animal)}")

            valid_animals = list(map(str, list(AnimalFactsEnum)))
            if animal not in valid_animals:
                raise ValueError(
                    f"'animal' must be an instance of `FactAnimal` or one of {', '.join(valid_animals)}, not {animal!r}"
                )

            _animal = AnimalFactsEnum(animal.upper())

        _endpoint: AnimalFactsEndpoint = AnimalFactsEndpoint._from_enum(_animal)  # type: ignore
        response = await self.__http.request(_endpoint)
        return response["fact"]
