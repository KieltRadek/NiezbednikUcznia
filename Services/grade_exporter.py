import csv

class grade_exporter:
    """
    Eksportuje listę obiektów Grade do pliku CSV z BOM UTF-8.
    """

    @staticmethod
    def export_to_csv(grades, filename):
        fieldnames = ["date", "subject", "grade_value", "comment"]
        with open(filename, mode='w', newline='', encoding='utf-8-sig') as fp:
            writer = csv.DictWriter(fp, fieldnames=fieldnames)
            writer.writeheader()
            for g in grades:
                writer.writerow({
                    "date":        g.date.isoformat(),
                    "subject":     g.subject or "",
                    "grade_value": f"{g.grade_value:.1f}",
                    "comment":     g.comment or ""
                })
