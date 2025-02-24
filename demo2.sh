python -m apps.simple_test -i ./static/img -o ./static/img
python apps/clean_mesh.py -f ./static/img/pifuhd_final/recon
python -m apps.render_turntable -f ./static/img/pifuhd_final/recon -ww 512 -hh 512