#!/usr/bin/env bash
export output_name=gxbzys-dlna-render_$(date "+%Y%m%d%H%M%S")_win32
export output_dir=../$output_name
mkdir -p $output_dir/gxbzys-dlna-render
cp -R -u render.py $output_dir
cd $output_dir
python -m nuitka --mingw64 --show-progress --nofollow-imports --follow-import-to=macast --follow-import-to=macast_renderer --follow-import-to=cheroot --follow-import-to=cherrypy --follow-import-to=more_itertools --follow-import-to=portend --follow-import-to=jaraco --follow-import-to=zc --follow-import-to=tempora --follow-import-to=requests --follow-import-to=urllib3 --follow-import-to=chardet --follow-import-to=idna --follow-import-to=pyperclip --module render.py