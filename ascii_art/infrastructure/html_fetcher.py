import requests
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class HTMLFetcher:
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
        if timeout is None:
            timeout = HTMLFetcher.DEFAULT_TIMEOUT
        
        if headers is None:
            headers = HTMLFetcher.DEFAULT_HEADERS.copy()
        
        logger.info(f"Fetching document from: {url}")
        
        try:
            response = requests.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()
            
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
        if not url:
            return False
            
        if "docs.google.com" not in url:
            logger.warning("URL does not appear to be a Google Docs URL")
            return False
        
        if "/pub" not in url:
            logger.warning("URL does not appear to be a published Google Docs URL (missing /pub)")
            return False
        
        return True