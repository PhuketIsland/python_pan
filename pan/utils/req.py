import struct


# 发送数据
def send_data(conn, content):
    data = content.encode("utf-8")
    header = struct.pack('i', len(data))  # 先发送数据大小
    conn.sendall(header)
    conn.sendall(data)


# 接收数据
def recv_data(conn, chunk_size=1024):
    # 获取数据长度
    has_read_size = 0
    bytes_list = []
    while has_read_size < 4:
        chunk_header = conn.recv(4 - has_read_size)
        has_read_size += len(chunk_header)
        bytes_list.append(chunk_header)
    header = b"".join(bytes_list)
    data_length = struct.unpack('i', header)[0]

    # 获取数据
    data_list = []
    has_read_data_size = 0
    while has_read_data_size < data_length:
        if data_length - has_read_data_size > chunk_size:
            size = chunk_size
        else:
            size = data_length - has_read_data_size
        chunk_data = conn.recv(size)
        data_list.append(chunk_data)
        has_read_data_size += len(chunk_data)

    data = b"".join(data_list)

    return data


# 接手并保存文件
def recv_save_file(conn, save_file_path, chunk_size=1024):
    # 获取头部信息：数据长度
    has_read_size = 0
    bytes_list = []
    while has_read_size < 4:
        chunk_header = conn.recv(4 - has_read_size)
        bytes_list.append(chunk_header)
        has_read_size += len(chunk_header)
    header = b"".join(bytes_list)
    data_length = struct.unpack('i', header)[0]

    # 获取数据
    file_object = open(save_file_path, mode='wb')
    has_read_data_size = 0
    while has_read_data_size < data_length:
        if data_length - has_read_data_size > chunk_size:
            size = chunk_size
        else:
            size = data_length - has_read_data_size
        chunk_data = conn.recv(size)
        file_object.write(chunk_data)
        file_object.flush()
        has_read_data_size += len(chunk_data)
    file_object.close()


# 读取并发送文件
def send_file_by_seek(conn, file_size, file_path, seek=0):
    header = struct.pack('i', file_size)
    conn.sendall(header)

    has_send_size = 0
    file_object = open(file_path, 'rb')
    if seek:
        file_object.seek(seek)
    while has_send_size < file_size:
        chunk = file_object.read(2048)
        conn.sendall(chunk)
        has_send_size += len(chunk)
    file_object.close()
