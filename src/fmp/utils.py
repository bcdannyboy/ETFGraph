import re


def analyze_etf_attributes(etf_name):
    """
    analyze_etf_attributes analyzes the name of an ETF to determine if it is leveraged or inversed.
    """
    # Patterns to identify leveraged ETFs
    leveraged_patterns = [
        r'\b(?:2x|3x|4x|5x|2\.5x|3\.5x|double|triple|quad|quint|daily)\b',
        r'\b(?:leveraged|multiplier)\b',
    ]
    # Patterns to identify inversed ETFs
    inversed_patterns = [
        r'\b(?:inverse|short|bear|-\d+x)\b'
    ]

    # Convert the ETF name to lower case to ensure case-insensitive matching
    etf_name_lower = etf_name.lower()

    # Check if any leveraged patterns match the ETF name
    is_leveraged = any(re.search(pattern, etf_name_lower) for pattern in leveraged_patterns)
    # Check if any inversed patterns match the ETF name
    is_inversed = any(re.search(pattern, etf_name_lower) for pattern in inversed_patterns)

    return is_leveraged, is_inversed