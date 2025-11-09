import requests
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class HTMLFetcher:
    """Handles fetching HTML content from web URLs."""
    
    DEFAULT_TIMEOUT = 15
    DEFAULT_HEADERS = {
        "User-Agent": "ascii-art-viewer/1.0 (Python requests)",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
    }

    @staticmethod
    def fetch(url: str, timeout: Optional[int] = None, headers: Optional[dict] = None) -> str:
        """
        Fetches HTML content from the specified URL.
        
        Args:
            url: The URL to fetch content from
            timeout: Request timeout in seconds (default: 15)
            headers: Optional custom headers (default: standard browser headers)
            
        Returns:
            The HTML content as a string
            
        Raises:
            requests.RequestException: If the request fails
        """
        if timeout is None:
            timeout = HTMLFetcher.DEFAULT_TIMEOUT
        
        if headers is None:
            headers = HTMLFetcher.DEFAULT_HEADERS.copy()
        
        logger.info(f"Fetching document from: {url}")
        
        try:
            response = requests.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()
            
            # Log successful fetch with some metadata
            content_length = len(response.text)
            content_type = response.headers.get('content-type', 'unknown')
            logger.info(f"Fetch successful. Content-Type: {content_type}, Size: {content_length} characters")
            
            return response.text
            
        except requests.exceptions.Timeout:
            logger.error(f"Request timed out after {timeout} seconds")
            raise
        except requests.exceptions.ConnectionError:
            logger.error(f"Failed to connect to {url}")
            raise
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error {e.response.status_code}: {e.response.reason}")
            raise
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {str(e)}")
            raise

    @staticmethod
    def validate_url(url: str) -> bool:
        """
        Validates if the URL appears to be a Google Docs published URL.
        
        Args:
            url: The URL to validate
            
        Returns:
            True if the URL appears valid for Google Docs, False otherwise
        """
        if not url:
            return False
            
        # Check if it's a Google Docs URL
        if "docs.google.com" not in url:
            logger.warning("URL does not appear to be a Google Docs URL")
            return False
        
        # Check if it's a published URL (should contain /pub)
        if "/pub" not in url:
            logger.warning("URL does not appear to be a published Google Docs URL (missing /pub)")
            return False
        
        return True