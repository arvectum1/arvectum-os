import importlib.util
import json
import pathlib
import sys
import tempfile
import unittest
from unittest import mock

HERE = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
SPEC = importlib.util.spec_from_file_location("p9_11_workspace_process", HERE / "p9_11_workspace_process.py")
process = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(process)


class WorkspaceProcessStatusTests(unittest.TestCase):
    def _root(self, current: str, listener: str) -> pathlib.Path:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = pathlib.Path(temporary.name)
        for release in {current, listener}:
            source = root / "releases" / release / "source/reference/python"
            source.mkdir(parents=True)
            (root / "venvs" / release / "bin").mkdir(parents=True)
            (root / "venvs" / release / "bin/python").touch()
            (source / "p9_03_workspace.py").touch()
            (source / "workspace_frontend/dist").mkdir(parents=True)
            (source / "workspace_frontend/dist/index.html").touch()
        return root.resolve()

    def _status(self, root: pathlib.Path, listener_release: str):
        source = root / "releases" / listener_release / "source/reference/python"
        with (
            mock.patch.object(process, "_current_release", return_value="current"),
            mock.patch.object(process, "_listener", return_value=(30686, "Python")),
            mock.patch.object(process, "_process_command", return_value="Python p9_03_workspace.py serve"),
            mock.patch.object(process, "_process_cwd", return_value=source),
            mock.patch.object(process, "_live_assets_match", return_value=True),
            mock.patch.object(process.p706, "verify_release"),
        ):
            return process.status(root)

    def test_current_exact_requires_exact_listener_release(self):
        root = self._root("current", "current")
        self.assertEqual(self._status(root, "current")["state"], process.CURRENT_EXACT)

    def test_historical_exact_listener_is_stale_known_exact(self):
        root = self._root("current", "historical")
        observed = self._status(root, "historical")
        self.assertEqual(observed["state"], process.STALE_KNOWN_EXACT)
        self.assertEqual(observed["pid"], 30686)

    def test_non_workspace_listener_is_unknown(self):
        root = self._root("current", "current")
        with (
            mock.patch.object(process, "_current_release", return_value="current"),
            mock.patch.object(process, "_listener", return_value=(30686, "Python")),
            mock.patch.object(process, "_process_command", return_value="unrelated"),
            mock.patch.object(process, "_process_cwd", return_value=None),
        ):
            self.assertEqual(process.status(root)["state"], process.UNKNOWN)

    def test_stop_refuses_unknown_without_signalling(self):
        with (
            mock.patch.object(process, "status", return_value={"state": process.UNKNOWN}),
            mock.patch.object(process.os, "kill") as kill,
            self.assertRaises(process.WorkspaceProcessError),
        ):
            process.stop_for_update(pathlib.Path("/tmp/runtime"))
        kill.assert_not_called()

    def test_process_metadata_uses_release_payload_beside_workspace_source(self):
        root = self._root("current", "current")
        release = root / "releases/current/source/reference/python"
        (release / "workspace_app").mkdir()
        (release / "workspace_app/release.json").write_text(json.dumps({"release_id": "p9.11.2"}))
        process._write_process_metadata(root, "current", 123)
        payload = json.loads((root / "run/workspace-process.json").read_text())
        self.assertEqual(payload["workspace_release"], "p9.11.2")


class LifecycleShellTests(unittest.TestCase):
    def test_update_stops_workspace_after_backup_and_restarts_target(self):
        text = (HERE / "p7_06_macos_deploy.sh").read_text()
        update = text[text.index("update_runtime()"):text.index("rollback_last()")]
        self.assertLess(update.index('backup_preupdate "$source"'), update.index("workspace_stop_for_update"))
        self.assertLess(update.index("workspace_stop_for_update"), update.index('sh "$P705" uninstall'))
        self.assertIn("Workspace listener is UNKNOWN; operator investigation required", update)
        self.assertIn("target Workspace exact-release restart failed", update)
        self.assertIn('"workspace_listener_disposition"', text)
        self.assertIn('printf \'%s\\n\' "$workspace_was_running" > "$txdir/workspace-was-running"', update)
        self.assertIn('source observer did not unload', update)
        self.assertIn('source runtime did not stop', update)
        restore = text[text.index("restore_plist_and_start()"):text.index("backup_preupdate()")]
        self.assertLess(restore.index("workspace_stop_for_update"), restore.index('rm -f "$RUNTIME_ROOT/current"'))
        self.assertIn('workspace-was-running" ]; then', text)

    def test_launcher_requires_current_exact_not_http_200(self):
        text = (HERE / "macos_launcher/launcher.sh").read_text()
        self.assertIn('= "CURRENT_EXACT"', text)
        self.assertIn('start --runtime-root "$RUNTIME_ROOT"', text)
        self.assertNotIn("http_code", text)
