#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# ///

"""
Claude Code statusline - Python version
Generated from statusline.sh v1.4.0 (https://www.npmjs.com/package/@chongdashu/cc-statusline)
Theme: detailed | Colors: true | Features: directory, git, model, context, tokens, burnrate, session
"""

import json
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

STATUSLINE_VERSION = "1.4.0"

# ---- color settings ----
use_color = os.environ.get("NO_COLOR") is None


def color(code: str) -> str:
    """Return ANSI color escape sequence if colors enabled."""
    return f"\033[{code}m" if use_color else ""


def rst() -> str:
    """Reset color."""
    return "\033[0m" if use_color else ""


# ---- modern sleek colors ----
def dir_color() -> str:
    return color("38;5;117")  # sky blue


def model_color() -> str:
    return color("38;5;147")  # light purple


def version_color() -> str:
    return color("38;5;180")  # soft yellow


def cc_version_color() -> str:
    return color("38;5;249")  # light gray


def style_color() -> str:
    return color("38;5;245")  # gray


def git_color() -> str:
    return color("38;5;150")  # soft green


def usage_color() -> str:
    return color("38;5;189")  # lavender


def cost_color() -> str:
    return color("38;5;222")  # light gold


def burn_color() -> str:
    return color("38;5;220")  # bright gold


def context_color_by_pct(remaining_pct: int) -> str:
    """Return context color based on remaining percentage."""
    if remaining_pct <= 20:
        return color("38;5;203")  # coral red
    elif remaining_pct <= 40:
        return color("38;5;215")  # peach
    else:
        return color("38;5;158")  # mint green


def session_color_by_pct(session_pct: int) -> str:
    """Return session color based on elapsed percentage."""
    rem_pct = 100 - session_pct
    if rem_pct <= 10:
        return color("38;5;210")  # light pink
    elif rem_pct <= 25:
        return color("38;5;228")  # light yellow
    else:
        return color("38;5;194")  # light green


# ---- utility functions ----
def progress_bar(pct: int, width: int = 10) -> str:
    """Create an ASCII progress bar."""
    pct = max(0, min(100, pct))
    filled = pct * width // 100
    empty = width - filled
    return "=" * filled + "-" * empty


