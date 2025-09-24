#!/usr/bin/env python3
"""
iPhone Photo Manager - GTK4 LibAdwaita aplikacija za pristup fotografijama
Zahteva: libimobiledevice, gi (GTK4), libadwaita
"""

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
gi.require_version('GdkPixbuf', '2.0')
from gi.repository import Gtk, Adw, GLib, GdkPixbuf, Gio, Gdk
import os
import subprocess
import threading
from pathlib import Path
import shutil
from datetime import datetime
import time
import json

# Lokalizacija/translations
TRANSLATIONS = {
    'sr': {
        'app_title': 'iPhone Photo Manager',
        'connection_status': 'Status konekcije',
        'checking': 'Proverava...',
        'connected': 'Povezan',
        'not_connected': 'Nije povezan',
        'mount': 'Montiraj',
        'unmount': 'Demontiraj',
        'mounting': 'Montiranje...',
        'error_retry': 'Greška - pokušaj ponovo',
        'connecting': 'Povezivanje',
        'refresh_connection': 'Osveži konekciju',
        'folders': 'Folderi',
        'destination_folder': 'Odredišna fascikla',
        'actions': 'Akcije',
        'select_all': 'Odaberi sve',
        'deselect_all': 'Poništi sve',
        'download_selected': 'Preuzmi odabrane',
        'photos': 'Fotografije',
        'items': 'stavki',
        'photo_details': 'Detalji fotografije',
        'filename': 'Ime fajla:',
        'size': 'Veličina:',
        'dimensions': 'Dimenzije:',
        'date': 'Datum:',
        'type': 'Tip:',
        'download_this': 'Preuzmi ovu',
        'add_to_selected': 'Dodaj u odabrane',
        'remove_from_selected': 'Ukloni iz odabranih',
        'copying': 'Kopiranje...',
        'photo_saved': 'Fotografija sačuvana',
        'copy_error': 'Greška pri kopiranju',
        'copied_files': 'Kopirano {0} fajlova',
        'error': 'Greška',
        'ok': 'U redu',
        'unknown': 'Nepoznato',
        'video_file': 'Video fajl',
        'photo': 'Photo',
        'video': 'Video',
        'settings': 'Podešavanja',
        'theme': 'Tema:',
        'language': 'Jezik:',
        'dark': 'Tamna',
        'light': 'Svetla',
        'serbian': 'Srpski',
        'english': 'English',
        'preferences': 'Podešavanja',
        'appearance': 'Izgled',
        'interface_language': 'Jezik interfejsa',
        'color_scheme': 'Šema boja',
        'restart_required': 'Potreban je restart aplikacije da bi se promena jezika primenila.',
        'cannot_load_thumbnail': 'Ne mogu da učitam thumbnail',
        'iphone_not_connected': 'iPhone nije povezan!',
        'mount_attempt': 'Pokušaj montiranja {0}/{1}',
        'cannot_remove_mount_point': 'Ne mogu da uklonjem postojeći mount point',
        'resetting_pairing': 'Resetujem pairing...',
        'pairing_device': 'Pairing uređaja...',
        'pairing_failed': 'Pairing failed',
        'trust_computer': 'MORATE kliknuti \'Trust This Computer\' na iPhone-u!',
        'pairing_validation_failed': 'Pairing validation failed',
        'attempting_mount': 'Pokušavam montiranje...',
        'mount_point_disappeared': 'Mount point nestao nakon montiranja',
        'cannot_access_mount_point': 'Ne mogu da pristupim mount point-u',
        'io_error_reboot': 'I/O error - možda je potreban reboot iPhone-a',
        'mount_successful': 'Uspešno montirano!',
        'dcim_unavailable': 'DCIM folder nije dostupan - možda nema fotografija',
        'mount_failed': 'Mount failed',
        'lockdown_unavailable': 'Lockdown servis nije dostupan - restartujte iPhone',
        'permission_problem': 'Permission problem - proverite fuse dozvole',
        'io_error_mount': 'I/O error na mount point-u (pokušaj {0})',
        'restart_suggestion': 'Možda je potreban restart iPhone-a ili računara',
        'all_attempts_failed': 'Svi pokušaji neuspešni!',
        'suggestions': 'Predlozi:',
        'restart_iphone': '1. Restartujte iPhone',
        'different_usb': '2. Koristite drugi USB port/kabel',
        'restart_usbmuxd': '3. sudo systemctl restart usbmuxd',
        'restart_system': '4. Logout/login ili restart sistema',
        'error_reading_folders': 'Error reading folders',
        'error_reading_photos': 'Error reading photos',
        'cannot_create_folder': 'Ne mogu da kreiram fasciklu',
        'copy_progress': 'Kopirano {0}/{1}',
        'copy_success': 'Uspešno kopirano {0} fajlova u:\n{1}',
        'copy_errors': 'Kopirano {0}/{1} fajlova.\nGreške:\n{2}',
        'and_more_errors': '... i još {0} grešaka',
        'missing_tools': 'GREŠKA: Nedostaju potrebni alati:',
        'install': 'Instaliraj',
        'ubuntu_install': 'Ubuntu/Debian:',
        'fedora_install': 'Fedora/RHEL:'
    },
    'en': {
        'app_title': 'iPhone Photo Manager',
        'connection_status': 'Connection Status',
        'checking': 'Checking...',
        'connected': 'Connected',
        'not_connected': 'Not connected',
        'mount': 'Mount',
        'unmount': 'Unmount',
        'mounting': 'Mounting...',
        'error_retry': 'Error - try again',
        'connecting': 'Connecting',
        'refresh_connection': 'Refresh Connection',
        'folders': 'Folders',
        'destination_folder': 'Destination Folder',
        'actions': 'Actions',
        'select_all': 'Select All',
        'deselect_all': 'Deselect All',
        'download_selected': 'Download Selected',
        'photos': 'Photos',
        'items': 'items',
        'photo_details': 'Photo Details',
        'filename': 'Filename:',
        'size': 'Size:',
        'dimensions': 'Dimensions:',
        'date': 'Date:',
        'type': 'Type:',
        'download_this': 'Download This',
        'add_to_selected': 'Add to Selected',
        'remove_from_selected': 'Remove from Selected',
        'copying': 'Copying...',
        'photo_saved': 'Photo saved',
        'copy_error': 'Copy error',
        'copied_files': 'Copied {0} files',
        'error': 'Error',
        'ok': 'OK',
        'unknown': 'Unknown',
        'video_file': 'Video file',
        'photo': 'Photo',
        'video': 'Video',
        'settings': 'Settings',
        'theme': 'Theme:',
        'language': 'Language:',
        'dark': 'Dark',
        'light': 'Light',
        'serbian': 'Srpski',
        'english': 'English',
        'preferences': 'Preferences',
        'appearance': 'Appearance',
        'interface_language': 'Interface Language',
        'color_scheme': 'Color Scheme',
        'restart_required': 'Application restart is required for language change to take effect.',
        'cannot_load_thumbnail': 'Cannot load thumbnail',
        'iphone_not_connected': 'iPhone not connected!',
        'mount_attempt': 'Mount attempt {0}/{1}',
        'cannot_remove_mount_point': 'Cannot remove existing mount point',
        'resetting_pairing': 'Resetting pairing...',
        'pairing_device': 'Pairing device...',
        'pairing_failed': 'Pairing failed',
        'trust_computer': 'YOU MUST click \'Trust This Computer\' on iPhone!',
        'pairing_validation_failed': 'Pairing validation failed',
        'attempting_mount': 'Attempting mount...',
        'mount_point_disappeared': 'Mount point disappeared after mounting',
        'cannot_access_mount_point': 'Cannot access mount point',
        'io_error_reboot': 'I/O error - iPhone reboot might be needed',
        'mount_successful': 'Successfully mounted!',
        'dcim_unavailable': 'DCIM folder unavailable - might have no photos',
        'mount_failed': 'Mount failed',
        'lockdown_unavailable': 'Lockdown service unavailable - restart iPhone',
        'permission_problem': 'Permission problem - check fuse permissions',
        'io_error_mount': 'I/O error at mount point (attempt {0})',
        'restart_suggestion': 'iPhone or computer restart might be needed',
        'all_attempts_failed': 'All attempts failed!',
        'suggestions': 'Suggestions:',
        'restart_iphone': '1. Restart iPhone',
        'different_usb': '2. Use different USB port/cable',
        'restart_usbmuxd': '3. sudo systemctl restart usbmuxd',
        'restart_system': '4. Logout/login or restart system',
        'error_reading_folders': 'Error reading folders',
        'error_reading_photos': 'Error reading photos',
        'cannot_create_folder': 'Cannot create folder',
        'copy_progress': 'Copied {0}/{1}',
        'copy_success': 'Successfully copied {0} files to:\n{1}',
        'copy_errors': 'Copied {0}/{1} files.\nErrors:\n{2}',
        'and_more_errors': '... and {0} more errors',
        'missing_tools': 'ERROR: Missing required tools:',
        'install': 'Install',
        'ubuntu_install': 'Ubuntu/Debian:',
        'fedora_install': 'Fedora/RHEL:'
    }
}

