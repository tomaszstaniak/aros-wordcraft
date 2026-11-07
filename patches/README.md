# Preserved source changes

| Directory | Applies to | Applied by |
|---|---|---|
| `wordcraft/` | storytold/wordcraft at the pin in `upstreams.json`; order in `series` | `scripts/craft.py materialize` (`git am`) |
| `wordcraft-v0.7/` | the previous base, v0.7.0 (series 0001-0018, kept for history; not applied) | nothing |
| `crates/` | crates.io crates named in `crates/crates.json` (registry checksum and patched-tree hash recorded) | `scripts/craft.py build` |
| `libc-aros/` | rust-aros `std-groundwork/libc-aros` at the commit in the local file (`rust_aros_commit`); currently no patch | `scripts/craft.py build` |
| `aros-pthread/` | deadwood2/AROS `compiler/pthread` at the commit in `scripts/craftconfig.py` (ABIv11 target only) | `scripts/craft.py build` |
| `aros-glue/` | pomaros-hosted `hosted/rust` C bridge at the commit in the local file (Raspberry Pi target only) | `scripts/craft.py build` |

Every patch carries its problem, rationale, scope, upstream status,
verification and removal condition in its header (for `wordcraft/`, the commit
message). The crate, libc-aros and pthread sets are shared with the other
Craft ports; their headers may name the port they were written for. See
[the patch workflow](../docs/patching.md).
