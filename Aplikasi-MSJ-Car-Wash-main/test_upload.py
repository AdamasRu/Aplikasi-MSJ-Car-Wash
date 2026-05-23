#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(__file__))

try:
    from github_upload import upload_pdf_github
    print("Import github_upload berhasil")

    # Test dengan file PDF dummy
    test_pdf = "test.pdf"
    if os.path.exists(test_pdf):
        result = upload_pdf_github(test_pdf)
        print(f"Upload result: {result}")
    else:
        print(" File test.pdf tidak ada")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()