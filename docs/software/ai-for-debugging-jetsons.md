---
title: AI for Debugging Jetsons
author: Max Gardenswartz
updated: 2026-11-10
applies_to: [apark, indoor-lab]
assisted_by: Claude
glance: >-
  How to give an AI coding agent such as Claude Code restricted, logged SSH access to a Jetson, so it can pull logs, add new logging, and speed up debugging on a quadcopter or any other Jetson.
---

Debugging a robot usually means hours of SSH, `docker logs`, copying files, and guessing what to log next. An AI coding agent running on your ground station can do much of that for you. Over SSH, it can pull logs from a Jetson, read them, add new logging to your code, run it again, and compare the results. This speeds up debugging on a quadcopter or any other Jetson.

This page sets up that access safely. The agent gets its own SSH key that can only run single commands (no interactive shell), and every command it runs is written to a log on the robot. You keep your normal password login.

The examples use Claude Code, but any agent that runs `ssh` commands works the same way. For the Jetsons themselves, see [Jetsons](../hardware/jetsons.md).

Two terms are used throughout. The **ground station** is the computer where the agent runs. The **robot** is each Jetson. Every section says which one to run it on. Shell variables do not carry between computers or terminals, so each section sets the ones it needs.

!!! danger "Lockout Rules: Read All of Them Before Typing Anything"
    1. Keep one working shell on each robot open the whole time. Open new terminals to test. Never close the working one until the tests pass.
    2. Confirm your human password login works **before** you restrict any key.
    3. Never overwrite `authorized_keys` (`>`). Only append (`>>`) and keep a backup.
    4. Never set `PasswordAuthentication no` unless you have another way in.
    5. Each `authorized_keys` entry must be **one line**. A line break silently breaks the key.
    6. If you lock yourself out anyway, see [Recovery](#recovery-if-you-are-locked-out).

!!! warning "Props Off While an Agent Is Connected"
    While the agent is unlocked, it can run commands on the robot. Arbitrary shell access plus Docker is effectively root, because Docker group membership is root-equivalent. The safety layers that remain are the sudo password and **props off and the ESC power disconnected** during debugging.

## Create the Agent's Key (Ground Station, Once)

Choose the names. `KEY_COMMENT` is the label inside the key. It is how the key is found and removed later.

```bash
KEY_NAME=claude_robot_key
KEY_COMMENT=claude-robot-debug
```

!!! important
    Set a **passphrase** when prompted. Do not leave it empty.

```bash
ssh-keygen -t ed25519 -f ~/.ssh/$KEY_NAME -C "$KEY_COMMENT"
```

## Add SSH Aliases for One Robot (Ground Station)

Replace the three `ROBOT_*` values for the robot you are doing. The `_claude` alias uses the restricted key. The `_me` alias forces password login and ignores the agent.

```bash
ROBOT_ALIAS=homebrew02
ROBOT_IP=robot-ip-address
ROBOT_USER=robot-username
```

```bash
cat >> ~/.ssh/config <<EOF

Host ${ROBOT_ALIAS}_claude
    HostName $ROBOT_IP
    User $ROBOT_USER
    IdentityFile ~/.ssh/$KEY_NAME
    IdentitiesOnly yes

Host ${ROBOT_ALIAS}_me
    HostName $ROBOT_IP
    User $ROBOT_USER
    PubkeyAuthentication no
    PreferredAuthentications password
EOF
```

The robots' IP addresses are on [IP Reservations](ip-reservations.md). For the username, see [Contacts](../start-here/contacts.md).

## Make Sure Password Login Works (Robot)

Open a shell on the robot (SSH, or keyboard and monitor). **Keep this terminal open for the whole guide.**

```bash
sudo sshd -T | grep -i passwordauthentication
```

If it prints `passwordauthentication yes`, skip to the next section. If it prints `no`, enable it with a drop-in file. The `01-` prefix makes it win over other config files.

```bash
DROPIN=/etc/ssh/sshd_config.d/01-human-password.conf
```

```bash
echo 'PasswordAuthentication yes' | sudo tee $DROPIN
sudo sshd -t && sudo systemctl restart ssh
sudo sshd -T | grep -i passwordauthentication
```

!!! warning
    `sshd -t` must print nothing. If it prints an error, do **not** restart. Delete the file you just made. The last command must say `yes`. If it still says `no`, another config overrides it. Run `grep -ri passwordauth /etc/ssh/`.

Restarting `ssh` does not kill existing sessions.

## Test Password Login, Then Print the Public Key (Ground Station)

Open a **new terminal** on the ground station. Set the same alias you used above:

```bash
ROBOT_ALIAS=homebrew02
```

```bash
ssh ${ROBOT_ALIAS}_me
```

!!! danger
    You must get a password prompt and a normal shell. **If you do not, stop here and fix it.** Do not continue.

Type `exit`, then print the public key line and copy it:

```bash
KEY_NAME=claude_robot_key
```

```bash
cat ~/.ssh/$KEY_NAME.pub
```

## Prepare the Robot and Create the Wrapper (Robot)

Use your still-open robot shell. Set the names (the same `KEY_COMMENT` as above):

```bash
KEY_COMMENT=claude-robot-debug
WRAPPER=$HOME/bin/ssh-wrapper.sh
LOG_FILE=$HOME/logs/ssh-claude.log
```

Check that sudo needs a password. This must print nothing:

```bash
sudo -l | grep -i nopasswd
```

!!! warning
    If it prints a line, remove that `NOPASSWD` entry (`sudo visudo`, or the file in `/etc/sudoers.d/`). A password-protected sudo is your hard stop for the agent.

Back up `authorized_keys`:

```bash
mkdir -p ~/.ssh ~/bin ~/logs
chmod 700 ~/.ssh
touch ~/.ssh/authorized_keys
cp ~/.ssh/authorized_keys ~/.ssh/authorized_keys.bak
```

Create the wrapper. It refuses interactive shells and logs every command and its exit code:

```bash
printf 'LOG=%q\n' "$LOG_FILE" > $WRAPPER
cat >> $WRAPPER <<'EOF'
if [ -z "$SSH_ORIGINAL_COMMAND" ]; then
  echo "interactive shells disabled for this key" >&2
  exit 1
fi
echo "=== $(date -Is) CMD: $SSH_ORIGINAL_COMMAND" >> "$LOG"
bash -c "$SSH_ORIGINAL_COMMAND" 2>&1 | tee -a "$LOG"
rc=${PIPESTATUS[0]}
echo "EXIT: $rc" >> "$LOG"
exit "$rc"
EOF
sed -i '1i #!/bin/bash' $WRAPPER
chmod +x $WRAPPER
```

## Install the Restricted Key (Robot)

First, set the public key. Paste the whole line you copied between the quotes:

```bash
PUBKEY='ssh-ed25519 AAAA...paste-here... claude-robot-debug'
```

Make sure the file ends in a newline, so the new entry does not merge into the last line:

```bash
[ -n "$(tail -c1 ~/.ssh/authorized_keys)" ] && echo >> ~/.ssh/authorized_keys
```

Append the restricted entry:

```bash
printf 'command="%s",no-pty,no-port-forwarding,no-X11-forwarding,no-agent-forwarding %s\n' "$WRAPPER" "$PUBKEY" >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

Verify. The last line must start with `command="/home/`:

```bash
tail -n 1 ~/.ssh/authorized_keys
```

Count how many lines contain this key. It must print `1`:

```bash
KEY_BLOB=$(echo "$PUBKEY" | awk '{print $2}')
grep -cF "$KEY_BLOB" ~/.ssh/authorized_keys
```

!!! warning
    If the count is 2 or more, the same key also exists **without** restrictions, and the unrestricted entry wins. Show the line numbers:

    ```bash
    grep -nF "$KEY_BLOB" ~/.ssh/authorized_keys
    ```

    Delete the line that does **not** start with `command=` (replace `N` with its line number), then run the count again:

    ```bash
    LINE=N
    sed -i "${LINE}d" ~/.ssh/authorized_keys
    ```

## Unlock the Key and Test (Ground Station)

Set the names:

```bash
KEY_NAME=claude_robot_key
ROBOT_ALIAS=homebrew02
```

Check for a running SSH agent. If this prints nothing, start one:

```bash
echo $SSH_AUTH_SOCK
```

```bash
eval "$(ssh-agent -s)"
```

Unlock the key. Enter the passphrase. It locks again by itself after 8 hours.

```bash
ssh-add -t 8h ~/.ssh/$KEY_NAME
```

Run the tests:

```bash
ssh ${ROBOT_ALIAS}_claude "echo hello; whoami"
ssh ${ROBOT_ALIAS}_claude "docker ps"
ssh ${ROBOT_ALIAS}_claude
ssh ${ROBOT_ALIAS}_me
```

Expected results, in order:

1. `hello` and your username.
2. Docker output (if Docker is installed).
3. A refusal such as `PTY allocation request failed`. This is **correct**.
4. A password prompt and a full interactive shell.

On the robot, confirm the log recorded the commands:

```bash
tail $LOG_FILE
```

Plain `ssh <robot>` without an alias offers the agent's restricted key and hits the same refusal. Always use the `_me` alias for yourself.

Repeat the alias, password, key and test sections for each robot.

## Use It with Claude Code

Start Claude Code from a ground station shell where the SSH agent is loaded. Tell it to run non-interactive commands only, in the form `ssh <robot>_claude "<command>"`. Good first requests are to pull the logs of a container, find the cause of an error, or add logging to a node, rebuild it, and run it again.

Lock the SSH agent when you are done:

```bash
ssh-add -D
```

## Undo Everything

On the **robot** (through `_me` or the console), set the names:

```bash
KEY_COMMENT=claude-robot-debug
WRAPPER=$HOME/bin/ssh-wrapper.sh
LOG_FILE=$HOME/logs/ssh-claude.log
```

```bash
sed -i "/$KEY_COMMENT/d" ~/.ssh/authorized_keys
rm -f $WRAPPER $LOG_FILE
```

Only if you created the password drop-in earlier:

```bash
DROPIN=/etc/ssh/sshd_config.d/01-human-password.conf
sudo rm -f $DROPIN
sudo sshd -t && sudo systemctl restart ssh
```

!!! danger
    Removing the password drop-in turns password login off again if it was off originally. **Only do this if you have another way in** (a different key, or physical access), and keep your shell open.

On the **ground station**, set the name:

```bash
KEY_NAME=claude_robot_key
```

```bash
ssh-add -d ~/.ssh/$KEY_NAME
rm -f ~/.ssh/$KEY_NAME ~/.ssh/$KEY_NAME.pub
nano ~/.ssh/config
```

In `nano`, delete the `_claude` and `_me` blocks for each robot.

## Recovery: If You Are Locked Out

Password login and the console do not depend on `authorized_keys`. In order of effort:

1. **Console:** plug in HDMI and a USB keyboard, log in with your account password, and run the robot undo commands above.
2. **Other password path:** if `PasswordAuthentication` is on, connect with:

    ```bash
    ssh -o PubkeyAuthentication=no user@robot-ip
    ```

3. **Offline edit:** power off, mount the robot's SD card or NVMe on another Linux computer, and edit `/home/<user>/.ssh/authorized_keys`. Remove the agent's key line or restore `authorized_keys.bak`.

Common causes of key failures: `~/.ssh` not `700`, `authorized_keys` not `600`, a broken or multi-line entry, or `command=` pointing to a script that does not exist or is not executable.
