init:
	pip3 install -r requirements.txt

clean:
	pystarter clean

run: clean
	python3 pi_ssh_vnc.py