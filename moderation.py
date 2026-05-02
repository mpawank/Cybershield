"""
CyberShield AI - Multilingual Content Moderation System
Detects harmful or unsafe language with contextual understanding
"""

import re
import json
from typing import Dict, Any
import langdetect
from langdetect import detect, DetectorFactory

# Set seed for consistent language detection
DetectorFactory.seed = 0

# Multilingual offensive terms dictionary
OFFENSIVE_PATTERNS = {
    'Hindi': {
        'abusive': [
            r'\bpagal\b', r'\bbekar\b', r'\bchutiya\b', r'\bbhosdi\b',
            r'\bmadarc*od\b', r'\bsala\b', r'\bbeghairat\b', r'\bharamzada\b',
            r'\bmurkh\b', r'\bbudhu\b', r'\bnakara\b', r'\basli\b'
        ],
        'threat': [
            r'\bmar\s*dal\b', r'\bmarunga\b', r'\bmar*u*ngi\b',
            r'\bpitai\b', r'\btorunga\b'
        ],
        'sexual': [
            r'\brandi\b', r'\brani\b.*\bchod\b', r'\bchod\b', r'\bkhud\s*chud\b'
        ]
    },
    'Odia': {
        'abusive': [
            r'\bboka\b', r'\bpagla\b', r'\bganda\b', r'\bchakri\b'
        ],
        'threat': [
            r'\bmar\s*dela\b', r'\bmarabu\b'
        ]
    },
    'Bengali': {
        'abusive': [
            r'\bbhonda\b', r'\bpagal\b', r'\bchal\b', r'\bgolay\b'
        ],
        'threat': [
            r'\bmarbo\b', r'\bmar\s*debo\b'
        ]
    },
    'Tamil': {
        'abusive': [
            r'\bsara\b', r'\bk*adi\b', r'\bpanna\b'
        ],
        'threat': [
            r'\bkolluvai\b', r'\bkottuvitta\b'
        ]
    },
    'English': {
        'abusive': [
            r'\bidiot\b', r'\bstupid\b', r'\bdumb\b', r'\basshole\b',
            r'\bmoron\b', r'\bimbecile\b', r'\bshit\b', r'\blook\s*idiot\b',
            r'\byou\s*suck\b', r'\btrash\b', r'\bgarbage\b', r'\bliar\b'
        ],
        'threat': [
            r'\bi\s*will\s*kill\b', r'\bdeath\s*threat\b', r'\bwill\s*hurt\b',
            r'\bbeat\s*you\b', r'\bbreak\s*your\b', r'\bi\s*will\s*hurt\b'
        ],
        'sexual': [
            r'\bsex\s*you\b', r'\bsex.*ass\b', r'\bporn\b', r'\bx-?rated\b'
        ],
        'spam': [
            r'(http|https)://\S+', r'click\s*here', r'buy\s*now', r'\$\d+\s*discount\b'
        ]
    }
}

# Positive context words that may negate toxicity
POSITIVE_CONTEXT = {
    'English': ['sorry', 'apologize', 'my bad', 'didn\'t mean', 'just joking', 'not serious'],
    'Hindi': ['maaf', 'mazak', 'joke', 'nahi matlab'],
    'Odia': ['maaf', 'mazak'],
    'Bengali': ['maaf', 'mazak'],
    'Tamil': ['maanai', 'mazak']
}

# Severity weights
SEVERITY_LEVELS = {
    'low': 0.3,
    'medium': 0.6,
    'high': 0.8
}


