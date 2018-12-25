class DictionaryParser:
    margin = 4
    char = ' '
    def save_dict(self, dict):
        file = open(self.path, 'w')
        s = str(dict)
        s = s[1:-1]
        s = s.replace(', ', '\n')
        count_spaces = 0
        i=0
        while i < len(s):
            if s[i] == '{':
                s = s[:i-1] + '\n' + s[i+1:]
                count_spaces += self.margin
                i-=2
            if s[i] == '\n':
                s = s[:i+1] + self.char*count_spaces + s[i+1:]
                i+=2
            if s[i] == '}':
                s = s[:i] + s[i+1:]
                count_spaces -= self.margin
                i -= 1
            i+=1

        file.write(s)
        file.close()

    def load_dict(self):
        file = open(self.path, 'r')
        s = file.read()

        i = 0
        prev_count_spaces = 0
        count_spaces = 0
        start_scobe = 0
        len_ch = len(self.char)
        while i<len(s):
            if s[i] == '\n':
                i+=1
                while s[i:i+len_ch] == self.char:
                    count_spaces += len_ch
                    i += len_ch
                if count_spaces > prev_count_spaces:
                    s = s[:i-count_spaces - 1] + ' {' + s[i:]
                    i -= count_spaces
                    start_scobe += 1
                elif count_spaces < prev_count_spaces:
                    mult = (prev_count_spaces - count_spaces)//self.margin//len_ch
                    s = s[:i - count_spaces - 1] + '}'*mult + ', ' + s[i:]
                    i -= count_spaces
                    start_scobe -= mult
                else:
                    s = s[:i - count_spaces - 1] + ', ' + s[i:]
                    i -= count_spaces
                prev_count_spaces = count_spaces
                count_spaces = 0
            i+=1
        for i in range(start_scobe):
            s += '}'
        s = '{' + s + '}'
        file.close()
        return eval(s)

    def __init__(self, path):
        self.path = path


