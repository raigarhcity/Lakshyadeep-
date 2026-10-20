# Synthesized score for the sleep explainer: soft pad, music-box arpeggio, whooshes and pops on cues.
import numpy as np, wave, sys

SR, DUR = 48000, 31.0
n = int(SR * DUR)
t = np.arange(n) / SR
L = np.zeros(n); R = np.zeros(n)
rng = np.random.default_rng(3)

def hz(midi): return 440 * 2 ** ((midi - 69) / 12)

def add(sig, start, pan=0.0, gain=1.0):
    i = int(start * SR); j = min(n, i + len(sig))
    if j <= i: return
    s = sig[: j - i] * gain
    L[i:j] += s * np.cos((pan + 1) * np.pi / 4)
    R[i:j] += s * np.sin((pan + 1) * np.pi / 4)

def env(length, a, r):
    k = np.arange(int(length * SR)) / SR
    e = np.minimum(1, k / a) * np.minimum(1, (length - k) / r)
    return np.clip(e, 0, 1)

# chord per scene (midi roots of a gentle I-vi-IV-V style loop in C)
scenes = [(0, 4.6, [57, 60, 64, 69]), (4.6, 9.8, [53, 57, 60, 65]), (9.8, 15.8, [48, 55, 60, 64]),
          (15.8, 21.6, [55, 59, 62, 67]), (21.6, 26.6, [50, 57, 60, 65]), (26.6, 31.0, [48, 55, 60, 64])]
for a, b, notes in scenes:
    length = b - a + 1.2
    k = np.arange(int(length * SR)) / SR
    e = env(length, 1.0, 1.4)
    for m in notes:
        f = hz(m)
        det = 1 + 0.002 * rng.standard_normal()
        tone = (np.sin(2 * np.pi * f * k) + 0.25 * np.sin(2 * np.pi * 2 * f * det * k) + 0.08 * np.sin(2 * np.pi * 3 * f * k))
        tone *= 1 + 0.15 * np.sin(2 * np.pi * 0.25 * k + m)
        add(tone * e, max(0, a - 0.6), pan=(m % 5 - 2) * 0.15, gain=0.045)
    # sub
    add(np.sin(2 * np.pi * hz(notes[0] - 12) * k) * e, max(0, a - 0.6), gain=0.05)

# music-box arpeggio, every half second, notes from the current chord up an octave
def bell(f, length=1.6):
    k = np.arange(int(length * SR)) / SR
    d = np.exp(-k * 3.2)
    return (np.sin(2 * np.pi * f * k) + 0.4 * np.sin(2 * np.pi * f * 2.76 * k) * np.exp(-k * 6)) * d * np.minimum(1, k / 0.004)

pattern = [0, 2, 1, 3, 2, 1, 3, 0]
for a, b, notes in scenes:
    step = 0
    x = a + 0.25
    while x < b - 0.3 and x < 30.2:
        m = notes[pattern[step % 8]] + 12
        add(bell(hz(m)), x, pan=0.4 * np.sin(step), gain=0.06)
        step += 1; x += 0.5

# whoosh into each scene change
def whoosh(length=0.9):
    k = int(length * SR)
    w = rng.standard_normal(k)
    # one-pole lowpass with a rising cutoff
    out = np.zeros(k); y = 0
    cut = np.linspace(0.02, 0.25, k) ** 1.5
    for i in range(k):
        y += cut[i] * (w[i] - y); out[i] = y
    e = np.sin(np.pi * np.linspace(0, 1, k)) ** 2
    return out * e

for c in [4.6, 9.8, 15.8, 21.6, 26.6]:
    add(whoosh(), c - 0.6, pan=-0.3, gain=0.5)
    add(whoosh(), c - 0.6, pan=0.3, gain=0.5)

# soft pops on pop-in moments
def pop(f=520, length=0.25):
    k = np.arange(int(length * SR)) / SR
    return np.sin(2 * np.pi * f * k * (1 + 1.5 * np.exp(-k * 30))) * np.exp(-k * 22)

for at, f in [(0.8, 660), (9.9, 520), (15.9, 590), (27.6, 660), (22.3, 440)]:
    add(pop(f), at, gain=0.22)

# low "heartbeat" thud on the warning card
for at in [22.4, 23.2]:
    k = np.arange(int(0.4 * SR)) / SR
    add(np.sin(2 * np.pi * 55 * k) * np.exp(-k * 9), at, gain=0.35)

mix = np.stack([L, R], 1)
fade = np.minimum(1, t / 0.6) * np.clip((DUR - t) / 1.5, 0, 1)
mix *= fade[:, None]
mix *= 0.89 / np.max(np.abs(mix))  # peak at about -1 dBFS

out = sys.argv[1] if len(sys.argv) > 1 else "out/score.wav"
with wave.open(out, "wb") as f:
    f.setnchannels(2); f.setsampwidth(2); f.setframerate(SR)
    f.writeframes((mix * 32767).astype("<i2").tobytes())
print("wrote", out)
