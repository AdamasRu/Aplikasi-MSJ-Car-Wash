#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(__file__))

from pdf_service import generate_pdf

# Buat data transaksi test
test_data = {
    "invoice": "TEST-001",
    "nama": "Test User",
    "no_hp": "08123456789",
    "plat": "B 1234 ABC",
    "layanan": "Cuci Mobil",
    "harga": 50000,
    "tanggal": "11-05-2026 10:00"
}

try:
    # Generate PDF
    pdf_file = generate_pdf(test_data)
    print(f"PDF berhasil dibuat: {pdf_file}")

    # Test upload
    from github_upload import upload_pdf_github
    result = upload_pdf_github(pdf_file)
    print(f"Upload result: {result}")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()