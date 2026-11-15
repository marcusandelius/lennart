# Körd 2026-11-15 i /home/claude/fix: patch11.py är patch10.py med andra in- och utfiler.
sed -e "s/load('parts_v8.json')/load('parts_v11base.json')/" -e "s/parts_v10.json/parts_v11.json/g" patch10.py > patch11.py && python3 patch11.py
