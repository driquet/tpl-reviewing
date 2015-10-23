# review - Generate reviewing templates
review() {
	local out name
	while out=$(
		python ~/perso/reviewing/template.py -l |
		fzf --ansi --no-sort --tac --toggle-sort=ctrl-r); do
			name=$(echo "$out" | cut -d':' -f2)
			python ~/perso/reviewing/template.py --clipping "$name"
	done
}
