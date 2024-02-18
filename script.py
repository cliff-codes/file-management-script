from pathlib import Path
import shutil
import magic

# quick config set-up
mime = magic.Magic(mime=True)

files = {
    'pdfs': [],
    'txts': [],
    'docxs': [],
    'pptx': [],
    'images': [],
    'videos': [],
    'others': []
}


def getLocation():
    path = input("Enter location")
    # remove all empty spaces from path
    formatted_path = path.replace(" ", "")

    location = Path(formatted_path)
    if location:
        return location
    else:
        print('invalid path provided')
        return None


# finding type of file.
def get_file_type(file):
    try:
        print(f'this is file {file}')
        file_path = str(file.resolve())
        print(f'file path: {file_path}')
        file_type = mime.from_file(file_path)
        return file_type
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except PermissionError:
        print(f"Permission denied for file: {file_path}")
        return None


def get_files_of_same_type(path):
    for file in path.glob('**/*'):

        if file.is_file():
            print(file)
            # check type of file
            file_type = get_file_type(file)
            print(f'file type : {file_type}')
            # add to files
            if file_type == 'application/pdf':
                files.get('pdfs').append(file)
            elif file_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
                files.get('docxs').append(file)
            elif file_type in ['image/jpeg']:
                files.get('images').append(file)
            elif file_type == 'application/zip':
                files.get('pptx').append(file)
            elif file_type == 'video/mp4':
                files.get('videos').append(file)
            else:
                files.get('others').append(file)


# categorize files based on their types
def categorize_file_on_types(path):
    if not path:
        print('provide a valid location to categorize files')
        return
    else:
        get_files_of_same_type(location)


# save files in thier respective folders
def save_files_in_their_respective_folders(path, folder_name):
    files_collection = files.get(folder_name)

    if len(files_collection) > 0:
        pathname = Path(path) / folder_name
        print(f'folder path: {pathname}')

        if not pathname.exists():
            pathname.mkdir(parents=True, exist_ok=True)

        print(f'pathname: {pathname}')
        for file in files_collection:
            print(file)
            source_path = file
            destination_path = pathname / file.name
            if source_path.exists():
                shutil.move(file, destination_path)
            else:
                print(f'file not found: {source_path}, skipping...')
    else:
        print('no files found')


# saving folders
def store_files(path):
    save_files_in_their_respective_folders(path, 'pdfs')
    save_files_in_their_respective_folders(path, 'docxs')
    save_files_in_their_respective_folders(path, 'txts')
    save_files_in_their_respective_folders(path, 'images')
    save_files_in_their_respective_folders(path, 'pptx')
    save_files_in_their_respective_folders(path, 'videos')
    save_files_in_their_respective_folders(path, 'others')


location = getLocation()
if location:
    categorize_file_on_types(location)
    # store files
    store_files(location)
else:
    print("invalid location try again 😒")

print("script ended")
