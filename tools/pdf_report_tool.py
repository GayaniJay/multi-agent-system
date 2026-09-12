from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.platypus import ListFlowable, ListItem
import datetime


class PDFReportTool:

    def generate(self,
                 pdf_path,
                 section_map,
                 metrics_table_data,
                 class_distribution,
                 total_images,
                 metric_chart,
                 confusion_chart):

        pdfmetrics.registerFont(UnicodeCIDFont('HeiseiMin-W3'))

        styles = getSampleStyleSheet()
        styles["Title"].fontName = "HeiseiMin-W3"
        styles["Heading2"].fontName = "HeiseiMin-W3"
        styles["BodyText"].fontName = "HeiseiMin-W3"

        elements = []

        # =========================
        # Dataset Table (DEFINE FIRST)
        # =========================
        table_data = [
            ["項目", "内容"],
            ["総画像数", total_images],
            ["クラス数", len(class_distribution)],
            ["クラス名", "画像数"],
        ]

        for class_name, count in class_distribution.items():
            table_data.append([class_name, count])

        dataset_table = Table(table_data, colWidths=[150],hAlign='CENTER')

        dataset_table.setStyle([
            ("FONTNAME", (0, 0), (-1, -1), "HeiseiMin-W3"),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("BACKGROUND", (0, 3), (-1, 3), colors.lightgrey),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("FONTSIZE", (0, 0), (-1, -1), 11),    
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8)
        ])

        # =========================
        # Metrics Table (DEFINE FIRST)
        # =========================
        metrics_table = Table(metrics_table_data, colWidths=[150] * len(metrics_table_data[0]), hAlign='CENTER')

        metrics_table.setStyle([
            ("FONTNAME", (0, 0), (-1, -1), "HeiseiMin-W3"),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("FONTSIZE", (0, 0), (-1, -1), 11),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8)
        ])

        # =========================
        # Title
        # =========================
        elements.append(Paragraph("AIモデル性能報告書", styles["Title"]))
        elements.append(Spacer(1, 10))

        # =========================
        # Date (RIGHT EDGE)
        # =========================
        today = datetime.date.today()
        today_str = today.strftime("%Y年%m月%d日")

        date_table = Table(
            [["", Paragraph(today_str, styles["BodyText"])]],
            colWidths=["*", 80]
        )

        date_table.setStyle([
            ("FONTNAME", (0, 0), (-1, -1), "HeiseiMin-W3"),
            ("ALIGN", (1, 0), (1, 0), "RIGHT"),
            ("RIGHTPADDING", (1, 0), (1, 0), 0),
        ])

        elements.append(date_table)
        elements.append(Spacer(1, 20))

        # =========================
        # 1. Conclusion (TOP)
        # =========================
        elements.append(Paragraph("1. 結論", styles["Heading2"]))
        elements.append(Spacer(1, 10))

        content = section_map.get("結論", "")
        lines = [line.strip() for line in content.split("\n") if line.strip()]

        bullet_items = []

        for line in lines:
            # remove existing bullet symbols if present
            if line.startswith("・") or line.startswith("-"):
                line = line[1:].strip()

            bullet_items.append(
                ListItem(
                    Paragraph(line, styles["BodyText"]),
                    bulletText="・"  
                )
            )

        if bullet_items:
            elements.append(ListFlowable(
                bullet_items,
                bulletType='bullet',
                leftIndent=20
            ))

        elements.append(Spacer(1, 20))

        # =========================
        # DATA SECTION
        # =========================

        # 2. Dataset
        elements.append(Paragraph("2. データセット情報", styles["Heading2"]))
        elements.append(Spacer(1, 10))
        elements.append(dataset_table)
        elements.append(Spacer(1, 20))

        # 3. Metrics Table
        elements.append(Paragraph("3. パフォーマンス指標", styles["Heading2"]))
        elements.append(Spacer(1, 10))
        elements.append(metrics_table)
        elements.append(Spacer(1, 20))

        elements.append(PageBreak())

        # 4. Metric Chart
        elements.append(Paragraph("4. 指標の可視化", styles["Heading2"]))
        elements.append(Spacer(1, 10))
        elements.append(Image(metric_chart, width=5 * inch, height=3 * inch))
        elements.append(Spacer(1, 20))

        # 5. Confusion Matrix
        elements.append(Paragraph("5. 混同行列", styles["Heading2"]))
        elements.append(Spacer(1, 10))
        elements.append(Image(confusion_chart, width=5 * inch, height=3 * inch))
        elements.append(Spacer(1, 30))

        elements.append(PageBreak())

        # =========================
        # ANALYSIS SECTION
        # =========================
        def add_section(title, key):
            elements.append(Paragraph(title, styles["Heading2"]))
            elements.append(Spacer(1, 10))

            content = section_map.get(key, "")
            lines = [line.strip() for line in content.split("\n") if line.strip()]

            bullet_items = []

            for line in lines:
                # remove bullet symbols if already present
                if line.startswith("・") or line.startswith("-"):
                    line = line[1:].strip()

                bullet_items.append(
                    ListItem(Paragraph(line, styles["BodyText"]))
                )

            if bullet_items:
                elements.append(ListFlowable(
                    bullet_items,
                    bulletType='bullet',
                    leftIndent=20
                ))
                elements.append(Spacer(1, 10))

        add_section("6. プロジェクト概要", "プロジェクト概要")
        add_section("7. モデル情報", "モデル情報")
        add_section("8. パフォーマンス指標分析", "パフォーマンス指標分析")
        add_section("9. 混同行列分析", "混同行列分析")
        add_section("10. エラー分析", "エラー分析")
        add_section("11. モデル信頼性評価", "モデル信頼性評価")
        add_section("12. 改善提案", "改善提案")
        # =========================
        # BUILD PDF
        # =========================
        doc = SimpleDocTemplate(pdf_path)
        doc.build(elements)