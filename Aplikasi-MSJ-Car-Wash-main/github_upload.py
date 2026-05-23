# =========================================================
# GITHUB PDF UPLOAD
# =========================================================

import requests
import base64
import os

# =========================================================
# CONFIG
# =========================================================

GITHUB_TOKEN = "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"  # <-- GANTI DENGAN TOKEN BARU YANG PUNYA SCOPE REPO
REPO_NAME = "barufaris782-droid/msj-carwash-storage"
BRANCH = "main"

# =========================================================
# UPLOAD PDF
# =========================================================

def upload_pdf_github(pdf_path):

    try:

        filename = os.path.basename(pdf_path)

        with open(pdf_path, "rb") as file:
            content = base64.b64encode(file.read()).decode("utf-8")

        url = f"https://api.github.com/repos/{REPO_NAME}/contents/{filename}"

        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }

        # Cek apakah file sudah ada untuk update
        check_response = requests.get(url, headers=headers)

        data = {
            "message": f"Upload invoice PDF: {filename}",
            "content": content,
            "branch": BRANCH
        }

        # Jika file sudah ada, tambahkan sha untuk update
        if check_response.status_code == 200:
            data["sha"] = check_response.json()["sha"]
            print(f"📝 File {filename} sudah ada, akan diupdate")

        response = requests.put(
            url,
            headers=headers,
            json=data
        )

        print(f"📡 Status Code: {response.status_code}")

        if response.status_code in [200, 201]:

            raw_url = f"https://raw.githubusercontent.com/{REPO_NAME}/{BRANCH}/{filename}"

            print(f"✅ Upload berhasil: {raw_url}")
            return raw_url

        else:

            error_data = response.json()
            error_msg = error_data.get('message', 'Unknown error')
            print(f"❌ UPLOAD GAGAL: {error_msg}")

            if 'documentation_url' in error_data:
                print(f"📖 Dokumentasi: {error_data['documentation_url']}")

            print(f"📄 Response lengkap: {response.text}")
            return None

    except Exception as e:

        print("ERROR :", e)
        return None