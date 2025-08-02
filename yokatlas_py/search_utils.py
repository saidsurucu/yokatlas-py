"""Search utilities for YOKATLAS with fuzzy matching and parameter normalization."""

from typing import Any, Optional, List
import difflib
from .form_data import UNIVERSITIES
from .onlisans_form_data import ONLISANS_UNIVERSITIES

# Program name expansions (short names to possible full names)
PROGRAM_EXPANSIONS = {
    "bilgisayar": [
        "Bilgisayar Mühendisliği",
        "Bilgisayar Bilimleri",
        "Bilgisayar Bilimleri ve Mühendisliği",
        "Bilgisayar ve Öğretim Teknolojileri Öğretmenliği",
        "Bilgisayar Mühendisliği (M.T.O.K.)",
        "Bilgisayar Teknolojisi ve Bilişim Sistemleri",
    ],
    "yazılım": [
        "Yazılım Mühendisliği",
        "Yazılım Geliştirme (Fakülte)",
        "Yazılım Geliştirme (Yüksekokul)",
        "Yazılım Mühendisliği (M.T.O.K.)",
    ],
    "elektrik": [
        "Elektrik Mühendisliği",
        "Elektrik-Elektronik Mühendisliği",
        "Elektrik-Elektronik Mühendisliği (M.T.O.K.)",
    ],
    "elektronik": [
        "Elektronik Mühendisliği",
        "Elektronik ve Haberleşme Mühendisliği",
        "Elektrik-Elektronik Mühendisliği",
        "Elektrik-Elektronik Mühendisliği (M.T.O.K.)",
    ],
    "makine": ["Makine Mühendisliği", "Makine Mühendisliği (M.T.O.K.)"],
    "endüstri": [
        "Endüstri Mühendisliği",
        "Endüstri Yönetimi Mühendisliği",
        "Endüstriyel Tasarım (Fakülte)",
        "Endüstriyel Tasarım (Yüksekokul)",
        "Endüstriyel Tasarım Mühendisliği",
    ],
    "endustri": [  # Common typo
        "Endüstri Mühendisliği",
        "Endüstri Yönetimi Mühendisliği",
    ],
    "inşaat": ["İnşaat Mühendisliği", "İnşaat Mühendisliği (M.T.O.K.)"],
    "insaat": ["İnşaat Mühendisliği", "İnşaat Mühendisliği (M.T.O.K.)"],
    "kimya": [
        "Kimya",
        "Kimya Mühendisliği",
        "Kimya Öğretmenliği",
        "Kimya-Biyoloji Mühendisliği",
    ],
    "fizik": ["Fizik", "Fizik Mühendisliği", "Fizik Öğretmenliği"],
    "matematik": [
        "Matematik",
        "Matematik Mühendisliği",
        "Matematik Öğretmenliği",
        "Matematik ve Bilgisayar Bilimleri",
        "İlköğretim Matematik Öğretmenliği",
    ],
    "tıp": ["Tıp"],
    "tip": ["Tıp"],
    "diş": ["Diş Hekimliği"],
    "dis": ["Diş Hekimliği"],
    "eczacılık": ["Eczacılık"],
    "eczacilik": ["Eczacılık"],
    "mimarlık": [
        "Mimarlık",
        "İç Mimarlık",
        "İç Mimarlık ve Mobilya Tasarımı",
        "Peyzaj Mimarlığı",
    ],
    "mimarlik": [
        "Mimarlık",
        "İç Mimarlık",
        "İç Mimarlık ve Mobilya Tasarımı",
        "Peyzaj Mimarlığı",
    ],
    "biyoloji": ["Biyoloji", "Biyoloji Öğretmenliği", "Moleküler Biyoloji ve Genetik"],
    "hemşire": ["Hemşirelik (Fakülte)", "Hemşirelik (Yüksekokul)"],
    "hemsire": ["Hemşirelik (Fakülte)", "Hemşirelik (Yüksekokul)"],
    "öğretmen": [
        "Bilgisayar ve Öğretim Teknolojileri Öğretmenliği",
        "Matematik Öğretmenliği",
        "Fen Bilgisi Öğretmenliği",
        "Fizik Öğretmenliği",
        "Kimya Öğretmenliği",
        "Biyoloji Öğretmenliği",
        "İlköğretim Matematik Öğretmenliği",
    ],
    "ogretmen": [
        "Bilgisayar ve Öğretim Teknolojileri Öğretmenliği",
        "Matematik Öğretmenliği",
        "Fen Bilgisi Öğretmenliği",
        "Fizik Öğretmenliği",
        "Kimya Öğretmenliği",
        "Biyoloji Öğretmenliği",
        "İlköğretim Matematik Öğretmenliği",
    ],
}


