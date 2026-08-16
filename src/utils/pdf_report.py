import os

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)


# FONT SETUP

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

FONT_DIR = os.path.join(BASE_DIR, "fonts")

REGULAR_FONT = os.path.join(
    FONT_DIR,
    "DejaVuSans.ttf"
)

BOLD_FONT = os.path.join(
    FONT_DIR,
    "DejaVuSans-Bold.ttf"
)


pdfmetrics.registerFont(
    TTFont(
        "DejaVuSans",
        REGULAR_FONT
    )
)

pdfmetrics.registerFont(
    TTFont(
        "DejaVuSans-Bold",
        BOLD_FONT
    )
)

registerFontFamily(
    "DejaVuSans",
    normal="DejaVuSans",
    bold="DejaVuSans-Bold"
)


# INDIAN CURRENCY FORMATTER

def format_inr(value):
    try:
        value = float(value)

        negative = value < 0
        value = abs(value)

        # Keep exactly 2 decimal places
        integer_part, decimal_part = f"{value:.2f}".split(".")

        # Indian numbering system
        if len(integer_part) > 3:

            last_three = integer_part[-3:]
            remaining = integer_part[:-3]

            groups = []

            while remaining:
                groups.insert(0, remaining[-2:])
                remaining = remaining[:-2]

            integer_part = ",".join(groups) + "," + last_three

        result = f"₹{integer_part}.{decimal_part}"

        if negative:
            result = "-" + result

        return result

    except (ValueError, TypeError):
        return str(value)


# PDF REPORT

class PDFReport:

    def generate(
        self,
        filename,
        applicant_name,
        phone,
        purpose,
        age,
        income,
        loan_amount,
        interest_rate,
        loan_term,
        metrics,
        result,
        decision_summary
    ):

        doc = SimpleDocTemplate(
            filename
        )

        styles = getSampleStyleSheet()

        # Use Unicode-compatible font
        styles["Title"].fontName = "DejaVuSans-Bold"
        styles["Heading2"].fontName = "DejaVuSans-Bold"
        styles["Heading3"].fontName = "DejaVuSans-Bold"
        styles["BodyText"].fontName = "DejaVuSans"

        elements = []

        # TITLE

        elements.append(
            Paragraph(
                "<b><font size=20 color='blue'>"
                "CreditGuard AI"
                "</font></b>",
                styles["Title"]
            )
        )

        elements.append(
            Paragraph(
                "<b>AI Credit Risk Assessment Report</b>",
                styles["Heading2"]
            )
        )

        elements.append(
            Spacer(1, 20)
        )

        # APPLICANT INFORMATION

        elements.append(
            Paragraph(
                "<b>Applicant Information</b>",
                styles["Heading2"]
            )
        )

        applicant_table = [

            ["Applicant Name", applicant_name],

            ["Phone", phone],

            ["Purpose", purpose],

            ["Age", str(age)]

        ]

        table = Table(
            applicant_table,
            colWidths=[180, 280]
        )

        table.setStyle(
            TableStyle([

                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    1,
                    colors.grey
                ),

                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    colors.lightblue
                ),

                (
                    "FONTNAME",
                    (0, 0),
                    (-1, -1),
                    "DejaVuSans-Bold"
                ),

                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    10
                )

            ])
        )

        elements.append(table)

        elements.append(
            Spacer(1, 20)
        )

        # LOAN DETAILS

        elements.append(
            Paragraph(
                "<b>Loan Details</b>",
                styles["Heading2"]
            )
        )

        loan_table = [

            [
                "Annual Income",
                format_inr(income)
            ],

            [
                "Loan Amount",
                format_inr(loan_amount)
            ],

            [
                "Interest Rate",
                f"{interest_rate}%"
            ],

            [
                "Loan Term",
                f"{loan_term} Months"
            ],

            [
                "Monthly EMI",
                format_inr(
                    metrics["monthly_emi"]
                )
            ],

            [
                "Loan vs Income",
                f"{metrics['loan_vs_income']} x"
            ],

            [
                "EMI Ratio",
                f"{metrics['emi_ratio']} %"
            ]

        ]

        table = Table(
            loan_table,
            colWidths=[180, 280]
        )

        table.setStyle(
            TableStyle([

                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    1,
                    colors.grey
                ),

                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    colors.beige
                ),

                (
                    "FONTNAME",
                    (0, 0),
                    (-1, -1),
                    "DejaVuSans-Bold"
                ),

                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    10
                )

            ])
        )

        elements.append(table)

        elements.append(
            Spacer(1, 20)
        )

        # AI RESULT

        elements.append(
            Paragraph(
                "<b>Prediction Result</b>",
                styles["Heading2"]
            )
        )

        result_table = [

            [
                "Decision",
                result["decision"]
            ],

            [
                "Confidence",
                f"{result['confidence']} %"
            ],

            [
                "Probability of Default",
                f"{result['probability']} %"
            ],

            [
                "Risk Level",
                result["risk"]
            ]

        ]

        table = Table(
            result_table,
            colWidths=[180, 280]
        )

        table.setStyle(
            TableStyle([

                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    1,
                    colors.grey
                ),

                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    colors.lightgreen
                ),

                (
                    "FONTNAME",
                    (0, 0),
                    (-1, -1),
                    "DejaVuSans-Bold"
                ),

                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    10
                )

            ])
        )

        elements.append(table)

        elements.append(
            Spacer(1, 20)
        )

        # AI DECISION SUMMARY

        elements.append(
            Paragraph(
                "<b>AI Decision Summary</b>",
                styles["Heading2"]
            )
        )

        for item in decision_summary:

            elements.append(
                Paragraph(
                    f"✔ {item}",
                    styles["BodyText"]
                )
            )

        elements.append(
            Spacer(1, 20)
        )

        # FOOTER

        elements.append(
            Paragraph(
                "<b>Generated by CreditGuard AI</b>",
                styles["Heading3"]
            )
        )

        elements.append(
            Paragraph(
                "Powered by LightGBM + Explainable AI",
                styles["BodyText"]
            )
        )

        # BUILD PDF

        doc.build(elements)

        return filename