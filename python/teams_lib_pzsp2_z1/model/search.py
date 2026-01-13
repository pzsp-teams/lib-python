from dataclasses import dataclass
from enum import Enum

from teams_lib_pzsp2_z1.model.message import Message


@dataclass
class SearchConfig:
    """
    Configuration parameters for search operations.

    Attributes:
        max_workers (int): The maximum number of worker threads to use for concurrent search operations. Defaults to 8.
    """

    max_workers: int = 8

    def __dict__(self):
        """Serializes the object keys to camelCase for the Go backend."""
        return {"maxWorkers": self.max_workers}


@dataclass
class SearchPage:
    """
    Represents pagination parameters for search results.

    Attributes:
        from_ (int): The starting index of the search results.
        size (int): The number of search results to return. Defaults to 25.
    """

    from_: int = 0
    size: int = 25

    def __dict__(self):
        """Serializes the object keys to camelCase for the Go backend."""
        return {"from": self.from_, "size": self.size}


class TimeInterval(Enum):
    """Enumeration of time intervals for filtering search results.

    Attributes:
        TODAY: Represents the current day.
        YESTERDAY: Represents the previous day.
        THIS_WEEK: Represents the current week.
        THIS_MONTH: Represents the current month.
        LAST_MONTH: Represents the previous month.
        THIS_YEAR: Represents the current year.
        LAST_YEAR: Represents the previous year.
    """

    TODAY = "today"
    YESTERDAY = "yesterday"
    THIS_WEEK = "this week"
    THIS_MONTH = "this month"
    LAST_MONTH = "last month"
    THIS_YEAR = "this year"
    LAST_YEAR = "last year"


@dataclass
class SearchMessagesOptions:
    """
    Configuration options for searching messages.

    Attributes:
        query (str | None): The search query string.
        search_page (SearchPage | None): Pagination options.
        from_ (list[str]): List of sender email addresses to include.
        not_from (list[str]): List of sender email addresses to exclude.
        is_read (bool | None): Filter by read status (True for read, False for unread).
        is_mentioned (bool | None): Filter by mention status (True for mentioned, False for not mentioned).
        to (list[str]): List of recipient email addresses to include.
        not_to (list[str]): List of recipient email addresses to exclude.
        start_time (datetime | None): Start time for the sent time range filter.
        end_time (datetime | None): End time for the sent time range filter.
        interval (TimeInterval | None): Predefined time interval for the sent time filter.
        not_from_me (bool): Exclude messages sent by the current user.
        not_to_me (bool): Exclude messages sent to the current user.
        from_me (bool): Include only messages sent by the current user.
        to_me (bool): Include only messages sent to the current user.

    Note: If interval is set, it takes precedence over start_time and end_time.
    Note: Using `to` clauses works only in chats, not in team channels.
    Note: Currently, queries for is_read may not function as expected due to API limitations.
    """

    query: str | None = None
    search_page: SearchPage | None = None
    from_: list[str] = None
    not_from: list[str] = None
    is_read: bool | None = None
    is_mentioned: bool | None = None
    to: list[str] = None
    not_to: list[str] = None
    start_time: object = None
    end_time: object = None
    interval: TimeInterval | None = None
    not_from_me: bool = False
    not_to_me: bool = False
    from_me: bool = False
    to_me: bool = False

    def __post_init__(self):
        if self.from_ is None:
            self.from_ = []
        if self.not_from is None:
            self.not_from = []
        if self.to is None:
            self.to = []
        if self.not_to is None:
            self.not_to = []

    def __dict__(self):
        """Serializes the object keys to camelCase for the Go backend."""

        result = {
            "query": self.query,
            "searchPage": self.search_page,
            "from": self.from_,
            "notFrom": self.not_from,
            "isRead": self.is_read,
            "isMentioned": self.is_mentioned,
            "to": self.to,
            "notTo": self.not_to,
            "startTime": self.start_time,
            "endTime": self.end_time,
            "interval": self.interval.value if self.interval else None,
            "notFromMe": self.not_from_me,
            "notToMe": self.not_to_me,
            "fromMe": self.from_me,
            "toMe": self.to_me,
        }
        return {k: v for k, v in result.items() if v is not None and v != []}


@dataclass
class SearchResult:
    """
    SearchResult represents a single search result containing a message and its context.

    Attributes:
        message (Message): The message that matched the search criteria.
        channel_id (str | None): The ID of the channel where the message was found (if applicable).
        team_id (str | None): The ID of the team where the message was found (if applicable).
        chat_id (str | None): The ID of the chat where the message was found (if applicable).
    """

    message: Message
    channel_id: str | None = None
    team_id: str | None = None
    chat_id: str | None = None


@dataclass
class SearchResults:
    """
    SearchResults represents the results of a message search.

    Attributes:
        messages (list[SearchResult]): A list of search results.
        next_from (int | None): The index to use for the next page of results,
            or None if there are no more results.
    """

    messages: list[SearchResult]
    next_from: int | None = None