def find_best_university_match(name: str, program_type: str = "lisans") -> str:
    """
    Find the best matching university name using fuzzy matching.

    Args:
        name: University name (can be partial or with typos)
        program_type: "lisans" or "onlisans" to determine which university list to use

    Returns:
        Best matching university name from official list
    """
    if not name:
        return ""

    # Choose the appropriate university list
    university_list = (
        UNIVERSITIES if program_type == "lisans" else ONLISANS_UNIVERSITIES
    )

    # Normalize input
    name_clean = name.upper().strip()

    # If it's already in the list exactly, return it
    if name_clean in university_list:
        return name_clean

    # Handle common abbreviations that fuzzy matching might miss
    common_abbreviations = {
        "ODTÜ": "ORTA DOĞU TEKNİK ÜNİVERSİTESİ",
        "ODTU": "ORTA DOĞU TEKNİK ÜNİVERSİTESİ",
        "METU": "ORTA DOĞU TEKNİK ÜNİVERSİTESİ",
        "İTÜ": "İSTANBUL TEKNİK ÜNİVERSİTESİ",
        "ITÜ": "İSTANBUL TEKNİK ÜNİVERSİTESİ",
        "ITU": "İSTANBUL TEKNİK ÜNİVERSİTESİ",
        "YTÜ": "YILDIZ TEKNİK ÜNİVERSİTESİ",
        "YTU": "YILDIZ TEKNİK ÜNİVERSİTESİ",
        "KTÜ": "KARADENİZ TEKNİK ÜNİVERSİTESİ",
        "KTU": "KARADENİZ TEKNİK ÜNİVERSİTESİ",
        "DEÜ": "DOKUZ EYLÜL ÜNİVERSİTESİ",
        "DEU": "DOKUZ EYLÜL ÜNİVERSİTESİ",
        "İYTE": "İZMİR YÜKSEK TEKNOLOJİ ENSTİTÜSÜ",
        "IYTE": "İZMİR YÜKSEK TEKNOLOJİ ENSTİTÜSÜ",
        "BOUN": "BOĞAZİÇİ ÜNİVERSİTESİ",
        "BU": "BOĞAZİÇİ ÜNİVERSİTESİ",
    }

    if name_clean in common_abbreviations:
        return common_abbreviations[name_clean]

    # First try: look for universities that contain the search term
    for university in university_list:
        if name_clean in university:
            return university

    # Third try: Use difflib fuzzy matching
    matches = difflib.get_close_matches(
        name_clean,
        university_list,
        n=1,  # Get only the best match
        cutoff=0.4,  # Lower threshold for better matching
    )

    if matches:
        return matches[0]

    # As last resort, return the input uppercased
    return name_clean


def normalize_university_name(name: str, program_type: str = "lisans") -> str:
    """
    Normalize university name for search using fuzzy matching.

    Args:
        name: University name (can be short form or with typos)
        program_type: "lisans" or "onlisans" to determine which university list to use

    Returns:
        Best matching university name from official list
    """
    return find_best_university_match(name, program_type)


def expand_program_name(name: str, program_type: str = "lisans") -> list[str]:
    """
    Expand program name to possible full names.

    Args:
        name: Program name (can be short form)
        program_type: "lisans" or "onlisans" to determine search strategy

    Returns:
        List of possible program names
    """
    if not name:
        return []

    name_lower = name.lower().strip()

    # For lisans, use the predefined expansions and partial matching
    if program_type == "lisans":
        from .form_data import PROGRAMS

        # First check if it's in the expansions
        if name_lower in PROGRAM_EXPANSIONS:
            return PROGRAM_EXPANSIONS[name_lower]

        # Then try partial matching within lisans programs
        matches = []
        for program in PROGRAMS:
            if name_lower in program.lower():
                matches.append(program)

        if matches:
            return matches
        else:
            return [name]

    # For önlisans, do more flexible partial matching
    elif program_type == "onlisans":
        from .onlisans_form_data import ONLISANS_PROGRAMS

        # Try partial matching within önlisans programs first
        matches = []
        for program in ONLISANS_PROGRAMS:
            if name_lower in program.lower():
                matches.append(program)

        if matches:
            return matches

        # If no matches found, check if it's in the expansions (fallback)
        if name_lower in PROGRAM_EXPANSIONS:
            return PROGRAM_EXPANSIONS[name_lower]

        # Last resort
        return [name]

    # Default case
    return [name]


def normalize_score_type(score_type: str) -> str:
    """
    Normalize score type to lowercase.

    Args:
        score_type: Score type (SAY, EA, SÖZ, DİL)

    Returns:
        Normalized score type in lowercase
    """
    if not score_type:
        return ""

    return score_type.lower().strip()


def normalize_search_params(
    params: dict[str, Any], program_type: str = "lisans"
) -> dict[str, Any]:
    """
    Normalize search parameters for YOKATLAS API.

    Args:
        params: Raw search parameters
        program_type: "lisans" or "onlisans" to determine which university list to use

    Returns:
        Normalized parameters
    """
    normalized = {}

    # Map common parameter variations to correct names
    param_mappings = {
        "uni_adi": "universite",
        "university": "universite",
        "uni": "universite",
        "program_adi": "program",
        "bolum": "program",
        "department": "program",
        "score_type": "puan_turu",
        "city": "sehir",
        "il": "sehir",
        "uni_type": "universite_turu",
        "university_type": "universite_turu",
        "fee": "ucret",
        "ucret_durumu": "ucret",
        "education_type": "ogretim_turu",
        "egitim_turu": "ogretim_turu",
    }

    # Process each parameter
    for key, value in params.items():
        # Skip if value is None or empty string
        if value is None or value == "":
            continue

        # Normalize the key
        normalized_key = param_mappings.get(key.lower(), key.lower())

        # Process based on parameter type
        if normalized_key == "universite":
            normalized[normalized_key] = normalize_university_name(value, program_type)
        elif normalized_key == "program":
            # Don't expand here, we'll handle it in the search wrapper
            normalized[normalized_key] = value
        elif normalized_key == "puan_turu":
            normalized[normalized_key] = normalize_score_type(value)
        elif normalized_key == "sehir":
            # Cities should be uppercase
            normalized[normalized_key] = value.upper()
        else:
            # Keep other parameters as is
            normalized[normalized_key] = value

    return normalized
