# NiezbędnikUcznia (Student's Essential)

## 📚 Opis projektu

**NiezbędnikUcznia** to kompleksowa aplikacja desktopowa dla studentów, umożliwiająca zarządzanie planem zajęć, ocenami i statystykami. Aplikacja oferuje intuicyjny interfejs graficzny oparty na Tkinter oraz bazę danych SQLite do przechowywania danych użytkowników.

### Główne funkcje:
- 👤 **System rejestracji i logowania** - bezpieczne konta użytkowników
- 📅 **Plan zajęć** - wizualizacja tygodniowego planu z możliwością dodawania zajęć
- 📊 **Moduł ocen** - śledzenie ocen z różnych przedmiotów
- 📈 **Statystyki** - automatyczne obliczanie średniej, min, max ocen
- 💾 **Import/Eksport** - obsługa plików CSV dla planu i ocen
- 🔄 **Powtarzające się zajęcia** - automatyczne generowanie cyklicznych wydarzeń

## 🛠️ Technologie

- **Python** (100%) - główny język programowania
- **Tkinter** - interfejs graficzny użytkownika
- **SQLAlchemy** - ORM do zarządzania bazą danych
- **SQLite** - baza danych
- **CSV** - import/eksport danych

## 📋 Wymagania

### Oprogramowanie:
- Python 3.8 lub nowszy
- SQLAlchemy 2.0+

### Biblioteki Python:
```bash
sqlalchemy
tkinter (zazwyczaj wbudowany w Pythona)
```

## 🚀 Instalacja

### 1. Sklonuj repozytorium

```bash
git clone https://github.com/KieltRadek/NiezbednikUcznia.git
cd NiezbednikUcznia
```

### 2. Zainstaluj zależności

```bash
pip install sqlalchemy
```

### 3. Utwórz bazę danych

```bash
python ModelsDataBase/CreateDataBase(setup).py
```

Ten skrypt utworzy plik `UsersDatabase.db` z tabelami:
- `users` - dane użytkowników
- `schedule` - plan zajęć
- `grades` - oceny

### 4. Uruchom aplikację

```bash
python Main.py
```

## 📖 Instrukcja użytkowania

### Pierwsze uruchomienie

1. **Rejestracja**
   - Po uruchomieniu aplikacji kliknij "Register"
   - Wypełnij formularz: imię, nazwisko, email, hasło
   - Kliknij "Confirm"

2. **Logowanie**
   - Wprowadź email i hasło
   - Kliknij "Confirm"
   - Po zalogowaniu zobaczysz menu główne

### Menu główne

Dostępne opcje:
- **Schedule** - zarządzanie planem zajęć
- **Grades** - moduł ocen
- **Statistics** - statystyki ocen

### 📅 Plan zajęć (Schedule)

#### Dodawanie zajęć:

1. Kliknij "+ Dodaj zajęcia"
2. Wypełnij formularz:
   - Kod przedmiotu (np. "MAT101")
   - Nazwa przedmiotu (np. "Matematyka")
   - Typ zajęć (Wykład/Ćwiczenia/Laboratorium)
   - Grupy (np. "1A")
   - Dydaktyk (nazwisko prowadzącego)
   - Budynek i sala
   - Liczba studentów
   - Godzina rozpoczęcia (HH:MM)
   - Godzina zakończenia (HH:MM)
   - Data (YYYY-MM-DD)
3. Wybierz opcję powtarzania (brak/co tydzień/co 2 tygodnie/co miesiąc)
4. Kliknij "Zapisz"

#### Dozwolone przedziały czasowe:
```
08:30 - 10:00
10:15 - 11:45
12:15 - 13:45
14:00 - 15:30
15:45 - 17:15
17:30 - 19:00
19:15 - 20:45
```

#### Nawigacja:
- **< Poprzedni tydzień** - wyświetl poprzedni tydzień
- **Następny tydzień >** - wyświetl następny tydzień

#### Usuwanie zajęć:
1. Kliknij na zajęcia w planie (zmienią kolor na jasnoniebieski)
2. Można zaznaczyć wiele zajęć
3. Kliknij "Usuń zajęcia"
4. Potwierdź usunięcie

#### Import/Eksport:

**Eksport do CSV:**
1. Kliknij "↯ Eksportuj plan"
2. Wybierz lokalizację i nazwę pliku
3. Plan zostanie zapisany w formacie CSV (UTF-8 with BOM)

