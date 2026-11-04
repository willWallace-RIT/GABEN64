import os
import shutil
import face_recognition
import numpy as np

class GabenClassifier:
    def __init__(self, ref_dir: str = "./reference_gaben", threshold: float = 0.55):
        self.ref_dir = ref_dir
        self.threshold = threshold
        self.encodings = []
        self._load_references()

    def _load_references(self):
        print(f"[*] Scanning reference encodings in {self.ref_dir}...")
        for file in os.listdir(self.ref_dir):
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                path = os.path.join(self.ref_dir, file)
                img = face_recognition.load_image_file(path)
                enc = face_recognition.face_encodings(img)
                if enc:
                    self.encodings.append(enc[0])
                else:
                    print(f"[!] Warning: No face detected in reference file {file}")
        print(f"[+] Loaded {len(self.encodings)} reference face encodings.")

    def filter_textures(self, src_dir: str = "./raw_sources", out_dir: str = "./validated_gaben"):
        os.makedirs(out_dir, exist_ok=True)
        print(f"[*] Evaluating source images from {src_dir}...")
        
        valid_count = 0
        for file in os.listdir(src_dir):
            if not file.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                continue
            
            path = os.path.join(src_dir, file)
            img = face_recognition.load_image_file(path)
            encs = face_recognition.face_encodings(img)
            
            if not encs:
                continue
            
            is_match = False
            for face_enc in encs:
                dists = face_recognition.face_distance(self.encodings, face_enc)
                if len(dists) > 0 and np.min(dists) <= self.threshold:
                    is_match = True
                    break
            
            if is_match:
                shutil.copy(path, os.path.join(out_dir, file))
                valid_count += 1
                print(f"[MATCH] Verified Gabe Newell image: {file}")
                
        print(f"[+] Verification complete. {valid_count} images staged for WAD injection.")

if __name__ == "__main__":
    classifier = GabenClassifier()
    classifier.filter_textures()