class AppSettings:
    """Klasa za upravljanje podešavanjima aplikacije"""
    def __init__(self):
        self.config_path = Path.home() / '.config' / 'iphone-photo-manager'
        self.config_file = self.config_path / 'settings.json'
        self.default_settings = {
            'language': 'en',
            'theme': 'dark'
        }
        self.settings = self.load_settings()
        
    def load_settings(self):
        """Učitava podešavanja iz fajla"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    # Merge with defaults for missing keys
                    for key, value in self.default_settings.items():
                        if key not in settings:
                            settings[key] = value
                    return settings
            else:
                return self.default_settings.copy()
        except Exception as e:
            print(f"Error loading settings: {e}")
            return self.default_settings.copy()
    
    def save_settings(self):
        """Čuva podešavanja u fajl"""
        try:
            self.config_path.mkdir(parents=True, exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving settings: {e}")
    
    def get(self, key, default=None):
        """Dobija vrednost podešavanja"""
        return self.settings.get(key, default)
    
    def set(self, key, value):
        """Postavlja vrednost podešavanja"""
        self.settings[key] = value
        self.save_settings()

class Localizer:
    """Klasa za lokalizaciju"""
    def __init__(self, settings):
        self.settings = settings
        self.current_lang = settings.get('language', 'en')
    
    def get_text(self, key, *args):
        """Dobija lokalizovani tekst"""
        text = TRANSLATIONS.get(self.current_lang, TRANSLATIONS['en']).get(key, key)
        if args:
            return text.format(*args)
        return text
    
    def set_language(self, lang):
        """Postavlja jezik"""
        if lang in TRANSLATIONS:
            self.current_lang = lang
            self.settings.set('language', lang)

class iPhonePhotoManager:
    def __init__(self, localizer):
        self.localizer = localizer
        self.device_connected = False
        self.device_udid = None
        self.device_name = None
        self.photos_path = None
        self.mount_point = Path.home() / "iphone_mount"
        
    def check_device_connection(self):
        """Proverava da li je iPhone povezan i dobija osnovne info"""
        try:
            # Proveri da li je uređaj povezan
            result = subprocess.run(['idevice_id', '-l'], 
                                 capture_output=True, text=True, timeout=5)
            if result.returncode == 0 and result.stdout.strip():
                self.device_udid = result.stdout.strip()
                
                # Pokušaj da dobije ime uređaja
                try:
                    name_result = subprocess.run(['ideviceinfo', '-k', 'DeviceName'], 
                                               capture_output=True, text=True, timeout=5)
                    if name_result.returncode == 0:
                        self.device_name = name_result.stdout.strip()
                except:
                    self.device_name = "iPhone"
                
                self.device_connected = True
                return True
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        
        self.device_connected = False
        self.device_udid = None
        self.device_name = None
        return False
    
    def mount_device(self, retry_count=3):
        """Montira iPhone file system sa retry logikom"""
        # Prvo proverava osnovnu konekciju
        if not self.check_device_connection():
            print(self.localizer.get_text('iphone_not_connected'))
            return False
            
        for attempt in range(retry_count):
            try:
                print(self.localizer.get_text('mount_attempt', attempt + 1, retry_count))
                
                # Forsiraj cleanup mount point-a
                self.force_cleanup_mount()
                
                # Kreiraj fresh mount point
                if self.mount_point.exists():
                    try:
                        self.mount_point.rmdir()
                    except:
                        print(self.localizer.get_text('cannot_remove_mount_point'))
                        
                self.mount_point.mkdir(exist_ok=True)
                
                # Reset pairing ako nije prvi pokušaj
                if attempt > 0:
                    print(self.localizer.get_text('resetting_pairing'))
                    subprocess.run(['idevicepair', 'unpair'], 
                                 capture_output=True, timeout=5)
                    time.sleep(2)
                
                # Pair device
                print(self.localizer.get_text('pairing_device'))
                pair_result = subprocess.run(['idevicepair', 'pair'], 
                                           capture_output=True, text=True, timeout=20)
                
                if pair_result.returncode != 0:
                    print(f"{self.localizer.get_text('pairing_failed')}: {pair_result.stderr}")
                    if "user denied" in pair_result.stderr.lower():
                        print(self.localizer.get_text('trust_computer'))
                        return False  # Ne retry ako user nije trust-ovao
                    time.sleep(3)
                    continue
                
                # Validacija pairinga
                validate_result = subprocess.run(['idevicepair', 'validate'], 
                                               capture_output=True, text=True, timeout=10)
                
                if validate_result.returncode != 0:
                    print(self.localizer.get_text('pairing_validation_failed'))
                    time.sleep(2)
                    continue
                
                print(self.localizer.get_text('attempting_mount'))
                # Mount sa dodatnim opcijama
                mount_cmd = ['ifuse', str(self.mount_point), '-o', 'allow_other,default_permissions']
                mount_result = subprocess.run(mount_cmd, 
                                            capture_output=True, text=True, timeout=15)
                
                if mount_result.returncode == 0:
                    # Proverava da li je mount uspešan
                    time.sleep(1)  # Kratka pauza
                    
                    if not self.mount_point.exists():
                        print(self.localizer.get_text('mount_point_disappeared'))
                        continue
                        
                    try:
                        # Test čitanja mount point-a
                        list(self.mount_point.iterdir())
                    except OSError as e:
                        print(f"{self.localizer.get_text('cannot_access_mount_point')}: {e}")
                        self.unmount_device()
                        if "Input/output error" in str(e):
                            print(self.localizer.get_text('io_error_reboot'))
                            return False
                        continue
                    
                    # Proverava DCIM folder
                    self.photos_path = self.mount_point / "DCIM"
                    if self.photos_path.exists():
                        print(self.localizer.get_text('mount_successful'))
                        return True
                    else:
                        print(self.localizer.get_text('dcim_unavailable'))
                        # Ipak returni True jer je mount uspešan
                        return True
                else:
                    print(f"{self.localizer.get_text('mount_failed')}: {mount_result.stderr}")
                    if "lockdownd" in mount_result.stderr:
                        print(self.localizer.get_text('lockdown_unavailable'))
                        return False
                    elif "Permission denied" in mount_result.stderr:
                        print(self.localizer.get_text('permission_problem'))
                        return False
                
                time.sleep(3)  # Pauza između pokušaja
                    
            except OSError as e:
                if "Input/output error" in str(e):
                    print(self.localizer.get_text('io_error_mount', attempt + 1) + f": {e}")
                    print(self.localizer.get_text('restart_suggestion'))
                    self.force_cleanup_mount()
                    if attempt == retry_count - 1:  # Poslednji pokušaj
                        return False
                else:
                    print(f"OS error (pokušaj {attempt + 1}): {e}")
                time.sleep(2)
            except Exception as e:
                print(f"Unexpected error (pokušaj {attempt + 1}): {e}")
                time.sleep(2)
        
        print(self.localizer.get_text('all_attempts_failed'))
        print(self.localizer.get_text('suggestions'))
        print(self.localizer.get_text('restart_iphone'))
        print(self.localizer.get_text('different_usb'))
        print(self.localizer.get_text('restart_usbmuxd'))
        print(self.localizer.get_text('restart_system'))
        return False
        
    def force_cleanup_mount(self):
        """Forsiraj cleanup mount point-a"""
        try:
            # Pokušaj različite načine demontiranja
            subprocess.run(['fusermount', '-uz', str(self.mount_point)], 
                         capture_output=True, timeout=5)
        except:
            pass
            
        try:
            subprocess.run(['umount', '-f', str(self.mount_point)], 
                         capture_output=True, timeout=5)
        except:
            pass
            
        try:
            subprocess.run(['sudo', 'umount', '-l', str(self.mount_point)], 
                         capture_output=True, timeout=5)
        except:
            pass
    
    def unmount_device(self):
        """Demontira iPhone"""
        try:
            subprocess.run(['fusermount', '-u', str(self.mount_point)], timeout=5)
        except:
            try:
                subprocess.run(['umount', str(self.mount_point)], timeout=5)
            except:
                pass
                
    def is_mounted(self):
        """Proverava da li je iPhone montiran"""
        return self.photos_path and self.photos_path.exists()
    
    def get_photo_folders(self):
        """Dobija listu foldera sa fotografijama"""
        folders = []
        if not self.is_mounted():
            return folders
            
        try:
            for folder in self.photos_path.iterdir():
                if folder.is_dir():
                    photo_count = len([f for f in folder.iterdir() 
                                     if f.suffix.lower() in ['.jpg', '.jpeg', '.png', '.heic', '.mov', '.mp4']])
                    if photo_count > 0:
                        folders.append((folder.name, photo_count, folder))
        except Exception as e:
            print(f"{self.localizer.get_text('error_reading_folders')}: {e}")
            
        return sorted(folders)
    
    def get_photos_from_folder(self, folder_path):
        """Dobija fotografije iz određenog foldera"""
        photos = []
        supported_formats = ['.jpg', '.jpeg', '.png', '.heic', '.mov', '.mp4']
        
        try:
            for photo in folder_path.iterdir():
                if photo.suffix.lower() in supported_formats:
                    try:
                        stat = photo.stat()
                        size = stat.st_size
                        modified = datetime.fromtimestamp(stat.st_mtime)
                        photos.append({
                            'name': photo.name,
                            'path': photo,
                            'size': size,
                            'modified': modified,
                            'type': self.localizer.get_text('video') if photo.suffix.lower() in ['.mov', '.mp4'] else self.localizer.get_text('photo')
                        })
                    except:
                        continue
        except Exception as e:
            print(f"{self.localizer.get_text('error_reading_photos')}: {e}")
            
        return sorted(photos, key=lambda x: x['modified'], reverse=True)

class PhotoListItem(Gtk.ListBoxRow):
    """Custom list item za fotografije"""
    def __init__(self, photo_data, localizer):
        super().__init__()
        self.photo_data = photo_data
        self.localizer = localizer
        self.selected = False
        
        # Main box
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        box.set_margin_top(6)
        box.set_margin_bottom(6)
        box.set_margin_start(12)
        box.set_margin_end(12)
        self.set_child(box)
        
        # Checkbox
        self.checkbox = Gtk.CheckButton()
        self.checkbox.connect("toggled", self.on_checkbox_toggled)
        box.append(self.checkbox)
        
        # Icon
        icon_name = "video-x-generic" if photo_data['type'] == localizer.get_text('video') else "image-x-generic"
        icon = Gtk.Image.new_from_icon_name(icon_name)
        icon.set_pixel_size(24)
        box.append(icon)
        
        # Info box
        info_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        box.append(info_box)
        
        # Name
        name_label = Gtk.Label(label=photo_data['name'])
        name_label.set_halign(Gtk.Align.START)
        name_label.add_css_class("heading")
        info_box.append(name_label)
        
        # Details
        size_str = self.format_size(photo_data['size'])
        date_str = photo_data['modified'].strftime("%d.%m.%Y %H:%M")
        detail_text = f"{size_str} • {date_str} • {photo_data['type']}"
        
        detail_label = Gtk.Label(label=detail_text)
        detail_label.set_halign(Gtk.Align.START)
        detail_label.add_css_class("dim-label")
        detail_label.add_css_class("caption")
        info_box.append(detail_label)
        
    def format_size(self, size_bytes):
        """Formatira veličinu fajla"""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024**2:
            return f"{size_bytes/1024:.1f} KB"
        elif size_bytes < 1024**3:
            return f"{size_bytes/(1024**2):.1f} MB"
        else:
            return f"{size_bytes/(1024**3):.1f} GB"
            
    def on_checkbox_toggled(self, checkbox):
        """Handle za checkbox toggle"""
        self.selected = checkbox.get_active()
        # Emit signal to parent to update download button
        if hasattr(self, '_parent_callback'):
            self._parent_callback()
        
    def set_selected(self, selected):
        """Postavlja selected state"""
        self.selected = selected
        self.checkbox.set_active(selected)
        
    def get_selected(self):
        """Vraća da li je item odabran"""
        return self.selected

class FolderListItem(Gtk.ListBoxRow):
    """Custom list item za foldere"""
    def __init__(self, folder_name, photo_count, folder_path, localizer):
        super().__init__()
        self.folder_name = folder_name
        self.photo_count = photo_count
        self.folder_path = folder_path
        self.localizer = localizer
        
        # Main box
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        box.set_margin_top(8)
        box.set_margin_bottom(8)
        box.set_margin_start(12)
        box.set_margin_end(12)
        self.set_child(box)
        
        # Folder icon
        icon = Gtk.Image.new_from_icon_name("folder")
        icon.set_pixel_size(24)
        box.append(icon)
        
        # Info box
        info_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        box.append(info_box)
        
        # Folder name
        name_label = Gtk.Label(label=folder_name)
        name_label.set_halign(Gtk.Align.START)
        name_label.add_css_class("heading")
        info_box.append(name_label)
        
        # Photo count
        count_label = Gtk.Label(label=f"{photo_count} {localizer.get_text('items')}")
        count_label.set_halign(Gtk.Align.START)
        count_label.add_css_class("dim-label")
        count_label.add_css_class("caption")
        info_box.append(count_label)

class PreferencesWindow(Adw.PreferencesWindow):
    """Prozor za podešavanja"""
    def __init__(self, parent, settings, localizer):
        super().__init__()
        self.settings = settings
        self.localizer = localizer
        self.set_transient_for(parent)
        self.set_title(localizer.get_text('preferences'))
        self.set_modal(True)
        
        # Appearance page
        appearance_page = Adw.PreferencesPage()
        appearance_page.set_title(localizer.get_text('appearance'))
        appearance_page.set_icon_name("applications-graphics-symbolic")
        self.add(appearance_page)
        
        # Language group
        lang_group = Adw.PreferencesGroup()
        lang_group.set_title(localizer.get_text('interface_language'))
        appearance_page.add(lang_group)
        
        # Language row
        lang_row = Adw.ActionRow()
        lang_row.set_title(localizer.get_text('language'))
        
        # Language dropdown
        lang_model = Gtk.StringList()
        lang_model.append(localizer.get_text('serbian'))
        lang_model.append(localizer.get_text('english'))
        
        self.lang_dropdown = Gtk.DropDown()
        self.lang_dropdown.set_model(lang_model)
        self.lang_dropdown.set_selected(0 if settings.get('language') == 'sr' else 1)
        self.lang_dropdown.connect('notify::selected', self.on_language_changed)
        
        lang_row.add_suffix(self.lang_dropdown)
        lang_group.add(lang_row)
        
        # Theme group
        theme_group = Adw.PreferencesGroup()
        theme_group.set_title(localizer.get_text('color_scheme'))
        appearance_page.add(theme_group)
        
        # Theme row
        theme_row = Adw.ActionRow()
        theme_row.set_title(localizer.get_text('theme'))
        
        # Theme dropdown
        theme_model = Gtk.StringList()
        theme_model.append(localizer.get_text('dark'))
        theme_model.append(localizer.get_text('light'))
        
        self.theme_dropdown = Gtk.DropDown()
        self.theme_dropdown.set_model(theme_model)
        self.theme_dropdown.set_selected(0 if settings.get('theme') == 'dark' else 1)
        self.theme_dropdown.connect('notify::selected', self.on_theme_changed)
        
        theme_row.add_suffix(self.theme_dropdown)
        theme_group.add(theme_row)
        
    def on_language_changed(self, dropdown, param):
        """Handle za promenu jezika"""
        selected = dropdown.get_selected()
        new_lang = 'sr' if selected == 0 else 'en'
        
        if new_lang != self.settings.get('language'):
            self.settings.set('language', new_lang)
            
            # Show restart dialog
            dialog = Adw.MessageDialog(parent=self)
            dialog.set_heading(self.localizer.get_text('preferences'))
            dialog.set_body(self.localizer.get_text('restart_required'))
            dialog.add_response("ok", self.localizer.get_text('ok'))
            dialog.present()
    
    def on_theme_changed(self, dropdown, param):
        """Handle za promenu teme"""
        selected = dropdown.get_selected()
        new_theme = 'dark' if selected == 0 else 'light'
        
        if new_theme != self.settings.get('theme'):
            self.settings.set('theme', new_theme)
            
            # Apply theme immediately
            style_manager = Adw.StyleManager.get_default()
            if new_theme == 'dark':
                style_manager.set_color_scheme(Adw.ColorScheme.FORCE_DARK)
            else:
                style_manager.set_color_scheme(Adw.ColorScheme.FORCE_LIGHT)

class iPhonePhotoManagerGUI(Adw.Application):
    def __init__(self):
        super().__init__(application_id="com.example.iphonephotomanager")
        
        # Initialize settings and localization
        self.settings = AppSettings()
        self.localizer = Localizer(self.settings)
        
        # Initialize theme
        self.apply_theme()
        
        self.manager = iPhonePhotoManager(self.localizer)
        self.photo_items = []
        self.current_folder = None
        self.current_preview_item = None
        
    def apply_theme(self):
        """Primenjuje temu"""
        style_manager = Adw.StyleManager.get_default()
        theme = self.settings.get('theme', 'dark')
        
        if theme == 'dark':
            style_manager.set_color_scheme(Adw.ColorScheme.FORCE_DARK)
        else:
            style_manager.set_color_scheme(Adw.ColorScheme.FORCE_LIGHT)
        
    def do_activate(self):
        """Aktivacija aplikacije"""
        self.window = self.create_window()
        self.window.present()
        self.refresh_connection()
        
    def create_window(self):
        """Kreira glavni prozor"""
        window = Adw.ApplicationWindow(application=self)
        window.set_title(self.localizer.get_text('app_title'))
        window.set_default_size(1200, 800)
        
        # Create header bar with menu
        header_bar = Adw.HeaderBar()
        
        # Preferences button
        prefs_button = Gtk.Button()
        prefs_button.set_icon_name("preferences-system-symbolic")
        prefs_button.add_css_class("flat")
        prefs_button.connect("clicked", self.on_preferences_clicked)
        header_bar.pack_end(prefs_button)
        
        # Main paned container (horizontal split)
        main_paned = Gtk.Paned(orientation=Gtk.Orientation.HORIZONTAL)
        main_paned.set_position(280)
        
        # Main box for header + content
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        main_box.append(header_bar)
        main_box.append(main_paned)
        window.set_content(main_box)
        
        # Sidebar
        sidebar = self.create_sidebar()
        main_paned.set_start_child(sidebar)
        
        # Right side - content + preview paned (vertical split)
        right_paned = Gtk.Paned(orientation=Gtk.Orientation.VERTICAL)
        right_paned.set_position(450)
        main_paned.set_end_child(right_paned)
        
        # Main content (top)
        content = self.create_main_content()
        right_paned.set_start_child(content)
        
        # Preview panel (bottom)
        preview_panel = self.create_preview_panel()
        right_paned.set_end_child(preview_panel)
        
        return window
        
    def on_preferences_clicked(self, button):
        """Handle za preferences dugme"""
        prefs_window = PreferencesWindow(self.window, self.settings, self.localizer)
        prefs_window.present()
        
    def create_sidebar(self):
        """Kreira sidebar sa folderima"""
        sidebar_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        sidebar_box.set_size_request(280, -1)
        
        # Header
        header_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        header_box.set_margin_top(12)
        header_box.set_margin_bottom(12)
        header_box.set_margin_start(12)
        header_box.set_margin_end(12)
        sidebar_box.append(header_box)
        
        # Status card
        self.status_card = Adw.ActionRow()
        self.status_card.set_title(self.localizer.get_text('connection_status'))
        self.status_card.set_subtitle(self.localizer.get_text('checking'))
        
        # Connection button
        self.connect_btn = Gtk.Button()
        self.connect_btn.add_css_class("pill")
        self.connect_btn.set_valign(Gtk.Align.CENTER)
        self.connect_btn.connect("clicked", self.on_connect_clicked)
        self.status_card.add_suffix(self.connect_btn)
        
        status_group = Adw.PreferencesGroup()
        status_group.add(self.status_card)
        header_box.append(status_group)
        
        # Refresh button
        refresh_btn = Gtk.Button(label=self.localizer.get_text('refresh_connection'))
        refresh_btn.add_css_class("flat")
        refresh_btn.set_icon_name("view-refresh-symbolic")
        refresh_btn.connect("clicked", self.on_refresh_clicked)
        header_box.append(refresh_btn)
        
        # Folders section
        folder_label = Gtk.Label(label=self.localizer.get_text('folders'))
        folder_label.set_halign(Gtk.Align.START)
        folder_label.add_css_class("heading")
        folder_label.set_margin_start(12)
        folder_label.set_margin_end(12)
        folder_label.set_margin_top(6)
        sidebar_box.append(folder_label)
        
        # Folders list
        self.folders_listbox = Gtk.ListBox()
        self.folders_listbox.add_css_class("boxed-list")
        self.folders_listbox.connect("row-selected", self.on_folder_selected)
        
        folders_scroll = Gtk.ScrolledWindow()
        folders_scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        folders_scroll.set_child(self.folders_listbox)
        folders_scroll.set_vexpand(True)
        folders_scroll.set_margin_start(12)
        folders_scroll.set_margin_end(12)
        folders_scroll.set_margin_bottom(12)
        sidebar_box.append(folders_scroll)
        
        return sidebar_box
        
    def create_main_content(self):
        """Kreira glavni sadržaj"""
        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        
        # Action bar
        action_bar = self.create_action_bar()
        content_box.append(action_bar)
        
        # Photos area
        photos_area = self.create_photos_area()
        content_box.append(photos_area)
        
        # Progress area
        progress_area = self.create_progress_area()
        content_box.append(progress_area)
        
        return content_box
        
    def create_action_bar(self):
        """Kreira action bar sa dugmićima"""
        action_group = Adw.PreferencesGroup()
        action_group.set_margin_start(12)
        action_group.set_margin_end(12)
        action_group.set_margin_top(6)
        
        # Destination row
        self.dest_row = Adw.ActionRow()
        self.dest_row.set_title(self.localizer.get_text('destination_folder'))
        
        self.dest_entry = Gtk.Entry()
        self.dest_entry.set_text(str(Path.home() / "Pictures" / "iPhone_Photos"))
        self.dest_entry.set_hexpand(True)
        self.dest_row.add_suffix(self.dest_entry)
        
        browse_btn = Gtk.Button()
        browse_btn.set_icon_name("document-open-symbolic")
        browse_btn.add_css_class("flat")
        browse_btn.connect("clicked", self.on_browse_clicked)
        self.dest_row.add_suffix(browse_btn)
        
        action_group.add(self.dest_row)
        
        # Buttons row
        buttons_row = Adw.ActionRow()
        buttons_row.set_title(self.localizer.get_text('actions'))
        
        # Select all button
        self.select_all_btn = Gtk.Button(label=self.localizer.get_text('select_all'))
        self.select_all_btn.add_css_class("pill")
        self.select_all_btn.set_sensitive(False)
        self.select_all_btn.connect("clicked", self.on_select_all_clicked)
        buttons_row.add_suffix(self.select_all_btn)
        
        # Download button
        self.download_btn = Gtk.Button(label=self.localizer.get_text('download_selected'))
        self.download_btn.add_css_class("pill")
        self.download_btn.add_css_class("suggested-action")
        self.download_btn.set_sensitive(False)
        self.download_btn.connect("clicked", self.on_download_clicked)
        buttons_row.add_suffix(self.download_btn)
        
        action_group.add(buttons_row)
        
        return action_group
        
    def create_photos_area(self):
        """Kreira oblast za prikaz fotografija"""
        photos_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        photos_box.set_vexpand(True)
        photos_box.set_margin_start(12)
        photos_box.set_margin_end(12)
        
        # Photos header
        photos_header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        photos_header.set_margin_top(12)
        photos_header.set_margin_bottom(6)
        
        self.photos_title = Gtk.Label(label=self.localizer.get_text('photos'))
        self.photos_title.set_halign(Gtk.Align.START)
        self.photos_title.add_css_class("title-2")
        photos_header.append(self.photos_title)
        
        self.photos_stats = Gtk.Label()
        self.photos_stats.set_halign(Gtk.Align.END)
        self.photos_stats.add_css_class("dim-label")
        self.photos_stats.set_hexpand(True)
        photos_header.append(self.photos_stats)
        
        photos_box.append(photos_header)
        
        # Photos list
        self.photos_listbox = Gtk.ListBox()
        self.photos_listbox.add_css_class("boxed-list")
        self.photos_listbox.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.photos_listbox.connect("row-selected", self.on_photo_row_selected)
        
        photos_scroll = Gtk.ScrolledWindow()
        photos_scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        photos_scroll.set_child(self.photos_listbox)
        photos_scroll.set_vexpand(True)
        photos_box.append(photos_scroll)
        
        return photos_box
        
    def create_preview_panel(self):
        """Kreira preview panel za fotografije"""
        preview_frame = Gtk.Frame()
        preview_frame.add_css_class("view")
        preview_frame.set_size_request(-1, 300)
        
        preview_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        preview_box.set_margin_top(12)
        preview_box.set_margin_bottom(12)
        preview_box.set_margin_start(12)
        preview_box.set_margin_end(12)
        preview_frame.set_child(preview_box)
        
        # Left side - image preview
        self.preview_image = Gtk.Picture()
        self.preview_image.set_size_request(250, 250)
        self.preview_image.set_halign(Gtk.Align.CENTER)
        self.preview_image.set_valign(Gtk.Align.CENTER)
        self.preview_image.add_css_class("card")
        
        # Placeholder
        self.set_placeholder_preview()
        
        preview_box.append(self.preview_image)
        
        # Right side - metadata
        metadata_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        metadata_box.set_hexpand(True)
        preview_box.append(metadata_box)
        
        # Metadata title
        metadata_title = Gtk.Label(label=self.localizer.get_text('photo_details'))
        metadata_title.add_css_class("heading")
        metadata_title.set_halign(Gtk.Align.START)
        metadata_box.append(metadata_title)
        
        # Metadata grid
        metadata_grid = Gtk.Grid()
        metadata_grid.set_row_spacing(6)
        metadata_grid.set_column_spacing(12)
        metadata_box.append(metadata_grid)
        
        # Metadata labels
        self.preview_filename = self.create_metadata_row(metadata_grid, 0, self.localizer.get_text('filename'))
        self.preview_size = self.create_metadata_row(metadata_grid, 1, self.localizer.get_text('size'))
        self.preview_dimensions = self.create_metadata_row(metadata_grid, 2, self.localizer.get_text('dimensions'))
        self.preview_date = self.create_metadata_row(metadata_grid, 3, self.localizer.get_text('date'))
        self.preview_type = self.create_metadata_row(metadata_grid, 4, self.localizer.get_text('type'))
        
        # Action buttons
        action_buttons = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        action_buttons.set_margin_top(12)
        metadata_box.append(action_buttons)
        
        self.preview_download_btn = Gtk.Button(label=self.localizer.get_text('download_this'))
        self.preview_download_btn.add_css_class("pill")
        self.preview_download_btn.add_css_class("suggested-action")
        self.preview_download_btn.set_sensitive(False)
        self.preview_download_btn.connect("clicked", self.on_preview_download_clicked)
        action_buttons.append(self.preview_download_btn)
        
        self.preview_toggle_btn = Gtk.Button(label=self.localizer.get_text('add_to_selected'))
        self.preview_toggle_btn.add_css_class("pill")
        self.preview_toggle_btn.set_sensitive(False)
        self.preview_toggle_btn.connect("clicked", self.on_preview_toggle_clicked)
        action_buttons.append(self.preview_toggle_btn)
        
        return preview_frame
        
    def create_metadata_row(self, grid, row, label_text):
        """Kreira red u metadata grid-u"""
        label = Gtk.Label(label=label_text)
        label.add_css_class("dim-label")
        label.set_halign(Gtk.Align.END)
        grid.attach(label, 0, row, 1, 1)
        
        value = Gtk.Label()
        value.set_halign(Gtk.Align.START)
        value.set_selectable(True)
        grid.attach(value, 1, row, 1, 1)
        
        return value
        
    def set_placeholder_preview(self):
        """Postavlja placeholder za preview"""
        # Create a simple placeholder
        placeholder_pixbuf = GdkPixbuf.Pixbuf.new(
            GdkPixbuf.Colorspace.RGB, True, 8, 200, 150
        )
        placeholder_pixbuf.fill(0x88888888)  # Gray with alpha
        
        texture = Gdk.Texture.new_for_pixbuf(placeholder_pixbuf)
        self.preview_image.set_paintable(texture)
        
    def create_progress_area(self):
        """Kreira oblast za progress bar"""
        self.progress_bar = Gtk.ProgressBar()
        self.progress_bar.set_margin_start(12)
        self.progress_bar.set_margin_end(12)
        self.progress_bar.set_margin_bottom(12)
        self.progress_bar.set_show_text(True)
        
        return self.progress_bar
        
    def format_size(self, size_bytes):
        """Formatira veličinu fajla"""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024**2:
            return f"{size_bytes/1024:.1f} KB"
        elif size_bytes < 1024**3:
            return f"{size_bytes/(1024**2):.1f} MB"
        else:
            return f"{size_bytes/(1024**3):.1f} GB"
            
    def refresh_connection(self):
        """Osvežava status konekcije"""
        def check_connection():
            connected = self.manager.check_device_connection()
            GLib.idle_add(self.update_connection_status, connected)
            
        threading.Thread(target=check_connection, daemon=True).start()
        
    def update_connection_status(self, connected):
        """Ažurira prikaz statusa konekcije"""
        if connected:
            device_name = self.manager.device_name or 'iPhone'
            self.status_card.set_subtitle(f"✓ {self.localizer.get_text('connected')}: {device_name}")
            self.status_card.add_css_class("success")
            self.connect_btn.set_label(self.localizer.get_text('mount'))
            self.connect_btn.set_sensitive(True)
            
            if self.manager.is_mounted():
                self.connect_btn.set_label(self.localizer.get_text('unmount'))
                self.load_folders()
        else:
            self.status_card.set_subtitle(f"✗ {self.localizer.get_text('not_connected')}")
            self.status_card.add_css_class("error")
            self.connect_btn.set_label(self.localizer.get_text('connecting'))
            self.connect_btn.set_sensitive(False)
            self.clear_folders()
            self.clear_photos()
            
    def on_connect_clicked(self, button):
        """Handle za connect dugme"""
        if self.manager.is_mounted():
            # Demontiranje
            self.manager.unmount_device()
            button.set_label(self.localizer.get_text('mount'))
            self.clear_folders()
            self.clear_photos()
            self.select_all_btn.set_sensitive(False)
            self.download_btn.set_sensitive(False)
        else:
            # Montiranje
            def mount_device():
                GLib.idle_add(button.set_sensitive, False)
                GLib.idle_add(button.set_label, self.localizer.get_text('mounting'))
                
                success = self.manager.mount_device()
                
                if success:
                    GLib.idle_add(button.set_label, self.localizer.get_text('unmount'))
                    GLib.idle_add(self.load_folders)
                    GLib.idle_add(self.select_all_btn.set_sensitive, True)
                else:
                    GLib.idle_add(button.set_label, self.localizer.get_text('error_retry'))
                    
                GLib.idle_add(button.set_sensitive, True)
                
            threading.Thread(target=mount_device, daemon=True).start()
        
    def on_refresh_clicked(self, button):
        """Handle za refresh dugme"""
        self.refresh_connection()
        if self.manager.is_mounted():
            self.load_folders()
        
    def clear_folders(self):
        """Briše listu foldera"""
        while True:
            row = self.folders_listbox.get_row_at_index(0)
            if row is None:
                break
            self.folders_listbox.remove(row)
            
    def clear_photos(self):
        """Briše listu fotografija"""
        while True:
            row = self.photos_listbox.get_row_at_index(0)
            if row is None:
                break
            self.photos_listbox.remove(row)
        self.photo_items.clear()
        
    def load_folders(self):
        """Učitava listu foldera"""
        def load():
            folders = self.manager.get_photo_folders()
            GLib.idle_add(self.update_folders, folders)
            
        threading.Thread(target=load, daemon=True).start()
        
    def update_folders(self, folders):
        """Ažurira listu foldera"""
        self.clear_folders()
        
        for name, count, path in folders:
            folder_item = FolderListItem(name, count, path, self.localizer)
            self.folders_listbox.append(folder_item)
            
        # Auto-select first folder
        if folders:
            first_row = self.folders_listbox.get_row_at_index(0)
            if first_row:
                self.folders_listbox.select_row(first_row)
            
    def on_folder_selected(self, listbox, row):
        """Handle za odabir foldera"""
        if row and hasattr(row, 'folder_path'):
            self.current_folder = row.folder_path
            self.photos_title.set_text(f"{self.localizer.get_text('photos')} - {row.folder_name}")
            self.load_photos(row.folder_path)
            
    def load_photos(self, folder_path):
        """Učitava fotografije iz foldera"""
        def load():
            photos = self.manager.get_photos_from_folder(folder_path)
            GLib.idle_add(self.update_photos, photos)
            
        threading.Thread(target=load, daemon=True).start()
        
    def update_photos(self, photos):
        """Ažurira listu fotografija"""
        self.clear_photos()
        
        total_size = 0
        for photo in photos:
            photo_item = PhotoListItem(photo, self.localizer)
            # Set parent callback for checkbox updates
            photo_item._parent_callback = self.on_photo_selection_changed
            self.photos_listbox.append(photo_item)
            self.photo_items.append(photo_item)
            total_size += photo['size']
            
        # Update stats
        self.photos_stats.set_text(
            f"{len(photos)} {self.localizer.get_text('items')} • {self.format_size(total_size)}"
        )
        
        self.download_btn.set_sensitive(False)
        
        # Auto-select first photo for preview
        if photos:
            first_row = self.photos_listbox.get_row_at_index(0)
            if first_row:
                self.photos_listbox.select_row(first_row)
                
    def on_photo_row_selected(self, listbox, row):
        """Handle za odabir reda u listi fotografija"""
        if row and hasattr(row, 'photo_data'):
            self.update_preview(row.photo_data)
            self.current_preview_item = row
        else:
            self.clear_preview()
            self.current_preview_item = None
            
    def update_preview(self, photo_data):
        """Ažurira preview panel sa podacima fotografije"""
        try:
            # Load image
            photo_path = photo_data['path']
            
            if photo_data['type'] == self.localizer.get_text('video'):
                # For videos, show video icon instead of thumbnail
                icon_theme = Gtk.IconTheme.get_for_display(Gdk.Display.get_default())
                icon_texture = icon_theme.lookup_icon(
                    "video-x-generic", None, 200, 1, Gtk.TextDirection.NONE, 0
                ).load_texture()
                self.preview_image.set_paintable(icon_texture)
            else:
                # Load image thumbnail
                try:
                    pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                        str(photo_path), 250, 250, True
                    )
                    texture = Gdk.Texture.new_for_pixbuf(pixbuf)
                    self.preview_image.set_paintable(texture)
                except Exception as e:
                    print(f"{self.localizer.get_text('cannot_load_thumbnail')}: {e}")
                    self.set_placeholder_preview()
            
            # Update metadata
            self.preview_filename.set_text(photo_data['name'])
            self.preview_size.set_text(self.format_size(photo_data['size']))
            
            # Try to get image dimensions
            if photo_data['type'] == self.localizer.get_text('photo'):
                try:
                    pixbuf = GdkPixbuf.Pixbuf.new_from_file(str(photo_path))
                    width = pixbuf.get_width()
                    height = pixbuf.get_height()
                    self.preview_dimensions.set_text(f"{width} × {height}")
                except:
                    self.preview_dimensions.set_text(self.localizer.get_text('unknown'))
            else:
                self.preview_dimensions.set_text(self.localizer.get_text('video_file'))
            
            self.preview_date.set_text(
                photo_data['modified'].strftime("%d.%m.%Y %H:%M:%S")
            )
            self.preview_type.set_text(photo_data['type'])
            
            # Enable buttons
            self.preview_download_btn.set_sensitive(True)
            self.preview_toggle_btn.set_sensitive(True)
            
            # Update toggle button text based on selection
            if hasattr(self.current_preview_item, 'get_selected') and self.current_preview_item.get_selected():
                self.preview_toggle_btn.set_label(self.localizer.get_text('remove_from_selected'))
                self.preview_toggle_btn.add_css_class("destructive-action")
                self.preview_toggle_btn.remove_css_class("suggested-action")
            else:
                self.preview_toggle_btn.set_label(self.localizer.get_text('add_to_selected'))
                self.preview_toggle_btn.add_css_class("suggested-action")
                self.preview_toggle_btn.remove_css_class("destructive-action")
            
        except Exception as e:
            print(f"Error updating preview: {e}")
            self.clear_preview()
            
    def clear_preview(self):
        """Briše preview panel"""
        self.set_placeholder_preview()
        
        self.preview_filename.set_text("-")
        self.preview_size.set_text("-")
        self.preview_dimensions.set_text("-")
        self.preview_date.set_text("-")
        self.preview_type.set_text("-")
        
        self.preview_download_btn.set_sensitive(False)
        self.preview_toggle_btn.set_sensitive(False)
        
    def on_preview_download_clicked(self, button):
        """Handle za preuzmi ovu fotografiju"""
        if not hasattr(self, 'current_preview_item') or not self.current_preview_item:
            return
            
        # Create temporary selection with just this photo
        original_selection = [item.get_selected() for item in self.photo_items]
        
        # Clear all selections
        for item in self.photo_items:
            item.set_selected(False)
            
        # Select only current photo
        self.current_preview_item.set_selected(True)
        
        # Download
        self.download_single_photo()
        
        # Restore original selection
        for item, selected in zip(self.photo_items, original_selection):
            item.set_selected(selected)
            
        self.on_photo_selection_changed()
        
    def on_preview_toggle_clicked(self, button):
        """Handle za toggle odabir trenutne fotografije"""
        if not hasattr(self, 'current_preview_item') or not self.current_preview_item:
            return
            
        current_state = self.current_preview_item.get_selected()
        self.current_preview_item.set_selected(not current_state)
        
        # Update preview button text
        if not current_state:  # Now selected
            button.set_label(self.localizer.get_text('remove_from_selected'))
            button.add_css_class("destructive-action")
            button.remove_css_class("suggested-action")
        else:  # Now deselected
            button.set_label(self.localizer.get_text('add_to_selected'))
            button.add_css_class("suggested-action")
            button.remove_css_class("destructive-action")
            
        self.on_photo_selection_changed()
        
    def download_single_photo(self):
        """Preuzima samo jednu fotografiju"""
        selected_items = [item for item in self.photo_items if item.get_selected()]
        
        if not selected_items:
            return
            
        destination = Path(self.dest_entry.get_text())
        
        # Use simple filename for single photo
        dest_folder = destination
        dest_folder.mkdir(parents=True, exist_ok=True)
            
        def copy_file():
            item = selected_items[0]
            
            try:
                source = item.photo_data['path']
                dest = dest_folder / source.name
                
                # Avoid overwriting
                counter = 1
                original_dest = dest
                while dest.exists():
                    name_parts = original_dest.stem, counter, original_dest.suffix
                    dest = original_dest.parent / f"{name_parts[0]}_{name_parts[1]}{name_parts[2]}"
                    counter += 1
                
                GLib.idle_add(self.progress_bar.set_fraction, 0.5)
                GLib.idle_add(self.progress_bar.set_text, self.localizer.get_text('copying'))
                
                shutil.copy2(source, dest)
                
                GLib.idle_add(self.progress_bar.set_fraction, 0)
                GLib.idle_add(self.progress_bar.set_text, "")
                GLib.idle_add(self.show_toast, f"{self.localizer.get_text('photo_saved')}: {dest.name}")
                
            except Exception as e:
                GLib.idle_add(self.show_error, f"{self.localizer.get_text('copy_error')}: {e}")
                GLib.idle_add(self.progress_bar.set_fraction, 0)
                GLib.idle_add(self.progress_bar.set_text, "")
                
        threading.Thread(target=copy_file, daemon=True).start()
        
    def on_photo_selection_changed(self):
        """Called when photo selection changes"""
        has_selected = any(item.get_selected() for item in self.photo_items)
        self.download_btn.set_sensitive(has_selected)
        
        # Update select all button text
        all_selected = all(item.get_selected() for item in self.photo_items if self.photo_items)
        if has_selected and all_selected:
            self.select_all_btn.set_label(self.localizer.get_text('deselect_all'))
        else:
            self.select_all_btn.set_label(self.localizer.get_text('select_all'))
        
    def on_select_all_clicked(self, button):
        """Handle za select all dugme"""
        # Check if any items are selected
        has_selected = any(item.get_selected() for item in self.photo_items)
        select_all = not has_selected
        
        for item in self.photo_items:
            item.set_selected(select_all)
            
        # Update button states
        self.on_photo_selection_changed()
        
    def on_browse_clicked(self, button):
        """Handle za browse dugme"""
        dialog = Gtk.FileDialog()
        
        def on_response(dialog, result):
            try:
                folder = dialog.select_folder_finish(result)
                if folder:
                    path = folder.get_path()
                    self.dest_entry.set_text(path)
            except Exception as e:
                pass
                
        dialog.select_folder(parent=self.window, callback=on_response)
        
    def on_download_clicked(self, button):
        """Handle za download dugme"""
        selected_items = [item for item in self.photo_items if item.get_selected()]
        
        if not selected_items:
            return
            
        destination = Path(self.dest_entry.get_text())
        
        # Kreiranje subfolder-a po datumu
        today = datetime.now().strftime("%Y-%m-%d")
        if self.current_folder:
            folder_name = self.current_folder.name
            dest_folder = destination / f"{today}_{folder_name}"
        else:
            dest_folder = destination / today
            
        try:
            dest_folder.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            self.show_error(f"{self.localizer.get_text('cannot_create_folder')}: {e}")
            return
            
        def copy_files():
            total = len(selected_items)
            copied = 0
            errors = []
            
            GLib.idle_add(button.set_sensitive, False)
            GLib.idle_add(button.set_label, self.localizer.get_text('copying'))
            
            for i, item in enumerate(selected_items):
                try:
                    source = item.photo_data['path']
                    dest = dest_folder / source.name
                    
                    # Avoid overwriting
                    counter = 1
                    original_dest = dest
                    while dest.exists():
                        name_parts = original_dest.stem, counter, original_dest.suffix
                        dest = original_dest.parent / f"{name_parts[0]}_{name_parts[1]}{name_parts[2]}"
                        counter += 1
                    
                    shutil.copy2(source, dest)
                    copied += 1
                    
                    progress = (i + 1) / total
                    progress_text = self.localizer.get_text('copy_progress', copied, total)
                    GLib.idle_add(self.progress_bar.set_fraction, progress)
                    GLib.idle_add(self.progress_bar.set_text, progress_text)
                    
                except Exception as e:
                    errors.append(f"{source.name}: {e}")
                    
            GLib.idle_add(self.progress_bar.set_fraction, 0)
            GLib.idle_add(self.progress_bar.set_text, "")
            GLib.idle_add(button.set_sensitive, True)
            GLib.idle_add(button.set_label, self.localizer.get_text('download_selected'))
            
            if errors:
                error_msg = self.localizer.get_text('copy_errors', copied, total, "\n".join(errors[:5]))
                if len(errors) > 5:
                    error_msg += "\n" + self.localizer.get_text('and_more_errors', len(errors)-5)
                GLib.idle_add(self.show_error, error_msg)
            else:
                success_msg = self.localizer.get_text('copy_success', copied, dest_folder)
                GLib.idle_add(self.show_toast, self.localizer.get_text('copied_files', copied))
                
        threading.Thread(target=copy_files, daemon=True).start()
        
    def show_error(self, message):
        """Prikazuje error dialog"""
        dialog = Adw.MessageDialog(parent=self.window)
        dialog.set_heading(self.localizer.get_text('error'))
        dialog.set_body(message)
        dialog.add_response("ok", self.localizer.get_text('ok'))
        dialog.present()
        
    def show_toast(self, message):
        """Prikazuje toast notifikaciju"""
        toast = Adw.Toast()
        toast.set_title(message)
        toast.set_timeout(3)
        # Note: Toast overlay treba da bude dodato u window strukture
        # Za sada ćemo koristiti print kao fallback
        print(f"Toast: {message}")

def main():
    """Glavna funkcija"""
    # Proverava da li su potrebni alati instalirani
    required_tools = ['idevice_id', 'idevicepair', 'ifuse']
    missing_tools = []
    
    # Initialize settings for localization
    settings = AppSettings()
    localizer = Localizer(settings)
    
    for tool in required_tools:
        try:
            subprocess.run([tool, '--help'], capture_output=True, timeout=2)
        except (FileNotFoundError, subprocess.TimeoutExpired):
            missing_tools.append(tool)
    
    if missing_tools:
        print(f"{localizer.get_text('missing_tools')}")
        print(f"{localizer.get_text('install')}: {', '.join(missing_tools)}")
        print(f"\n{localizer.get_text('ubuntu_install')}")
        print("sudo apt install libimobiledevice-utils ifuse python3-gi gir1.2-adw-1")
        print(f"\n{localizer.get_text('fedora_install')}")
        print("sudo dnf install libimobiledevice-utils fuse-ifuse python3-gobject libadwaita-devel")
        return 1
    
    # Inicijalizacija Adwaita
    Adw.init()
    
    app = iPhonePhotoManagerGUI()
    return app.run(None)

if __name__ == "__main__":
    exit(main())
