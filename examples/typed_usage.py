#!/usr/bin/env python3
"""
Example usage of YOKATLAS with pydantic types and validation.
"""

from typing import List, Dict, Any, Optional
from yokatlas_py import YOKATLASLisansTercihSihirbazi
from yokatlas_py.models import (
    SearchParams, 
    ProgramInfo, 
    YearlyData,
    ErrorResponse
)
from yokatlas_py.config import settings
from pydantic import ValidationError
import asyncio


def example_search_with_validation():
    """Example using pydantic models for validation."""
    print("=== Search with Pydantic Validation ===")
    
    # Create validated search parameters
    try:
        # This will validate the parameters
        search_params = SearchParams(
            puan_turu="say",
            length=5,
            sehir="İstanbul",
            universite_turu="Devlet"
        )
        print(f"✓ Valid search parameters: {search_params.model_dump()}")
        
        # Convert to dict for API (compatibility)
        params_dict = search_params.model_dump(exclude_none=True)
        
        # Perform search
        search_client = YOKATLASLisansTercihSihirbazi(params_dict)
        results = search_client.search()
        
        print(f"Found {len(results)} programs")
        
        # Parse results with validation
        for i, result in enumerate(results[:2]):  # Show first 2
            try:
                # This will validate the program data
                program = ProgramInfo(**result)
                print(f"\nProgram {i+1}:")
                print(f"  YOP Kodu: {program.yop_kodu}")
                print(f"  Üniversite: {program.uni_adi}")
                print(f"  Program: {program.program_adi}")
                print(f"  Şehir: {program.sehir_adi}")
                if program.taban:
                    print(f"  Taban 2024: {program.taban.year_2024}")
            except ValidationError as e:
                print(f"  ⚠️  Validation error for program {i+1}: {e}")
            except Exception as e:
                print(f"  ❌ Error processing program {i+1}: {e}")
                
    except ValidationError as e:
        print(f"❌ Parameter validation error: {e}")
    except Exception as e:
        print(f"❌ Search error: {e}")


def example_invalid_validation():
    """Example showing validation errors."""
    print("\n=== Validation Error Examples ===")
    
    # Invalid puan_turu
    try:
        SearchParams(puan_turu="invalid", length=10)
    except ValidationError as e:
        print(f"✓ Caught puan_turu validation error: {e.errors()[0]['msg']}")
    
    # Invalid length (too large)
    try:
        SearchParams(length=1000)  # Max is 500
    except ValidationError as e:
        print(f"✓ Caught length validation error: {e.errors()[0]['msg']}")
    
    # Invalid YOP kodu
    try:
        program_data = {
            "yop_kodu": "12345",  # Should be 9 digits
            "uni_adi": "Test Uni",
            "fakulte": "Test Fakülte", 
            "program_adi": "Test Program",
            "sehir_adi": "Test Şehir"
        }
        ProgramInfo(**program_data)
    except ValidationError as e:
        print(f"✓ Caught YOP kodu validation error: {e.errors()[0]['msg']}")


def example_configuration():
    """Example using configuration settings."""
    print("\n=== Configuration Example ===")
    
    print(f"Base URL: {settings.base_url}")
    print(f"Timeout: {settings.timeout} seconds")
    print(f"Supported years: {settings.supported_years}")
    print(f"SSL verification: {settings.verify_ssl}")
    
    # Check if year is supported
    test_year = 2024
    if settings.is_year_supported(test_year):
        print(f"✓ Year {test_year} is supported")
    else:
        print(f"❌ Year {test_year} is not supported")
    
    # Get headers
    headers = settings.get_headers()
    print(f"Default headers: {list(headers.keys())}")


def example_type_annotations():
    """Example showing proper type annotations."""
    print("\n=== Type Annotations Example ===")
    
    def process_search_results(
        results: List[Dict[str, Any]]
    ) -> List[ProgramInfo]:
        """Process raw search results with type safety."""
        validated_programs: List[ProgramInfo] = []
        
        for result in results:
            try:
                program = ProgramInfo(**result)
                validated_programs.append(program)
            except ValidationError:
                # Skip invalid programs
                continue
                
        return validated_programs
    
    # Use the function
    search_client = YOKATLASLisansTercihSihirbazi({"puan_turu": "say", "length": 3})
    raw_results = search_client.search()
    validated_results = process_search_results(raw_results)
    
    print(f"Processed {len(validated_results)} valid programs out of {len(raw_results)} total")


async def example_fetcher_typing():
    """Example showing fetcher with type hints."""
    print("\n=== Fetcher Type Hints Example ===")
    
    from yokatlas_py.lisans_fetchers.kontenjan_yerlesme import fetch_kontenjan_yerlesme
    
    # This function now has proper type hints
    program_id: str = "104810617"  # Hacettepe Tıp
    year: int = 2024
    
    try:
        result = await fetch_kontenjan_yerlesme(program_id, year)
        print(f"✓ Fetcher returned data for program {program_id}")
        print(f"  Keys: {list(result.keys())}")
        
        if "kontenjan_yerlesme" in result:
            data = result["kontenjan_yerlesme"]
            print(f"  Kontenjan data rows: {len(data)}")
            if data:
                print(f"  First row keys: {list(data[0].keys())}")
    except Exception as e:
        print(f"❌ Fetcher error: {e}")


def main():
    """Run all examples."""
    print("YOKATLAS Pydantic & Typing Examples")
    print("=" * 50)
    
    example_search_with_validation()
    example_invalid_validation()
    example_configuration()
    example_type_annotations()
    
    # Run async example
    asyncio.run(example_fetcher_typing())
    
    print("\n" + "=" * 50)
    print("All examples completed!")


if __name__ == "__main__":
    main()