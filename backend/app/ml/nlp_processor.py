from typing import List, Dict, Any, Optional
import spacy
from spacy.language import Language
import hashlib
from textblob import TextBlob
from langdetect import detect, LangDetectException
from loguru import logger

from app.core.config import settings


class NLPProcessor:
    """Natural Language Processing for claim analysis."""

    def __init__(self) -> None:
        self.nlp: Optional[Language] = None
        self._initialized = False

    def initialize(self) -> None:
        """Load NLP models."""
        try:
            # Load spaCy model
            try:
                self.nlp = spacy.load(settings.spacy_model)
            except OSError:
                logger.warning(
                    f"spaCy model {settings.spacy_model} not found, using en_core_web_sm"
                )
                self.nlp = spacy.load("en_core_web_sm")

            self._initialized = True
            logger.info("NLP models loaded successfully")

        except Exception as e:
            logger.error(f"Failed to initialize NLP models: {e}")
            raise

    def extract_entities(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract named entities from text.

        Args:
            text: Input text

        Returns:
            List of entities with their types and positions
        """
        if not self._initialized or not self.nlp:
            raise RuntimeError("NLP processor not initialized")

        doc = self.nlp(text)

        entities = []
        for ent in doc.ents:
            entities.append({
                "text": ent.text,
                "label": ent.label_,
                "start": ent.start_char,
                "end": ent.end_char,
            })

        return entities

    def extract_claims(self, text: str) -> List[str]:
        """
        Extract individual claims from longer text.

        Args:
            text: Input text

        Returns:
            List of extracted claims
        """
        if not self._initialized or not self.nlp:
            raise RuntimeError("NLP processor not initialized")

        doc = self.nlp(text)

        # Extract sentences that contain factual claims
        claims = []
        for sent in doc.sents:
            # Simple heuristic: sentences with proper nouns, dates, or numbers
            # are more likely to contain verifiable claims
            has_proper_noun = any(token.pos_ == "PROPN" for token in sent)
            has_date = any(ent.label_ == "DATE" for ent in sent.ents)
            has_number = any(token.like_num for token in sent)

            if has_proper_noun or has_date or has_number:
                claims.append(sent.text.strip())

        return claims if claims else [text]

    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """
        Analyze sentiment of text.

        Args:
            text: Input text

        Returns:
            Sentiment scores and classification
        """
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity

        # Classify sentiment
        if polarity > 0.1:
            classification = "positive"
        elif polarity < -0.1:
            classification = "negative"
        else:
            classification = "neutral"

        return {
            "polarity": polarity,
            "subjectivity": subjectivity,
            "classification": classification,
        }

    def detect_language(self, text: str) -> Optional[str]:
        """
        Detect the language of text.

        Args:
            text: Input text

        Returns:
            ISO 639-1 language code or None
        """
        try:
            return detect(text)
        except LangDetectException:
            logger.warning(f"Could not detect language for text: {text[:50]}...")
            return None

    def compute_text_hash(self, text: str) -> str:
        """
        Compute hash of normalized text for deduplication.

        Args:
            text: Input text

        Returns:
            SHA256 hash of normalized text
        """
        # Normalize: lowercase, strip whitespace, remove extra spaces
        normalized = " ".join(text.lower().strip().split())
        return hashlib.sha256(normalized.encode()).hexdigest()

    def extract_keywords(self, text: str, top_n: int = 10) -> List[Dict[str, Any]]:
        """
        Extract keywords from text.

        Args:
            text: Input text
            top_n: Number of top keywords to return

        Returns:
            List of keywords with scores
        """
        if not self._initialized or not self.nlp:
            raise RuntimeError("NLP processor not initialized")

        doc = self.nlp(text)

        # Extract nouns and proper nouns
        keywords = {}
        for token in doc:
            if token.pos_ in ["NOUN", "PROPN"] and not token.is_stop:
                lemma = token.lemma_.lower()
                keywords[lemma] = keywords.get(lemma, 0) + 1

        # Sort by frequency
        sorted_keywords = sorted(
            keywords.items(), key=lambda x: x[1], reverse=True
        )[:top_n]

        return [{"keyword": kw, "frequency": freq} for kw, freq in sorted_keywords]

    def analyze_complexity(self, text: str) -> Dict[str, Any]:
        """
        Analyze text complexity metrics.

        Args:
            text: Input text

        Returns:
            Complexity metrics
        """
        if not self._initialized or not self.nlp:
            raise RuntimeError("NLP processor not initialized")

        doc = self.nlp(text)

        # Calculate various metrics
        num_sentences = len(list(doc.sents))
        num_words = len([token for token in doc if not token.is_punct])
        num_unique_words = len(set(token.text.lower() for token in doc if not token.is_punct))

        avg_word_length = sum(len(token.text) for token in doc) / len(doc) if len(doc) > 0 else 0
        avg_sentence_length = num_words / num_sentences if num_sentences > 0 else 0
        lexical_diversity = num_unique_words / num_words if num_words > 0 else 0

        return {
            "num_sentences": num_sentences,
            "num_words": num_words,
            "num_unique_words": num_unique_words,
            "avg_word_length": round(avg_word_length, 2),
            "avg_sentence_length": round(avg_sentence_length, 2),
            "lexical_diversity": round(lexical_diversity, 3),
        }

    @property
    def is_initialized(self) -> bool:
        """Check if processor is initialized."""
        return self._initialized


# Global instance
nlp_processor = NLPProcessor()
