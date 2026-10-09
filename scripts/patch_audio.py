"""Reproducibly enable the unused forceMono flag in pinned audioI2S 3.0.12."""
from pathlib import Path
Import("env")
source = Path(env.subst("$PROJECT_LIBDEPS_DIR")) / env.subst("$PIOENV") / "ESP32-audioI2S/src/Audio.cpp"
(source.parent / "MonoMix.h").write_text((Path(env.subst("$PROJECT_DIR")) / "include/MonoMix.h").read_text())
text = source.read_text()
marker = "// CM-Radio: mono before filters and balance"
if marker not in text:
    anchor = "        computeVUlevel(*sample);"
    if text.count(anchor) != 1:
        raise RuntimeError("Pinned Audio.cpp layout changed; refusing an unverified mono patch")
    text = '#include "MonoMix.h"\n' + text.replace(anchor, "        " + marker + "\n        if(m_f_forceMono) monoMix::frame(*sample);\n" + anchor)
    source.write_text(text)
env.Append(CPPPATH=[str(Path(env.subst("$PROJECT_DIR")) / "include")])
