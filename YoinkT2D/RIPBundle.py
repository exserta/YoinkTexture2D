import os
import shutil
import UnityPy
from PIL import Image
import platform
import wave
import numpy as np

def extract_all_objects(bundle_path):
    main_dir = os.path.dirname(os.path.abspath(__file__))  
    temp_dir = os.path.join(main_dir, "Temporary")  
    os.makedirs(temp_dir, exist_ok=True)
    {}
    
    base_name = os.path.splitext(os.path.basename(bundle_path))[0]
    output_folder = os.path.join(main_dir, f"{base_name}_originalbundlename")
    os.makedirs(output_folder, exist_ok=True)
    
    
    temp_bundle_path = os.path.join(temp_dir, os.path.basename(bundle_path))
    shutil.copy2(bundle_path, temp_bundle_path)
    
    
    env = UnityPy.load(temp_bundle_path)
    count = 0
    texture_count = 0
    audio_count = 0
    found_any = False

    
    for obj in env.objects:
        try:
            
            if obj.type.name == "Texture2D":
                found_any = True
                texture = obj.read()
                img = texture.image
                if img:
                    
                    texture_name = obj.name if obj.name else f"texture_{texture_count}"
                    
                    
                    img_path = os.path.join(output_folder, f"{texture_name}.png")
                    img.save(img_path)
                    texture_count += 1

            
            elif obj.type.name == "AudioClip":
                found_any = True
                audio_clip = obj.read()
                
                
                channels = audio_clip.m_Channels
                frequency = audio_clip.m_Frequency
                audio_data = audio_clip.m_Resource
                
                
                if hasattr(audio_data, 'm_Source'):
                    external_file_path = audio_data.m_Source
                    if external_file_path:
                        print(f"External audio resource found: {external_file_path}")
                        
                        
                        if os.path.exists(external_file_path):
                            external_audio_name = obj.name if obj.name else f"audio_{audio_count}"
                            external_audio_path = os.path.join(output_folder, f"{external_audio_name}.wav")
                            shutil.copy2(external_file_path, external_audio_path)
                            audio_count += 1
                        else:
                            print(f"External file not found: {external_file_path}")
                else:
                    
                    audio_name = obj.name if obj.name else f"audio_{audio_count}"
                    audio_path = os.path.join(output_folder, f"{audio_name}.wav")
                    
                    
                    with wave.open(audio_path, 'wb') as wav_file:
                        wav_file.setnchannels(channels)
                        wav_file.setsampwidth(2)  
                        wav_file.setframerate(frequency)
                        wav_file.writeframes(np.array(audio_data, dtype=np.int16).tobytes())
                    
                    audio_count += 1

        except Exception as e:
            print(f"Error processing object: {e}")
            pass  
    
    
    if found_any:
        print(f"Textures Exported: {texture_count}")
        print(f"Audio Clips Exported: {audio_count}")
        print("Successfully exported all textures and audio clips.")
    else:
        print("No textures or audio clips found that could be exported.")

    print("\n" + "="*30)
    print(f"Bundle Path: {bundle_path}")
    print(f"Files saved in: {output_folder}")

def clear_console():
    
    os.system('cls' if platform.system() == 'Windows' else 'clear')

if __name__ == "__main__":
    while True:
        bundle_file = input("Drag and drop a .bundle file here and press Enter: ").strip().strip('"')
        if os.path.isfile(bundle_file) and bundle_file.endswith(".bundle"):
            clear_console()  
            extract_all_objects(bundle_file)
        else:
            print("Invalid file. Try again.")
