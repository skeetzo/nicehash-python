#!/usr/bin/env bash
sudo bin/clean.sh
if [ -z "$1" ]; then
	set "Saved"
fi
git add . && git commit -m "$1" && git push origin python