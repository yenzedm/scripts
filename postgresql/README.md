bash

sudo apt-get update -y && sudo apt-get install -y python3-pip python3.10-venv && python3 -m venv venv && source venv/bin/activate && pip install docker psycopg2-binary && sudo venv/bin/python3 add_user_and_access_to_db-2.py && deactivate && rm -rf venv


pyinstaller

sudo apt-get update -y && sudo apt-get install -y python3-pip python3.10-venv && python3 -m venv venv && source venv/bin/activate && pip install docker psycopg2-binary pyinstaller && sudo venv/bin/python3 add_user_and_access_to_db-2.py && pyinstaller --onefile -n add_user_and_access_to_db add_user_and_access_to_db-2.py && deactivate && rm -rf venv


cmd

python -m venv venv && .\venv\Scripts\activate && pip install docker psycopg2-binary && python add_user_and_access_to_db-2.py && deactivate && rd/s/q venv


pyinstaller

python -m venv venv && .\venv\Scripts\activate && pip install docker psycopg2-binary pyinstaller && python add_user_and_access_to_db-2.py && pyinstaller --onefile -n add_user_and_access_to_db add_user_and_access_to_db-2.py && deactivate && rd/s/q venv


------------------------------------------------------------------------------------------


pyinstaller bash astra
sudo apt-get update -y && sudo apt-get install -y python3-pip python3-venv && python3 -m venv venv && source venv/bin/activate && pip install docker psycopg2-binary==2.8.3 pyinstaller==3.6 && pyinstaller --onefile -n add_user_and_access_to_db add_user_and_access_to_db-2.py && deactivate && rm -rf venv


pyinstaller cmd
python -m venv venv && .\venv\Scripts\activate && pip install docker psycopg2-binary pyinstaller && pyinstaller --onefile -n add_user_and_access_to_db add_user_and_access_to_db-2.py && deactivate && rd/s/q venv
