import json
def transform_data(files: list[str], links: list[str]) -> None:
    data_list = []
    for idx, (file, link) in enumerate(zip(files, links), start=1):  
        try:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"Có lỗi xảy ra khi đọc file {file}: {e}")
            continue 
        data = {
            'id': idx,  
            'content': content,
            'link': link
        }
        data_list.append(data)

    json_file_path = '../data/data_temp/data_temp.json'
    try:
        with open(json_file_path, 'w', encoding='utf-8') as json_f:
            json.dump(data_list, json_f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Có lỗi xảy ra khi lưu vào file JSON {json_file_path}: {e}")
