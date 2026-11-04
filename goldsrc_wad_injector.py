import os
import struct
import random
from PIL import Image

def convert_to_goldsrc_texture(img_path: str, width: int, height: int):
    """Resizes image and quantizes to 256-color GoldSrc indexed format."""
    img = Image.open(img_path).convert("RGB")
    img = img.resize((width, height), Image.Resampling.LANCZOS)
    
    # Quantize to 256 colors for GoldSrc paletted format
    paletted = img.quantize(colors=256)
    
    pixel_data = bytes(paletted.getdata())
    palette_data = bytearray()
    
    # Extract palette bytes (RGB)
    raw_palette = paletted.getpalette()[:768]
    palette_data.extend(raw_palette)
    
    return pixel_data, palette_data

def replace_wad_textures(wad_path: str, gaben_dir: str, output_wad_path: str):
    """Parses WAD3 header and overrides wall textures with Gabe Newell assets."""
    gaben_files = [
        os.path.join(gaben_dir, f) for f in os.listdir(gaben_dir) 
        if f.lower().endswith(('.png', '.jpg', '.jpeg'))
    ]
    
    if not gaben_files:
        raise FileNotFoundError("No validated Gabe Newell images found in directory!")

    print(f"[*] Reading GoldSrc WAD3 archive: {wad_path}")
    with open(wad_path, "rb") as f:
        magic, num_lumps, dir_offset = struct.unpack("<4sII", f.read(12))
        
        if magic != b"WAD3":
            raise ValueError("Target file is not a valid GoldSrc WAD3 archive.")

        f.seek(dir_offset)
        lumps = []
        for _ in range(num_lumps):
            # Lump structure: offset(4), disk_size(4), size(4), type(1), compression(1), pad(2), name(16)
            data = f.read(32)
            offset, disk_size, size, l_type, comp, _, name = struct.unpack("<IIIBBh16s", data)
            clean_name = name.rstrip(b"\x00").decode("latin-1")
            lumps.append({
                "offset": offset,
                "disk_size": disk_size,
                "size": size,
                "type": l_type,
                "name": clean_name
            })

    print(f"[+] Loaded {len(lumps)} texture lumps. Patching with Gabe Newell assets...")

    # Write patched WAD file
    with open(wad_path, "rb") as src, open(output_wad_path, "wb") as dst:
        # Copy header
        src.seek(0)
        dst.write(src.read(dir_offset))
        
        # Override lump entries matching standard wall textures
        for lump in lumps:
            # Type 67 = Standard Bounded Miptex Texture
            if lump["type"] == 67:
                src.seek(lump["offset"])
                tex_header = src.read(40) # Read name + dimensions
                tex_name, width, height = struct.unpack("<16sII", tex_header[:24])
                
                # Choose random Gaben image from validated pool
                chosen_gaben = random.choice(gaben_files)
                pixel_data, palette_data = convert_to_goldsrc_texture(chosen_gaben, width, height)
                
                # Write original texture header
                dst.seek(lump["offset"])
                dst.write(tex_header)
                
                # Write pixel buffer and mipmap buffers
                dst.write(pixel_data)
                
                # Write trailing palette count (256) and color table
                dst.seek(lump["offset"] + lump["size"] - 768 - 2)
                dst.write(struct.pack("<H", 256))
                dst.write(palette_data)
            else:
                # Copy unmodified non-texture lump
                src.seek(lump["offset"])
                dst.seek(lump["offset"])
                dst.write(src.read(lump["disk_size"]))

    print(f"[+] Patched WAD successfully saved to: {output_wad_path}")

if __name__ == "__main__":
    replace_wad_textures(
        wad_path="./valve/halflife.wad",
        gaben_dir="./validated_gaben",
        output_wad_path="./valve/halflife_gaben.wad"
    )
