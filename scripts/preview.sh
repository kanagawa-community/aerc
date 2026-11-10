# Preview hook for .github/scripts/render-previews.sh: aerc runs in a headless
# tmux pane with each styleset on a fixed maildir in scripts/fixtures/mail, so
# the folder list, read, unread and flagged messages, the selected row and the
# status line show.
# Requires: aerc, tmux.
# shellcheck shell=bash
name=aerc

setup() {
  mkdir -p "$work/cfg/aerc/stylesets"
  cp "$root"/themes/* "$work/cfg/aerc/stylesets/"
  printf '[kanagawa]\nsource = maildir://%s\nfrom = kanagawa <kanagawa@example.org>\ndefault = INBOX\n' \
    "$root/scripts/fixtures/mail" >"$work/cfg/aerc/accounts.conf"
  chmod 600 "$work/cfg/aerc/accounts.conf"
}

cleanup() {
  tmux -L kanagawa-preview kill-server 2>/dev/null || true
}

capture() {
  cleanup
  printf '[ui]\nstyleset-name=kanagawa-%s\n' "$1" >"$work/cfg/aerc/aerc.conf"
  sleep 0.5
  tmux -L kanagawa-preview new-session -d -s s -x 100 -y 14 -c "$work" \
    -e XDG_CONFIG_HOME="$work/cfg" -e HOME="$work" -e COLORTERM=truecolor \
    -e TERM=xterm-256color -e LC_ALL=C.UTF-8 aerc
  sleep 2.5
  tmux -L kanagawa-preview send-keys -t s j j
  sleep 1
  tmux -L kanagawa-preview capture-pane -p -e -t s >"$2"
}
