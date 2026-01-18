import os
import re

TARGET_DIR = "/Users/sagnikjana/Developer/diagram-copilot/client/src/assets/aws-icons"

def main():
    print(f"Scanning directory: {TARGET_DIR}")
    
    # 1. Collect all files
    all_files = []
    for root, dirs, files in os.walk(TARGET_DIR):
        for f in files:
            all_files.append(os.path.join(root, f))
            
    print(f"Total files found: {len(all_files)}")

    svg_files = []
    to_delete = []

    # 2. Identify files to delete (non-SVG) and collect SVGs
    for f in all_files:
        if f.lower().endswith('.svg'):
            svg_files.append(f)
        elif f.endswith('cleanup_aws_icons.py'):
            continue
        elif f.lower().endswith('.ds_store'):
            to_delete.append(f)
        else:
            # Delete all non-svg files (png, jpg, etc.)
            to_delete.append(f)
            
    print(f"Found {len(svg_files)} SVG files.")
    print(f"Found {len(to_delete)} non-SVG files to delete.")

    # 3. Group SVGs to handle size requirement
    # Logic: Group by base name. If multiple sizes exist for the same base name, keep only 64x64.
    
    # Map: base_name -> list of (size, filepath)
    icon_groups = {}
    
    # Regex to capture: (BaseName)_(Size).svg
    # Example: Arch_AWS-App-Runner_64.svg -> BaseName: Arch_AWS-App-Runner, Size: 64
    pattern = re.compile(r'(.*)_(\d+)\.svg$', re.IGNORECASE)

    for f in svg_files:
        filename = os.path.basename(f)
        match = pattern.search(filename)
        if match:
            base_name = match.group(1)
            size = int(match.group(2))
            
            if base_name not in icon_groups:
                icon_groups[base_name] = []
            icon_groups[base_name].append((size, f))
        else:
            # File doesn't match size pattern (e.g. icon.svg).
            # We treat these as unique/singleton and keep them.
            pass

    # 4. Determine which SVGs to delete based on groups
    redundant_svgs = 0
    for base_name, variants in icon_groups.items():
        # variants is list of (size, filepath)
        if len(variants) > 1:
            # Check for 64 size
            # The user requirement: "for the elements which are having the multiple svg elements keep only 64 * 64 elements"
            
            # Find if 64 exists
            has_64 = any(v[0] == 64 for v in variants)
            
            if has_64:
                # If 64 exists, keep ONLY 64. Delete all others (16, 32, 48, etc.)
                for size, path in variants:
                    if size != 64:
                        to_delete.append(path)
                        redundant_svgs += 1
            else:
                # If 64 does NOT exist, but we have multiple (e.g. 16, 32, 48).
                # The instruction implies we want 64. If 64 is missing, the preference is ambiguous.
                # However, usually "keep only 64" implies filtering for 64.
                # But to avoid data loss in case 64 is just missing from the set, we will KEEP the largest available?
                # Or keep all?
                # Given strict instruction, one might argue to delete all if 64 isn't there, 
                # but "elements which are having the multiple... keep only 64" acts as a filter on the set.
                # I will play it safe and NOT delete if 64 is missing. 
                # (Or strictly, I could just ensure I'm getting rid of obviously smaller ones if I wanted to be aggressive).
                # I'll leave them alone if 64 is missing.
                pass

    print(f"Identified {redundant_svgs} redundant SVG files (sizes != 64 where 64 exists).")
    
    total_delete_count = len(to_delete)
    if total_delete_count == 0:
        print("No files to delete.")
        return

    print(f"Starting deletion of {total_delete_count} files...")
    
    deleted_count = 0
    for f in to_delete:
        try:
            os.remove(f)
            deleted_count += 1
        except Exception as e:
            print(f"Error deleting {f}: {e}")

    # 5. Clean up empty directories
    print("Cleaning up empty directories...")
    removed_dirs = 0
    for root, dirs, files in os.walk(TARGET_DIR, topdown=False):
        for name in dirs:
            d = os.path.join(root, name)
            try:
                # check if dir is empty
                if not os.listdir(d):
                    os.rmdir(d)
                    removed_dirs += 1
            except OSError:
                pass

    print(f"Summary: Deleted {deleted_count} files. Removed {removed_dirs} empty directories.")

if __name__ == "__main__":
    main()
