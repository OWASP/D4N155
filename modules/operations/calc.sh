#!/usr/env/bin bash

# Run operations
{
  # 1: Source
  # 2: Target
  # 3: Output

  cat "$1" | while read url 
		do
			echo "$url";
			bash "modules/operations/read.sh" "$url" \
				>> "reports/db/$2.blob.txt" && \
				echo -e ":.........................................$correct" || \
			  echo -e ":.........................................$incorrect"
      sleep $time
		done && _load "Make operations" """./modules/GoMutation reports/db/$2.blob.txt $3
      if [ \"$?\" != \"0\" ]
      then
        echo -e \"\n$red Error fatal$green\"
        [ -e reports/db/$2.blob.txt ] && rm -rf reports/db/$2.*
        exit 2
      fi
      """
      kill $! 1> /dev/null
}
