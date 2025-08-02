"""
Pydantic models for YOKATLAS API data structures and validation.
"""

from typing import Dict, List, Optional, Union, Any
from pydantic import BaseModel, Field, field_validator
from typing_extensions import Literal


class YearlyData(BaseModel):
    """Model for yearly data (kontenjan, yerleşen, taban puan, etc.)"""

    year_2025: Optional[str] = Field(None, alias="2025")
    year_2024: Optional[str] = Field(None, alias="2024")
    year_2023: Optional[str] = Field(None, alias="2023")
    year_2022: Optional[str] = Field(None, alias="2022")

    model_config = {"populate_by_name": True}


class ProgramInfo(BaseModel):
    """Model for university program information"""

    yop_kodu: str = Field(..., description="YÖK Program Kodu")
    uni_adi: str = Field(..., description="Üniversite Adı")
    fakulte: str = Field(..., description="Fakülte Adı")
    program_adi: str = Field(..., description="Program Adı")
    program_detay: Optional[str] = Field(None, description="Program Detayları")
    sehir_adi: str = Field(..., description="Şehir Adı")
    universite_turu: Optional[str] = Field(
        None, description="Üniversite Türü (Devlet/Vakıf)"
    )
    ucret_burs: Optional[str] = Field(None, description="Ücret/Burs Durumu")
    ogretim_turu: Optional[str] = Field(None, description="Öğretim Türü")
    kontenjan: Optional[YearlyData] = Field(None, description="Kontenjan bilgileri")
    yerlesen: Optional[YearlyData] = Field(None, description="Yerleşen sayıları")
    taban: Optional[YearlyData] = Field(None, description="Taban puanları")
    tbs: Optional[YearlyData] = Field(None, description="Taban başarı sırası")

    @field_validator("yop_kodu")
    @classmethod
    def validate_yop_kodu(cls, v):
        if v and not v.isdigit():
            raise ValueError("YOP kodu sadece rakam içerebilir")
        if v and len(v) != 9:
            raise ValueError("YOP kodu 9 haneli olmalıdır")
        return v


class SearchParams(BaseModel):
    """Model for search parameters"""

    puan_turu: Optional[Literal["say", "ea", "söz", "dil"]] = Field(
        "say", description="Puan türü"
    )
    ust_bs: Optional[Union[int, str]] = Field(None, description="Üst başarı sırası")
    alt_bs: Optional[Union[int, str]] = Field(None, description="Alt başarı sırası")
    universite: Optional[str] = Field(None, description="Üniversite filtresi")
    program: Optional[str] = Field(None, description="Program filtresi")
    sehir: Optional[str] = Field(None, description="Şehir filtresi")
    universite_turu: Optional[Literal["Devlet", "Vakıf"]] = Field(
        None, description="Üniversite türü"
    )
    ucret: Optional[Literal["Burslu", "Ücretli", "%50 İndirimli"]] = Field(
        None, description="Ücret durumu"
    )
    ogretim_turu: Optional[Literal["Örgün", "İkinci Öğretim"]] = Field(
        None, description="Öğretim türü"
    )
    length: Optional[int] = Field(50, ge=1, le=500, description="Sonuç sayısı")
    start: Optional[int] = Field(0, ge=0, description="Başlangıç indexi")
    page: Optional[int] = Field(None, ge=1, description="Sayfa numarası")


class SearchResponse(BaseModel):
    """Model for search API response"""

    data: List[ProgramInfo] = Field(..., description="Program listesi")
    total: Optional[int] = Field(None, description="Toplam sonuç sayısı")
    filtered: Optional[int] = Field(None, description="Filtrelenmiş sonuç sayısı")


class ErrorResponse(BaseModel):
    """Model for error responses"""

    error: str = Field(..., description="Hata mesajı")
    details: Optional[Dict[str, Any]] = Field(None, description="Hata detayları")


class FetcherResponse(BaseModel):
    """Base model for fetcher module responses"""

    error: Optional[str] = Field(None, description="Hata mesajı varsa")
    data: Optional[Dict[str, Any]] = Field(None, description="Fetcher verisi")

    @field_validator("data")
    @classmethod
    def validate_response(cls, v, info):
        # Either error or data should be present, not both
        if hasattr(info, "data") and info.data.get("error") and v:
            raise ValueError("Response cannot have both error and data")
        return v


class KontenjhanYerlesmeData(BaseModel):
    """Model for kontenjan yerleşme data"""

    tur: Optional[str] = Field(None, alias="Tür", description="Yerleşme türü")

    model_config = {
        "populate_by_name": True,
        "extra": "allow",  # Allow additional fields from dynamic table headers
    }


class KontenjhanYerlesmeResponse(FetcherResponse):
    """Specific response model for kontenjan yerleşme fetcher"""

    kontenjan_yerlesme: Optional[List[KontenjhanYerlesmeData]] = Field(
        None, description="Kontenjan yerleşme verileri"
    )


class CinsiyetDagilimiData(BaseModel):
    """Model for cinsiyet dağılımı data"""

    cinsiyet: Optional[str] = Field(None, description="Cinsiyet")

    model_config = {"extra": "allow"}  # Allow additional year columns


class GeografiBolgeData(BaseModel):
    """Model for coğrafi bölge dağılımı"""

    bolge: Optional[str] = Field(None, alias="Bölge", description="Coğrafi bölge")

    model_config = {"populate_by_name": True, "extra": "allow"}


class SehirDagilimiData(BaseModel):
    """Model for şehir dağılımı"""

    tur: Optional[str] = Field(None, alias="Tür", description="Şehir türü")

    model_config = {"populate_by_name": True, "extra": "allow"}


class SehirVeCografiBolgeResponse(FetcherResponse):
    """Response model for şehir ve coğrafi bölge dağılımı"""

    sehir_dagilimi: Optional[List[SehirDagilimiData]] = Field(
        None, description="Şehir dağılımı"
    )
    cografi_bolge_dagilimi: Optional[List[GeografiBolgeData]] = Field(
        None, description="Coğrafi bölge dağılımı"
    )


class YearRange(BaseModel):
    """Valid year range for API calls"""

    min_year: int = Field(2022, description="Minimum supported year")
    max_year: int = Field(2025, description="Maximum supported year")
    supported_years: List[int] = Field(
        [2022, 2023, 2024, 2025], description="Supported years"
    )

    @field_validator("supported_years")
    @classmethod
    def validate_years(cls, v):
        if not all(isinstance(year, int) and 2022 <= year <= 2025 for year in v):
            raise ValueError("All years must be integers between 2022 and 2025")
        return v


# Type aliases for common use cases
ProgramList = List[ProgramInfo]
SearchResult = Union[SearchResponse, ErrorResponse]
FetcherResult = Union[FetcherResponse, ErrorResponse]
APIResponse = Union[Dict[str, Any], List[Dict[str, Any]], str]
