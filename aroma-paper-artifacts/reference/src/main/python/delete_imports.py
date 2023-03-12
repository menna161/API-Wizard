def delete_imports(obj):
    hash = obj["ast"][0]
    count_hash = hash.count('#')
    hash_index = []
    for i in range(1, count_hash+1):
        if "import" in obj["ast"][i][1][0]:
            hash_index.append(i)

    for x in hash_index:
        del obj["ast"][x]
