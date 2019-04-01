for i in *;do convert -crop -100 "$i" "$i""cut" && rm "$i";done
