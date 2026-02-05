import os
import json

def main():
    target_dir = "aws_icons"
    output_file = "aws_icons.json"
    
    icons_data = []
    
    print(f"Scanning {target_dir} for icons...")
    
    # Walk through the directory to find all svg files
    for root, dirs, files in os.walk(target_dir):
        for file in files:
            if file.lower().endswith(".svg"):
                # Get the full path relative to the script
                full_path = os.path.join(root, file)
                
                # ID: filename excluding .svg
                file_name_no_ext = os.path.splitext(file)[0]
                icon_id = file_name_no_ext
                
                # Name: replace - and _ with space and convert to lowercase
                icon_name = file_name_no_ext.replace("-", " ").replace("_", " ").lower()
                
                # URL: data URI string of the svg content (base64)
                try:
                    with open(full_path, 'rb') as svg_file:
                        svg_content = svg_file.read()
                        
                        import base64
                        encoded_svg = base64.b64encode(svg_content).decode('utf-8')
                        
                        icon_url = f"data:image/svg+xml;base64,{encoded_svg}"
                        
                        icons_data.append({
                            "id": icon_id,
                            "name": icon_name,
                            "url": icon_url
                        })
                except Exception as e:
                    print(f"Error reading {full_path}: {e}")
    
    # Sort for consistency
    icons_data.sort(key=lambda x: x['id'])
    
    # Write to json
    with open(output_file, 'w') as f:
        json.dump(icons_data, f, indent=2)
        
    print(f"Successfully generated {output_file} with {len(icons_data)} icons.")

if __name__ == "__main__":
    main()
