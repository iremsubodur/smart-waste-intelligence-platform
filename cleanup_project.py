import os
import shutil
import subprocess

ROOT = os.path.dirname(os.path.abspath(__file__))

TARGETS = [

    # dataset split copy (EN BÜYÜK KAZANÇ)
    "datasets/waste_dataset",

    # python cache
    "__pycache__",

    # torch cache
    ".torch",

    # logs / outputs (istersen)
    "outputs/plots",

]

def delete_path(path):
    full_path = os.path.join(ROOT, path)

    if os.path.exists(full_path):

        try:
            if os.path.isdir(full_path):
                shutil.rmtree(full_path)
            else:
                os.remove(full_path)

            print(f"Deleted: {path}")

        except Exception as e:
            print(f"Failed: {path} -> {e}")

def clean_pycache():

    print("\nCleaning __pycache__ ...")

    for root, dirs, files in os.walk(ROOT):

        for d in dirs:

            if d == "__pycache__":

                path = os.path.join(root, d)

                try:
                    shutil.rmtree(path)
                    print(f"Deleted: {path}")

                except:
                    pass

def clean_pip_cache():

    print("\nCleaning pip cache ...")

    try:
        subprocess.run(["pip", "cache", "purge"], check=True)
        print("pip cache cleaned")
    except:
        print("pip cache skip")

def show_disk_usage():

    print("\nProject size summary:\n")

    total = 0

    for root, dirs, files in os.walk(ROOT):

        for f in files:

            fp = os.path.join(root, f)

            try:
                total += os.path.getsize(fp)
            except:
                pass

    print(f"Total size: {round(total / (1024*1024), 2)} MB")

def main():

    print("\n==============================")
    print("SMART WASTE CLEANUP TOOL")
    print("==============================\n")

    show_disk_usage()

    print("\n--- Deleting heavy folders ---\n")

    for t in TARGETS:
        delete_path(t)

    clean_pycache()
    clean_pip_cache()

    print("\nDONE CLEANUP")

    show_disk_usage()

if __name__ == "__main__":
    main()