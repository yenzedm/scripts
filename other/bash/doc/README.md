# tagdoc - Small script for search by tags in text guide (TUI/CLI)

## About

Консольный (TUI/CLI) справочник для поиска информации по тегам.

Может быть использован сотрудниками в качестве адресной книги, справочника.

Студентами, при изучении новых языков программирования.

Cотрудниками IT, для записи полезных, но редко используемых конструкций, а также в качестве дополнения 
для man, в котором очень мало примеров использования.

Может использоваться любыми сотрудниками для записи интересных ссылок/статей.

Основным плюсом программы является то, что тэги задаете лично вы, и их всегда можно заменить для улучшения ассоциаций.

В отличие от grep поиск производится только по тэгам, не затрагивая тело статьи(заметки/комментария)

Строка тэгов может выделяться цветом.

Весь вывод идет в stdout, поэтому дополнительно можно воспользоваться любым фильтром (grep sed)

## Detailed

Вся инфа хранится в конфигурационном файле в виде:
```
#ekaterinburg bashdays devops shubin roman may 
Шубин Роман
tel 123456789
bashdays@telegram
ats 12587
loip 10.10.18.07
birth 22.05.2956
https://t.me/bashdays

#moscow admin malinin dmitry january gitgate
Малинин Дмитрий
tel 987654321
gitgate@telegram
ats 12586
birth 01.01.2953
https://t.me/gitgate
```
для поиска всех контактов из Екатеринбурга наберите

**tagdoc.sh ekaterinburg**

для поиска сотрудников московского филиала, с днем рождения в январе:

**tagdoc.sh moscow january**

порядок набора тэгов не важен.

При поиске можно использовать "_" для уточнения (граница слова)

**tagdoc.sh bcd**   = вхождение bcd (найдет bcd, abcd, bcde, abcde)

**tagdoc.sh _bcd**  = начинается на bcd (найдет _bcd, _bcde)

**tagdoc.sh bcd_**  = заканчивается на bcd (найдет bcd, abcd)

**tagdoc.sh _bcd_** = строго bcd (найдет bcd)

если нужно просмотреть список всех тэгов: **tagdoc.sh list**

если не помните ничего: **tagdoc.sh edit**

Конфигурационный файл откроется в редакторе и можно будет воспользоваться средствами редактора для поиска. Этот режим используется и для изменения/добавления информации.

Ключевые слова 'list' 'edit'  можно изменить в начале скрипта.

там же задается редактор.

Обычно имя конфигурационного файла соответствует имени скрипта. Создайте
жесткую ссылку (или копию) скрипта, если вы хотите использовать его для разных конфигурационных файлов.

## Attention:
IT IS UNDESIRABLE TO USE THE UNDERSCORE CHARACTER "_" IN CONFIG TAGS

В ТЭГАХ КОНФИГА ИСПОЛЬЗОВАТЬ СИМВОЛ ПОДЧЕРКИВАНИЯ "_" НЕЖЕЛАТЕЛЬНО

Использовать для хранения учетных данных нежелательно. Для этого есть **KeePassXC** и аналоги.

## Usage:

download tagdoc.sh tagdoc.conf

mkdir -p ~/work/tagdoc создали каталог
cd ~/work/tagdoc  перешли в него скачали файл.
wget https://raw.githubusercontent.com/tagd-tagd/tagdoc/refs/heads/main/tagdoc.sh

создали полный путь в переменной
AL="$PWD/doc.sh"

сделали исполняемым.
chmod a+x "$AL"

создали алиас для удобного запуска
содержимое $AL в кавычках
echo alias doc=${AL@Q} >> ~/.bashrc

применили изменение .bashrc
exec bash

**chmod +x ./tagdoc.sh**

**./tagdoc.sh**

**./tagdoc.sh list**

**./tagdoc.sh edit**


### Dependencies

**bash, awk**
