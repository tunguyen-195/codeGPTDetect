"""
Download basakdemirok/AIGCodeSet từ HuggingFace và lưu về máy.

Dataset:
  - 15,200 Python samples từ CodeNet competitive programming
  - train: 7,580 rows | test: 7,620 rows
  - HF labels: 0=Human, 1=LLM  →  Our labels: 0=AI, 1=Human (flip)
  - LLMs: CodeStral (Mistral), Gemini (Google), CodeLLaMA (Meta)

Output structure:
  DATASETS/AIGCodeSet/
  ├── training_data/   (7,580 files: 0_ai_*.py và 1_human_*.py)
  ├── testing_data/    (7,620 files)
  └── info.json        (thống kê dataset)
"""

import os
import json
import time
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────
SCRIPT_DIR   = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
OUT_DIR      = PROJECT_ROOT / "DATASETS" / "AIGCodeSet"
TRAIN_DIR    = OUT_DIR / "training_data"
TEST_DIR     = OUT_DIR / "testing_data"

def flip_label(hf_label: int) -> int:
    """HF: 0=Human, 1=LLM  →  Our: 0=AI, 1=Human"""
    return 1 - hf_label

def save_split(split, out_dir: Path, split_name: str):
    """Lưu một split thành .py files."""
    out_dir.mkdir(parents=True, exist_ok=True)

    ai_count    = 0
    human_count = 0
    skipped     = 0
    llm_sources = {}

    for i, row in enumerate(split):
        code      = row.get("code", "")
        hf_label  = int(row.get("label", -1))
        llm_name  = row.get("LLM", "unknown") or "unknown"

        if not code or hf_label not in (0, 1):
            skipped += 1
            continue

        our_label = flip_label(hf_label)
        prefix    = "ai" if our_label == 0 else "human"
        filename  = f"{our_label}_{prefix}_{split_name}_{i:05d}.py"
        fpath     = out_dir / filename

        fpath.write_text(code, encoding="utf-8")

        if our_label == 0:
            ai_count += 1
            llm_sources[llm_name] = llm_sources.get(llm_name, 0) + 1
        else:
            human_count += 1

        if (i + 1) % 1000 == 0:
            print(f"  [{split_name}] {i+1}/{len(split)} files saved ...")

    print(f"  [{split_name}] Done: AI={ai_count}, Human={human_count}, Skipped={skipped}")
    return {
        "total": ai_count + human_count,
        "ai":    ai_count,
        "human": human_count,
        "skipped": skipped,
        "llm_breakdown": llm_sources,
    }

def main():
    print("=" * 65)
    print("  Download: basakdemirok/AIGCodeSet")
    print("  Target  : DATASETS/AIGCodeSet/")
    print("=" * 65)

    # Check if already downloaded
    if TRAIN_DIR.exists() and len(list(TRAIN_DIR.glob("*.py"))) > 7000:
        print(f"\n[OK] Dataset already exists: {OUT_DIR}")
        print(f"  Train: {len(list(TRAIN_DIR.glob('*.py')))} files")
        print(f"  Test : {len(list(TEST_DIR.glob('*.py')))} files")
        info_path = OUT_DIR / "info.json"
        if info_path.exists():
            with open(info_path, encoding="utf-8") as f:
                info = json.load(f)
            print("\nDataset info:")
            print(json.dumps(info, indent=2, ensure_ascii=False))
        print("\nTo re-download, delete DATASETS/AIGCodeSet/ first.")
        return

    # Download from HuggingFace
    print("\nDownloading from HuggingFace (may take 2-5 minutes)...")
    t0 = time.time()

    try:
        from datasets import load_dataset
        hf_ds = load_dataset("basakdemirok/AIGCodeSet")
    except Exception as e:
        print(f"\n[ERROR] Failed to load dataset: {e}")
        print("Check internet connection and try again.")
        return

    elapsed_download = time.time() - t0
    print(f"[OK] Downloaded in {elapsed_download:.1f}s")
    print(f"  Splits  : {list(hf_ds.keys())}")
    print(f"  Columns : {hf_ds['train'].column_names}")
    print(f"  Train   : {len(hf_ds['train'])} rows")
    print(f"  Test    : {len(hf_ds['test'])} rows")

    # Save splits
    print(f"\nSaving to {OUT_DIR} ...")
    t1 = time.time()

    train_stats = save_split(hf_ds["train"], TRAIN_DIR, "train")
    test_stats  = save_split(hf_ds["test"],  TEST_DIR,  "test")

    elapsed_save = time.time() - t1

    # Save info.json
    info = {
        "dataset":     "basakdemirok/AIGCodeSet",
        "source":      "HuggingFace",
        "description": "Python code from CodeNet competitive programming - AI vs Human, same domain",
        "label_mapping": {
            "hf_original": {"0": "Human", "1": "LLM-generated"},
            "our_convention": {"0": "AI-Generated", "1": "Human-Written"},
        },
        "llms": ["CodeStral (Mistral AI)", "Gemini (Google DeepMind)", "CodeLLaMA (Meta)"],
        "training_data": train_stats,
        "testing_data":  test_stats,
        "total": {
            "files": train_stats["total"] + test_stats["total"],
            "ai":    train_stats["ai"]    + test_stats["ai"],
            "human": train_stats["human"] + test_stats["human"],
        },
        "download_time_sec": round(elapsed_download, 1),
        "save_time_sec":     round(elapsed_save, 1),
    }

    info_path = OUT_DIR / "info.json"
    with open(info_path, "w", encoding="utf-8") as f:
        json.dump(info, f, indent=2, ensure_ascii=False)

    # Summary
    print("\n" + "=" * 65)
    print("  DONE")
    print("=" * 65)
    print(f"\n  Folder  : {OUT_DIR}")
    print(f"  Train   : {train_stats['total']} files (AI={train_stats['ai']}, Human={train_stats['human']})")
    print(f"  Test    : {test_stats['total']} files  (AI={test_stats['ai']}, Human={test_stats['human']})")
    print(f"  Total   : {info['total']['files']} files")
    print(f"\n  LLM breakdown (train AI files):")
    for llm, count in sorted(train_stats["llm_breakdown"].items(), key=lambda x: -x[1]):
        print(f"    {llm:20s}: {count:,}")
    print(f"\n  info.json: {info_path}")
    print(f"\n  Download time: {elapsed_download:.1f}s | Save time: {elapsed_save:.1f}s")

if __name__ == "__main__":
    main()
