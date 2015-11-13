# review - Generate reviewing templates

BASE_DIR="/home/driquet/perso/reviewing"
PYTHON="python"

review() {
	local out name config
	config="$BASE_DIR/review.cfg"
	while out=$(
		$PYTHON $BASE_DIR/template.py --config "$config" -l |
		fzf --ansi --no-sort --tac --toggle-sort=ctrl-r); do
			name=$(echo "$out" | cut -d':' -f2)
			$PYTHON $BASE_DIR/template.py --config "$config" --clipping "$name"
	done
}