**Import z CSV:**
1. Kliknij "+ Importuj plan"
2. Wybierz plik CSV
3. Zdecyduj czy usunąć istniejące zajęcia
4. Potwierdź import

**Format CSV planu:**
```csv
date,day_of_week,start_time,end_time,code,subject,type,group,teacher,building,room,student_count
2025-01-15,Monday,08:30,10:00,MAT101,Matematyka,Wykład,1A,Dr Kowalski,A,101,30
```

### 📊 Moduł ocen (Grades)

#### Dodawanie oceny:

1. Kliknij "+ Dodaj ocenę"
2. Wypełnij formularz:
   - Data (YYYY-MM-DD)
   - Przedmiot
   - Ocena (format: 3.5 lub 3,5)
   - Komentarz (opcjonalnie)
3. Kliknij "Zapisz"

#### Usuwanie ocen:
1. Zaznacz oceny w tabeli (Ctrl+klik dla wielokrotnego zaznaczenia)
2. Kliknij "Usuń zaznaczone"
3. Potwierdź usunięcie

#### Import/Eksport ocen:

**Eksport:**
1. Kliknij "↯ Eksportuj oceny"
2. Wybierz lokalizację pliku
3. Oceny zostaną zapisane w CSV

**Import:**
1. Kliknij "+ Importuj oceny"
2. Wybierz plik CSV
3. Zdecyduj czy wyczyścić istniejące oceny
4. Potwierdź

**Format CSV ocen:**
```csv
date,subject,grade_value,comment
2025-01-15,Matematyka,4.5,Egzamin końcowy
2025-01-20,Fizyka,3.0,Kolokwium
```

### 📈 Statystyki (Statistics)

Automatycznie wyświetlane dane:
- **Liczba ocen** - całkowita liczba wprowadzonych ocen
- **Średnia ocen** - obliczona z dokładnością do 2 miejsc po przecinku
- **Najwyższa ocena** - maksymalna ocena
- **Najniższa ocena** - minimalna ocena

**Eksport statystyk:**
1. Kliknij "Export"
2. Plik zostanie zapisany jako `statistics_user_{user_id}.csv`

## 📁 Struktura projektu

```
NiezbednikUcznia/
├── GUI/
│   ├── LoginOrRegister.py      # Okno wyboru logowania/rejestracji
│   ├── LoginWindow.py           # Okno logowania
│   ├── RegisterWindow.py        # Okno rejestracji
│   ├── MainMenuView.py          # Menu główne
│   ├── ScheduleWindow.py        # Zarządzanie planem zajęć
│   ├── GradesWindow.py          # Moduł ocen
│   └── StatisticWindow.py       # Okno statystyk
│
├── ModelsDataBase/
│   ├── DataBase.py              # Konfiguracja bazy danych (SQLAlchemy)
│   ├── User.py                  # Model użytkownika
│   ├── Schedule.py              # Model planu zajęć
│   ├── Grade.py                 # Model ocen
│   └── CreateDataBase(setup).py # Skrypt tworzący bazę
│
├── Services/
│   ├── schedule_exporter.py     # Eksport planu do CSV
│   ├── schedule_importer.py     # Import planu z CSV
│   ├── grade_exporter.py        # Eksport ocen do CSV
│   └── grade_importer.py        # Import ocen z CSV
│
├── Main.py                      # Główny plik uruchomieniowy
└── README.md                    # Dokumentacja
```

## 🗄️ Struktura bazy danych

### Tabela `users`
| Kolumna  | Typ     | Opis              |
|----------|---------|-------------------|
| id       | Integer | Klucz główny      |
| name     | String  | Imię użytkownika  |
| surname  | String  | Nazwisko          |
| email    | String  | Email (login)     |
| password | String  | Hasło             |

### Tabela `schedule`
| Kolumna       | Typ     | Opis                        |
|---------------|---------|-----------------------------|
| id            | Integer | Klucz główny                |
| user_id       | Integer | FK do users                 |
| date          | Date    | Data zajęć                  |
| day_of_week   | String  | Dzień tygodnia              |
| start_time    | Time    | Godzina rozpoczęcia         |
| end_time      | Time    | Godzina zakończenia         |
| code          | String  | Kod przedmiotu              |
| subject       | String  | Nazwa przedmiotu            |
| type          | String  | Typ zajęć                   |
| group         | String  | Grupa                       |
| teacher       | String  | Prowadzący                  |
| building      | String  | Budynek                     |
| room          | String  | Sala                        |
| student_count | Integer | Liczba studentów            |

