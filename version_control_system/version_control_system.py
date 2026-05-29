import sys
import os
import shutil
import hashlib

VCS_DIR = "vcs"
CONFIG_FILE = os.path.join(VCS_DIR, "config.txt")
INDEX_FILE = os.path.join(VCS_DIR, "index.txt")
LOG_FILE = os.path.join(VCS_DIR, "log.txt")
COMMITS_DIR = os.path.join(VCS_DIR, "commits")

HELP_TEXT = """These are VCS commands:
config   Get and set a username.
add      Add a file to the index.
log      Show commit logs.
commit   Save changes.
checkout Switch between commits and restore a previous file state."""


def init_vcs():
    for path in [VCS_DIR, COMMITS_DIR]:
        if not os.path.exists(path): os.makedirs(path)
    for file in [CONFIG_FILE, INDEX_FILE, LOG_FILE]:
        if not os.path.exists(file):
            with open(file, "w", encoding="utf-8") as f: pass


def get_tracked_files():
    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def get_file_hash(filepath):
    if not os.path.exists(filepath): return ""
    hasher = hashlib.sha1()
    with open(filepath, "rb") as f:
        buf = f.read(65536)
        while len(buf) > 0:
            hasher.update(buf)
            buf = f.read(65536)
    return hasher.hexdigest()


def calculate_vcs_hash(tracked_files):
    hasher = hashlib.sha1()
    for file in sorted(tracked_files):
        if os.path.exists(file):
            hasher.update(file.encode("utf-8"))
            hasher.update(get_file_hash(file).encode("utf-8"))
    return hasher.hexdigest()


def cmd_config(args):
    if len(args) == 0:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            name = f.read().strip()
        print(f"The username is {name}." if name else "Please, tell me who you are.")
    else:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            f.write(args[0])
        print(f"The username is {args[0]}.")


def cmd_add(args):
    if len(args) == 0:
        files = get_tracked_files()
        if not files:
            print("Add a file to the index.")
        else:
            print("Tracked files:")
            for f in files: print(f)
    else:
        filename = args[0]
        if not os.path.exists(filename):
            print(f"Can't find '{filename}'.")
            return
        files = get_tracked_files()
        if filename not in files:
            with open(INDEX_FILE, "a", encoding="utf-8") as f: f.write(filename + "\n")
        print(f"The file '{filename}' is tracked.")


def cmd_commit(args):
    if len(args) == 0:
        print("Message was not passed.")
        return
    commit_message = args[0]
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        author = f.read().strip()
    tracked_files = get_tracked_files()
    existing_tracked = [f for f in tracked_files if os.path.exists(f)]

    if not existing_tracked:
        print("Nothing to commit.")
        return

    current_state_hash = calculate_vcs_hash(existing_tracked)
    last_commit_id = None
    if os.path.exists(LOG_FILE) and os.path.getsize(LOG_FILE) > 0:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            first_line = f.readline()
            if first_line.startswith("commit "):
                last_commit_id = first_line.replace("commit ", "").strip()

    if last_commit_id and last_commit_id == current_state_hash:
        print("Nothing to commit.")
        return

    commit_id = current_state_hash
    new_commit_dir = os.path.join(COMMITS_DIR, commit_id)
    if os.path.exists(new_commit_dir):
        print("Nothing to commit.")
        return

    os.makedirs(new_commit_dir)
    for file in existing_tracked:
        shutil.copy2(file, os.path.join(new_commit_dir, file))

    new_log_entry = f"commit {commit_id}\nAuthor: {author}\n{commit_message}\n\n"
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        old_logs = f.read()
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write(new_log_entry + old_logs)
    print("Changes are committed.")


def cmd_log(args):
    if not os.path.exists(LOG_FILE) or os.path.getsize(LOG_FILE) == 0:
        print("No commits yet.")
        return
    with open(LOG_FILE, "r", encoding="utf-8") as f: logs = f.read().strip()
    print(logs if logs else "No commits yet.")


def cmd_checkout(args):
    if len(args) == 0:
        print("Commit id was not passed.")
        return
    commit_id = args[0]
    target_commit_dir = os.path.join(COMMITS_DIR, commit_id)
    if not os.path.exists(target_commit_dir):
        print("Commit does not exist.")
        return
    for root, dirs, files in os.walk(target_commit_dir):
        for file in files:
            full_src_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_src_path, target_commit_dir)
            shutil.copy2(full_src_path, rel_path)
    print(f"Switched to commit {commit_id}.")


def main():
    init_vcs()
    args = sys.argv[1:]
    if not args or args[0] == "--help":
        print(HELP_TEXT)
        return

    command = args[0]
    command_args = args[1:]

    commands = {
        "config": cmd_config,
        "add": cmd_add,
        "commit": cmd_commit,
        "log": cmd_log,
        "checkout": cmd_checkout
    }

    if command in commands:
        commands[command](command_args)
    else:
        print(f"'{command}' is not a VCS command.")


if __name__ == "__main__":
    main()