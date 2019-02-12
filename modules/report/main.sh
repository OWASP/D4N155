#!/usr/bin/env bash

# $1 →  File to delete : Target urls
# $2 →  Report file    : All texts
# $3 →  Wordlist       : Output general
# $4 →  Target
export numberOfUrls="$(cat $1 | wc -l)"
export numberOfContents="$(du -hs $2 | awk '{print $1}')"
export numberOfResult="$(cat $3 | wc -l)"

# Defining name → $4
export name="$(echo $4 | cut -d '.' -f 1)"

__make(){
  # Head default of gruff
  # https://www.gnu.org/software/groff/manual/groff.html#Page-Layout
  cat << EOF > /tmp/report.txt
.TL
Report of $name

.LP
Urls processed: \fB$numberOfUrls\fP

Data processed:  \fB$numberOfContents\fP

Possibles passwords: \fB$numberOfResult\fP



EOF
  groff -ms /tmp/report.txt -T pdf > "../$name.pdf" && \
  ( echo -e "[\e[92m✔\e[m] The file has been saved in\n\e[33m\t→ $name.pdf\e[m";rm -rf tmp/report.txt ) || \
  ( echo -e "[\e[31m✘\e[m] groff dont are installed?";rm -rf /tmp/report.txt;exit 2 )
}

# call
__make