### Tabela `grades`
| Kolumna     | Typ     | Opis             |
|-------------|---------|------------------|
| id          | Integer | Klucz główny     |
| user_id     | Integer | FK do users      |
| date        | Date    | Data oceny       |
| subject     | String  | Przedmiot        |
| grade_value | Float   | Wartość oceny    |
| comment     | String  | Komentarz        |

## 🎨 Schemat kolorów

Aplikacja wykorzystuje spójną paletę kolorów:
- **PeachPuff2** (#FFDAB9) - tło okien
- **PeachPuff3** (#CDAA7D) - przyciski i pola tekstowe
- **Salmon** (#FA8072) - przyciski usuwania
- **LightBlue** (#ADD8E6) - przyciski importu
- **LightGreen** (#90EE90) - przyciski eksportu
- **#e6f3ff** - tło zajęć w planie

## 🔐 Bezpieczeństwo

⚠️ **Uwaga:** Aktualna wersja przechowuje hasła w postaci jawnej (plain text). 
**Nie używaj tej aplikacji do przechowywania wrażliwych danych produkcyjnych.**

Rekomendacje dla wersji produkcyjnej:
- Implementacja hashowania haseł (np. bcrypt, argon2)
- Walidacja siły hasła
- Dodanie mechanizmu odzyskiwania hasła
- Implementacja sesji użytkownika z timeout

## 🐛 Znane ograniczenia

- Hasła przechowywane bez hashowania
- Brak walidacji formatu email
- Brak mechanizmu wylogowania
- Plan zajęć ograniczony do 7 predefiniowanych slotów czasowych
- Import/eksport nie obsługuje attachmentów czy notatek

## 🚧 Przyszłe rozszerzenia

Planowane funkcjonalności:
- [ ] Kalendarz z widokiem miesięcznym
- [ ] Powiadomienia o zbliżających się zajęciach
- [ ] Notatki do zajęć
- [ ] Tryb ciemny (dark mode)
- [ ] Eksport do formatu PDF
- [ ] Integracja z Google Calendar
- [ ] Mobilna wersja aplikacji
- [ ] Synchronizacja w chmurze

## 🤝 Rozwój projektu

Chcesz przyczynić się do rozwoju?
1. Fork repozytorium
2. Utwórz branch: `git checkout -b feature/nowa-funkcja`
3. Commit zmian: `git commit -am 'Dodaj nową funkcję'`
4. Push: `git push origin feature/nowa-funkcja`
5. Otwórz Pull Request

## 📝 Przykłady użycia

### Przykład 1: Tworzenie użytkownika programowo

```python
from ModelsDataBase.DataBase import Session
from ModelsDataBase.User import User

session = Session()
new_user = User(
    name="Jan",
    surname="Kowalski",
    email="jan.kowalski@example.com",
    password="password123"
)
session.add(new_user)
session.commit()
session.close()
```

### Przykład 2: Dodanie oceny programowo

```python
from ModelsDataBase.DataBase import Session
from ModelsDataBase.Grade import Grade
from datetime import date

session = Session()
grade = Grade(
    user_id=1,
    date=date(2025, 1, 15),
    subject="Matematyka",
    grade_value=4.5,
    comment="Egzamin końcowy"
)
session.add(grade)
session.commit()
session.close()
```

### Przykład 3: Dodanie zajęć programowo

```python
from ModelsDataBase.DataBase import Session
from ModelsDataBase.Schedule import Schedule
from datetime import date, time

session = Session()
schedule = Schedule(
    user_id=1,
    date=date(2025, 1, 15),
    day_of_week="Monday",
    start_time=time(8, 30),
    end_time=time(10, 0),
    code="MAT101",
    subject="Matematyka",
    type="Wykład",
    group="1A",
    teacher="Dr Kowalski",
    building="A",
    room="101",
    student_count=30
)
session.add(schedule)
session.commit()
session.close()
```

## 📄 Licencja

Projekt stworzony na potrzeby edukacyjne.

## 👤 Autor

**KieltRadek**
- GitHub: [@KieltRadek](https://github.com/KieltRadek)
- Repozytorium: [NiezbednikUcznia](https://github.com/KieltRadek/NiezbednikUcznia)

## 🙏 Podziękowania

Projekt powstał jako kompleksowa aplikacja demonstrująca:
- Wzorce projektowe w Pythonie
- Architekturę MVC
- Integrację GUI z bazą danych
- Obsługę importu/eksportu danych

---

**Ostatnia aktualizacja**: 2025-11-24