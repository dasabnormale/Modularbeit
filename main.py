import sys
import traceback
import mysql.connector

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QMessageBox, QDialog,
    QFormLayout, QLineEdit, QTextEdit, QDateEdit, QTimeEdit,
    QDialogButtonBox, QComboBox, QCheckBox
)
from PyQt5.QtCore import QTimer, QDate, QTime
from PyQt5.QtWidgets import QAbstractItemView
from datetime import datetime, date, time, timedelta

# --------------- Konfiguration ---------------
DB_CONFIG = {
    "host": "192.168.0.14",
    "user": "pi",
    "password": "pi",
    "database": "Modularbeit",
    "use_pure": True
}

# --------------- Helfer ---------------
def verbinde_datenbank():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        # Optional: Session-TZ auf lokale Zeit setzen (falls deine MySQL-Timezone-Tables nicht installiert sind, nimm +02:00 im Sommer)
        # with conn.cursor() as cur:
        #     cur.execute("SET time_zone = '+02:00'")
        return conn
    except Exception:
        traceback.print_exc()
        raise

def lade_offene_todos():
    """Offene Todos inkl. RememberDateTime und IsNotified (für Statusanzeige)."""
    try:
        conn = verbinde_datenbank()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT t.TodoID, t.TodoName, t.TodoDescription,
                   s.StateDescription, p.Percent, e.Enddate,
                   r.RememberDateTime, r.IsNotified
            FROM TodoTodolist t
            JOIN TodoState s ON t.StateID = s.StateID
            JOIN TodoPercent p ON s.PercentID = p.PercentID
            JOIN TodoEnddate e ON t.EnddateID = e.EnddateID
            LEFT JOIN TodoRememberme r ON t.RemembermeID = r.RemembermeID
            WHERE p.Percent < 100
            ORDER BY t.TodoID
        """)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
    except Exception:
        traceback.print_exc()
        return []

def lade_done_todos():
    try:
        conn = verbinde_datenbank()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT t.TodoID, t.TodoName, s.StateDescription, p.Percent, e.Enddate
            FROM TodoTodolist t
            JOIN TodoState s ON t.StateID = s.StateID
            JOIN TodoPercent p ON s.PercentID = p.PercentID
            JOIN TodoEnddate e ON t.EnddateID = e.EnddateID
            WHERE p.Percent = 100
            ORDER BY t.TodoID
        """)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
    except Exception:
        traceback.print_exc()
        return []

def lade_percent_options():
    try:
        conn = verbinde_datenbank()
        cursor = conn.cursor()
        cursor.execute("SELECT PercentID, Percent FROM TodoPercent ORDER BY PercentID")
        opts = cursor.fetchall()
        cursor.close()
        conn.close()
        return opts
    except Exception:
        traceback.print_exc()
        return []

def speichere_neues_todo(name, desc, enddate, rem_dt):
    try:
        conn = verbinde_datenbank()
        cursor = conn.cursor()
        rememberme_id = None
        if rem_dt:
            cursor.execute(
                "INSERT INTO TodoRememberme (RememberDateTime, IsNotified) VALUES (%s, FALSE)",
                (rem_dt,)
            )
            rememberme_id = cursor.lastrowid
        cursor.execute("INSERT INTO TodoEnddate (Enddate) VALUES (%s)", (enddate,))
        enddate_id = cursor.lastrowid
        percent_id = 1  # Neu
        state_desc = "Neu"
        cursor.execute(
            "INSERT INTO TodoState (PercentID, StateDescription) VALUES (%s, %s)",
            (percent_id, state_desc)
        )
        state_id = cursor.lastrowid
        cursor.execute(
            "INSERT INTO TodoTodolist (TodoName, TodoDescription, StateID, EnddateID, RemembermeID) VALUES (%s, %s, %s, %s, %s)",
            (name, desc, state_id, enddate_id, rememberme_id)
        )
        todo_id = cursor.lastrowid
        cursor.execute("INSERT INTO TodoStateHistory (TodoID, StateID) VALUES (%s, %s)", (todo_id, state_id))
        if rememberme_id:
            cursor.execute(
                "INSERT INTO TodoRememberHistory (TodoID, RemembermeID) VALUES (%s, %s)",
                (todo_id, rememberme_id)
            )
        conn.commit()
        cursor.close()
        conn.close()
        return todo_id
    except Exception:
        traceback.print_exc()
        return None

