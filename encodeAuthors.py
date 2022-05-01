import codecs

split_str = ' ||| '

if __name__ == '__main__':
    source = codecs.open('./authors.txt', 'r', 'utf-8')
    result = codecs.open('./authors_encoded.txt', 'w', 'utf-8')
    index = codecs.open('./authors_index.txt', 'w', 'utf-8')
    index_dict = {}
    name_id = 0

    for line in source:
        words = line.split(split_str)
        length = len(words)
        result.write(words[0] + split_str + words[1] + split_str)
        for i in range(2, length-1):
            name = words[i]
            if not name in index_dict.keys():
                index_dict[name] = [name_id, 1]
                name_id += 1
            else:
                index_dict[name][1] += 1
            result.write(str(index_dict[name][0]) + split_str)
        result.write('\r\n')
    
    for name in index_dict.keys():
        index.write(str(index_dict[name][0]) + split_str \
            + name + split_str \
            + str(index_dict[name][1]) + u'\r\n')

    source.close()
    result.close()
    index.close()

'''
python encodeAuthors.py
'''