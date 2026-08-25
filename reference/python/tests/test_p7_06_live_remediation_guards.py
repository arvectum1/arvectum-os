import subprocess
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
PYTHON_ROOT = HERE.parent
P702 = PYTHON_ROOT / "p7_02_macos_service.sh"
P706 = PYTHON_ROOT / "p7_06_macos_deploy.sh"


def function_block(text: str, name: str, next_name: str) -> str:
    start = text.index(f"{name}()")
    end = text.index(f"{next_name}()", start)
    return text[start:end]


class P706LiveRemediationGuardTests(unittest.TestCase):
    def test_p702_install_bootstrap_does_not_force_replace_runatload_process(self):
        text = P702.read_text(encoding="utf-8")
        install = function_block(text, "install_runtime", "start_runtime")
        self.assertIn('launchctl bootstrap "$DOMAIN" "$LAUNCH_AGENT"', install)
        self.assertIn('wait_healthy || fail "runtime did not become healthy after install"', install)
        self.assertNotIn('launchctl kickstart -k "$SERVICE_TARGET"', install)

    def test_p702_explicit_restart_keeps_replacement_semantics(self):
        text = P702.read_text(encoding="utf-8")
        restart = function_block(text, "restart_runtime", "status_runtime")
        self.assertIn('launchctl kickstart -k "$SERVICE_TARGET"', restart)
        self.assertIn('wait_healthy || fail "runtime did not become healthy after restart"', restart)

    def test_p706_wait_loaded_does_not_clobber_git_target_release(self):
        text = P706.read_text(encoding="utf-8")
        wait_loaded = function_block(text, "wait_loaded", "runtime_lock_available")
        self.assertIn("wait_target=$1", wait_loaded)
        self.assertIn('launchctl print "$wait_target"', wait_loaded)
        self.assertNotIn("\n  target=$1\n", wait_loaded)

        failure = function_block(text, "rollback_and_record_failure", "preflight")
        self.assertIn('write_payload "$payload" "$plan_id" "$source" "$target" ROLLED_BACK', failure)

    def test_pre_activation_stop_failure_is_not_labelled_rollback(self):
        text = P706.read_text(encoding="utf-8")
        start = text.index("record_pre_activation_stop_failure()")
        end = text.index("preflight()", start)
        failure = text[start:end]
        self.assertIn('"not executed: target activation never began; current pointer unchanged; backup retained', failure)
        self.assertIn("post_stop_state=not_queried_after_signal", failure)
        self.assertNotIn("workspace_status", failure)
        self.assertIn('"canonical_mutation_performed_by_deploy": False', text)
        self.assertIn('"product_external_effect_invoked": False', text)
        self.assertIn('"historical_effect_replay_invoked": False', text)
        self.assertNotIn("rollback_and_record_failure", failure)

    def test_remediated_shell_scripts_keep_posix_syntax(self):
        for script in (P702, P706):
            checked = subprocess.run(
                ["sh", "-n", str(script)],
                cwd=str(PYTHON_ROOT),
                text=True,
                capture_output=True,
                timeout=5,
            )
            self.assertEqual(checked.returncode, 0, checked.stderr)


if __name__ == "__main__":
    unittest.main()
