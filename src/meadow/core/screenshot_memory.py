"""Module for comparing screenshots"""

from typing import Any, Dict, Optional
from meadow.core.topic_similarity import get_similarity_score

class ScreenshotMemory:
    """Stores information about the previous screenshot for comparison"""
    def __init__(self):
        # Core metadata
        self.app: Optional[str] = None
        self.title: Optional[str] = None
        self.url: Optional[str] = None
        self.ocr_text: Optional[str] = None
        self.last_timestamp: Optional[str] = None

        # Configurable thresholds
        self._text_similarity_threshold = 0.85  # Increased from 0.6 for stricter matching
        self._min_text_length = 50  # Minimum text length to consider for comparison
        self._max_time_threshold = 300  # Maximum seconds between screenshots to consider as duplicate (5 minutes)

        print("[DEBUG] ScreenshotMemory initialized with similarity threshold:", self._text_similarity_threshold)

    async def matches_current(self, window_info: Dict[str, Any], ocr_text: str, timestamp: str) -> bool:
        """
        Check if current screenshot is similar enough to previous to be considered a duplicate.

        Args:
            window_info: Dictionary containing app, title, and optional url
            ocr_text: Extracted text from the current screenshot
            timestamp: Current timestamp string

        Returns:
            bool: True if current screenshot is considered a duplicate
        """
        if not self.app:  # No previous screenshot
            print("[DEBUG] ScreenshotMemory: No previous screenshot stored")
            return False

        # 1. Check if we're within the time threshold
        time_diff = self._get_time_diff_seconds(self.last_timestamp, timestamp)
        if time_diff > self._max_time_threshold:
            print(f"[DEBUG] ScreenshotMemory: Time difference ({time_diff}s) exceeds threshold")
            return False

        # 2. Check basic metadata matches
        metadata_match = (
            self.app == window_info['app'] and
            self.title == window_info['title'] and
            self.url == window_info.get('url')
        )

        if not metadata_match:
            print("[DEBUG] ScreenshotMemory: Metadata mismatch")
            print(f"[DEBUG] Previous: app={self.app}, title={self.title}, url={self.url}")
            print(f"[DEBUG] Current: app={window_info['app']}, title={window_info['title']}, url={window_info.get('url')}")
            return False

        # 3. Check if we have enough text for meaningful comparison
        if not self.ocr_text or not ocr_text or \
           len(self.ocr_text) < self._min_text_length or \
           len(ocr_text) < self._min_text_length:
            print("[DEBUG] ScreenshotMemory: Insufficient text for comparison")
            print(f"[DEBUG] Previous text length: {len(self.ocr_text) if self.ocr_text else 0}")
            print(f"[DEBUG] Current text length: {len(ocr_text)}")
            return False

        # 4. Check text similarity using topic_similarity's functionality
        try:
            similarity = await get_similarity_score(
                ocr_text,
                [self.ocr_text],  # Pass previous text as a "topic" to compare against
                chunk_threshold=self._text_similarity_threshold,
                min_chunks=1  # Only need one chunk to match since we're comparing same content
            )

            print(f"[DEBUG] ScreenshotMemory: Text similarity score: {similarity}")

            # Calculate length difference ratio
            len_ratio = min(len(ocr_text), len(self.ocr_text)) / max(len(ocr_text), len(self.ocr_text))
            print(f"[DEBUG] ScreenshotMemory: Length ratio: {len_ratio:.2f}")

            # Consider it a match if both similarity and length ratio are high
            is_duplicate = similarity >= self._text_similarity_threshold and len_ratio > 0.8

            if is_duplicate:
                print("[DEBUG] ScreenshotMemory: Detected duplicate screenshot")

            return is_duplicate

        except Exception as e:
            print(f"[DEBUG] ScreenshotMemory: Error during similarity comparison: {e}")
            return False

    def update(self, window_info: Dict[str, Any], ocr_text: str, timestamp: str) -> None:
        """
        Update memory with current screenshot info.

        Args:
            window_info: Dictionary containing app, title, and optional url
            ocr_text: Extracted text from the current screenshot
            timestamp: Current timestamp string
        """
        print("[DEBUG] ScreenshotMemory: Updating state")
        print(f"[DEBUG] Previous state: app={self.app}, title={self.title}, url={self.url}")
        print(f"[DEBUG] New state: app={window_info['app']}, title={window_info['title']}, url={window_info.get('url')}")

        self.app = window_info['app']
        self.title = window_info['title']
        self.url = window_info.get('url')
        self.ocr_text = ocr_text
        self.last_timestamp = timestamp

    def _get_time_diff_seconds(self, timestamp1: Optional[str], timestamp2: str) -> float:
        """Calculate time difference in seconds between two timestamps"""
        if not timestamp1:
            return float('inf')

        from datetime import datetime
        time1 = datetime.strptime(timestamp1, '%Y-%m-%d %H:%M:%S')
        time2 = datetime.strptime(timestamp2, '%Y-%m-%d %H:%M:%S')
        return abs((time2 - time1).total_seconds())