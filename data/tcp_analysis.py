import numpy

def tcp_client_num_fps(folder):
    tcp_list = []
    for x in range(3):
        fps_group = []
        for y in range(x + 1):
            fps = []
            f = open("./{}/tcp_client_{}_{}.txt".format(folder, x, y), "r")
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
        f = open("./{}/tcp_compress_{}.txt".format(folder, x), "r")
        for line in f:
            fps.append(float(line.strip("\n")))
        fps_list.append(numpy.average(fps))
        fps.clear()
        f.close()
    return fps_list

# TCPLIST
tcplist_client_fps = tcp_client_num_fps("tcplist")
print(tcplist_client_fps)
# TCPTHREAD
tcpthread_client_fps = tcp_client_num_fps("tcpthread")
print(tcpthread_client_fps)
# TCPLIST compression
tcplist_compression_fps = tcp_compression_fps("tcplistcompress")
print(tcplist_compression_fps)
# TCPTHREAD compression
tcpthread_compression_fps = tcp_compression_fps("tcpthreadcompress")
print(tcpthread_compression_fps)

f = open("./tcp_client_fps.csv", "w")
f.write('"Type","One Clients","Two Clients","Three Clients"\n')
data = '"LIST"'
for fps in tcplist_client_fps:
    data += ","
    data += '"{}"'.format(str(fps))
f.write(data + "\n")
data = '"THREAD"'
for fps in tcpthread_client_fps:
    data += ","
    data += '"{}"'.format(str(fps))
f.write(data + "\n")
f.close()

f = open("./tcp_compression_level.csv", "w")
data = '"Type"'
for x in range(1, 7):
    data += ","
    data += '"Compression Level {}"'.format(x)
f.write(data + "\n")
data = '"LIST"'
for fps in tcplist_compression_fps:
    data += ","
    data += '"{}"'.format(str(fps))
f.write(data + "\n")
data = '"THREAD"'
for fps in tcpthread_compression_fps:
    data += ","
    data += '"{}"'.format(str(fps))
f.write(data + "\n")
f.close()