from reportlab.platypus import *
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus.tables import Table
from reportlab.platypus.tables import TableStyle

def generate_pdf(transaksi):

    filename = f"{transaksi['invoice']}.pdf"

    doc = SimpleDocTemplate(
        filename,
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=20
    )

    styles = getSampleStyleSheet()

    elements = []

    # =========================================
    # HEADER
    # =========================================

    title = Paragraph(
        """
        <font size=20>
        <b>MSJ CARWASH</b>
        </font>
        <br/>
        <font size=12>
        Kuitansi Pembayaran
        </font>
        """,
        styles['Title']
    )

    elements.append(title)

    elements.append(Spacer(1, 20))

    # =========================================
    # DATA
    # =========================================

    data = [

        ["Invoice", transaksi["invoice"]],

        ["Nama Pelanggan", transaksi["nama"]],

        ["Nomor WhatsApp", transaksi["no_hp"]],

        ["Plat Nomor", transaksi["plat"]],

        ["Layanan", transaksi["layanan"]],

        ["Tanggal", transaksi["tanggal"]],

        ["Total Bayar", f"Rp {transaksi['harga']:,}"],
    ]

    table = Table(
        data,
        colWidths=[180, 280]
    )

    table.setStyle(TableStyle([

        ('BACKGROUND', (0,0), (-1,0), colors.cyan),

        ('TEXTCOLOR', (0,0), (-1,-1), colors.black),

        ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),

        ('FONTSIZE', (0,0), (-1,-1), 11),

        ('BOTTOMPADDING', (0,0), (-1,-1), 10),

        ('BACKGROUND', (0,0), (0,-1), colors.lightgrey),

        ('GRID', (0,0), (-1,-1), 1, colors.black),

    ]))

    elements.append(table)

    elements.append(Spacer(1, 30))

    # =========================================
    # FOOTER
    # =========================================

    footer = Paragraph(
        """
        Terima kasih telah menggunakan layanan MSJ Carwash.<br/>
        Simpan kuitansi ini sebagai bukti pembayaran resmi.
        """,
        styles['BodyText']
    )

    elements.append(footer)

    doc.build(elements)

    return filename