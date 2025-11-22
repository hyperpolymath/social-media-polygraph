from typing import Any, Dict, List, Optional
from datetime import datetime
import httpx
from loguru import logger

from app.core.config import settings


class XTDBClient:
    """Client for interacting with XTDB for temporal data storage."""

    def __init__(self) -> None:
        self.base_url = settings.xtdb_node_url
        self.client: Optional[httpx.AsyncClient] = None
        self._initialized = False

    async def connect(self) -> None:
        """Initialize XTDB client."""
        try:
            self.client = httpx.AsyncClient(
                base_url=self.base_url,
                timeout=30.0,
                headers={"Content-Type": "application/json"},
            )

            # Test connection
            response = await self.client.get("/status")
            response.raise_for_status()

            self._initialized = True
            logger.info("XTDB connection established successfully")

        except Exception as e:
            logger.error(f"Failed to connect to XTDB: {e}")
            raise

    async def put(self, doc: Dict[str, Any], valid_time: Optional[datetime] = None) -> Dict[str, Any]:
        """
        Put a document into XTDB.

        Args:
            doc: Document to store (must contain :xt/id key)
            valid_time: Optional valid time for the document

        Returns:
            Transaction result
        """
        if not self.client:
            raise RuntimeError("XTDB client not initialized")

        tx_ops = [["put", doc]]

        payload = {"tx-ops": tx_ops}
        if valid_time:
            payload["valid-time"] = valid_time.isoformat()

        response = await self.client.post("/_xtdb/submit-tx", json=payload)
        response.raise_for_status()
        return response.json()

    async def get(self, doc_id: str, valid_time: Optional[datetime] = None) -> Optional[Dict[str, Any]]:
        """
        Get a document by ID at a specific valid time.

        Args:
            doc_id: Document ID
            valid_time: Optional valid time to query

        Returns:
            Document or None if not found
        """
        if not self.client:
            raise RuntimeError("XTDB client not initialized")

        params = {"eid": doc_id}
        if valid_time:
            params["valid-time"] = valid_time.isoformat()

        response = await self.client.get("/_xtdb/entity", params=params)

        if response.status_code == 404:
            return None

        response.raise_for_status()
        return response.json()

    async def history(
        self,
        doc_id: str,
        with_docs: bool = True,
        start_valid_time: Optional[datetime] = None,
        end_valid_time: Optional[datetime] = None,
    ) -> List[Dict[str, Any]]:
        """
        Get the history of a document.

        Args:
            doc_id: Document ID
            with_docs: Include document content in results
            start_valid_time: Start of time range
            end_valid_time: End of time range

        Returns:
            List of historical versions
        """
        if not self.client:
            raise RuntimeError("XTDB client not initialized")

        params = {
            "eid": doc_id,
            "history": "true",
            "with-docs": str(with_docs).lower(),
        }

        if start_valid_time:
            params["start-valid-time"] = start_valid_time.isoformat()
        if end_valid_time:
            params["end-valid-time"] = end_valid_time.isoformat()

        response = await self.client.get("/_xtdb/entity", params=params)
        response.raise_for_status()
        return response.json()

    async def query(
        self,
        query: Dict[str, Any],
        valid_time: Optional[datetime] = None,
    ) -> List[List[Any]]:
        """
        Execute a datalog query.

        Args:
            query: Datalog query map
            valid_time: Optional valid time for the query

        Returns:
            Query results
        """
        if not self.client:
            raise RuntimeError("XTDB client not initialized")

        payload = query
        if valid_time:
            payload["valid-time"] = valid_time.isoformat()

        response = await self.client.post("/_xtdb/query", json=payload)
        response.raise_for_status()
        return response.json()

    async def await_tx(self, tx_id: int, timeout: int = 10000) -> Dict[str, Any]:
        """
        Wait for a transaction to be indexed.

        Args:
            tx_id: Transaction ID to wait for
            timeout: Timeout in milliseconds

        Returns:
            Transaction status
        """
        if not self.client:
            raise RuntimeError("XTDB client not initialized")

        params = {"tx-id": tx_id, "timeout": timeout}
        response = await self.client.get("/_xtdb/await-tx", params=params)
        response.raise_for_status()
        return response.json()

    async def put_claim_verification(
        self,
        claim_id: str,
        verification_data: Dict[str, Any],
        valid_time: Optional[datetime] = None,
    ) -> Dict[str, Any]:
        """
        Store a claim verification with temporal tracking.

        Args:
            claim_id: Unique claim identifier
            verification_data: Verification details
            valid_time: Time of verification

        Returns:
            Transaction result
        """
        doc = {
            ":xt/id": f"claim-verification/{claim_id}",
            "claim-id": claim_id,
            "verified-at": (valid_time or datetime.utcnow()).isoformat(),
            **verification_data,
        }

        return await self.put(doc, valid_time)

    async def get_claim_history(self, claim_id: str) -> List[Dict[str, Any]]:
        """
        Get the complete verification history of a claim.

        Args:
            claim_id: Claim identifier

        Returns:
            List of all verifications over time
        """
        doc_id = f"claim-verification/{claim_id}"
        return await self.history(doc_id, with_docs=True)

    async def disconnect(self) -> None:
        """Close XTDB client."""
        if self.client:
            await self.client.aclose()
            self._initialized = False
            logger.info("XTDB connection closed")

    @property
    def is_connected(self) -> bool:
        """Check if client is connected."""
        return self._initialized and self.client is not None


# Global instance
xtdb_client = XTDBClient()
