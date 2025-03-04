import abc
from typing import Iterator

from connectors.node_names import NodeName
from database.model.publication import OrmPublication


class PublicationConnector(abc.ABC):
    """For every node that offers publications, this PublicationConnector should be implemented."""

    @property
    def node_name(self) -> NodeName:
        """The node of this connector"""
        return NodeName.from_class(self.__class__)

    @abc.abstractmethod
    def fetch_all(self, limit: int | None) -> Iterator[OrmPublication]:
        """Retrieve all publications"""
        pass
