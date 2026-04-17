from __future__ import annotations

import os
import sys
import time
from pathlib import Path

import cups
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QAction, QColor, QCloseEvent, QFont, QIcon
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMenu,
    QMessageBox,
    QStatusBar,
    QSystemTrayIcon,
    QVBoxLayout,
    QWidget,
)


JOB_STATE_LABELS = {
    2: "Sconosciuto",
    3: "In coda",
    4: "In attesa",
    5: "In stampa",
    6: "Fermato",
    7: "Annullato",
    8: "Errore",
    9: "Completato",
}

ACTIVE_STATES = {3, 4, 5, 6}
DONE_STATES = {7, 8, 9}


def resource_path(*parts: str) -> str:
    base = Path(__file__).resolve().parent
    return str(base.joinpath(*parts))


class DropPrint(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.conn = self._connect_cups()
        self.printers = self.conn.getPrinters()
        self.active_jobs: dict[int, dict[str, object]] = {}
        self._tray_enabled = False

        self.init_ui()
        self.init_tray()

        self.monitor_timer = QTimer(self)
        self.monitor_timer.timeout.connect(self.update_jobs_status)
        self.monitor_timer.start(2000)

    def _connect_cups(self) -> cups.Connection:
        try:
            return cups.Connection()
        except Exception as exc:
            QMessageBox.critical(None, "Errore CUPS", f"Impossibile connettersi a CUPS:\n{exc}")
            raise SystemExit(1)

    def init_ui(self) -> None:
        self.setWindowTitle("DropPrint")
        self.setMinimumSize(840, 620)
        self.setWindowIcon(QIcon(resource_path("assets", "dropprint.png")))

        main_layout = QVBoxLayout()

        top_layout = QHBoxLayout()
        header = QLabel("DropPrint")
        header.setFont(QFont("Sans Serif", 22, QFont.Weight.Bold))
        top_layout.addWidget(header)
        top_layout.addStretch()

        printer_box = QVBoxLayout()
        printer_box.addWidget(QLabel("Stampante attiva:"))
        self.printer_combo = QComboBox()
        self.printer_combo.addItems(sorted(self.printers.keys()))
        self.printer_combo.setMinimumWidth(260)
        printer_box.addWidget(self.printer_combo)
        top_layout.addLayout(printer_box)
        main_layout.addLayout(top_layout)

        self.drop_frame = QFrame()
        self.drop_frame.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Sunken)
        self.drop_frame.setStyleSheet(
            "QFrame { border: 3px dashed #35b9ab; border-radius: 20px; background-color: #f0fdfa; }"
        )

        frame_layout = QVBoxLayout(self.drop_frame)
        self.drop_label = QLabel("Trascina qui i file per stamparli")
        self.drop_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.drop_label.setFont(QFont("Sans Serif", 12))
        frame_layout.addWidget(self.drop_label)

        self.file_list = QListWidget()
        self.file_list.setStyleSheet(
            "QListWidget { background: white; border-radius: 10px; padding: 6px; font-size: 12pt; }"
        )
        frame_layout.addWidget(self.file_list)
        main_layout.addWidget(self.drop_frame)

        self.status_bar = QStatusBar()
        main_layout.addWidget(self.status_bar)

        self.setLayout(main_layout)
        self.setAcceptDrops(True)

    def init_tray(self) -> None:
        if not QSystemTrayIcon.isSystemTrayAvailable():
            return

        tray_icon = QIcon(resource_path("assets", "dropprint.png"))
        self.tray = QSystemTrayIcon(tray_icon, self)
        self.tray.setToolTip("DropPrint")

        tray_menu = QMenu()
        show_action = QAction("Apri DropPrint", self)
        show_action.triggered.connect(self.show_from_tray)
        tray_menu.addAction(show_action)

        hide_action = QAction("Nascondi", self)
        hide_action.triggered.connect(self.hide)
        tray_menu.addAction(hide_action)

        tray_menu.addSeparator()

        quit_action = QAction("Esci", self)
        quit_action.triggered.connect(self.exit_application)
        tray_menu.addAction(quit_action)

        self.tray.setContextMenu(tray_menu)
        self.tray.activated.connect(self.on_tray_activated)
        self.tray.show()
        self._tray_enabled = True

    def on_tray_activated(self, reason: QSystemTrayIcon.ActivationReason) -> None:
        if reason in (
            QSystemTrayIcon.ActivationReason.Trigger,
            QSystemTrayIcon.ActivationReason.DoubleClick,
        ):
            if self.isVisible():
                self.hide()
            else:
                self.show_from_tray()

    def show_from_tray(self) -> None:
        self.show()
        self.raise_()
        self.activateWindow()

    def exit_application(self) -> None:
        if self._tray_enabled:
            self.tray.hide()
        QApplication.instance().quit()

    def closeEvent(self, event: QCloseEvent) -> None:
        if self._tray_enabled:
            event.ignore()
            self.hide()
            self.status_bar.showMessage("DropPrint è ancora attivo nel vassoio di sistema.", 4000)
            self.tray.showMessage(
                "DropPrint",
                "L'app resta attiva nel vassoio di sistema.",
                QSystemTrayIcon.MessageIcon.Information,
                2500,
            )
            return
        event.accept()

    def dragEnterEvent(self, event) -> None:
        if event.mimeData().hasUrls():
            event.accept()
            self.drop_frame.setStyleSheet(
                "QFrame { border: 3px solid #2da094; background-color: #ccf2ef; border-radius: 20px; }"
            )
        else:
            event.ignore()

    def dragLeaveEvent(self, event) -> None:
        self.drop_frame.setStyleSheet(
            "QFrame { border: 3px dashed #35b9ab; background-color: #f0fdfa; border-radius: 20px; }"
        )

    def dropEvent(self, event) -> None:
        self.drop_frame.setStyleSheet(
            "QFrame { border: 3px dashed #35b9ab; background-color: #f0fdfa; border-radius: 20px; }"
        )
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        printer_name = self.printer_combo.currentText()

        for file_path in files:
            file_name = os.path.basename(file_path)
            try:
                job_id = self.conn.printFile(printer_name, file_path, file_name, {})
                item = QListWidgetItem(f"⏳ {file_name} (ID: {job_id})")
                item.setForeground(QColor("red"))
                self.file_list.addItem(item)
                self.active_jobs[job_id] = {
                    "item": item,
                    "file_name": file_name,
                    "finish_time": None,
                    "last_state": 3,
                }
                self.status_bar.showMessage(f"Inviato in stampa: {file_name}", 3000)
            except Exception as exc:
                self.status_bar.showMessage(f"Errore durante l'invio di {file_name}: {exc}", 5000)

    def get_job_info(self, job_id: int):
        try:
            return self.conn.getJobAttributes(job_id)
        except Exception:
            return None

    def update_jobs_status(self) -> None:
        if not self.active_jobs:
            return

        current_time = time.time()
        jobs_to_remove: list[int] = []

        for job_id, info in list(self.active_jobs.items()):
            item = info["item"]
            file_name = info["file_name"]
            job_info = self.get_job_info(job_id)
            job_state = None if not job_info else job_info.get("job-state")

            if job_state in ACTIVE_STATES:
                state_text = JOB_STATE_LABELS.get(job_state, "In lavorazione")
                prefix = "🖨️" if job_state == 5 else "⏳"
                color = QColor("orange") if job_state == 5 else QColor("red")
                item.setText(f"{prefix} {file_name} - {state_text}")
                item.setForeground(color)
                info["last_state"] = job_state
                continue

            if job_state in DONE_STATES:
                self._mark_finished(job_state, info, current_time)
            elif job_state is None:
                last_state = info.get("last_state")
                assumed_state = 9 if last_state in ACTIVE_STATES else 2
                self._mark_finished(assumed_state, info, current_time)

            finish_time = info.get("finish_time")
            if isinstance(finish_time, (int, float)) and current_time - finish_time > 60:
                jobs_to_remove.append(job_id)

        for job_id in jobs_to_remove:
            item_to_del = self.active_jobs[job_id]["item"]
            row = self.file_list.row(item_to_del)
            self.file_list.takeItem(row)
            del self.active_jobs[job_id]

    def _mark_finished(self, job_state: int, info: dict[str, object], current_time: float) -> None:
        item = info["item"]
        file_name = str(info["file_name"])
        if info.get("finish_time") is None:
            if job_state == 9:
                item.setText(f"✅ {file_name} - Completato")
                item.setForeground(QColor("green"))
                self.status_bar.showMessage(f"Completato: {file_name}", 3000)
            elif job_state == 7:
                item.setText(f"❌ {file_name} - Annullato")
                item.setForeground(QColor("#b91c1c"))
                self.status_bar.showMessage(f"Annullato: {file_name}", 3000)
            elif job_state == 8:
                item.setText(f"⚠️ {file_name} - Errore di stampa")
                item.setForeground(QColor("#b91c1c"))
                self.status_bar.showMessage(f"Errore di stampa: {file_name}", 4000)
            else:
                item.setText(f"✅ {file_name} - Completato")
                item.setForeground(QColor("green"))
            info["finish_time"] = current_time
            info["last_state"] = job_state


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("DropPrint")
    app.setQuitOnLastWindowClosed(False)
    app.setStyle("Fusion")
    window = DropPrint()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
