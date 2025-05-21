import sys
import os
# Qt plugin yolunu manuel olarak ayarlayın (Genellikle önerilmez, PyQt5 doğru kurulmalı)
# Eğer "This application failed to start because no Qt platform plugin could be initialized"
# hatası alıyorsanız ve başka çözüm bulamıyorsanız bu satırı kendi sisteminize göre
# düzenleyip aktif hale getirebilirsiniz. Ancak bu, taşınabilirliği azaltır.
# os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = r'C:\Users\HUAWEİ\AppData\Local\Programs\Python\Python313\Lib\site-packages\PyQt5\Qt5\plugins'

from PyQt5.QtWidgets import (QApplication, QMainWindow, QTextEdit, QAction,
                             QFileDialog, QMessageBox, QFontDialog, QStatusBar,
                             QToolBar, QMenu, QToolButton)
from PyQt5.QtGui import QFont, QIcon, QTextCursor, QFontMetrics, QFontDatabase, QFontInfo
from PyQt5.QtCore import Qt, QDate, QSize # QSysInfo kaldırıldı, kullanılmıyordu.
# Qt plugin yolunu manuel olarak ayarlayın
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = r'C:\Users\HUAWEİ\AppData\Local\Programs\Python\Python313\Lib\site-packages\PyQt5\Qt5\plugins'
# --- Stil Sayfaları (QSS) ---
SHARED_STYLES = """
QWidget {
    background-color: black;
    color: %(text_color)s;
    border: none;
}
QTextEdit {
    background-color: black;
    color: %(text_color)s;
    border: 1px solid %(border_color)s;
    selection-background-color: %(text_color)s;
    selection-color: black;
    padding: 5px;
}
QStatusBar {
    background-color: black;
    color: %(text_color)s;
    border-top: 1px solid %(border_color)s;
}
QStatusBar::item {
    border: none;
}
QMenuBar {
    background-color: black;
    color: %(text_color)s;
    border-bottom: 1px solid %(border_color)s;
    font-family: "Consolas", "DejaVu Sans Mono", "Courier New", monospace;
    font-size: 10pt;
}
QMenuBar::item {
    background-color: black;
    color: %(text_color)s;
    padding: 4px 10px;
}
QMenuBar::item:selected {
    background-color: %(text_color)s;
    color: black;
}
QMenu {
    background-color: black;
    color: %(text_color)s;
    border: 1px solid %(border_color)s;
    padding: 5px;
    font-family: "Consolas", "DejaVu Sans Mono", "Courier New", monospace;
    font-size: 10pt;
}
QMenu::item {
    padding: 5px 20px 5px 20px;
}
QMenu::item:selected {
    background-color: %(text_color)s;
    color: black;
}
QMenu::separator {
    height: 1px;
    background-color: %(border_color)s;
    margin-left: 10px;
    margin-right: 5px;
}
QToolBar {
    background-color: black;
    border-bottom: 1px solid %(border_color)s;
    spacing: 3px;
}
QToolButton {
    background-color: black;
    color: %(text_color)s;
    border: 1px solid %(border_color)s;
    padding: 4px;
    font-family: "Consolas", "DejaVu Sans Mono", "Courier New", monospace;
    font-size: 10pt;
}
QToolButton:hover {
    background-color: %(hover_bg_color)s;
    border: 1px solid %(text_color)s;
}
QToolButton:pressed {
    background-color: %(pressed_bg_color)s;
}
QToolButton:checked {
    background-color: %(text_color)s;
    color: black;
}
QScrollBar:vertical {
    border: 1px solid %(border_color)s; background: black; width: 15px; margin: 0px;
}
QScrollBar::handle:vertical { background: %(text_color)s; min-height: 20px; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { border: none; background: none; height: 0px;}
QScrollBar:horizontal {
    border: 1px solid %(border_color)s; background: black; height: 15px; margin: 0px;
}
QScrollBar::handle:horizontal { background: %(text_color)s; min-width: 20px; }
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { border: none; background: none; width: 0px;}

QDialog { background-color: black; color: %(text_color)s; border: 1px solid %(text_color)s; }
QDialog QLabel, QDialog QPushButton, QDialog QListView, QDialog QTreeView, QDialog QLineEdit {
    background-color: black; color: %(text_color)s;
    font-family: "Consolas", "DejaVu Sans Mono", "Courier New", monospace;
    font-size: 10pt;
}
QDialog QPushButton { border: 1px solid %(text_color)s; padding: 5px 10px; }
QDialog QPushButton:hover { background-color: %(hover_bg_color)s; }
QDialog QPushButton:pressed { background-color: %(pressed_bg_color)s; }
QDialog QListView, QDialog QTreeView { border: 1px solid %(border_color)s; selection-background-color: %(text_color)s; selection-color: black; }
QDialog QLineEdit { border: 1px solid %(border_color)s; }
"""

