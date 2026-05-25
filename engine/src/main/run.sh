clear
python ~/git/Neuroshima-online/engine/src/main/communication/komunikacja.py &
PID=$!

sleep 2
python client.py

kill -- $PID