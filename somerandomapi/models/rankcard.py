from __future__ import annotations
from typing import TYPE_CHECKING, Tuple, Optional

from dataclasses import dataclass, field

from ..internals.endpoints import Premium
from .abc import BaseModel
from .. import utils as _utils

if TYPE_CHECKING:
    from ..models.image import Image

__all__: Tuple[str, ...] = ("Rankcard",)


@dataclass
class Rankcard(BaseModel):
    """Represents a rank card."""

    _endpoint = Premium.RANK_CARD

    _image: Image = field(init=False)

    username: str = field(metadata={"max_length": 32})
    """The username of the user. Max 32 characters."""
    avatar_url: str = field(metadata={"alias_of": "avatar"})
    """The avatar URL of the user. Must be .png or .jpg."""
    discriminator: int
    """The discriminator of the user."""
    level: int
    """The current level of the user."""
    current_xp: int = field(metadata={"alias_of": "cxp"})
    """The current XP of the user."""
    needed_xp: int = field(metadata={"alias_of": "nxp"})
    """The needed XP to level up."""
    key: Optional[str] = None
    """The API key for the rank card. Not required if you have a key set in the client."""
    background_url: Optional[str] = field(default=None, metadata={"alias_of": "bg"})
    """The custom background of the rank card as url. Tier 2+ key required.
    
    This cannot be used with background_color.
    """
    background_color: Optional[str] = field(default=None, metadata={"alias_of": "cbg"})
    """The custom background color of the rank card. Tier 1+ key required.

    Can put "random" to get a random color.
    
    This cannot be used with background.
    """
    text_color: Optional[str] = field(default=None, metadata={"alias_of": "ctext"})
    """The custom text color of the rank card as hex.
    
    Can put "random" to get a random color.
    """
    current_xp_color: Optional[str] = field(default=None, metadata={"alias_of": "ccxp"})
    """The color of the current XP as hex.

    Can put "random" to get a random color.
    """
    xp_bar_color: Optional[str] = field(default=None, metadata={"alias_of": "cbar"})
    """The color of the XP bar as hex.

    Can put "random" to get a random color.
    """

    if TYPE_CHECKING:

        @classmethod
        def from_dict(
            cls,
            *,
            username: str,
            avatar: str,
            discriminator: int,
            level: int,
            cxp: int,
            nxp: int,
            key: Optional[str] = None,
            bg: Optional[str] = None,
            cbg: Optional[str] = None,
            ctext: Optional[str] = None,
            ccxp: Optional[str] = None,
            cbar: Optional[str] = None,
        ):
            ...

    def __post_init__(self) -> None:
        super().__post_init__()

        COLOR_ERROR = (
            "Invalid {0} color. Must be a valid hex color or 'random'. Valid formats: '#000000', 0x000000, 000000"
        )
        if self.background_color is not None:
            if not (
                color := _utils._check_colour_value(self.background_color, random=self.background_color == "random")
            ):
                raise ValueError(COLOR_ERROR.format("background"))
            self.background_color = color
        if self.text_color is not None:
            if not (color := _utils._check_colour_value(self.text_color, random=self.text_color == "random")):
                raise ValueError(COLOR_ERROR.format("text"))
            self.text_color = color
        if self.current_xp_color is not None:
            if not (
                color := _utils._check_colour_value(self.current_xp_color, random=self.current_xp_color == "random")
            ):
                raise ValueError(COLOR_ERROR.format("current xp"))
            self.current_xp_color = color
        if self.xp_bar_color is not None:
            if not (color := _utils._check_colour_value(self.xp_bar_color, random=self.xp_bar_color == "random")):
                raise ValueError(COLOR_ERROR.format("xp bar"))
            self.bar_color = color

    @property
    def image(self) -> Image:
        """The image of the tweet.

        Returns
        -------
        :class:`Image`
            The image of the tweet.
        """
        return self._image