def speichere_bearbeitung(todo_id, percent_id, desc, new_end=None, rem_dt=None):
    try:
        conn = verbinde_datenbank()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO TodoState (PercentID, StateDescription) VALUES (%s, %s)",
            (percent_id, desc)
        )
        sid = cursor.lastrowid
        cursor.execute("UPDATE TodoTodolist SET StateID=%s WHERE TodoID=%s", (sid, todo_id))
        cursor.execute("INSERT INTO TodoStateHistory (TodoID, StateID) VALUES (%s,%s)", (todo_id, sid))
        if new_end is not None:
            cursor.execute("INSERT INTO TodoEnddate (Enddate) VALUES (%s)", (new_end,))
            eid = cursor.lastrowid
            cursor.execute("UPDATE TodoTodolist SET EnddateID=%s WHERE TodoID=%s", (eid, todo_id))
        if rem_dt is not None:
            cursor.execute(
                "INSERT INTO TodoRememberme (RememberDateTime, IsNotified) VALUES (%s, FALSE)",
                (rem_dt,)
            )
            rid = cursor.lastrowid
            cursor.execute("UPDATE TodoTodolist SET RemembermeID=%s WHERE TodoID=%s", (rid, todo_id))
            cursor.execute(
                "INSERT INTO TodoRememberHistory (TodoID, RemembermeID) VALUES (%s,%s)",
                (todo_id, rid)
            )
        conn.commit()
        cursor.close()
        conn.close()
    except Exception:
        traceback.print_exc()

