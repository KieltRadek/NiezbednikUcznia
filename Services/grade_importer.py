import csv
from datetime import datetime
from ModelsDataBase.DataBase import Session
from ModelsDataBase.Grade import Grade


class grade_importer:
    """
    Importuje plik CSV (z BOM UTF-8) do tabeli grades.
    """

    @staticmethod
    def import_from_csv(filename, user_id, clear_existing=False):
        session = Session()
        try:
            if clear_existing:
                session.query(Grade) \
                    .filter(Grade.user_id == user_id) \
                    .delete(synchronize_session=False)
                session.commit()

            count = 0
            with open(filename, mode='r', newline='', encoding='utf-8-sig') as fp:
                reader = csv.DictReader(fp)
                for row in reader:
                    date = datetime.fromisoformat(row["date"]).date()
                    subject = row.get("subject", "").strip()
                    grade_value = float(row.get("grade_value", "0").replace(",", "."))
                    comment = row.get("comment", "").strip()

                    gr = Grade(
                        user_id=user_id,
                        date=date,
                        subject=subject,
                        grade_value=grade_value,
                        comment=comment
                    )
                    session.add(gr)
                    count += 1

            session.commit()
            return count

        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
