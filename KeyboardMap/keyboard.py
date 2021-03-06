# coding=utf-8
# MIT License
#
# Copyright (c) 2020 UCAS Web Security Course
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import time

key_map_big = [
    # line 1
    [['`', '~'], ['-1'], ['1', '!'], ['-1'], ['2', '@'], ['-1'], ['3', '#'], ['-1'], ['4', '$'], ['-1'], ['5', '%'],
     ['-1'], ['6', '^'], ['-1'], ['7', '&'], ['-1'], ['8', '*'], ['-1'],
     ['9', '('], ['-1'], ['0', ')'], ['-1'], ['-', '_'], ['-1'], ['=', '+'], ['-1']],
    # line 2
    [['-1'], ['-1'], ['-1'], ['q'], ['-1'], ['w'], ['-1'], ['e'], ['-1'], ['r'], ['-1'], ['t'], ['-1'], ['y'],
     ['-1'], ['u'], ['-1'], ['i'], ['-1'], ['o'], ['-1'], ['p'], ['-1'], ['[', '{'], ['-1'], [']', '}'], ['-1'],
     ['\\', '|'], ['-1'], ],
    # line 3
    [['-1'], ['-1'], ['-1'], ['-1'], ['a'], ['-1'], ['s'], ['-1'], ['d'], ['-1'], ['f'], ['-1'], ['g'], ['-1'],
     ['h'], ['-1'], ['j'], ['-1'], ['k'], ['-1'], ['l'], ['-1'], [';', ':'], ['-1'], ['\'', '"'], ['-1'], ],
    # line 4
    [['-1'], ['-1'], ['-1'], ['-1'], ['-1'], ['z'], ['-1'], ['x'], ['-1'], ['c'], ['-1'], ['v'], ['-1'], ['b'],
     ['-1'], ['n'], ['-1'], ['m'], ['-1'], [',', '<'], ['-1'], ['.', '>'], ['-1'], ['/', '?'], ['-1'], ]
]

key_map_small = [
    [['-1'], ['-1'], ['/'], ['-1'], ['*'], ['-1'], ['-']],
    [['7'], ['-1'], ['8'], ['-1'], ['9'], ['-1'], ['+']],
    [['4'], ['-1'], ['5'], ['-1'], ['6'], ['-1'], ['-1']],
    [['1'], ['-1'], ['2'], ['-1'], ['3'], ['-1'], ['-1']],
    [['-1'], ['0'], ['-1'], ['-1'], ['-1'], ['-1'], ['-1']]
]

use_small = False

key_map = key_map_small if use_small else key_map_big


def keyboard_map(dataset_param):
    print_map()
    result = {}
    j = 0
    time_start = time.time()
    for data in dataset_param:  # 遍历全部密码
        aim_str = ''
        last_index = (-2, -2)
        for char in data:  # 遍历密码字符串
            x, y = find_index(char)
            # 计算和上一个位置的差值
            distance_x = 0.5 * (x - last_index[0])
            distance_y = y - last_index[1]
            distance = distance_x * distance_x + distance_y * distance_y
            if distance < 2 and x != -2:  # 如果邻位则加上
                aim_str += char
                # if len(aim_str) >= 3:
                #     if aim_str in result:
                #         result[aim_str] += 1
                #     else:
                #         result[aim_str] = 1
            else:
                if len(aim_str) >= 3:
                    if aim_str in result:
                        result[aim_str] += 1
                    else:
                        result[aim_str] = 1
                aim_str = char
            last_index = (x, y)
        if len(aim_str) >= 3:
            if aim_str in result:
                result[aim_str] += 1
            else:
                result[aim_str] = 1
        j += 1
        if j % 100000 == 0:
            time_end = time.time()
            percent = j / len(dataset_param) * 100
            print(f'Analyze 10W lines within {(time_end - time_start):.1f} seconds! {percent:.2f}%')
            time_start = time_end
    return result


# 拿到char在键盘里的index
def find_index(char):
    if char.isalpha():
        char = char.lower()
    for y in range(len(key_map)):
        for x in range(len(key_map[y])):
            for symbol in key_map[y][x]:
                if symbol == char:
                    return x, y
    return -2, -2


def print_map():
    print('\nThe key map which I used is like this:')
    for y in range(len(key_map)):
        for x in range(len(key_map[y])):
            if key_map[y][x][0] == '-1':
                print(' ', end='')
            else:
                print(key_map[y][x][0], end='')
        print()
    print()


if __name__ == "__main__":
    with open('../plaintxt_yahoo.txt', 'r+', encoding='utf-8', errors='ignore') as data_file:
        dataset = []
        line = data_file.readline()
        i = 0
        while line:
            # str_s = line.split(' # ')
            str_s = line.split(':', 2)
            if len(str_s) == 3:
                # dataset.append(str_s[1])
                dataset.append(str_s[2])
            else:
                print(f'error data: {line}')
            i += 1
            if i % 1000000 == 0:
                print(f'Load {len(dataset)} lines!')
                # break
            line = data_file.readline()
        print(f'Load file({len(dataset)} lines) complete!')
    result_map = keyboard_map(dataset)
    result_list = result_map.items()
    order_list = sorted(result_list, key=lambda item: item[1], reverse=True)
    with open(('result_small_csdn.dat' if use_small else 'result_big_yahoo_number.dat'), 'w', encoding='utf-8',
              errors='ignore') as out_file:
        j = 0
        for item in order_list:
            if item[0].isdigit():
                out_file.write(f'{item[0]} {item[1]} {(item[1]/i):.6f} {len(item[0])}\n')
                j += 1
                if j % 1000:
                    out_file.flush()
