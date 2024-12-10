- Создаётся ветка в gitlab с названием target ветки
- source ветка указывается через переменную в gitlab
- при вызове скрипта check_page_exist.py пайплайном, скрипт:
- проверяет есть ли подходящая страница
- возвращает статус код exit(1) если нет, exit(0) если есть
	1. если exit(1)
		выполняется create_gitgraph.py
		создаётся файл diagram.mmd с содержимым gitgraph 
		дальше идёт bash команды по преобразованию diagram.mmd в diagram.svg
		выполняется скрипт confluence_page_not_exist.py
		создаёт страницу в конфе "mermaid n.n.n" по релизу target ветки
		создаёт html блок с содержимым diagram.svg
		добавляется на страницу файл diagram.mmd
	2. если exit(0)
		выполняется скрипт update_gitgraph.py
		ищет подходящую страницу в конфе которая содержит версию релиза target ветки
		забирает из комментария содержимое файла diagram.mmd
		и создаёт обновленный файл diagram.mmd в соответствии с target and source branch
		дальше идёт bash команды по преобразованию diagram.mmd в diagram.svg
		обновляет файл diagram.mmd на странице
		выполняется скрипт confluence_page_exist.py
		обновляет html блок содержимым diagram.svg
***
ubuntu 22.04
- sudo apt install nodejs
- sudo apt install npm
- sudo npm install -g n
- sudo n lts - обновить nodejs
- sudo npm install -g @mermaid-js/mermaid-cli
- npx puppeteer browsers install chrome или npx puppeteer browsers install chrome-headless-shell (rm -rf ~/.cache/puppeteer)
- sudo apt install -y libnss3 libatk1.0-0 libatk-bridge2.0-0 libxdamage1 libasound2
- sudo apt install -y libcups2 libxcomposite1 libxrandr2 libgbm1 libpango-1.0-0 libpangocairo-1.0-0 libxshmfence1
- mmdc -i diagram.mmd -o diagram.svg
***
ubuntu 24.04
sudo apt install nodejs
sudo apt install npm
sudo npm install -g n
sudo n lts - обновить nodejs
sudo npm install -g @mermaid-js/mermaid-cli
npx puppeteer browsers install chrome или npx puppeteer browsers install chrome-headless-shell (rm -rf ~/.cache/puppeteer)
Отключить AppArmor:
sudo sysctl -w kernel.apparmor_restrict_unprivileged_unconfined=0
sudo sysctl -w kernel.apparmor_restrict_unprivileged_userns=0
mmdc -i diagram.mmd -o diagram.svg
Включить AppArmor:
sudo sysctl -w kernel.apparmor_restrict_unprivileged_unconfined=1
sudo sysctl -w kernel.apparmor_restrict_unprivileged_userns=1