import shutil
import os

origin_dir = 'static'
destination_dir = 'public'

def recursive_copy(paths = []):
    if len(paths) == 0:
        return

    origin_path = os.path.join(origin_dir, paths[0])
    destination_path = os.path.join(destination_dir, paths[0])

    subdir_paths = []
    if os.path.isfile(origin_path):
        shutil.copy(origin_path, destination_path)
    else:
        os.mkdir(destination_path)
        subdir_paths = list(map(lambda p: os.path.join(paths[0], p), os.listdir(origin_path)))

    recursive_copy(paths[1:] + subdir_paths)

def copy_static():
    if os.path.exists(destination_dir):
        shutil.rmtree(destination_dir)
    os.mkdir(destination_dir)

    if not os.path.exists(origin_dir):
        raise FileNotFoundError(f"{origin_dir} directory not found")
    
    recursive_copy( os.listdir(origin_dir))



def main():
    try:
        copy_static()
    except FileNotFoundError as err:
        print(err)


if __name__ == '__main__':
    main()
    