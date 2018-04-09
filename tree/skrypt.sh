for name in output-*
do
	new_name=tree"$(echo $name | cut -c7-)"
	mv "$name" "$new_name"
done
