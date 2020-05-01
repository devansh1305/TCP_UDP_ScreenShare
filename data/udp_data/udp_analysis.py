import numpy

# used to read the fps data collected for each client
def get_avg_fps(fil):
    fps = []
    infile = open(fil, 'r', encoding = "utf-16")
    for line in infile:
        #print(line)
        fps.append(float(line.strip("\n")))
    avg = numpy.average(fps)
    #print(avg)
    return avg

if __name__ == "__main__":
    #fpsg1 = get_avg_fps(".\\fps_record_clients_1.txt")
    
    #fps21 = get_avg_fps(".\\fps_record_clients_2_1.txt")
    #fps22 = get_avg_fps(".\\fps_record_clients_2_2.txt")
    #fpgs_a_2 = []
    #fpgs_a_2.append(fps21)
    #fpgs_a_2.append(fps22)
    #fpgs_avg_2 = numpy.average(fpgs_a_2)
    #print("fps:",fpgs_avg_2)

    fps31 = get_avg_fps(".\\fps_record_clients_3_1.txt")
    fps32 = get_avg_fps(".\\fps_record_clients_3_2.txt")
    fps33 = get_avg_fps(".\\fps_record_clients_3_3.txt")
    fpgs_a_3 = []
    fpgs_a_3.append(fps31)
    fpgs_a_3.append(fps32)
    fpgs_a_3.append(fps33)
    fpgs_avg_3 = numpy.average(fpgs_a_3)

    fps31_1 = get_avg_fps(".\\fps_res_360_240_clients_3_1.txt")
    fps32_1 = get_avg_fps(".\\fps_res_360_240_clients_3_2.txt")
    fps33_1 = get_avg_fps(".\\fps_res_360_240_clients_3_3.txt")
    fpgs_a_3_1 = []
    fpgs_a_3_1.append(fps31_1)
    fpgs_a_3_1.append(fps32_1)
    fpgs_a_3_1.append(fps33_1)
    fpgs_avg_3_1 = numpy.average(fpgs_a_3_1)

    fps31_2 = get_avg_fps(".\\fps_res_540_360_clients_3_1.txt")
    fps32_2 = get_avg_fps(".\\fps_res_540_360_clients_3_2.txt")
    fps33_2 = get_avg_fps(".\\fps_res_540_360_clients_3_3.txt")
    fpgs_a_3_2 = []
    fpgs_a_3_2.append(fps31_2)
    fpgs_a_3_2.append(fps32_2)
    fpgs_a_3_2.append(fps33_2)
    fpgs_avg_3_2 = numpy.average(fpgs_a_3_2)

    #f = open("./udp_client_fps_rec.csv", "w")
    #f.write('"Clients","Average FPS"\n')
    #data = '"One Client",'
    #data += '"{}"'.format(str(fpsg1))
    #f.write(data + "\n")
    #data = '"Two Clients",'
    #data += '"{}"'.format(str(fpgs_avg_2))
    #f.write(data + "\n")
    #data = '"Three Clients",'
    #data += '"{}"'.format(str(fpgs_avg_3))
    #f.write(data + "\n")
    #f.close()

    #fpgs_res_avg_2 = 0

    f = open("./udp_client_fps_res.csv", "w")
    f.write('"Resolution","Average FPS"\n')
    data = '"720*480",'
    data += '"{}"'.format(str(fpgs_avg_3))
    f.write(data + "\n")
    data = '"540*360",'
    data += '"{}"'.format(str(fpgs_avg_3_2))
    f.write(data + "\n")
    data = '"360*240",'
    data += '"{}"'.format(str(fpgs_avg_3_1))
    f.write(data + "\n")
    f.close()
