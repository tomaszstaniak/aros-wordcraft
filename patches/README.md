# Preserved source changes

| Directory | Applies to | Applied by |
|---|---|---|
| `wordcraft/` | storytold/wordcraft at the pin in `upstreams.json`; order in `series` | `scripts/wc.py materialize` (`git am`) |
| `crates/` | crates.io crates named in `crates/crates.json` (registry checksum and patched-tree hash recorded) | `scripts/wc.py build` |
| `libc-aros/` | rust-aros `std-groundwork/libc-aros` at the commit in `scripts/wcconfig.py` | `scripts/wc.py build` |
| `aros-pthread/` | deadwood2/AROS `compiler/pthread` at the commit in `scripts/wcconfig.py` | `scripts/wc.py build` |

Every patch carries its problem, rationale, scope, upstream status, verification and removal condition in its header (for `wordcraft/`, the commit message). `crates/`, `libc-aros/` and `aros-pthread/` are the PhotoCraft AROS port's patches, copied unchanged; their headers name that port. The libc-aros patch was written against rust-aros `49324c45`; it applies with an offset to the newer commit used here. See [the patch workflow](../docs/patching.md).
