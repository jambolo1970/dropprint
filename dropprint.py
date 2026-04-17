import os
import sys
import cups
import time
from pathlib import Path

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QAction, QColor, QFont, QIcon, QPixmap, QPainter
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


class DropPrint(QWidget):
    JOB_PENDING = getattr(cups, "IPP_JOB_PENDING", 3)
    JOB_HELD = getattr(cups, "IPP_JOB_HELD", 4)
    JOB_PROCESSING = getattr(cups, "IPP_JOB_PROCESSING", 5)
    JOB_STOPPED = getattr(cups, "IPP_JOB_STOPPED", 6)
    JOB_CANCELED = getattr(cups, "IPP_JOB_CANCELED", 7)
    JOB_ABORTED = getattr(cups, "IPP_JOB_ABORTED", 8)
    JOB_COMPLETED = getattr(cups, "IPP_JOB_COMPLETED", 9)

    def __init__(self):
        super().__init__()
        try:
            self.conn = cups.Connection()
            self.printers = self.conn.getPrinters()
        except Exception as e:
            print(f"Errore CUPS: {e}")
            sys.exit(1)

        if not self.printers:
            QMessageBox.critical(None, "DropPrint", "Nessuna stampante trovata in CUPS.")
            sys.exit(1)

        self.active_jobs = {}
        self.init_ui()
        self.init_tray()

        self.monitor_timer = QTimer(self)
        self.monitor_timer.timeout.connect(self.update_jobs_status)
        self.monitor_timer.start(2000)

    def init_ui(self):
        self.setWindowTitle("DropPrint")
        self.setMinimumSize(800, 600)
        self.setWindowIcon(self.build_app_icon())

        main_layout = QVBoxLayout()

        top_layout = QHBoxLayout()
        header = QLabel("DropPrint")
        header.setFont(QFont("sans-serif", 22, QFont.Weight.Bold))
        top_layout.addWidget(header)
        top_layout.addStretch()

        printer_box = QVBoxLayout()
        printer_box.addWidget(QLabel("Stampante attiva:"))
        self.printer_combo = QComboBox()
        self.printer_combo.addItems(sorted(self.printers.keys()))
        self.printer_combo.setMinimumWidth(250)
        printer_box.addWidget(self.printer_combo)
        top_layout.addLayout(printer_box)
        main_layout.addLayout(top_layout)

        self.drop_frame = QFrame()
        self.drop_frame.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Sunken)
        self.drop_frame.setStyleSheet(
            "QFrame { border: 3px dashed #35b9ab; border-radius: 20px; background-color: #f0fdfa; }"
        )

        frame_layout = QVBoxLayout(self.drop_frame)
        self.drop_label = QLabel("Trascina qui i file per stampare\n(PDF, JPG, PNG, TXT)")
        self.drop_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.drop_label.setFont(QFont("sans-serif", 12))
        frame_layout.addWidget(self.drop_label)

        self.file_list = QListWidget()
        self.file_list.setStyleSheet(
            "QListWidget { background: white; border-radius: 10px; padding: 5px; font-size: 12pt; }"
        )
        frame_layout.addWidget(self.file_list)
        main_layout.addWidget(self.drop_frame)

        self.status_bar = QStatusBar()
        main_layout.addWidget(self.status_bar)
        self.setLayout(main_layout)
        self.setAcceptDrops(True)

    def build_app_icon(self):
        icon_path = Path.home() / ".local/share/dropprint/icon.png"
        if icon_path.exists():
            return QIcon(str(icon_path))

        pixmap = QPixmap(64, 64)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QColor("#35b9ab"))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(4, 4, 56, 56, 12, 12)
        painter.setPen(QColor("white"))
        font = QFont("sans-serif", 28, QFont.Weight.Bold)
        painter.setFont(font)
        painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, "DP")
        painter.end()
        return QIcon(pixmap)

    def init_tray(self):
        self.tray_icon = None
        if not QSystemTrayIcon.isSystemTrayAvailable():
            self.status_bar.showMessage("System tray non disponibile in questo ambiente desktop.", 5000)
            return

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.windowIcon())
        self.tray_icon.setToolTip("DropPrint")

        tray_menu = QMenu()
        show_action = QAction("Apri DropPrint", self)
        show_action.triggered.connect(self.show_normal)
        tray_menu.addAction(show_action)

        hide_action = QAction("Nascondi", self)
        hide_action.triggered.connect(self.hide)
        tray_menu.addAction(hide_action)

        tray_menu.addSeparator()

        quit_action = QAction("Esci", self)
        quit_action.triggered.connect(QApplication.instance().quit)
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.on_tray_activated)
        self.tray_icon.show()

    def on_tray_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            if self.isVisible():
                self.hide()
            else:
                self.show_normal()

    def show_normal(self):
        self.show()
        self.raise_()
        self.activateWindow()

    def closeEvent(self, event):
        if self.tray_icon and self.tray_icon.isVisible():
            self.hide()
            self.tray_icon.showMessage(
                "DropPrint",
                "L'applicazione è ancora attiva nel vassoio di sistema.",
                QSystemTrayIcon.MessageIcon.Information,
                2500,
            )
            event.ignore()
            return
        event.accept()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
            self.drop_frame.setStyleSheet(
                "QFrame { border: 3px solid #2da094; background-color: #ccf2ef; border-radius: 20px; }"
            )
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        self.drop_frame.setStyleSheet(
            "QFrame { border: 3px dashed #35b9ab; border-radius: 20px; background-color: #f0fdfa; }"
        )

    def dropEvent(self, event):
        self.drop_frame.setStyleSheet(
            "QFrame { border: 3px dashed #35b9ab; border-radius: 20px; background-color: #f0fdfa; }"
        )
        files = [u.toLocalFile() for u in event.mimeData().urls() if u.isLocalFile()]
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
                    "last_state": None,
                }
                self.status_bar.showMessage(f"Inviato a {printer_name}: {file_name}", 3000)
            except Exception as e:
                self.status_bar.showMessage(f"Errore di stampa: {e}", 7000)

    def get_job_state(self, job_id, cups_jobs):
        job_info = cups_jobs.get(job_id)
        if job_info:
            state = job_info.get("job-state")
            if state is not None:
                return state, job_info

        try:
            attrs = self.conn.getJobAttributes(job_id)
            return attrs.get("job-state"), attrs
        except Exception:
            return None, None

    def mark_completed(self, info, current_time):
        item = info["item"]
        if info["finish_time"] is None:
            item.setText(f"✅ {info['file_name']} - Stampato")
            item.setForeground(QColor("green"))
            info["finish_time"] = current_time
            self.status_bar.showMessage(f"Completato: {info['file_name']}", 3000)
            if self.tray_icon:
                self.tray_icon.showMessage(
                    "DropPrint",
                    f"Stampato: {info['file_name']}",
                    QSystemTrayIcon.MessageIcon.Information,
                    2500,
                )

    def mark_failed(self, info, label):
        item = info["item"]
        item.setText(f"❌ {info['file_name']} - {label}")
        item.setForeground(QColor("darkred"))
        if info["finish_time"] is None:
            info["finish_time"] = time.time()

    def update_jobs_status(self):
        if not self.active_jobs:
            return

        current_time = time.time()
        try:
            cups_jobs = self.conn.getJobs(which_jobs="all", my_jobs=True)
        except Exception:
            cups_jobs = {}

        jobs_to_remove = []

        for job_id, info in list(self.active_jobs.items()):
            item = info["item"]
            state, _job_info = self.get_job_state(job_id, cups_jobs)

            if state is None:
                # Se il job non è più recuperabile da CUPS, lo consideriamo completato.
                self.mark_completed(info, current_time)
            elif state == self.JOB_COMPLETED:
                self.mark_completed(info, current_time)
            elif state in (self.JOB_PENDING, self.JOB_HELD):
                item.setText(f"⏳ {info['file_name']} - In coda...")
                item.setForeground(QColor("red"))
            elif state == self.JOB_PROCESSING:
                item.setText(f"🖨️ {info['file_name']} - In stampa...")
                item.setForeground(QColor("darkorange"))
            elif state == self.JOB_STOPPED:
                self.mark_failed(info, "Lavoro fermato")
            elif state == self.JOB_CANCELED:
                self.mark_failed(info, "Annullato")
            elif state == self.JOB_ABORTED:
                self.mark_failed(info, "Errore di stampa")
            else:
                item.setText(f"ℹ️ {info['file_name']} - Stato job: {state}")
                item.setForeground(QColor("blue"))

            if info["finish_time"] is not None and current_time - info["finish_time"] > 60:
                jobs_to_remove.append(job_id)

        for job_id in jobs_to_remove:
            item_to_del = self.active_jobs[job_id]["item"]
            row = self.file_list.row(item_to_del)
            if row >= 0:
                self.file_list.takeItem(row)
            del self.active_jobs[job_id]


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("DropPrint")
    app.setQuitOnLastWindowClosed(False)
    app.setStyle("Fusion")

    window = DropPrint()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
