import warnings
from functools import total_ordering

CHAR_TO_INT = {str(i): i for i in range(10)}
INT_TO_CHAR = [(str(i%10),i//10) for i in range(0,90)] + [(str(i%10),i//10) for i in range(-10,0)]

def compare(a:str, b:str) -> int: # a,b为非负数，不建议作为独立函数使用
    if a == '.':
        if b == '.':
            return 0
        else:
            return -1
    if b == '.':
        return 1
    a_integer, a_fractional = a.split(".")
    b_integer, b_fractional = b.split(".")
    a_len = (len(a_integer), len(a_fractional))
    b_len = (len(b_integer), len(b_fractional))
    len_diff = (a_len[0] - b_len[0], a_len[1] - b_len[1])
    if len_diff[0] < 0:
        return -1
    elif len_diff[0] == 0:
        a_num = a_integer + a_fractional
        b_num = b_integer + b_fractional
        if a_num == b_num:
            return 0
        for i in range(a_len[0] + min(a_len[1], b_len[1])):
            if CHAR_TO_INT[a_num[i]] > CHAR_TO_INT[b_num[i]]:
                return 1
            elif CHAR_TO_INT[a_num[i]] < CHAR_TO_INT[b_num[i]]:
                return -1
        if len_diff[1] < 0:
            return -1
    return 1

def plus(a:str, b:str) -> str:
    a, a_sign = num_format(a)
    b, b_sign = num_format(b)
    if a_sign == b_sign:
        rule = 1
    else:
        rule = -1
    if a == '.':
        if b == '.':
            return '.'
        else:
            return b_sign + b
    if b == '.':
        return a_sign + a
    a_integer, a_fractional = a.split(".")
    b_integer, b_fractional = b.split(".")
    a_integer = a_integer[::-1]
    b_integer = b_integer[::-1]
    a_fractional = a_fractional[::-1]
    b_fractional = b_fractional[::-1]
    a_len = (len(a_integer), len(a_fractional))
    b_len = (len(b_integer), len(b_fractional))
    len_diff = (a_len[0] - b_len[0], a_len[1] - b_len[1])
    if rule == 1:
        carry = 0
        if len_diff[1] > 0:
            ans = a_fractional[:len_diff[1]]
            a_fractional = a_fractional[len_diff[1]:]
        else:
            ans = b_fractional[:-len_diff[1]]
            b_fractional = b_fractional[-len_diff[1]:]
        for i in range(min(a_len[1], b_len[1])):
            achar, carry = INT_TO_CHAR[CHAR_TO_INT[a_fractional[i]] + CHAR_TO_INT[b_fractional[i]] + carry]
            ans += achar
        ans += '.'
        for i in range(min(a_len[0], b_len[0])):
            achar, carry = INT_TO_CHAR[CHAR_TO_INT[a_integer[i]] + CHAR_TO_INT[b_integer[i]] + carry]
            ans += achar
        if len_diff[0] > 0:
            integer = a_integer[b_len[0]:]
        else:
            integer = b_integer[a_len[0]:]
        while carry and integer:
            achar, carry = INT_TO_CHAR[CHAR_TO_INT[integer[0]] + carry]
            ans += achar
            integer = integer[1:]
        ans += integer
        if carry:
            ans += '1'
        ans = ans.strip('0')
        if a_sign == '-':
            ans += '-'
        return ans[::-1]
    else:
        exchange = compare(a, b)
        if exchange == 0:
            return '.'
        if exchange == -1:
            a, b = b, a
            a_integer, b_integer = b_integer, a_integer
            a_fractional, b_fractional = b_fractional, a_fractional
            a_len, b_len = b_len, a_len
            len_diff = (-len_diff[0], -len_diff[1])
            a_sign, b_sign = b_sign, a_sign
        carry = 0
        if len_diff[1] > 0:
            ans = a_fractional[:len_diff[1]]
            a_fractional = a_fractional[len_diff[1]:]
        else:
            ans = ''
            for i in range(-len_diff[1]):
                achar, carry = INT_TO_CHAR[-CHAR_TO_INT[b_fractional[i]] + carry]
                ans += achar
            b_fractional = b_fractional[-len_diff[1]:]
        for i in range(min(a_len[1], b_len[1])):
            achar, carry = INT_TO_CHAR[CHAR_TO_INT[a_fractional[i]] - CHAR_TO_INT[b_fractional[i]] + carry]
            ans += achar
        ans += '.'
        for i in range(min(a_len[0], b_len[0])):
            achar, carry = INT_TO_CHAR[CHAR_TO_INT[a_integer[i]] - CHAR_TO_INT[b_integer[i]] + carry]
            ans += achar
        integer = a_integer[b_len[0]:]
        while carry:
            achar, carry = INT_TO_CHAR[CHAR_TO_INT[integer[0]] + carry]
            ans += achar
            integer = integer[1:]
        ans += integer
        ans = ans.strip('0')
        if a_sign == '-':
            ans += '-'
        return ans[::-1]

def minus(a:str, b:str) -> str:
    if b[0] == '-':
        b = b[1:]
    else:
        b = '-' + b
    return plus(a, b)

def num_times(k:str, x:str) -> str: # k为1位整数字符串，x为正数，不建议作为独立函数使用
    if k == '0' or x == '.':
        return '.'
    if k == '1':
        return x
    x_integer, x_fractional = x.split(".")
    k = CHAR_TO_INT[k]
    x_integer = x_integer[::-1]
    x_fractional = x_fractional[::-1]
    ans = ''
    carry = 0
    for char in x_fractional:
        achar, carry = INT_TO_CHAR[CHAR_TO_INT[char] * k + carry]
        ans += achar
    ans += '.'
    for char in x_integer:
        achar, carry = INT_TO_CHAR[CHAR_TO_INT[char] * k + carry]
        ans += achar
    if carry:
        ans += INT_TO_CHAR[carry][0]
    ans = ans.strip('0')
    return ans[::-1]

def shift(a:str, k:int) -> str: # a为正数，k为整数，相当于乘以10的k次方，不建议作为独立函数使用
    if a == '.':
        return '.'
    if k == 0:
        return a
    a_integer, a_fractional = a.split(".")
    a_num = a_integer + a_fractional
    a_len = (len(a_integer), len(a_fractional))
    if k > 0:
        sign = 1
    else:
        sign = 0
        k = -k
    if k < a_len[sign]:
        sign0 = 2 * sign - 1
        ans = a_num[:sign0 * (k - a_len[sign])] + '.' + a_num[sign0 * (k - a_len[sign]):]
    else:
        if sign:
            ans = a_num + '0' * (k - a_len[sign]) + '.'
        else:
            ans = '.' + '0' * (k - a_len[sign]) + a_num
    return ans.strip('0')

def times(a:str, b:str) -> str:
    a, a_sign = num_format(a)
    b, b_sign = num_format(b)
    if a_sign == b_sign:
        sign = ''
    else:
        sign = '-'
    if a == '.' or b == '.':
        return '.'
    a_integer, a_fractional = a.split(".")
    a_integer = a_integer[::-1]
    ans = ''
    for i, num in enumerate(a_integer):
        if num == '0':
            continue
        if num == '1':
            kb = b
        else:
            kb = num_times(num, b)
        kb = shift(kb, i)
        ans = plus(ans, kb)
    for i, num in enumerate(a_fractional):
        neg_i = -i - 1
        if num == '0':
            continue
        if num == '1':
            kb = b
        else:
            kb = num_times(num, b)
        kb = shift(kb, neg_i)
        ans = plus(ans, kb)
    return sign + ans

def power(x:str, p:int) -> str: # p为整数
    x, x_sign = num_format(x)
    if x_sign == '-' and p % 2:
        sign = '-'
    else:
        sign = ''
    if x == '.':
        if p == 0:
            warnings.warn('未定式: 0^0, 将返回1.')
            return '1.'
        if p < 0:
            raise Exception('无定义: 1/0')
        return '.'
    ans = '1.'
    for _ in range(abs(p)):
        ans = times(ans, x)
    if p < 0:
        ans = divide('1.', ans)
    return sign + ans

def divide(a:str, b:str) -> str:
    a, a_sign = num_format(a)
    b, b_sign = num_format(b)
    if a_sign == b_sign:
        sign = ''
    else:
        sign = '-'
    if a == '.':
        if b == '.':
            raise Exception('未定式: 0/0')
        else:
            return '.'
    if b == '.':
        raise Exception('无定义: 1/0')
    a_integer, a_fractional = a.split(".")
    b_integer, b_fractional = b.split(".")
    a_len = (len(a_integer), len(a_fractional))
    b_len = (len(b_integer), len(b_fractional))
    a_num = a_integer + a_fractional
    b_num = b_integer + b_fractional
    a_num = a_num.strip("0")
    b_num = b_num.strip("0")
    a_num_len = len(a_num)
    b_num_len = len(b_num)
    if a_len[1] > 0:
        a_shift = -a_len[1]
    else:
        a_shift = a_len[0] - a_num_len
    if b_len[1] > 0:
        b_shift = -b_len[1]
    else:
        b_shift = b_len[0] - b_num_len
    if a_num == b_num:
        if a_shift < b_shift:
            return sign + '.' + '0' * (b_shift - a_shift - 1) + '1'
        else:
            return sign + '1' + '0' * (a_shift - b_shift) + '.'
    a = '.' + a_num # shift(a, -a_shift - a_num_len)
    b = '.' + b_num # shift(b, -b_shift - b_num_len)
    shift_diff = a_shift + a_num_len - b_shift - b_num_len
    if compare(a, b) == 1:
        b = shift(b, 1)
        shift_diff += 1
    kb_list = [num_times(i, b) for i in '9876543210']
    num = shift(a, 1)
    num_list = []
    ans = ''
    idx = 0
    cycle = False
    while not cycle and num != '.':
        num_list.append(num)
        for i, kb in enumerate(kb_list):
            if compare(num, kb) >= 0:
                ans += INT_TO_CHAR[9 - i][0]
                num = shift(plus(num, '-' + kb), 1)
                break
        idx += 1
        if num in num_list:
            cycle = True
            cycle_len = num_list[::-1].index(num) + 1
            cycle_num = ans[-cycle_len:]
            ans = ans[:-cycle_len]
    if cycle:
        ans_len = len(ans)
        if shift_diff <= 0:
            ans = '.' + '0' * (-shift_diff) + ans + '(' + cycle_num + ')'
        elif shift_diff <= ans_len:
            ans = ans[:shift_diff] + '.' + ans[shift_diff:] + '(' + cycle_num + ')'
        else:
            shift_ans = shift_diff - ans_len
            cycle_times = shift_ans // cycle_len
            cycle_remain = shift_ans % cycle_len
            ans = ans + cycle_num * cycle_times + cycle_num[:cycle_remain] + '.' + '(' + cycle_num[cycle_remain:] + cycle_num[:cycle_remain] + ')'
        return sign + ans
    else:
        return sign + shift('.' + ans, shift_diff)

def floor_divide(a:str, b:str) -> str:
    ans = divide(a, b).split('.')
    if ans[1] and ans[0][0] == '-':
        ans = minus(ans, '1')
    return times(ans[0] + '.', b)

def modulo(a:str, b:str) -> str:
    ans = floor_divide(a, b)
    return minus(a, ans)

def num_format(x:str) -> tuple:
    if '.' not in x:
        x += '.'
    sign = ''
    if x[0] == '-':
        x = x[1:].strip('0')
        if x != '.':
            sign = '-'
    else:
        x = x.strip('0')
    return x, sign

def print_format(x:str) -> str:
    if 'i' in x:
        x, y = x.split('i')
        x = print_format(x)
        y = print_format(y)
        y = '+' + y if y and y[0] != '-' else y
        return print_format(x) + print_format(y) + 'i'
    cycle = False
    if '(' in x:
        cycle = True
        acc = 20
        cycle_num = x.split('(')[1][:-1]
        cycle_len = len(cycle_num)
        x = x.split('(')[0]
        x_len = len(x.split('.')[1])
        x = x + cycle_num * ((acc - x_len if acc > x_len else 0) // cycle_len + 1) + '...'
    sign = ''
    if x[0] == '-':
        sign = '-'
        x = x[1:]
    if x[0] == '.':
        x = '0' + x
    if x[-1] == '.' and not cycle:
        x = x[:-1]
    return sign + x

# complex number operations

def conjugate(z:str) -> str:
    x, y = z.split('i')
    if y[0] == '-':
        y = y[1:]
    else:
        y = '-' + y
    return x + 'i' + y

def complex_plus(z1:str, z2:str) -> str:
    x1, y1 = z1.split('i')
    x2, y2 = z2.split('i')
    x = plus(x1, x2)
    y = plus(y1, y2)
    return x + 'i' + y

def complex_minus(z1:str, z2:str) -> str:
    x1, y1 = z1.split('i')
    x2, y2 = z2.split('i')
    x = minus(x1, x2)
    y = minus(y1, y2)
    return x + 'i' + y

def complex_times(z1:str, z2:str) -> str:
    x1, y1 = z1.split('i')
    x2, y2 = z2.split('i')
    x = minus(times(x1, x2), times(y1, y2))
    y = plus(times(x1, y2), times(y1, x2))
    return x + 'i' + y

def complex_power(z:str, p:int) -> str:
    x, y = z.split('i')
    x = num_format(x)[0]
    y = num_format(y)[0]
    if x == '.' and y == '.':
        if p == 0:
            warnings.warn('未定式: 0^0, 将返回1.i.')
            return '1.i.'
        if p < 0:
            raise Exception('无定义: 1/0')
        return '.i.'
    ans = '1.i.'
    for _ in range(abs(p)):
        ans = complex_times(ans, z)
    if p < 0:
        ans = complex_divide('1.i.', ans)
    return ans

def complex_divide(z1:str, z2:str) -> str:
    x, y = z2.split('i')
    denom = plus(power(x, 2), power(y, 2))
    x, y = complex_times(z1, conjugate(z2)).split('i')
    x = divide(x, denom)
    y = divide(y, denom)
    return x + 'i' + y

def complex_floor_divide(z1:str, z2:str) -> str:
    x1, y1 = z1.split('i')
    x2, y2 = z2.split('i')
    x = floor_divide(x1, x2)
    y = floor_divide(y1, x2)
    return x + 'i' + y

def complex_modulo(z1:str, z2:str) -> str:
    x, y = z1.split('i')
    x2, y2 = z2.split('i')
    x = modulo(x, x2)
    y = modulo(y, y2)
    return x + 'i' + y

@total_ordering
class StrNumber:
    def __init__(self, value: str):
        if isinstance(value, StrNumber):
            self.value = value.value
            self.sign = value.sign
            self.num = value.num
            return
        elif isinstance(value, str):
            self.num, self.sign = num_format(value)
        elif isinstance(value, int):
            if value < 0:
                self.num = str(-value) + '.'
                self.sign = '-'
            else:
                self.num = str(value) + '.'
                self.sign = ''
        elif isinstance(value, float):
            warnings.warn('警告: 浮点数存在精度误差, 谨慎使用浮点数')
            self.num, self.sign = num_format(str(value))
        else:
            raise Exception('类型错误: 不支持的类型')
        self.value = self.sign + self.num

    def __add__(self, other):
        if isinstance(other, int):
            return StrNumber(plus(self.value, str(other)))
        elif isinstance(other, float):
            warnings.warn('警告: 浮点数存在精度误差, 谨慎使用浮点数')
            return StrNumber(plus(self.value, str(other)))
        elif isinstance(other, StrNumber):
            return StrNumber(plus(self.value, other.value))
        return NotImplemented
    
    def __radd__(self, other):
        if isinstance(other, int):
            return StrNumber(plus(str(other), self.value))
        elif isinstance(other, float):
            warnings.warn('警告: 浮点数存在精度误差, 谨慎使用浮点数')
            return StrNumber(plus(str(other), self.value))
        elif isinstance(other, StrNumber):
            return StrNumber(plus(other.value, self.value))
        return NotImplemented
    
    def __iadd__(self, other):
        if isinstance(other, int):
            self.value = plus(self.value, str(other))
        elif isinstance(other, float):
            warnings.warn('警告: 浮点数存在精度误差, 谨慎使用浮点数')
            self.value = plus(self.value, str(other))
        elif isinstance(other, StrNumber):
            self.value = plus(self.value, other.value)
        else:
            return NotImplemented
        self.num, self.sign = num_format(self.value)
        return self

    def __sub__(self, other):
        if isinstance(other, int):
            return StrNumber(minus(self.value, str(other)))
        elif isinstance(other, float):
            warnings.warn('警告: 浮点数存在精度误差, 谨慎使用浮点数')
            return StrNumber(minus(self.value, str(other)))
        elif isinstance(other, StrNumber):
            return StrNumber(minus(self.value, other.value))
        return NotImplemented
    
    def __rsub__(self, other):
        if isinstance(other, int):
            return StrNumber(minus(str(other), self.value))
        elif isinstance(other, float):
            warnings.warn('警告: 浮点数存在精度误差, 谨慎使用浮点数')
            return StrNumber(minus(str(other), self.value))
        elif isinstance(other, StrNumber):
            return StrNumber(minus(other.value, self.value))
        return NotImplemented
    
    def __isub__(self, other):
        if isinstance(other, int):
            self.value = minus(self.value, str(other))
        elif isinstance(other, float):
            warnings.warn('警告: 浮点数存在精度误差, 谨慎使用浮点数')
            self.value = minus(self.value, str(other))
        elif isinstance(other, StrNumber):
            self.value = minus(self.value, other.value)
        else:
            return NotImplemented
        self.num, self.sign = num_format(self.value)
        return self

    def __mul__(self, other):
        if isinstance(other, int):
            return StrNumber(times(self.value, str(other)))
        elif isinstance(other, float):
            warnings.warn('警告: 浮点数存在精度误差, 谨慎使用浮点数')
            return StrNumber(times(self.value, str(other)))
        elif isinstance(other, StrNumber):
            return StrNumber(times(self.value, other.value))
        return NotImplemented
    
    def __rmul__(self, other):
        if isinstance(other, int):
            return StrNumber(times(str(other), self.value))
        elif isinstance(other, float):
            warnings.warn('警告: 浮点数存在精度误差, 谨慎使用浮点数')
            return StrNumber(times(str(other), self.value))
        elif isinstance(other, StrNumber):
            return StrNumber(times(other.value, self.value))
        return NotImplemented
    
    def __imul__(self, other):
        if isinstance(other, int):
            self.value = times(self.value, str(other))
        elif isinstance(other, float):
            warnings.warn('警告: 浮点数存在精度误差, 谨慎使用浮点数')
            self.value = times(self.value, str(other))
        elif isinstance(other, StrNumber):
            self.value = times(self.value, other.value)
        else:
            return NotImplemented
        self.num, self.sign = num_format(self.value)
        return self

    def __truediv__(self, other):
        if isinstance(other, int):
            return StrNumber(divide(self.value, str(other)))
        elif isinstance(other, float):
            warnings.warn('警告: 浮点数存在精度误差, 谨慎使用浮点数')
            return StrNumber(divide(self.value, str(other)))
        elif isinstance(other, StrNumber):
            return StrNumber(divide(self.value, other.value))
        return NotImplemented
    
    def __rtruediv__(self, other):
        if isinstance(other, int):
            return StrNumber(divide(str(other), self.value))
        elif isinstance(other, float):
            warnings.warn('警告: 浮点数存在精度误差, 谨慎使用浮点数')
            return StrNumber(divide(str(other), self.value))
        elif isinstance(other, StrNumber):
            return StrNumber(divide(other.value, self.value))
        return NotImplemented
    
    def __itruediv__(self, other):
        if isinstance(other, int):
            self.value = divide(self.value, str(other))
        elif isinstance(other, float):
            warnings.warn('警告: 浮点数存在精度误差, 谨慎使用浮点数')
            self.value = divide(self.value, str(other))
        elif isinstance(other, StrNumber):
            self.value = divide(self.value, other.value)
        else:
            return NotImplemented
        self.num, self.sign = num_format(self.value)
        return self
    
    def __floordiv__(self, other):
        if isinstance(other, int):
            return StrNumber(floor_divide(self.value, str(other)))
        elif isinstance(other, float):
            warnings.warn('警告: 浮点数存在精度误差, 谨慎使用浮点数')
            return StrNumber(floor_divide(self.value, str(other)))
        elif isinstance(other, StrNumber):
            return StrNumber(floor_divide(self.value, other.value))
        return NotImplemented
    
    def __rfloordiv__(self, other):
        if isinstance(other, int):
            return StrNumber(floor_divide(str(other), self.value))
        elif isinstance(other, float):
            warnings.warn('警告: 浮点数存在精度误差, 谨慎使用浮点数')
            return StrNumber(floor_divide(str(other), self.value))
        elif isinstance(other, StrNumber):
            return StrNumber(floor_divide(other.value, self.value))
        return NotImplemented
    
    def __ifloordiv__(self, other):
        if isinstance(other, int):
            self.value = floor_divide(self.value, str(other))
        elif isinstance(other, float):
            warnings.warn('警告: 浮点数存在精度误差, 谨慎使用浮点数')
            self.value = floor_divide(self.value, str(other))
        elif isinstance(other, StrNumber):
            self.value = floor_divide(self.value, other.value)
        else:
            return NotImplemented
        self.num, self.sign = num_format(self.value)
        return self
    
    def __mod__(self, other):
        if isinstance(other, int):
            return StrNumber(modulo(self.value, str(other)))
        elif isinstance(other, float):
            warnings.warn('警告: 浮点数存在精度误差, 谨慎使用浮点数')
            return StrNumber(modulo(self.value, str(other)))
        elif isinstance(other, StrNumber):
            return StrNumber(modulo(self.value, other.value))
        return NotImplemented
    
    def __rmod__(self, other):
        if isinstance(other, int):
            return StrNumber(modulo(str(other), self.value))
        elif isinstance(other, float):
            warnings.warn('警告: 浮点数存在精度误差, 谨慎使用浮点数')
            return StrNumber(modulo(str(other), self.value))
        elif isinstance(other, StrNumber):
            return StrNumber(modulo(other.value, self.value))
        return NotImplemented
    
    def __imod__(self, other):
        if isinstance(other, int):
            self.value = modulo(self.value, str(other))
        elif isinstance(other, float):
            warnings.warn('警告: 浮点数存在精度误差, 谨慎使用浮点数')
            self.value = modulo(self.value, str(other))
        elif isinstance(other, StrNumber):
            self.value = modulo(self.value, other.value)
        else:
            return NotImplemented
        self.num, self.sign = num_format(self.value)
        return self

    def __pow__(self, other: int):
        if isinstance(other, float):
            warnings.warn('传入了float作为幂, 向下取整转为int')
            other = int(other // 1)
        elif isinstance(other, StrNumber):
            warnings.warn('传入了StrNumber作为幂, 向下取整转为int')
            other = int(other)
        if isinstance(other, int):
            return StrNumber(power(self.value, other))
        else:
            return NotImplemented
    
    def __rpow__(self, other: int):
        if isinstance(other, float):
            warnings.warn('警告: 浮点数存在精度误差, 谨慎使用浮点数')
        warnings.warn('传入了StrNumber作为幂, 向下取整转为int')
        return StrNumber(power(str(other), int(self)))
    
    def __ipow__(self, other: int):
        if isinstance(other, float):
            warnings.warn('传入了float作为幂, 向下取整转为int')
            other = int(other // 1)
        elif isinstance(other, StrNumber):
            warnings.warn('传入了StrNumber作为幂, 向下取整转为int')
            other = int(other)
        if isinstance(other, int):
            self.value = power(self.value, other)
            self.num, self.sign = num_format(self.value)
            return self
        else:
            return NotImplemented

    def __str__(self):
        return f'StrNumber({self.value})'

    def __repr__(self):
        return print_format(self.value)
    
    def __neg__(self):
        value = self.num
        if self.sign == '':
            value = '-' + value
        return StrNumber(value)
    
    def __pos__(self):
        return StrNumber(self)
    
    def __abs__(self):
        return StrNumber(self.num)
    
    def __eq__(self, other):
        if not isinstance(other, StrNumber):
            try:
                other = StrNumber(other) # str int float -> StrNumber
            except:
                return NotImplemented
        return self.value == other.value
    
    def __bool__(self):
        return self.value != '.'
    
    def __lt__(self, other):
        if not isinstance(other, StrNumber):
            try:
                other = StrNumber(other) # str int float -> StrNumber
            except:
                return NotImplemented
        if self.sign != other.sign:
            return self.sign == '-'
        else:
            ans = compare(self.num, other.num)
            if self.sign == '':
                return ans == -1
            return ans == 1

    def __le__(self, other):
        return not self > other

    def __gt__(self, other):
        if not isinstance(other, StrNumber):
            try:
                other = StrNumber(other) # str int float -> StrNumber
            except:
                return NotImplemented
        if self.sign != other.sign:
            return self.sign == ''
        else:
            ans = compare(self.num, other.num)
            if self.sign == '':
                return ans == 1
            return ans == -1

    def __ge__(self, other):
        return not self < other
    
    def __int__(self):
        ans = self // 1
        if ans.value == '.':
            return 0
        return int(ans.value[:-1])
    
    def __float__(self):
        if self.value == '.':
            return 0.
        return float(self.value)

class StrComplex: # TODO: 反向方法与原地赋值方法待补充
    def __init__(self, value: str):
        if isinstance(value, StrNumber):
            self.real = value.value
            self.imag = '.'
        else:
            if 'i' not in value:
                value += 'i.'
            self.real, self.imag = value.split('i')
            self.real = StrNumber(self.real)
            self.imag = StrNumber(self.imag)
        self.value = self.real.value + 'i' + self.imag.value

    def __add__(self, other):
        return StrComplex(complex_plus(self.value, other.value))

    def __sub__(self, other):
        return StrComplex(complex_minus(self.value, other.value))

    def __mul__(self, other):
        return StrComplex(complex_times(self.value, other.value))

    def __truediv__(self, other):
        return StrComplex(complex_divide(self.value, other.value))
    
    def __floordiv__(self, other):
        return StrComplex(complex_floor_divide(self.value, other.value))
    
    def __mod__(self, other):
        return StrComplex(complex_modulo(self.value, other.value))

    def __pow__(self, power: int):
        return StrComplex(complex_power(self.value, power))

    def __str__(self):
        return f'StrComplex({self.value})'

    def __repr__(self):
        return print_format(self.value)
    
    def conj(self):
        return StrComplex(conjugate(self.value))
    
    def __neg__(self):
        return StrComplex(complex_minus('0', self.value))
    
    def __pos__(self):
        return self
    
    def __eq__(self, other):
        return self.value == other.value
    
    def __ne__(self, other):
        return self.value != other.value
    
    def __bool__(self):
        return self.value != '.i.'

one = StrNumber('1')
zeo = StrNumber('0')
onc = StrComplex('1')
zec = StrComplex('0')
oic = StrComplex('i1')

# tests = [
#     ("123","456"),("1.5","2.25"),("-5","3"),("5","-3"),("-2.5","-0.5"),("0","0"),
#     ("999","1"),("9999","1"),("0.9","0.2"),("1.234","0.766"),("123.4500","0.0055"),
#     ("0.000","0.000"),("000","000"),("-0","0"),("-0.0","0.0"),("0.1","0.2"),
#     ("0.999","0.001"),("999","999"),("-1000","1"),("-1","1"),("1","-1"),
#     ("12345678901234567890","1"),("0.0001","0.0009"),("1.005","0.005"),("-1.005","0.005"),
#     ("3.1415926","2.7182818"), ("-0.000","-0.000"), ("10.0","-10.0"), ("-123.45","23.45"), 
#     ('1000','999'), ('1','2'), ('1','3'), ('10','4'), ('22','7'), ('1','8'), ('123.456','0.001'),
#     ('1','6'), ('-10','4'), ('5', '0.2'), ('0.9', '0.3'), ('1', '7'), ('1.2345','2'), ('123456789','3'),
#     ('', '')
# ]

# diff = 0
# for a, b in tests[:-1]:
#     plus_res = print_format(plus(a, b))
#     diff += abs(float(plus_res)-float(a)-float(b))
#     print(f'{a}+{b} = {plus_res} = {float(a)+float(b)}, diff={float(plus_res)-float(a)-float(b)}')
#     times_res = print_format(times(a, b))
#     diff += abs(float(times_res)-float(a)*float(b))
#     print(f'{a}×{b} = {times_res} = {float(a)*float(b)}, diff={float(times_res)-float(a)*float(b)}')
#     if plus(b, '') != '.' and a != "3.1415926":
#         divide_res = print_format(divide(a, b))
#         diff += abs(float(divide_res)-float(a)/float(b))
#         print(f'{a}÷{b} = {divide_res} = {float(a)/float(b)}, diff={float(divide_res)-float(a)/float(b)}')
#     if a == "3.1415926":
#         a, b = '3.14', '2.72'
#         divide_res = print_format(divide(a, b))
#         diff += abs(float(divide_res)-float(a)/float(b))
#         print(f'{a}÷{b} = {divide_res} = {float(a)/float(b)}, diff={float(divide_res)-float(a)/float(b)}')
# print(f'{tests[-1][0]}+{tests[-1][1]} = {plus(tests[-1][0], tests[-1][1])}')
# print(f'{tests[-1][0]}×{tests[-1][1]} = {times(tests[-1][0], tests[-1][1])}')
# print(f'Total diff - 1: {diff - 1}')



# ans = None
# while True:
#     func = input('输入运算: ')
#     if func == '':
#         continue
#     if func == '+':
#         func = plus
#     if func == '-':
#         func = minus
#     if func == '*':
#         func = times
#     if func == '/':
#         func = divide
#     if func == '^':
#         func = power
#     if func == 'command':
#         print(eval(input()))
#         continue
#     if func == 'exit':
#         break
#     a = input().split(",")
#     if a[0] == 'ans':
#         if ans:
#             a = ans
#         else:
#             print('无上次结果')
#             continue
#     b = input().split(",")
#     if func == power:
#         b = [int(x) for x in b]
#     if len(b) == 1:
#         b = b[0]
#         ans = [func(i, b) for i in a]
#     elif len(b) == len(a):
#         ans = [func(a[i], b[i]) for i in range(len(a))]
#     else:
#         print('输入长度不一致')
#     print(','.join(ans))

# 临时代码

# 多项式导数
def derivative(f_coeffs: list) -> list:
    complex_q = 'i' in ''.join(f_coeffs)
    if complex_q:
        if len(f_coeffs) <= 1:
            return ['.i.']
        return [complex_times(str(i) + '.i.', f_coeffs[i]) for i in range(1, len(f_coeffs))]
    else:
        if len(f_coeffs) <= 1:
            return ['.']
        return [times(str(i), f_coeffs[i]) for i in range(1, len(f_coeffs))]

def polynomial_print(f_coeffs: list) -> str:
    complex_q = 'i' in ''.join(f_coeffs)
    terms = []
    if complex_q:
        for i, coeff in enumerate(f_coeffs):
            if coeff == '.i.':
                continue
            if i == 0:
                term = print_format(coeff)
            else:
                term = '(' + print_format(coeff) + ')x'
                if i > 1:
                    term += '^' + str(i)
            terms.append(term)
    else:
        for i, coeff in enumerate(f_coeffs):
            if coeff == '.':
                continue
            if i == 0:
                term = print_format(coeff)
            else:
                term = print_format(coeff) + 'x'
                if i > 1:
                    term += '^' + str(i)
            terms.append(term)
    if not terms:
        return '.i.' if complex_q else '.'
    return ' + '.join(terms[::-1]).replace('+ -', '- ')

def list_operation(a: list, b: any, func: callable) -> list:
    if isinstance(b, list):
        if len(a) != len(b):
            raise Exception('列表长度不一致')
        return [func(ai, bi) for ai, bi in zip(a, b)]
    else:
        return [func(item, b) for item in a]

def trim_coeffs(coeffs: list) -> list:
    complex_q = 'i' in ''.join(coeffs)
    zero = '.i.' if complex_q else '.'
    while coeffs and coeffs[-1] == zero:
        coeffs.pop()
    if not coeffs:
        return [zero]
    return coeffs