class ContentModerator:
    """Multilingual content moderation system"""

    def __init__(self):
        self.categories = [
            'Safe',
            'Offensive',
            'Hate Speech',
            'Harassment / Abuse',
            'Threat / Violence',
            'Sexual / Explicit',
            'Spam / Irrelevant'
        ]

    def detect_language(self, text: str) -> str:
        """Detect the language of the text"""
        try:
            # Handle mixed language (Hinglish, etc.)
            detected = detect(text)

            # Map common codes
            lang_map = {
                'hi': 'Hindi',
                'or': 'Odia',
                'te': 'Telugu',
                'bn': 'Bengali',
                'ta': 'Tamil',
                'en': 'English'
            }

            return lang_map.get(detected, detected)
        except:
            return 'English'  # Default to English if detection fails

    def check_pattern_matches(self, text: str, language: str) -> Dict[str, Any]:
        """Check for pattern matches in offensive terms"""
        text_lower = text.lower()
        matches = {
            'abusive': False,
            'threat': False,
            'sexual': False,
            'spam': False,
            'matches': []
        }

        lang_patterns = OFFENSIVE_PATTERNS.get(language, {})

        for category, patterns in lang_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    matches[category] = True
                    matches['matches'].append((category, pattern))

        return matches

    def check_positive_context(self, text: str, language: str) -> bool:
        """Check if positive context words reduce toxicity"""
        text_lower = text.lower()
        positive_words = POSITIVE_CONTEXT.get(language, [])

        for word in positive_words:
            if word.lower() in text_lower:
                return True
        return False

    def detect_harassment(self, text: str) -> bool:
        """Detect indirect harassment, sarcasm, passive aggression"""
        # Check for repeated character patterns (aggression indicator)
        if re.search(r'([a-z])\1{3,}', text.lower()):
            return True

        # Check for all caps (shouting)
        if len(text) > 10 and text.isupper():
            return True

        # Check for excessive punctuation
        if len(re.findall(r'[!?]{2,}', text)) > 2:
            return True

        return False

    def detect_hate_speech(self, text: str) -> bool:
        """Detect hate speech patterns"""
        hate_patterns = [
            r'\ball\s+\w+\s+(are|is)\s+(bad|evil|stupid|dumb)',
            r'\b(shouldn\'t|should not|can\'t|cannot)\s+(exist|live|speak)',
            r'\b(kill|erase|eliminate)\s+all\s+\w+',
            r'\b(these|those|the)\s+\w+\s+(people|guys|girls)\s+(are|is)',
        ]

        for pattern in hate_patterns:
            if re.search(pattern, text.lower()):
                return True

        return False

    def normalize_text(self, text: str) -> str:
        """Normalize text (convert to proper script if in transliteration)"""
        # For demonstration, return the cleaned version
        return text.strip()

    def moderate(self, content: str) -> Dict[str, Any]:
        """
        Main moderation function - analyzes content and returns classification

        Args:
            content: User-generated text content

        Returns:
            JSON-compatible dictionary with moderation results
        """

        # Detect language
        detected_language = self.detect_language(content)

        # Normalize text
        normalized = self.normalize_text(content)

        # Check pattern matches
        pattern_matches = self.check_pattern_matches(
            content, detected_language)

        # Initialize classification
        is_toxic = False
        category = 'Safe'
        confidence = 0.0
        severity = 'low'
        reason = ''

        # Determine if content has positive context
        has_positive_context = self.check_positive_context(
            content, detected_language)

        # Classification logic
        if pattern_matches['threat']:
            is_toxic = True
            category = 'Threat / Violence'
            confidence = 0.95 if not has_positive_context else 0.4
            severity = 'high' if confidence > 0.75 else 'medium'
            reason = f"Direct threat detected in {detected_language}"

        elif pattern_matches['sexual']:
            is_toxic = True
            category = 'Sexual / Explicit'
            confidence = 0.90
            severity = 'high'
            reason = f"Sexual or explicit content detected"

        elif pattern_matches['spam']:
            is_toxic = True
            category = 'Spam / Irrelevant'
            confidence = 0.85
            severity = 'low'
            reason = f"Spam or irrelevant content detected"

        elif self.detect_hate_speech(content):
            is_toxic = True
            category = 'Hate Speech'
            confidence = 0.88
            severity = 'high'
            reason = f"Hate speech pattern detected"

        elif self.detect_harassment(content):
            is_toxic = True
            category = 'Harassment / Abuse'
            confidence = 0.75
            severity = 'medium'
            reason = f"Harassment or abusive tone detected"

        elif pattern_matches['abusive']:
            is_toxic = True
            category = 'Offensive'
            confidence = 0.85 if not has_positive_context else 0.45
            severity = 'medium'
            reason = f"Abusive or offensive language detected in {detected_language}"

        else:
            is_toxic = False
            category = 'Safe'
            confidence = 0.98
            severity = 'low'
            reason = "Content appears safe and appropriate"

        # Adjust confidence if positive context found
        if has_positive_context and is_toxic:
            confidence = max(0.3, confidence - 0.2)
            severity = 'low' if confidence < 0.5 else severity

        # Build response
        response = {
            'is_toxic': is_toxic,
            'category': category,
            'confidence': round(confidence, 2),
            'severity': severity,
            'detected_language': detected_language,
            'normalized_text': normalized,
            'reason': reason
        }

        return response


# Initialize global moderator
moderator = ContentModerator()


def moderate_content(content: str) -> str:
    """
    Public interface for content moderation

    Args:
        content: User-generated text

    Returns:
        JSON string with moderation results
    """
    result = moderator.moderate(content)
    return json.dumps(result, ensure_ascii=False, indent=2)
