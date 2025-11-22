from typing import Optional
from arango import ArangoClient
from arango.database import StandardDatabase
from arango.collection import StandardCollection
from loguru import logger

from app.core.config import settings


class ArangoDBManager:
    """Manager for ArangoDB connections and operations."""

    def __init__(self) -> None:
        self.client: Optional[ArangoClient] = None
        self.db: Optional[StandardDatabase] = None
        self._initialized = False

    async def connect(self) -> None:
        """Establish connection to ArangoDB and initialize database."""
        try:
            self.client = ArangoClient(hosts=settings.arango_url)

            # Connect to system database first
            sys_db = self.client.db(
                "_system",
                username=settings.arango_user,
                password=settings.arango_password,
            )

            # Create database if it doesn't exist
            if not sys_db.has_database(settings.arango_database):
                sys_db.create_database(settings.arango_database)
                logger.info(f"Created database: {settings.arango_database}")

            # Connect to application database
            self.db = self.client.db(
                settings.arango_database,
                username=settings.arango_user,
                password=settings.arango_password,
            )

            # Initialize collections
            await self._initialize_collections()

            self._initialized = True
            logger.info("ArangoDB connection established successfully")

        except Exception as e:
            logger.error(f"Failed to connect to ArangoDB: {e}")
            raise

    async def _initialize_collections(self) -> None:
        """Create necessary collections and indices."""
        if not self.db:
            raise RuntimeError("Database not connected")

        collections_config = {
            # Document collections
            "claims": {"type": "document", "indices": ["url", "text_hash", "created_at"]},
            "sources": {"type": "document", "indices": ["domain", "credibility_score"]},
            "fact_checks": {"type": "document", "indices": ["claim_id", "verdict", "checked_at"]},
            "users": {"type": "document", "indices": ["email", "username"]},
            "api_keys": {"type": "document", "indices": ["key_hash", "user_id"]},

            # Edge collections (for graph relationships)
            "claim_sources": {"type": "edge"},
            "claim_entities": {"type": "edge"},
            "source_relationships": {"type": "edge"},
        }

        for coll_name, config in collections_config.items():
            if not self.db.has_collection(coll_name):
                is_edge = config["type"] == "edge"
                collection = self.db.create_collection(coll_name, edge=is_edge)
                logger.info(f"Created collection: {coll_name}")

                # Create indices for document collections
                if not is_edge and "indices" in config:
                    for field in config["indices"]:
                        collection.add_hash_index(fields=[field], unique=False)
                        logger.debug(f"Created index on {coll_name}.{field}")

        # Create graph if it doesn't exist
        if not self.db.has_graph("knowledge_graph"):
            self.db.create_graph(
                "knowledge_graph",
                edge_definitions=[
                    {
                        "edge_collection": "claim_sources",
                        "from_vertex_collections": ["claims"],
                        "to_vertex_collections": ["sources"],
                    },
                    {
                        "edge_collection": "claim_entities",
                        "from_vertex_collections": ["claims"],
                        "to_vertex_collections": ["sources"],  # entities stored as sources
                    },
                    {
                        "edge_collection": "source_relationships",
                        "from_vertex_collections": ["sources"],
                        "to_vertex_collections": ["sources"],
                    },
                ],
            )
            logger.info("Created knowledge graph")

    def get_collection(self, name: str) -> StandardCollection:
        """Get a collection by name."""
        if not self.db:
            raise RuntimeError("Database not connected")
        return self.db.collection(name)

    async def disconnect(self) -> None:
        """Close ArangoDB connection."""
        if self.client:
            self.client.close()
            self._initialized = False
            logger.info("ArangoDB connection closed")

    @property
    def is_connected(self) -> bool:
        """Check if database is connected."""
        return self._initialized and self.db is not None


# Global instance
arango_manager = ArangoDBManager()
