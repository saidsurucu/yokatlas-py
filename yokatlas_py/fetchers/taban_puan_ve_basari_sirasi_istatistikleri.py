"""
Taban Puan ve Basari Sirasi Istatistikleri (Base Score and Success Ranking Stats) Fetcher.

Multi-table parser with HTML comment extraction for base score statistics.
"""

from typing import Any

from bs4 import Comment

from ..base_fetcher import BaseFetcher


class TabanPuanVeBasariSirasiIstatistikleriBaseFetcher(BaseFetcher):
    """Base fetcher for base score and success ranking statistics."""

    RESULT_KEY = "taban_puan_ve_basari_sirasi_istatistikleri"

    def parse(self, html_content: str) -> dict[str, Any]:
        """Parse HTML content to extract base score statistics."""
        # Note: Don't use clean=True here because we need to process comments
        soup = self.create_soup(html_content, clean=False)

        # Uncomment HTML comments to access hidden tables
        comments = soup.find_all(string=lambda text: isinstance(text, Comment))
        for comment in comments:
            if comment.string:
                uncommented = self.create_soup(comment.string, clean=False)
                comment.insert_after(uncommented)

        tables = soup.find_all("table", {"class": "table table-bordered"})

        if len(tables) < 2:
            return {"error": "Required tables not found in the HTML content"}

        result: dict[str, Any] = {
            "son_kisi_puan_bilgileri": [],
            "son_kisi_basari_sirasi_bilgileri": [],
        }

        def parse_table(table):
            headers = [
                "Kontenjan Türü",
                "Kontenjan",
                "Yerleşen Sayısı",
                "0,12 Katsayı ile",
                "0,12 + 0,06 Katsayı ile",
            ]

            data = []
            rows = table.find_all("tr")

            for row in rows:
                cols = row.find_all(["td", "th"])

                if len(cols) >= 4:
                    entry = {}
                    for header, col in zip(headers, cols + [None] * (5 - len(cols))):
                        text = col.get_text(strip=True) if col else None
                        entry[header] = text if text and text != "---" else None

                    # Filter out header rows and invalid entries
                    if entry["Kontenjan Türü"] and entry["Kontenjan Türü"] not in [
                        "Kontenjan Türü",
                        "",
                        "Kontenjan",
                    ]:
                        # Normalize YKS Kontenjanı to Genel Kontenjan
                        if entry["Kontenjan Türü"] == "YKS Kontenjanı":
                            entry["Kontenjan Türü"] = "Genel Kontenjan"
                        # Skip Sınavsız Geçiş Kontenjanı
                        if entry["Kontenjan Türü"] != "Sınavsız Geçiş Kontenjanı":
                            data.append(entry)

            return data

        result["son_kisi_puan_bilgileri"] = parse_table(tables[0])
        result["son_kisi_basari_sirasi_bilgileri"] = parse_table(tables[1])

        return result


class TabanPuanVeBasariSirasiIstatistikleriLisansFetcher(
    TabanPuanVeBasariSirasiIstatistikleriBaseFetcher
):
    """Lisans fetcher for base score and success ranking statistics."""

    ENDPOINT = "1000_3.php"
    PROGRAM_TYPE = "lisans"


class TabanPuanVeBasariSirasiIstatistikleriOnlisansFetcher(
    TabanPuanVeBasariSirasiIstatistikleriBaseFetcher
):
    """Onlisans fetcher for base score and success ranking statistics."""

    ENDPOINT = "3000_3.php"
    PROGRAM_TYPE = "onlisans"
