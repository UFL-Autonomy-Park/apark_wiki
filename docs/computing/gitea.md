---
title: Gitea SSH Setup
---

We use [Gitea](https://git.autonomypark.org) to manage our code for the Autonomy Park. To get an account, send the admin your preferred email address.

## Add an SSH Key to Gitea

Once you create your account, you will likely want to clone some repos. Add an SSH key to your Gitea account by navigating to **Settings -> SSH/GPG Keys -> Add Key**. Name the key and open a terminal. Run `ssh-keygen -t ed25519 -C "your_email@example.com"` and press enter until the prompts go away (no passphrase needed). 

Your public key will be saved as `~/.ssh/id_ed25519.pub`, and your private key will be saved as `~/.ssh/id_ed25519`. **Never share your private key.**

Now, run
```
cat ~/.ssh/id_ed25519.pub
```
Highlight the entire output, which starts with `ssh-ed25519`, and copy it to your clipboard. Paste the output in the "Content" field in your Gitea window.

Lastly, you need to verify your key. Open a new terminal and run 
```
echo -n '4ce37aba0aa035e8cc748ecf142cdc4183d44cc69a8d89fce36bebb840f2fa96' | ssh-keygen -Y sign -n gitea -f ~/.ssh/id_ed25519
```
Highlight the entire output which begins with `-----BEGIN SSH SIGNATURE-----` and copy it to your clipboard. Open Gitea and click "Verify" next to the SSH key you just added. Then, paste the output into the "Armored SSH signature" field and click "Verify."

## Connect SSH to Cloudflare
Your computer's SSH client needs to know how to use our Cloudflare tunnel when connecting to the Gitea SSH domain.

First, install cloudflared with the following commands
```
# Add Cloudflare's package signing key:
sudo mkdir -p --mode=0755 /usr/share/keyrings
curl -fsSL https://pkg.cloudflare.com/cloudflare-main.gpg | sudo tee /usr/share/keyrings/cloudflare-main.gpg >/dev/null

# Add this repo to your apt repositories
echo "deb [signed-by=/usr/share/keyrings/cloudflare-main.gpg] https://pkg.cloudflare.com/cloudflared any main" | sudo tee /etc/apt/sources.list.d/cloudflared.list

# install cloudflared
sudo apt-get update && sudo apt-get install cloudflared
```

Then, log in toe cloudflared by running `cloudflared login` in your terminal and follow the browser prompts to authenticate with your Cloudflare account. Next, open `~/.ssh/config` in a text editor (create it if it doesn't exist: `nano ~/.ssh/config`). Add the following block:
```
Host git-ssh.autonomypark.org
  ProxyCommand /usr/local/bin/cloudflared access ssh --hostname %h
```

You should now be able to do normal Git stuff with our code on Gitea. 