# seed_fire_spin.py
# Generate ". )" ASCII fire-spin frames from your private seed.
# Keep your seed private: do NOT paste it into chat.

import hashlib
import random
import time

SEED = "zjh"  # <-- replace locally

def seed_to_int(s: str) -> int:
    h = hashlib.sha256(s.encode("utf-8")).hexdigest()
    return int(h[:16], 16)

def make_frame(rng: random.Random, w: int, h: int, phase: float) -> list[str]:
    # Simple "flame" probability field + swirl via phase
    cx = (w - 1) / 2.0
    out = []
    for y in range(h):
        row = []
        # bottom is hotter
        heat = (h - 1 - y) / (h - 1 + 1e-9)
        for x in range(w):
            # swirl: shift center with phase and height
            shift = 2.0 * (1.0 - heat) * (0.5 + 0.5 * (rng.random()))
            swirl = cx + (w * 0.08) * ( (y / (h-1+1e-9)) * (1.0) ) * (1 if (int(phase) % 2 == 0) else -1)
            dx = abs(x - (swirl + (phase % 2.0 - 1.0) * shift))
            # flame density: more at center, more at bottom
            p = max(0.0, 0.55 * heat - 0.06 * dx)
            # choose chars
            r = rng.random()
            if r < p * 0.15:
                ch = ")"
            elif r < p * 0.45:
                ch = ")"
            elif r < p:
                ch = "."
            else:
                ch = "."
            row.append(ch)
        out.append("".join(row))
    return out

def generate_frames(seed: str, n_frames: int = 16, w: int = 13, h: int = 12) -> list[list[str]]:
    base = seed_to_int(seed)
    frames = []
    for k in range(n_frames):
        rng = random.Random(base + k * 1013)
        phase = k / n_frames * 6.28
        frames.append(make_frame(rng, w, h, phase))
    return frames

if __name__ == "__main__":
    frames = generate_frames(SEED, n_frames=16, w=13, h=12)
    for i, fr in enumerate(frames):
        print(f"FRAME {i}")
        for line in fr:
            print(line)
        print()
        time.sleep(0.03)  # optional pacing