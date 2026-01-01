from pathlib import Path
import shutil

def main():
    cwd=Path.cwd()
    script_path=Path(__file__)
    script_name=script_path.name
    counters = {"moved_files": 0, "skipped_files": 0, "folders_created": 0, "errors": 0}
    created_folders=set()
    error_log=[]
    
    for item in cwd.iterdir():
        if item.is_dir():
            print(f"{item.name} is a directory, skipped")
            continue
        elif item.name.startswith('.'):
            print(f"{item.name} is hidden, skipped")
            counters["skipped_files"]+=1
            continue
        elif item.name==script_name:
            continue
        else:
            if item.suffix:
                folder_name=item.suffix[1:].upper()
            else:
                folder_name="no-extension"
            folder_path=cwd/folder_name
            if folder_name not in created_folders:
                    try:
                        Path(folder_name).mkdir(exist_ok=True)
                        created_folders.add(folder_name)
                        counters["folders_created"]+=1
                    except OSError as e:
                        print(f"Error creating folder {folder_name}: {e}")
                        counters["errors"]+=1
                        error_log.append(e)
            dest_path=folder_path/item.name
            if dest_path.exists():
                counters["skipped_files"]+=1
                print(f"{item.name} already exists in folder \"{folder_name}\",skipped")                
            else:
                try:
                    shutil.move(item,dest_path)
                    counters["moved_files"]+=1
                except OSError as e:
                    counters["errors"]+=1
                    error_log.append(e)
    print("---------------")
    print("Operation completed.")
    print("---------------")
    print("Logs:")
    for i in counters:
        print(f"{i} : {counters[i]}")
    print("---------------")
    if error_log:
        print("Error Log:")
        for i in error_log:
            print(i)



if __name__=="__main__":
    main()
