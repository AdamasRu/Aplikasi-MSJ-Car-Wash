import requests

TOKEN = "1YfTobfBVHjCmcQo1YMv"

def kirim_whatsapp(
    nomor,
    pesan,
    file_url
):

    try:

        nomor = nomor.replace("+", "")

        if nomor.startswith("08"):
            nomor = "62" + nomor[1:]

        url = "https://api.fonnte.com/send"

        headers = {
            "Authorization": TOKEN
        }

        data = {
            "target": nomor,
            "message": pesan,
            "file": file_url
        }

        response = requests.post(
            url,
            headers=headers,
            data=data
        )

        print(response.text)

    except Exception as e:

        print(e)