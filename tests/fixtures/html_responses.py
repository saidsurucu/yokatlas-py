"""
Mock HTML responses for testing fetchers.

These mock responses simulate YOKATLAS API responses without requiring
network access, enabling fast and reliable unit tests.
"""

# Standard single table response (cinsiyet_dagilimi pattern)
SINGLE_TABLE_HTML = """
<!DOCTYPE html>
<html>
<body>
<table class="table table-bordered">
    <thead>
        <tr>
            <th>Cinsiyet</th>
            <th>2024</th>
            <th>2023</th>
            <th>2022</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Erkek</td>
            <td>55</td>
            <td>50</td>
            <td>48</td>
        </tr>
        <tr>
            <td>Kadin</td>
            <td>45</td>
            <td>50</td>
            <td>52</td>
        </tr>
    </tbody>
</table>
</body>
</html>
"""

# Table with totals row (ogrenim_durumu pattern)
TABLE_WITH_TOTALS_HTML = """
<!DOCTYPE html>
<html>
<body>
<table class="table table-bordered">
    <thead>
        <tr>
            <th>Durum</th>
            <th>2024</th>
            <th>2023</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Yeni Mezun</td>
            <td>60</td>
            <td>55</td>
        </tr>
        <tr>
            <td>Onceki Yil Mezun</td>
            <td>30</td>
            <td>35</td>
        </tr>
        <tr>
            <td>Diger</td>
            <td>10</td>
            <td>10</td>
        </tr>
        <tr>
            <td>TOPLAM</td>
            <td>100</td>
            <td>100</td>
        </tr>
    </tbody>
</table>
</body>
</html>
"""

# Multiple tables response (genel_bilgiler pattern)
MULTI_TABLE_HTML = """
<!DOCTYPE html>
<html>
<body>
<table class="table table-bordered">
    <tbody>
        <tr>
            <td>Program Adi</td>
            <td>Bilgisayar Muhendisligi</td>
        </tr>
        <tr>
            <td>Fakulte</td>
            <td>Muhendislik Fakultesi</td>
        </tr>
    </tbody>
</table>

<table class="table table-bordered">
    <thead>
        <tr>
            <th>Tur</th>
            <th>2024</th>
            <th>2023</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Kontenjan</td>
            <td>100</td>
            <td>90</td>
        </tr>
        <tr>
            <td>Yerlesen</td>
            <td>100</td>
            <td>90</td>
        </tr>
    </tbody>
</table>
</body>
</html>
"""

# Empty table response
EMPTY_TABLE_HTML = """
<!DOCTYPE html>
<html>
<body>
<table class="table table-bordered">
    <thead>
        <tr>
            <th>Type</th>
            <th>2024</th>
        </tr>
    </thead>
    <tbody>
    </tbody>
</table>
</body>
</html>
"""

# Response with placeholder values (---)
PLACEHOLDER_VALUES_HTML = """
<!DOCTYPE html>
<html>
<body>
<table class="table table-bordered">
    <thead>
        <tr>
            <th>Type</th>
            <th>2024</th>
            <th>2023</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Row1</td>
            <td>50</td>
            <td>---</td>
        </tr>
        <tr>
            <td>Row2*</td>
            <td>---</td>
            <td>40</td>
        </tr>
    </tbody>
</table>
</body>
</html>
"""

# Error response (no table found)
NO_TABLE_HTML = """
<!DOCTYPE html>
<html>
<body>
<div class="error">Veri bulunamadi</div>
</body>
</html>
"""

# Kontenjan yerlesme table (specific format)
KONTENJAN_YERLESME_HTML = """
<!DOCTYPE html>
<html>
<body>
<table class="table table-bordered">
    <thead>
        <tr>
            <th>Tur</th>
            <th>2024</th>
            <th>2023</th>
            <th>2022</th>
            <th>2021</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Kontenjan</td>
            <td>100</td>
            <td>90</td>
            <td>85</td>
            <td>80</td>
        </tr>
        <tr>
            <td>Yerlesen</td>
            <td>100</td>
            <td>90</td>
            <td>85</td>
            <td>80</td>
        </tr>
        <tr>
            <td>Bos Kalan</td>
            <td>0</td>
            <td>0</td>
            <td>0</td>
            <td>0</td>
        </tr>
    </tbody>
</table>
</body>
</html>
"""

# Search API response (JSON format)
SEARCH_API_RESPONSE = {
    "draw": 1,
    "recordsTotal": 1000,
    "recordsFiltered": 50,
    "data": [
        [
            "1",
            "123456789",
            "BOGAZICI UNIVERSITESI<br><font color='#CC0000'>Muhendislik Fakultesi</font>",
            "1",
            "Bilgisayar Muhendisligi<br><font color='#CC0000'>(Ingilizce)</font>",
            "1",
            "ISTANBUL",
            "Devlet",
            "---",
            "Orgün Öğretim",
            "Kontenjan<br><font color='red'>100</font><br><font color='purple'>90</font>",
        ]
    ],
}

# Search API empty response
SEARCH_API_EMPTY_RESPONSE = {
    "draw": 1,
    "recordsTotal": 0,
    "recordsFiltered": 0,
    "data": [],
}
