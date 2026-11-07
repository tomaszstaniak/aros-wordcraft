"""The catalogue descriptions name the C runtime of their own target.

    python3 -m unittest tests/package/test_requirements.py

An AROS program opens its C runtime libraries at start: crt, stdlib and m on ABIv11, stdc,
posixc and stdcio on mainline ABIv1. apkg probes every library a description requires before
it downloads anything, so a description that names the other ABI's runtime makes the package
uninstallable on the system it was built for (the 0.16.0 mainline and Raspberry Pi packages
had the ABIv11 list). package.py refuses such a description; this checks that it does, for
synthetic programs and for the descriptions in packaging/catalogue/.
"""
import sys
import tomllib
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))
import package  # noqa: E402

V11 = {"crt.library", "stdlib.library", "m.library"}
V1 = {"stdc.library", "posixc.library", "stdcio.library"}
# What every target's programs open besides the C runtime (window, pictures, requesters).
SHARED = ["dos.library", "intuition.library", "graphics.library", "cybergraphics.library",
          "iffparse.library", "asl.library", "datatypes.library", "keymap.library",
          "gl.library", "codesets.library", "bsdsocket.library"]
RUNTIME_OF = {"v11": V11, "v1": V1}


def programs(runtime):
    """Two programs whose bytes name the given C runtime and the shared libraries, as the
    auto-open tables of a real build do."""
    names = b"\0".join(n.encode() for n in sorted(runtime) + SHARED)
    return {"WordCraft": b"\x7fELF\0" + names, "wordcraft-cli": b"\x7fELF\0" + names}


def description(libraries):
    return {"requires_system": [{"type": "library", "id": lib} for lib in libraries]}


class Requirements(unittest.TestCase):
    def test_matching_runtime_passes(self):
        for runtime in (V11, V1):
            package.check_requirements(description(sorted(runtime) + ["asl.library"]), programs(runtime))

    def test_other_abis_runtime_is_refused(self):
        with self.assertRaises(package.Failure) as e:
            package.check_requirements(description(V11), programs(V1))
        self.assertIn("posixc.library", str(e.exception))
        with self.assertRaises(package.Failure):
            package.check_requirements(description(V1), programs(V11))

    def test_runtime_left_out_is_refused(self):
        with self.assertRaises(package.Failure) as e:
            package.check_requirements(description(["asl.library"]), programs(V1))
        self.assertIn("stdc.library", str(e.exception))

    def test_optional_libraries_may_stay_unlisted(self):
        package.check_requirements(description(V11), programs(V11))

    def test_library_no_program_names_is_refused(self):
        with self.assertRaises(package.Failure) as e:
            package.check_requirements(description(sorted(V1) + ["muimaster.library"]), programs(V1))
        self.assertIn("muimaster.library", str(e.exception))


class CatalogueDescriptions(unittest.TestCase):
    """packaging/catalogue/<id>.<arch>.<abi>.toml, one per target in package.CATALOGUE."""

    def descriptions(self):
        out = []
        for target, (arch, abi) in package.CATALOGUE.items():
            path = REPO / "packaging" / "catalogue" / f"{package.ID}.{arch}.{abi}.toml"
            out.append((target, abi, tomllib.loads(path.read_text())))
        self.assertEqual(len(out), 3)
        return out

    def test_each_names_its_own_runtime(self):
        for target, abi, meta in self.descriptions():
            required = {r["id"] for r in meta["requires_system"]}
            self.assertEqual(required & package.C_RUNTIME, RUNTIME_OF[abi], target)
            package.check_requirements(meta, programs(RUNTIME_OF[abi]))

    def test_each_is_refused_for_the_other_runtime(self):
        for target, abi, meta in self.descriptions():
            other = V1 if abi == "v11" else V11
            with self.assertRaises(package.Failure, msg=target):
                package.check_requirements(meta, programs(other))

    def test_revision_and_source_archive_follow_release_json(self):
        release = package.json.loads((REPO / "packaging" / "release.json").read_text())
        for target, abi, meta in self.descriptions():
            self.assertEqual(meta.get("revision"), release.get("revision"), target)
            self.assertEqual(meta["source"]["archive"], release["source_archive"], target)
        self.assertEqual(release["source_archive"], package.package_name(release, "source.zip"))


class PackageName(unittest.TestCase):
    def test_revision_in_every_name(self):
        base = {"name": "WordCraft", "release": "0.16.0"}
        self.assertEqual(package.package_name(base, "source.zip"), "WordCraft-0.16.0-source.zip")
        self.assertEqual(package.package_name({**base, "revision": 1}, "aros-x86_64-abiv1-pc.zip"),
                         "WordCraft-0.16.0-r1-aros-x86_64-abiv1-pc.zip")
        for bad in (0, -1, "1"):
            with self.assertRaises(package.Failure):
                package.package_name({**base, "revision": bad}, "source.zip")


if __name__ == "__main__":
    unittest.main()
