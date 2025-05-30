import json

def load_arabic_verses(arabic_path):
    with open(arabic_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["quran"]

def load_english_translation(english_path):
    with open(english_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["quran"]

def merge_quran(arabic_data, english_data):
    merged = []
    for ar in arabic_data:
        match = next(
            (en for en in english_data if en["chapter"] == ar["chapter"] and en["verse"] == ar["verse"]),
            None
        )
        if match:
            merged.append({
                "surah": ar["chapter"],
                "ayah": ar["verse"],
                "arabic": ar["text"],
                "english": match["text"]
            })
    return merged

def save_merged_json(merged, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(merged, f, indent=2, ensure_ascii=False)

def main():
    arabic_file = "arabic.json"
    english_file = "eng-sahih.json"
    output_file = "quran.json"

    arabic_verses = load_arabic_verses(arabic_file)
    english_data = load_english_translation(english_file)

    if len(arabic_verses) != len(english_data):
        print(f"❌ Mismatch: Arabic ({len(arabic_verses)}), English ({len(english_data)})")
        return

    merged = merge_quran(arabic_verses, english_data)
    if merged:
        save_merged_json(merged, output_file)
        print(f"✅ Merged successfully. Output saved to {output_file}")

if __name__ == "__main__":
    main()