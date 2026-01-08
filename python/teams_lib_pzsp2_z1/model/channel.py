from dataclasses import dataclass


@dataclass
class Channel:
    """Represents a Microsoft Teams channel.

    This model serves as a data container for channel properties returned
    by the underlying Go library.

    Attributes:
        id (str): The unique identifier of the channel.
        name (str): The display name of the channel (e.g., "General", "Development").
        is_general (bool): Indicates whether this is the default 'General' channel.
            The General channel typically cannot be deleted or renamed.
    """

    id: str
    name: str
    is_general: bool
