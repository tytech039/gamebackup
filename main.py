import os
import shutil
import json
import datetime
import zipfile

# Constants
CONFIG_FILE = 'backup_config.json'


def load_or_create_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as file:
            return json.load(file)
    else:
        config = {
            'source_folder': input('Enter the path to the folder you want to back up: '),
            'backup_type': 'local',
            'destination_folder': input('Enter the path for storing backups locally: ')
        }
        with open(CONFIG_FILE, 'w') as file:
            json.dump(config, file, indent=4)
        return config


def zip_folder(source_folder, zip_filename):
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_folder):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), source_folder))


def backup(config):
    temp_folder = os.path.join(os.path.dirname(__file__), 'temp_backup')
    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)

    # Copy files to temp folder
    for item in os.listdir(config['source_folder']):
        s = os.path.join(config['source_folder'], item)
        d = os.path.join(temp_folder, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, dirs_exist_ok=True)
        else:
            shutil.copy2(s, d)

    # Create zip file
    date_str = datetime.datetime.now().strftime('%Y-%m-%d')
    zip_filename = f'backup_{date_str}.zip'
    zip_folder(temp_folder, zip_filename)

    # Move zip file to destination folder
    shutil.move(zip_filename, os.path.join(config['destination_folder'], zip_filename))

    # Cleanup
    shutil.rmtree(temp_folder)
    if os.path.exists(zip_filename):
        os.remove(zip_filename)


def main():
    config = load_or_create_config()
    backup(config)


if __name__ == '__main__':
    main()
