import numpy

def tcp_client_num_fps(folder):
    tcp_list = []
    for x in range(3):
        fps_group = []
        for y in range(x + 1):
            fps = []
            f = open("../data/{}/tcp_client_{}_{}.txt".format(folder, x, y), "r")
            for line in f:
                fps.append(float(line.strip("\n")))
            fps_group.append(numpy.average(fps))
            fps.clear()
            f.close()
        tcp_list.append(numpy.average(fps_group))
        fps_group.clear()
    return tcp_list

def tcp_compression_fps(folder):
    fps_list = []
    for x in range(1, 7):
        fps = []
        f = open("../data/{}/tcp_compress_{}.txt".format(folder, x), "r")
        for line in f:
            fps.append(float(line.strip("\n")))
        fps_list.append(numpy.average(fps))
        fps.clear()
        f.close()
    return fps_list

# TCPLIST
print(tcp_client_num_fps("tcplist"))
# TCPTHREAD
print(tcp_client_num_fps("tcpthread"))
# TCPLIST compression
print(tcp_compression_fps("tcplistcompress"))
# TCPTHREAD compression
print(tcp_compression_fps("tcpthreadcompress"))