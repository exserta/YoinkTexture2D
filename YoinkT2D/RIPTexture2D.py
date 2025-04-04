import os
import shutil
import UnityPy
import sys
import tempfile
import time
import platform

def extract_textures(asset_path):
    main_dir = os.path.dirname(os.path.abspath(__file__))  
    temp_dir = os.path.join(main_dir, "Temporary")  
    os.makedirs(temp_dir, exist_ok=True)
    
    base_name = os.path.splitext(os.path.basename(asset_path))[0]
    output_folder = os.path.join(main_dir, base_name.replace("sharedassets", "Assets"))
    os.makedirs(output_folder, exist_ok=True)
    
    
    temp_asset_path = os.path.join(temp_dir, os.path.basename(asset_path))
    shutil.copy2(asset_path, temp_asset_path)
    
    resS_path = asset_path + ".resS"
    if os.path.exists(resS_path):
        temp_resS_path = temp_asset_path + ".resS"
        shutil.copy2(resS_path, temp_resS_path)
    
    
    env = UnityPy.load(temp_asset_path)
    count = 0
    found_any = False

    
    for obj in env.objects:
        obj_type = obj.type.name if hasattr(obj.type, 'name') else str(obj.type)
        if obj_type == "Texture2D":
            found_any = True
            texture = obj.read()
            try:
                img = texture.image
                if img:
                    
                    texture_name = None
                    if hasattr(texture, 'name') and texture.name:
                        texture_name = texture.name
                    elif hasattr(texture, 'fileID') and texture.fileID:
                        texture_name = f"texture_{texture.fileID}"
                    elif hasattr(texture, 'pathID') and texture.pathID:
                        texture_name = f"texture_{texture.pathID}"
                    else:
                        texture_name = f"texture_{count}"
                    
                    
                    img_path = os.path.join(output_folder, f"{texture_name}.png")
                    img.save(img_path)
                    count += 1
            except (FileNotFoundError, PermissionError) as e:
                pass  
    
    
    if found_any:
        print(f"Texture2D Objects Exported: {count}")
        print("Successfully exported all Texture2D objects")
    else:
        print("No Texture2D objects found.")
    
    print("\n" + "="*30)
    print(f"Assets Path: {asset_path}")
    
    
    print(f"Temporary files saved in: {temp_dir}")

def clear_console():
    
    os.system('cls' if platform.system() == 'Windows' else 'clear')

if __name__ == "__main__":
    while True:
        asset_file = input("Drag and drop a .assets file here and press Enter: ").strip().strip('"')
        if os.path.isfile(asset_file) and asset_file.endswith(".assets"):
            clear_console()  
            extract_textures(asset_file)
        else:
            print("Invalid file. Try again.")
