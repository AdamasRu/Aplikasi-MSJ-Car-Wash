# upload_service.py

import cloudinary
import cloudinary.uploader

# =========================================================
# CLOUDINARY CONFIG
# =========================================================

cloudinary.config(
    cloud_name="dfocooeud",
    api_key="725939567348889",
    api_secret="xwPoHSXppUTTH_iFVamt_D3Wywg"
)

# =========================================================
# UPLOAD PDF
# =========================================================

def upload_pdf(file_path):

    try:

        result = cloudinary.uploader.upload(
            file_path,
            resource_type="raw",
            folder="invoice_pdf"
        )

        return result["secure_url"]

    except Exception as e:

        print("UPLOAD ERROR :", e)

        return None