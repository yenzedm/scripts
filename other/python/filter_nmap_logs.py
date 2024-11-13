import re


with open('logs_test.txt', 'r') as file_read:
    with open('logs_output.txt', 'r+') as file_write:
        logs_output = file_write.read()
        flag = False
        result = ''
        pattern = r'(\b25[0-5]|\b2[0-4][0-9]|\b[01]?[0-9][0-9]?)(\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}'
        for line in file_read:
            if 'Nmap scan report' in line:
                if flag:
                    result = ''
                    flag = False
                if not re.search(pattern, line).group(0) in logs_output:
                    if 'Linux' in result:
                        file_write.write(result)
                        result = ''
                    else:
                        result = ''
                    result = line
                    continue
                else:
                    flag = True
                    continue
            result += line
        file_read.close()
        file_write.close()


# фильтр для команды nmap -O