# ---- Reminder-spezifische DB-Helfer ----
def lade_alle_offenen_erinnerungen():
    """Gibt (TodoID, Name, Beschreibung, RemembermeID, RememberDateTime) zurück,
       deren Erinnerung noch NICHT notifiziert ist. Zeitvergleich machen wir in Python (lokale Zeit)."""
    try:
        conn = verbinde_datenbank()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT t.TodoID, t.TodoName, t.TodoDescription, r.RemembermeID, r.RememberDateTime
            FROM TodoTodolist t
            JOIN TodoState s ON t.StateID = s.StateID
            JOIN TodoPercent p ON s.PercentID = p.PercentID
            JOIN TodoRememberme r ON t.RemembermeID = r.RemembermeID
            WHERE p.Percent < 100
              AND r.IsNotified = 0
            ORDER BY r.RememberDateTime ASC
        """)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
    except Exception:
        traceback.print_exc()
        return []

def setze_erinnerung_als_benachrichtigt(rememberme_id: int):
    try:
        conn = verbinde_datenbank()
        cursor = conn.cursor()
        cursor.execute("UPDATE TodoRememberme SET IsNotified = 1 WHERE RemembermeID = %s", (rememberme_id,))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception:
        traceback.print_exc()

def verschiebe_erinnerung(todo_id: int, new_dt: datetime):
    """Neue Rememberme anlegen, Todo darauf zeigen lassen, History schreiben."""
    try:
        conn = verbinde_datenbank()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO TodoRememberme (RememberDateTime, IsNotified) VALUES (%s, 0)",
            (new_dt,)
        )
        new_rid = cursor.lastrowid
        cursor.execute("UPDATE TodoTodolist SET RemembermeID=%s WHERE TodoID=%s", (new_rid, todo_id))
        cursor.execute(
            "INSERT INTO TodoRememberHistory (TodoID, RemembermeID) VALUES (%s, %s)",
            (todo_id, new_rid)
        )
        conn.commit()
        cursor.close()
        conn.close()
    except Exception:
        traceback.print_exc()

# --------------- Dialoge ---------------
class NewTodoDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Neues Todo anlegen")
        form = QFormLayout(self)
        self.input_name = QLineEdit()
        self.input_desc = QTextEdit()
        self.input_end = QDateEdit(calendarPopup=True)
        self.input_end.setDate(QDate.currentDate())
        self.input_rem_date = QDateEdit(calendarPopup=True)
        self.input_rem_date.setDate(QDate.currentDate())
        self.input_rem_time = QTimeEdit()
        self.input_rem_time.setTime(QTime.currentTime())
        form.addRow("Name:", self.input_name)
        form.addRow("Beschreibung:", self.input_desc)
        form.addRow("Enddatum:", self.input_end)
        form.addRow("Erinnerungsdatum (optional):", self.input_rem_date)
        form.addRow("Erinnerungsuhrzeit (optional):", self.input_rem_time)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        form.addWidget(buttons)

    def get_data(self):
        name = self.input_name.text().strip()
        desc = self.input_desc.toPlainText().strip()
        enddate = self.input_end.date().toPyDate()
        date_part = self.input_rem_date.date().toPyDate()
        time_part = self.input_rem_time.time().toPyTime()
        default_date = QDate.currentDate().toPyDate()
        default_time = QTime.currentTime().toPyTime()
        rem_dt = None
        if date_part != default_date or time_part != default_time:
            rem_dt = datetime.combine(date_part, time_part)
        return name, desc, enddate, rem_dt

class EditTodoDialog(QDialog):
    """Bearbeiten-Dialog für die ausgewählte Zeile (Offene Todos)."""
    def __init__(self, todo_row_data, parent=None):
        """
        todo_row_data:
          (TodoID, Name, Beschreibung, StateDescription, Percent, Enddate, RememberDateTime)
        """
        super().__init__(parent)
        self.setWindowTitle(f"Todo bearbeiten – ID {todo_row_data[0]}")
        self.todo_id = int(todo_row_data[0])

        form = QFormLayout(self)

        self.percent_opts = lade_percent_options()
        self.cb_percent = QComboBox()
        current_percent = todo_row_data[4]
        for pid, pct in self.percent_opts:
            self.cb_percent.addItem(f"{pct} %", pid)
            if current_percent is not None and str(pct) == str(current_percent):
                self.cb_percent.setCurrentIndex(self.cb_percent.count() - 1)

        self.txt_state_desc = QLineEdit(todo_row_data[3] or "")

        self.chk_change_end = QCheckBox("Enddatum ändern")
        self.de_end = QDateEdit(calendarPopup=True)
        if isinstance(todo_row_data[5], date):
            self.de_end.setDate(QDate(todo_row_data[5].year, todo_row_data[5].month, todo_row_data[5].day))
        else:
            try:
                d = datetime.strptime(str(todo_row_data[5]), "%Y-%m-%d").date()
                self.de_end.setDate(QDate(d.year, d.month, d.day))
            except Exception:
                self.de_end.setDate(QDate.currentDate())
        self.de_end.setEnabled(False)
        self.chk_change_end.toggled.connect(self.de_end.setEnabled)

        self.chk_change_rem = QCheckBox("Erinnerung ändern")
        self.de_rem_date = QDateEdit(calendarPopup=True)
        self.te_rem_time = QTimeEdit()
        rdt = todo_row_data[6]
        if isinstance(rdt, datetime):
            self.de_rem_date.setDate(QDate(rdt.year, rdt.month, rdt.day))
            self.te_rem_time.setTime(QTime(rdt.hour, rdt.minute, rdt.second))
        else:
            parsed = None
            for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"):
                try:
                    parsed = datetime.strptime(str(rdt), fmt)
                    break
                except Exception:
                    pass
            if parsed:
                self.de_rem_date.setDate(QDate(parsed.year, parsed.month, parsed.day))
                self.te_rem_time.setTime(QTime(parsed.hour, parsed.minute, parsed.second))
            else:
                self.de_rem_date.setDate(QDate.currentDate())
                self.te_rem_time.setTime(QTime.currentTime())
        self.de_rem_date.setEnabled(False)
        self.te_rem_time.setEnabled(False)
        self.chk_change_rem.toggled.connect(self.de_rem_date.setEnabled)
        self.chk_change_rem.toggled.connect(self.te_rem_time.setEnabled)

        form.addRow("Fortschritt (%):", self.cb_percent)
        form.addRow("Statusbeschreibung:", self.txt_state_desc)
        form.addRow(self.chk_change_end)
        form.addRow("Neues Enddatum:", self.de_end)
        form.addRow(self.chk_change_rem)
        form.addRow("Neues Erinnerungsdatum:", self.de_rem_date)
        form.addRow("Neue Erinnerungszeit:", self.te_rem_time)

        buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        form.addWidget(buttons)

    def get_changes(self):
        percent_id = self.cb_percent.currentData()
        desc = self.txt_state_desc.text().strip() or "Status aktualisiert"
        new_end = None
        rem_dt = None
        if self.chk_change_end.isChecked():
            new_end = self.de_end.date().toPyDate()
        if self.chk_change_rem.isChecked():
            rem_dt = datetime.combine(self.de_rem_date.date().toPyDate(),
                                      self.te_rem_time.time().toPyTime())
        return self.todo_id, percent_id, desc, new_end, rem_dt

class ReminderDialog(QDialog):
    """Dialog, der erscheint, wenn eine Erinnerung fällig ist."""
    def __init__(self, todo_name: str, current_dt: datetime, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Erinnerung")
        form = QFormLayout(self)

        name_field = QLineEdit(todo_name)
        name_field.setReadOnly(True)
        form.addRow("Todo:", name_field)

        self.de_date = QDateEdit(calendarPopup=True)
        self.te_time = QTimeEdit()
        suggested = datetime.now() + timedelta(hours=1)
        self.de_date.setDate(QDate(suggested.year, suggested.month, suggested.day))
        self.te_time.setTime(QTime(suggested.hour, suggested.minute, 0))

        form.addRow("Neue Erinnerung (Datum):", self.de_date)
        form.addRow("Neue Erinnerung (Zeit):", self.te_time)

        self.btns = QDialogButtonBox()
        self.btn_ok = self.btns.addButton("Neu setzen", QDialogButtonBox.AcceptRole)
        self.btn_ack = self.btns.addButton("Nur bestätigen", QDialogButtonBox.DestructiveRole)
        self.btn_cancel = self.btns.addButton(QDialogButtonBox.Cancel)

        self.btns.accepted.connect(self.accept)   # Neu setzen
        self.btns.rejected.connect(self.reject)   # Abbrechen
        self.btn_ack.clicked.connect(self._only_ack)

        form.addWidget(self.btns)
        self._only_acknowledged = False

    def _only_ack(self):
        self._only_acknowledged = True
        self.accept()

    def result_data(self):
        if self._only_acknowledged:
            return True, None
        new_dt = datetime.combine(self.de_date.date().toPyDate(), self.te_time.time().toPyTime())
        return False, new_dt

# --------------- GUI-Klasse ---------------
class TodoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📋 Todo Manager")
        self.resize(1150, 640)

        self.view_mode = "open"  # "open" oder "done"

        main_layout = QVBoxLayout(self)
        btn_layout = QHBoxLayout()

        self.btn_neu = QPushButton("Neues Todo")
        self.btn_bearbeiten = QPushButton("Bearbeiten")
        self.btn_historie = QPushButton("Historie")      # nur in 'done'
        self.btn_offen = QPushButton("Offene Todos")
        self.btn_erledigt = QPushButton("Erledigte Todos")
        self.btn_beenden = QPushButton("Beenden")

        for btn in (self.btn_neu, self.btn_bearbeiten, self.btn_historie, self.btn_offen, self.btn_erledigt, self.btn_beenden):
            btn_layout.addWidget(btn)

        self.table = QTableWidget()
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)

        main_layout.addLayout(btn_layout)
        main_layout.addWidget(self.table)

        # Verbindungen
        self.btn_neu.clicked.connect(self.todo_neu)
        self.btn_bearbeiten.clicked.connect(self.todo_bearbeiten)
        self.btn_historie.clicked.connect(self.zeige_historie_aus_auswahl)
        self.btn_offen.clicked.connect(lambda: self.switch_view("open"))
        self.btn_erledigt.clicked.connect(lambda: self.switch_view("done"))
        self.btn_beenden.clicked.connect(self.close)

        # Reminder-Check alle 60 Sekunden (Pausieren während Dialogen)
        self.reminder_timer = QTimer(self)
        self.reminder_timer.setInterval(60_000)
        self.reminder_timer.timeout.connect(self.pruefe_erinnerungen)
        self.reminder_timer.start()
        QTimer.singleShot(1000, self.pruefe_erinnerungen)

        self.switch_view("open")

    # ----- Ansicht wechseln -----
    def switch_view(self, mode):
        self.view_mode = mode
        if mode == "open":
            self.btn_offen.setEnabled(False)
            self.btn_offen.show()
            self.btn_erledigt.show()
            self.btn_erledigt.setEnabled(True)
            self.btn_bearbeiten.show()
            self.btn_historie.hide()
            self.set_table_headers(["ID","Name","Beschreibung","Status","%","Enddatum","Erinnerung","Erinn.-Status"])
            self.fill_open_table()
        else:
            self.btn_erledigt.hide()
            self.btn_offen.setEnabled(True)
            self.btn_offen.show()
            self.btn_bearbeiten.hide()
            self.btn_historie.show()
            self.set_table_headers(["ID","Name","Status","%","Enddatum"])
            self.fill_done_table()

    def set_table_headers(self, headers):
        self.table.clear()
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setRowCount(0)

    def fill_open_table(self):
        rows = lade_offene_todos()
        now = datetime.now()
        self.table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            # row: (ID, Name, Desc, StateDesc, Percent, Enddate, RememberDateTime, IsNotified)
            for j, val in enumerate(row):
                if j == 6 and isinstance(val, datetime):
                    self.table.setItem(i, j, QTableWidgetItem(val.strftime("%Y-%m-%d %H:%M:%S")))
                else:
                    self.table.setItem(i, j, QTableWidgetItem("" if val is None else str(val)))
            # Erinn.-Status Spalte (Index 7)
            rdt = row[6]
            is_notified = row[7]
            if rdt and not is_notified:
                status = "fällig" if rdt <= now else "geplant"
            elif rdt and is_notified:
                status = "abgehakt"
            else:
                status = "keine"
            self.table.setItem(i, 7, QTableWidgetItem(status))

    def fill_done_table(self):
        rows = lade_done_todos()
        self.table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem("" if val is None else str(val)))

    # ----- Aktionen -----
    def get_selected_row_data(self):
        sel = self.table.currentRow()
        if sel < 0:
            return None
        cols = self.table.columnCount()
        return tuple(self.table.item(sel, c).text() if self.table.item(sel, c) else "" for c in range(cols))

    def todo_neu(self):
        dlg = NewTodoDialog(self)
        if dlg.exec_() == QDialog.Accepted:
            try:
                name, desc, enddate, rem_dt = dlg.get_data()
                if not name:
                    raise ValueError("Der Name darf nicht leer sein.")
                todo_id = speichere_neues_todo(name, desc, enddate, rem_dt)
                if todo_id is None:
                    raise RuntimeError("Speichern in der Datenbank gescheitert.")
                QMessageBox.information(self, "Erfolg", f"Todo (ID {todo_id}) angelegt.")
                if self.view_mode == "open":
                    self.fill_open_table()
                else:
                    self.fill_done_table()
            except Exception as e:
                QMessageBox.critical(self, "Fehler beim Erstellen", str(e))
                traceback.print_exc()

    def todo_bearbeiten(self):
        if self.view_mode != "open":
            return
        row_data = self.get_selected_row_data()
        if not row_data:
            QMessageBox.information(self, "Info", "Bitte zuerst eine Zeile auswählen.")
            return

        def parse_int(s):
            try:
                return int(s)
            except Exception:
                return None

        def parse_date_str(s):
            try:
                return datetime.strptime(s, "%Y-%m-%d").date()
            except Exception:
                return None

        def parse_dt_str(s):
            for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"):
                try:
                    return datetime.strptime(s, fmt)
                except Exception:
                    pass
            return None

        reconstructed = (
            parse_int(row_data[0]),
            row_data[1],
            row_data[2],
            row_data[3],
            parse_int(row_data[4]),
            parse_date_str(row_data[5]),
            parse_dt_str(row_data[6])
        )

        dlg = EditTodoDialog(reconstructed, self)
        if dlg.exec_() == QDialog.Accepted:
            todo_id, percent_id, desc, new_end, rem_dt = dlg.get_changes()
            try:
                speichere_bearbeitung(todo_id, percent_id, desc, new_end, rem_dt)
                QMessageBox.information(self, "Erfolg", "Todo aktualisiert.")
                self.fill_open_table()
            except Exception as e:
                QMessageBox.critical(self, "Fehler beim Aktualisieren", str(e))
                traceback.print_exc()

    def zeige_historie_aus_auswahl(self):
        if self.view_mode != "done":
            return
        row_data = self.get_selected_row_data()
        if not row_data:
            QMessageBox.information(self, "Info", "Bitte zuerst eine Zeile auswählen.")
            return
        try:
            todo_id = int(row_data[0])
        except Exception:
            QMessageBox.warning(self, "Fehler", "Ungültige Auswahl.")
            return
        try:
            conn = verbinde_datenbank()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT h.ChangedAt, s.StateDescription, p.Percent
                FROM TodoStateHistory h
                JOIN TodoState s ON h.StateID=s.StateID
                JOIN TodoPercent p ON s.PercentID=p.PercentID
                WHERE h.TodoID=%s
                ORDER BY h.ChangedAt
            """, (todo_id,))
            hist = cursor.fetchall()
            cursor.execute("""
                SELECT rh.ChangedAt, r.RememberDateTime, r.IsNotified
                FROM TodoRememberHistory rh
                JOIN TodoRememberme r ON rh.RemembermeID=r.RemembermeID
                WHERE rh.TodoID=%s
                ORDER BY rh.ChangedAt
            """, (todo_id,))
            rems = cursor.fetchall()
            cursor.close()
            conn.close()
            text = "Statusverlauf:\n"
            for dt, desc, pct in hist:
                text += f"{dt} - {desc} ({pct}%)\n"
            text += "\nErinnerungshistorie:\n"
            for dt, rdt, notif in rems:
                text += f"{dt} - {rdt} | Erinnert: {notif}\n"
            dlg = QMessageBox(self)
            dlg.setWindowTitle(f"Verlauf – ID {todo_id}")
            dlg.setText(text)
            dlg.exec_()
        except Exception:
            traceback.print_exc()
            QMessageBox.critical(self, "Fehler", "Historie konnte nicht geladen werden.")

    # ----- Reminder-Check -----
    def pruefe_erinnerungen(self):
        # Timer pausieren, damit während Dialogen nichts reentriert
        self.reminder_timer.stop()
        try:
            all_open = lade_alle_offenen_erinnerungen()
            now = datetime.now()
            due = [row for row in all_open if isinstance(row[4], datetime) and row[4] <= now]
            if not due:
                return
            # mehrere nacheinander behandeln
            for todo_id, name, desc, rid, rdt in due:
                try:
                    dlg = ReminderDialog(name, rdt, self)
                    if dlg.exec_() == QDialog.Accepted:
                        only_ack, new_dt = dlg.result_data()
                        setze_erinnerung_als_benachrichtigt(rid)
                        if not only_ack and new_dt:
                            verschiebe_erinnerung(todo_id, new_dt)
                except Exception:
                    traceback.print_exc()
            # Tabelle auffrischen
            if self.view_mode == "open":
                self.fill_open_table()
            else:
                self.fill_done_table()
        finally:
            # Timer wieder starten
            self.reminder_timer.start()

# --------------- Programmstart ---------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TodoApp()
    window.show()
    sys.exit(app.exec_())
