# Services/schedule_importer.py

import csv
from datetime import datetime
from ModelsDataBase.DataBase import Session
from ModelsDataBase.Schedule import Schedule

class ScheduleImporter:
    """
    Importuje plan z CSV (UTF-8 with BOM) do tabeli schedule.
    """

    @staticmethod
    def import_from_csv(filename, user_id, clear_existing=False):
        session = Session()
        try:
            if clear_existing:
                session.query(Schedule) \
                       .filter(Schedule.user_id == user_id) \
                       .delete(synchronize_session=False)
                session.commit()

            count = 0
            with open(filename, mode='r', newline='', encoding='utf-8-sig') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    date = datetime.fromisoformat(row["date"]).date()
                    start_time = datetime.strptime(row["start_time"], "%H:%M").time()
                    end_time   = datetime.strptime(row["end_time"],   "%H:%M").time()

                    sch = Schedule(
                        user_id=user_id,
                        date=date,
                        day_of_week=row.get("day_of_week", date.strftime("%A")),
                        start_time=start_time,
                        end_time=end_time,
                        code=row.get("code", ""),
                        subject=row.get("subject", ""),
                        type=row.get("type", ""),
                        group=row.get("group", ""),
                        teacher=row.get("teacher", ""),
                        building=row.get("building", ""),
                        room=row.get("room", ""),
                        student_count=int(row.get("student_count") or 0)
                    )
                    session.add(sch)
                    count += 1

            session.commit()
            return count

        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