GREEN_THEME_COLORS = {
    "text_color": "#33FF33", "border_color": "#228B22",
    "hover_bg_color": "#115511", "pressed_bg_color": "#003300"
}
AMBER_THEME_COLORS = {
    "text_color": "#FFB000", "border_color": "#8B4513",
    "hover_bg_color": "#6F4F00", "pressed_bg_color": "#5F3F00"
}

RETRO_STYLE_GREEN = SHARED_STYLES % GREEN_THEME_COLORS
RETRO_STYLE_AMBER = SHARED_STYLES % AMBER_THEME_COLORS


class MBNotDefteri(QMainWindow):
    def __init__(self): # YAPICI METOT ADI DÜZELTİLDİ
        super().__init__()
        self.current_file = None
        self.current_theme_style_name = "green"

        self.base_font_family = "Consolas"
        self.base_font_size = 12

        self.initUI()
        self.apply_theme() # apply_theme çağrısı initUI'dan sonra ve font ayarlarını da içeriyor
        self.update_window_title()
        # self.statusBar().showMessage("mb not defteri Hazır.") # İsteğe bağlı başlangıç mesajı

    def initUI(self):
        self.setWindowTitle("mb not defteri")
        self.setGeometry(150, 150, 800, 600)

        self.text_area = QTextEdit()
        self.text_area.setAcceptRichText(False) # Düz metin için
        self.text_area.setCursorWidth(8) # Retro bir görünüm için kalın imleç
        self.setCentralWidget(self.text_area)

        self.setStatusBar(QStatusBar(self))

        self._create_actions()
        self._create_menu_bar()
        self._create_tool_bar()

        # Belge içeriği değiştiğinde pencere başlığını güncelle
        self.text_area.document().modificationChanged.connect(self.update_window_title)

    def _create_actions(self):
        # İkonlar için QIcon.fromTheme kullanılıyor. Sistemde ikon teması yoksa görünmeyebilir.
        # Daha taşınabilir bir çözüm için ikonları kaynak olarak eklemek veya dosyadan yüklemek gerekebilir.
        self.new_action = QAction(QIcon.fromTheme("document-new"), "&Yeni", self, shortcut="Ctrl+N", triggered=self.new_file)
        self.open_action = QAction(QIcon.fromTheme("document-open"), "&Aç...", self, shortcut="Ctrl+O", triggered=self.open_file)
        self.save_action = QAction(QIcon.fromTheme("document-save"), "&Kaydet", self, shortcut="Ctrl+S", triggered=self.save_file)
        self.save_as_action = QAction(QIcon.fromTheme("document-save-as"), "Farklı &Kaydet...", self, shortcut="Ctrl+Shift+S", triggered=self.save_as_file)
        self.exit_action = QAction(QIcon.fromTheme("application-exit"), "&Çıkış", self, shortcut="Ctrl+Q", triggered=self.close)

        self.green_theme_action = QAction("Yeşil Terminal", self, checkable=True, triggered=lambda: self.set_theme("green"))
        self.amber_theme_action = QAction("Amber Terminal", self, checkable=True, triggered=lambda: self.set_theme("amber"))
        self.choose_font_action = QAction(QIcon.fromTheme("preferences-desktop-font"), "Yazı Tipi &Seç...", self, triggered=self.choose_font)
        self.increase_font_action = QAction(QIcon.fromTheme("zoom-in"), "Boyutu &Artır", self, shortcut="Ctrl++", triggered=self.increase_font_size)
        self.decrease_font_action = QAction(QIcon.fromTheme("zoom-out"), "Boyutu &Azalt", self, shortcut="Ctrl+-", triggered=self.decrease_font_size)

        self.about_action = QAction(QIcon.fromTheme("help-about"), "&Hakkında", self, triggered=self.about_dialog)

    def _create_menu_bar(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("&Dosya")
        file_menu.addAction(self.new_action); file_menu.addAction(self.open_action)
        file_menu.addAction(self.save_action); file_menu.addAction(self.save_as_action)
        file_menu.addSeparator(); file_menu.addAction(self.exit_action)

        view_menu = menubar.addMenu("&Görünüm")
        theme_submenu = view_menu.addMenu("Temalar")
        theme_submenu.addAction(self.green_theme_action); theme_submenu.addAction(self.amber_theme_action)
        view_menu.addSeparator(); view_menu.addAction(self.choose_font_action)
        view_menu.addAction(self.increase_font_action); view_menu.addAction(self.decrease_font_action)

        help_menu = menubar.addMenu("&Yardım")
        help_menu.addAction(self.about_action)

    def _create_tool_bar(self):
        toolbar = QToolBar("Ana Araç Çubuğu")
        toolbar.setIconSize(QSize(20, 20)) # İkon boyutunu ayarla
        self.addToolBar(Qt.TopToolBarArea, toolbar) # Toolbar'ı en üste ekle

        toolbar.addAction(self.new_action); toolbar.addAction(self.open_action); toolbar.addAction(self.save_action)
        toolbar.addSeparator()
        toolbar.addAction(self.increase_font_action); toolbar.addAction(self.decrease_font_action)
        toolbar.addSeparator()

        self.toggle_theme_button = QToolButton(self)
        self.toggle_theme_button.setText("Tema Değiştir") # Başlangıç metni, apply_theme'de güncellenecek
        self.toggle_theme_button.setCheckable(False) # Normal buton gibi davranacak
        self.toggle_theme_button.clicked.connect(self._quick_toggle_theme)
        toolbar.addWidget(self.toggle_theme_button)

    def _quick_toggle_theme(self):
        self.set_theme("amber" if self.current_theme_style_name == "green" else "green")

    def set_theme(self, theme_name):
        self.current_theme_style_name = theme_name
        self.green_theme_action.setChecked(theme_name == "green")
        self.amber_theme_action.setChecked(theme_name == "amber")
        self.apply_theme()
        self.statusBar().showMessage(f"Tema '{theme_name.capitalize()}' olarak ayarlandı.")

    def apply_theme(self):
        if self.current_theme_style_name == "green":
            self.setStyleSheet(RETRO_STYLE_GREEN)
            if hasattr(self, 'toggle_theme_button'): self.toggle_theme_button.setText("Amber'e Geç")
        elif self.current_theme_style_name == "amber":
            self.setStyleSheet(RETRO_STYLE_AMBER)
            if hasattr(self, 'toggle_theme_button'): self.toggle_theme_button.setText("Yeşil'e Geç")
        else: # Varsayılan bir durum (eğer gelecekte ek tema seçenekleri olursa)
            self.setStyleSheet("") # Temayı temizle
            if hasattr(self, 'toggle_theme_button'): self.toggle_theme_button.setText("Tema Seç")

        self.apply_font_settings() # Tema değiştiğinde font ayarlarını da uygula

    def apply_font_settings(self):
        current_font = QFont()
        db = QFontDatabase()

        # Kullanıcının seçtiği font ailesi sistemde varsa onu kullan
        if self.base_font_family and self.base_font_family in db.families():
            current_font.setFamily(self.base_font_family)
        else:
            # Tercih edilen sabit genişlikli fontları dene
            preferred_families = ["Consolas", "DejaVu Sans Mono", "Menlo", "Courier New"]
            found_preferred = False
            for family in preferred_families:
                if family in db.families():
                    font_info_test = QFontInfo(QFont(family))
                    if font_info_test.fixedPitch():
                        current_font.setFamily(family)
                        self.base_font_family = family # Bulunan geçerli fontu kaydet
                        found_preferred = True
                        break
            if not found_preferred:
                # Hiçbiri bulunamazsa genel bir monospace kullan
                current_font.setFamily("monospace")
                self.base_font_family = current_font.family() # Gerçekte atanan fontu kaydet

        current_font.setPointSize(self.base_font_size)
        self.text_area.setFont(current_font)

        # Durum çubuğu fontunu da ayarla (ana fonttan biraz daha küçük)
        status_bar_font = QFont(current_font)
        status_bar_font.setPointSize(max(8, self.base_font_size - 3)) # En az 8pt
        self.statusBar().setFont(status_bar_font)

        # Menü ve Toolbar fontları QSS ile ayarlandığı için burada tekrar ayarlanmasına gerek yok.
        # Ancak istenirse QSS'ten kaldırılıp buradan dinamik olarak ayarlanabilirler.

        # Tab genişliğini ayarla (bir 'M' karakterinin genişliği kadar)
        fm = QFontMetrics(self.text_area.font())
        tab_stop_width_pixels = fm.horizontalAdvance('M') # 'M' genellikle en geniş karakterlerden biridir
        if tab_stop_width_pixels <= 0: # 'M' için geçerli bir genişlik alınamazsa
             tab_stop_width_pixels = fm.horizontalAdvance(' ') * 4 # 4 boşluk karakteri
        if tab_stop_width_pixels <= 0: # Hala 0 ise
            tab_stop_width_pixels = 30 # Mantıklı bir varsayılan piksel değeri
        self.text_area.setTabStopDistance(int(tab_stop_width_pixels))


    def choose_font(self):
        initial_font = QFont(self.base_font_family, self.base_font_size)
        font, ok = QFontDialog.getFont(initial_font, self, "Yazı Tipi Seç")
        if ok:
            self.base_font_family = font.family()
            self.base_font_size = font.pointSize()
            self.apply_font_settings()
            self.statusBar().showMessage(f"Yazı tipi '{self.base_font_family}', Boyut: {self.base_font_size}pt olarak ayarlandı.")

    def increase_font_size(self):
        if self.base_font_size < 72: # Maksimum boyut sınırı
            self.base_font_size += 1
            self.apply_font_settings()
            self.statusBar().showMessage(f"Yazı tipi boyutu: {self.base_font_size}pt")

    def decrease_font_size(self):
        if self.base_font_size > 6: # Minimum boyut sınırı
            self.base_font_size -= 1
            self.apply_font_settings()
            self.statusBar().showMessage(f"Yazı tipi boyutu: {self.base_font_size}pt")

    def update_window_title(self):
        title_base = "mb not defteri"
        filename_display = " [Yeni Dosya]"
        if self.current_file:
            filename_display = f" [{os.path.basename(self.current_file)}]"

        modified_indicator = "*" if self.text_area.document().isModified() else ""
        self.setWindowTitle(f"{modified_indicator}{title_base}{filename_display}")

    def _confirm_unsaved_changes(self):
        if not self.text_area.document().isModified():
            return True # Değişiklik yoksa devam et

        reply = QMessageBox.warning(self, "Kaydedilmemiş Değişiklikler",
                                      "Belgede kaydedilmemiş değişiklikler var.\nDevam etmeden önce kaydetmek ister misiniz?",
                                      QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
                                      QMessageBox.Cancel) # Varsayılan buton Cancel

        if reply == QMessageBox.Save:
            return self.save_file() # Kaydet ve sonucu döndür (başarılı/başarısız)
        elif reply == QMessageBox.Cancel:
            self.statusBar().showMessage("İşlem iptal edildi.")
            return False # İptal edildi, devam etme
        # reply == QMessageBox.Discard ise True dönecek (kaydetme, devam et)
        return True

    def new_file(self):
        if not self._confirm_unsaved_changes():
            return # Kullanıcı iptal etti veya kaydetme başarısız oldu
        self.text_area.clear()
        self.current_file = None
        self.text_area.document().setModified(False) # Yeni dosya değiştirilmemiş olarak başlar
        self.update_window_title()
        self.statusBar().showMessage("Yeni dosya oluşturuldu.")

    def open_file(self):
        if not self._confirm_unsaved_changes():
            return
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog # Eğer gerekirse standart olmayan diyalog için
        filename, _ = QFileDialog.getOpenFileName(self, "Dosya Aç", "",
                                                  "Metin Dosyaları (*.txt);;Tüm Dosyalar (*.*)",
                                                  options=options)
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    self.text_area.setPlainText(f.read())
                self.current_file = filename
                self.text_area.document().setModified(False)
                self.update_window_title()
                self.statusBar().showMessage(f"'{os.path.basename(filename)}' açıldı.")
            except Exception as e:
                QMessageBox.critical(self, "Hata", f"Dosya açılamadı:\n{e}")
                self.current_file = None # Hata durumunda mevcut dosyayı sıfırla
                self.update_window_title() # Başlığı güncelle

    def save_file(self):
        if not self.current_file: # Eğer dosya hiç kaydedilmemişse, Farklı Kaydet'e yönlendir
            return self.save_as_file()
        try:
            with open(self.current_file, 'w', encoding='utf-8') as f:
                f.write(self.text_area.toPlainText())
            self.text_area.document().setModified(False)
            self.update_window_title()
            self.statusBar().showMessage(f"'{os.path.basename(self.current_file)}' kaydedildi.")
            return True # Kaydetme başarılı
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Dosya kaydedilemedi:\n{e}")
            return False # Kaydetme başarısız

    def save_as_file(self):
        options = QFileDialog.Options()
        suggested_name = os.path.basename(self.current_file) if self.current_file else "adsiz.txt"
        filename, _ = QFileDialog.getSaveFileName(self, "Farklı Kaydet", suggested_name,
                                                  "Metin Dosyaları (*.txt);;Tüm Dosyalar (*.*)",
                                                  options=options)
        if filename:
            self.current_file = filename
            return self.save_file() # Seçilen yeni dosya adıyla normal kaydetmeyi çağır
        self.statusBar().showMessage("Farklı kaydetme iptal edildi.")
        return False # Farklı kaydetme iptal edildi veya başarısız

    def about_dialog(self):
        year = QDate.currentDate().year()
        QMessageBox.about(self, "mb not defteri Hakkında",
                          f"<p><b>mb not defteri</b></p>"
                          "<p>PyQt5 ile oluşturulmuş retro temalı metin düzenleyici.</p>"
                          f"<p>Telif Hakkı (c) {year}. Tüm hakları saklıdır.</p>"
                          "<p>Bu basit bir not defteri uygulamasıdır.</p>")

    def closeEvent(self, event):
        if self._confirm_unsaved_changes():
            # self.statusBar().showMessage("mb not defteri kapatılıyor...") # İsteğe bağlı
            event.accept() # Uygulamanın kapanmasına izin ver
        else:
            event.ignore() # Kapanmayı engelle

if __name__ == '__main__':
    # Yüksek DPI ölçeklemeyi etkinleştir (Qt 5.6+)
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    # Yüksek DPI piksmaplarını kullan (Qt 5.1+)
    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    editor = MBNotDefteri() # Sınıf adı doğru
    editor.show()
    sys.exit(app.exec_())