def get_git_branch() -> str | None:
    """Get current git branch name."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--git-dir"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode != 0:
            return None

        result = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()

        # Fallback to short HEAD
        result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    return None


def parse_iso_timestamp(ts: str) -> datetime | None:
    """Parse ISO timestamp string to datetime."""
    if not ts:
        return None
    try:
        # Handle Z suffix
        ts = ts.replace("Z", "+00:00")
        return datetime.fromisoformat(ts)
    except ValueError:
        return None


def fmt_time_hm(dt: datetime) -> str:
    """Format datetime as HH:MM."""
    return dt.strftime("%H:%M")


def get_ccusage_session_info() -> tuple[str, int, str] | None:
    """
    Get session time info from ccusage if available.
    Returns (session_txt, session_pct, session_bar) or None.
    """
    try:
        # Find ccusage executable (handles Windows .cmd files)
        ccusage_path = shutil.which("ccusage")
        if not ccusage_path:
            return None

        result = subprocess.run(
            [ccusage_path, "blocks", "--json"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode != 0:
            return None

        blocks_data = json.loads(result.stdout)
        blocks = blocks_data.get("blocks", [])

        # Find active block
        active_block = None
        for block in blocks:
            if block.get("isActive"):
                active_block = block
                break

        if not active_block:
            return None

        reset_time_str = active_block.get("usageLimitResetTime") or active_block.get("endTime")
        start_time_str = active_block.get("startTime")

        if not reset_time_str or not start_time_str:
            return None

        start_dt = parse_iso_timestamp(start_time_str)
        end_dt = parse_iso_timestamp(reset_time_str)
        now_dt = datetime.now(start_dt.tzinfo) if start_dt and start_dt.tzinfo else datetime.now()

        if not start_dt or not end_dt:
            return None

        total_seconds = (end_dt - start_dt).total_seconds()
        if total_seconds < 1:
            total_seconds = 1

        elapsed_seconds = (now_dt - start_dt).total_seconds()
        elapsed_seconds = max(0, min(elapsed_seconds, total_seconds))

        session_pct = int(elapsed_seconds * 100 / total_seconds)
        remaining_seconds = max(0, (end_dt - now_dt).total_seconds())

        rh = int(remaining_seconds // 3600)
        rm = int((remaining_seconds % 3600) // 60)
        end_hm = fmt_time_hm(end_dt)

        session_txt = f"{rh}h {rm}m until reset at {end_hm} ({session_pct}%)"
        session_bar = progress_bar(session_pct, 10)

        return (session_txt, session_pct, session_bar)

    except (subprocess.TimeoutExpired, FileNotFoundError, json.JSONDecodeError, TypeError):
        return None


def write_debug_log(input_data: str, script_dir: Path) -> None:
    """Write debug info to log file."""
    debug_log = script_dir / "statusline_debug.log"
    try:
        with open(debug_log, "a", encoding="utf-8") as f:
            f.write(f"=== DEBUG {datetime.now()} ===\n")
            f.write(f"INPUT_LENGTH={len(input_data)}\n")
            f.write(f"INPUT_PREVIEW={input_data[:500]}\n")
    except OSError:
        pass


def main() -> None:
    # Fix Windows console encoding for emoji support
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stdin.reconfigure(encoding="utf-8")

    # Read JSON input from stdin
    input_data = sys.stdin.read()
    script_dir = Path(__file__).parent

    # Write debug log
    write_debug_log(input_data, script_dir)

    # Parse JSON
    try:
        data = json.loads(input_data)
    except json.JSONDecodeError:
        data = {}

    # ---- extract basics ----
    home = os.environ.get("HOME", os.environ.get("USERPROFILE", ""))

    # Current directory
    workspace = data.get("workspace", {})
    current_dir = workspace.get("current_dir") or data.get("cwd") or "unknown"
    # Convert Windows backslashes to forward slashes
    current_dir = current_dir.replace("\\", "/")
    # Replace home with ~
    if home:
        home_normalized = home.replace("\\", "/")
        if current_dir.startswith(home_normalized):
            current_dir = "~" + current_dir[len(home_normalized) :]

    # Model info
    model = data.get("model", {})
    model_name = model.get("display_name") or "Claude"
    model_version = model.get("version") or ""

    # Session and version info
    session_id = data.get("session_id", "")
    cc_version = data.get("version", "")

    # Output style
    output_style_obj = data.get("output_style", {})
    output_style = output_style_obj.get("name", "") if isinstance(output_style_obj, dict) else ""

    # ---- git ----
    git_branch = get_git_branch()

    # ---- context window calculation ----
    context_pct = ""
    context_remaining_pct = 0
    ctx_color = color("1;37")  # default white

    context_window = data.get("context_window", {})
    context_size = context_window.get("context_window_size", 200000)
    current_usage = context_window.get("current_usage", {})

    if current_usage:
        input_tokens = current_usage.get("input_tokens", 0) or 0
        cache_creation = current_usage.get("cache_creation_input_tokens", 0) or 0
        cache_read = current_usage.get("cache_read_input_tokens", 0) or 0
        current_tokens = input_tokens + cache_creation + cache_read

        if current_tokens > 0 and context_size > 0:
            context_used_pct = current_tokens * 100 // context_size
            context_remaining_pct = max(0, min(100, 100 - context_used_pct))
            ctx_color = context_color_by_pct(context_remaining_pct)
            context_pct = f"{context_remaining_pct}%"

    # ---- cost and usage extraction ----
    cost_data = data.get("cost", {})
    cost_usd = cost_data.get("total_cost_usd")
    total_duration_ms = cost_data.get("total_duration_ms")

    # Calculate burn rate ($/hour)
    cost_per_hour = None
    if cost_usd is not None and total_duration_ms and total_duration_ms > 0:
        cost_per_hour = cost_usd * 3600000 / total_duration_ms

    # Token data
    input_tokens_total = context_window.get("total_input_tokens", 0) or 0
    output_tokens_total = context_window.get("total_output_tokens", 0) or 0
    tot_tokens = input_tokens_total + output_tokens_total
    if tot_tokens == 0:
        tot_tokens = None

    # Calculate tokens per minute
    tpm = None
    if tot_tokens and total_duration_ms and total_duration_ms > 0:
        tpm = tot_tokens * 60000 / total_duration_ms

    # ---- session info from ccusage ----
    session_txt = ""
    session_pct = 0
    session_bar = ""

    session_info = get_ccusage_session_info()
    if session_info:
        session_txt, session_pct, session_bar = session_info

    # ---- render statusline ----
    # Line 1: Core info (directory, git, model, claude code version, output style)
    line1_parts = []
    line1_parts.append(f"\U0001F4C1 {dir_color()}{current_dir}{rst()}")

    if git_branch:
        line1_parts.append(f"\U0001F33F {git_color()}{git_branch}{rst()}")

    line1_parts.append(f"\U0001F916 {model_color()}{model_name}{rst()}")

    if model_version:
        line1_parts.append(f"\U0001F3F7\uFE0F {version_color()}{model_version}{rst()}")

    if cc_version:
        line1_parts.append(f"\U0001F4DF {cc_version_color()}v{cc_version}{rst()}")

    if output_style:
        line1_parts.append(f"\U0001F3A8 {style_color()}{output_style}{rst()}")

    print("  ".join(line1_parts))

    # Line 2: Context and session time
    line2_parts = []

    if context_pct:
        context_bar = progress_bar(context_remaining_pct, 10)
        line2_parts.append(f"\U0001F9E0 {ctx_color}Context Remaining: {context_pct} [{context_bar}]{rst()}")
    else:
        line2_parts.append(f"\U0001F9E0 {ctx_color}Context Remaining: TBD{rst()}")

    if session_txt:
        sess_color = session_color_by_pct(session_pct)
        line2_parts.append(f"\u231B {sess_color}{session_txt}{rst()} {sess_color}[{session_bar}]{rst()}")

    if line2_parts:
        print("  ".join(line2_parts))

    # Line 3: Cost and usage analytics
    line3_parts = []

    if tot_tokens is not None:
        if tpm is not None:
            tpm_formatted = int(round(tpm))
            line3_parts.append(f"\U0001F4CA {usage_color()}{tot_tokens} tok ({tpm_formatted} tpm){rst()}")
        else:
            line3_parts.append(f"\U0001F4CA {usage_color()}{tot_tokens} tok{rst()}")

    if line3_parts:
        print("  ".join(line3_parts))


if __name__ == "__main__":
    main()
