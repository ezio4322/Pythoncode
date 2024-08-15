import os
import json

p_path = '/home/cosmin/Logs/TID'
time = '2024-08-15'
user = '269142149150212'

time_interval = 30


def main():
    file_path = os.path.join(p_path, f'time-{time}', f'user-{user}')
    if not os.path.isfile(file_path):
        print('file not found')
        return
    if os.stat(file_path).st_size == 0:
        print('file empty')
        return
    arranged_file_path = create_arranged_file()
    if not arranged_file_path:
        print('arranged file already exists')
        return
    with open(file_path, mode='r') as f:
        line = f.readline()
        sequence = ''
        for element in json.loads(line):
            sequence = sequence + element['name'] + ' '
        last_time = element['time']
        with open(arranged_file_path, mode='a') as g:
            g.write(sequence)
            line = f.readline()
            while line:
                dec_line = json.loads(line)
                if dec_line[0]['time'] - last_time > time_interval:
                    g.write('\n')
                sequence = ''
                for element in dec_line:
                    sequence = sequence + element['name'] + ' '
                last_time = element['time']
                g.write(sequence)
                line = f.readline()


def create_arranged_file():
    file_location = os.path.join(p_path, f'time-{time}',  f'arranged_file-user-{user}')
    if not os.path.exists(file_location):
        with open(file_location, mode='w'):
            print('Log file created')
        return file_location
    return False


if __name__ == '__main__':
    main()
