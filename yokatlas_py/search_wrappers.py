"""Enhanced search wrappers with fuzzy matching and smart parameter handling."""

from typing import Any, Optional, Union
from .lisanstercihsihirbazi import YOKATLASLisansTercihSihirbazi
from .onlisanstercihsihirbazi import YOKATLASOnlisansTercihSihirbazi
from .search_utils import normalize_search_params, expand_program_name


def search_lisans_programs(
    params: dict[str, Any], smart_search: bool = True
) -> list[dict[str, Any]]:
    """
    Enhanced search for lisans (bachelor's) programs.

    Args:
        params: Search parameters (can use common variations)
        smart_search: Enable smart parameter normalization and program expansion

    Returns:
        List of programs found, or empty list if none

    Example:
        >>> # These all work now:
        >>> search_lisans_programs({"uni_adi": "Boğaziçi", "program_adi": "Bilgisayar"})
        >>> search_lisans_programs({"universite": "ODTÜ", "program": "Yazılım"})
        >>> search_lisans_programs({"uni": "itü", "bolum": "elektrik", "puan_turu": "SAY"})
    """
    if not smart_search:
        # Use original search without enhancements
        search = YOKATLASLisansTercihSihirbazi(params)
        return search.search()

    # Normalize parameters
    normalized_params = normalize_search_params(params, "lisans")

    # If program is specified, try expanding it
    if "program" in normalized_params:
        program_query = normalized_params["program"]
        program_variations = expand_program_name(program_query, "lisans")

        all_results = []

        # Try each program variation
        for program_name in program_variations:
            search_params = normalized_params.copy()
            search_params["program"] = program_name

            search = YOKATLASLisansTercihSihirbazi(search_params)
            results = search.search()

            if isinstance(results, list) and len(results) > 0:
                # Add results, avoiding duplicates
                for result in results:
                    # Check if this program is already in results (by program code)
                    if not any(
                        r.get("yop_kodu") == result.get("yop_kodu") for r in all_results
                    ):
                        all_results.append(result)

        return all_results
    else:
        # No program specified, just do normal search
        search = YOKATLASLisansTercihSihirbazi(normalized_params)
        results = search.search()
        return results if isinstance(results, list) else []


def search_onlisans_programs(
    params: dict[str, Any], smart_search: bool = True
) -> list[dict[str, Any]]:
    """
    Enhanced search for önlisans (associate) programs.

    Args:
        params: Search parameters (can use common variations)
        smart_search: Enable smart parameter normalization and program expansion

    Returns:
        List of programs found, or empty list if none
    """
    if not smart_search:
        # Use original search without enhancements
        search = YOKATLASOnlisansTercihSihirbazi(params)
        return search.search()

    # Normalize parameters (note: önlisans uses "tyt" instead of score types)
    normalized_params = normalize_search_params(params, "onlisans")

    # Ensure correct score type for önlisans
    if "puan_turu" in normalized_params and normalized_params["puan_turu"] in [
        "say",
        "ea",
        "söz",
        "dil",
    ]:
        normalized_params["puan_turu"] = "tyt"

    # If program is specified, try expanding it
    if "program" in normalized_params:
        program_query = normalized_params["program"]
        program_variations = expand_program_name(program_query, "onlisans")

        all_results = []

        # Try each program variation
        for program_name in program_variations:
            search_params = normalized_params.copy()
            search_params["program"] = program_name

            search = YOKATLASOnlisansTercihSihirbazi(search_params)
            results = search.search()

            if isinstance(results, list) and len(results) > 0:
                # Add results, avoiding duplicates
                for result in results:
                    # Check if this program is already in results (by program code)
                    if not any(
                        r.get("yop_kodu") == result.get("yop_kodu") for r in all_results
                    ):
                        all_results.append(result)

        return all_results
    else:
        # No program specified, just do normal search
        search = YOKATLASOnlisansTercihSihirbazi(normalized_params)
        results = search.search()
        return results if isinstance(results, list) else []


def search_programs(
    params: dict[str, Any],
    program_type: Optional[str] = None,
    smart_search: bool = True,
) -> dict[str, list[dict[str, Any]]]:
    """
    Universal search for both lisans and önlisans programs.

    Args:
        params: Search parameters
        program_type: "lisans", "onlisans", or None for both
        smart_search: Enable smart parameter normalization

    Returns:
        Dictionary with "lisans" and/or "onlisans" keys containing results

    Example:
        >>> results = search_programs({"uni": "boğaziçi", "program": "bilgisayar"})
        >>> print(f"Found {len(results['lisans'])} lisans programs")
        >>> print(f"Found {len(results['onlisans'])} önlisans programs")
    """
    results = {}

    if program_type is None or program_type == "lisans":
        results["lisans"] = search_lisans_programs(params, smart_search)

    if program_type is None or program_type == "onlisans":
        results["onlisans"] = search_onlisans_programs(params, smart_search)

    return results
