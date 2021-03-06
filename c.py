import cv2


sum_sum =0
#   提取字符数据库需要的提取文件的路径
import os
path = "/Users/Quantum/Desktop/croped/"
files = os.listdir(path)
for file in files:
    file=file[:file.index(".")]
    print(list(file))

    print(path+file+".jpg")
    image = cv2.imread(path+file+".jpg")
    # Grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # cv2.namedWindow("Image")
    # cv2.imwrite("/Users/Quantum/Desktop/Grayscale.jpg",Grayscale)
    cv2.imwrite("/Users/Quantum/Desktop/Grayscale.jpg",gray)


    #   中值滤波进行去噪处理
    gray = cv2.medianBlur(gray,3)
    cv2.imwrite("/Users/Quantum/Desktop/medianBlur.jpg",gray)


    # cv2.imshow("Image",gray)
    # cv2.waitKey(10)

    # from matplotlib import pyplot as plt
    # plt.imshow(gray, 'gray')
    # plt.show()


    #  车牌的大小
    sp = image.shape
    print ("维度"+str(sp))
    rows = sp[0]  # height(rows) of image
    colums = sp[1]  # width(colums) of image
    # sz3 = sp[2]  # the pixels value is made up of three primary colors
    # print ('width: %d \nheight: %d \nnumber: %d' % (sz1, sz2, sz3))


    #   找到一个合理的阈值为二值化处理提前准备好条件
    sum =0
    num =0
    for i in range(rows):
        for j in range(colums):
            sum+=gray[i,j]
            num+=1

    mean_value = (int)(sum/num)
    print("所有像素点平均值: "+str(mean_value))


    black_num = 0
    white_num = 0
    #  二值化处理,同时存储白色与黑色像素点的多少来判断字母和底色的颜色是黑是白
    for y in range(colums):
        num=0
        for x in range(rows):
            if(gray[x,y]>mean_value-10):
                gray[x, y]=255
                white_num+=1

            else:
                gray[x,y]=0
                black_num+=1


    if (black_num>white_num):
        tag = 255
        print("白色的字体")
    else:
        tag =0
        print("黑色的字体")


    # gray = cv2.adaptiveThreshold(Grayscale, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 5, 10)



    # cv2.imshow("Image",gray)
    # 存储二值化处理之后的图像
    cv2.imwrite("/Users/Quantum/Desktop/gray.jpg",gray)


    #   列坐标序号
    # colums_list =[]
    # for i in range(colums):
    #     colums_list.append(i)
    # print(colums_list)





    # sum_colum = 0
    # sum_colums = [0 for n in range(colums)]
    # #  纵向的投影
    # for y in range(colums):
    #     num=0
    #     for x in range(rows):
    #         if(gray[x,y]==tag):
    #             sum_colums[y]=sum_colums[y]+1
    #
    # print(sum_colums)
    #
    # for i in range(colums):
    #     sum_colum+=sum_colums[i]
    # tag_colum = int(sum_colum/colums)
    # print("mean_sum_colum:  " +  str(tag_colum))
    #
    #
    # tag_colums=[0 for n in range(colums)]
    # for i in range(colums):
    #     if(sum_colums[i]>tag_colum):
    #         tag_colums[i]=1
    #     else:
    #         tag_colums[i]=0
    #
    # print(tag_colums)
    #
    # # 对投影进行排序
    # colums_copy = sum_colums.copy()
    # colums_copy.sort()
    # # print(colums_copy)







    sum_row = 0
    sum_rows = [0 for n in range(rows)]
    #  横向的投影
    # for x in range(rows):
    #     num=0
    #     for y in range(colums):
    #         if(gray[x,y]==tag):
    #             sum_rows[x]=sum_rows[x]+1
    for x in range(rows):
        num=0
        for y in range((int)(colums/12),(int)(colums*11/12)):
            if(gray[x,y]==tag):
                sum_rows[x]=sum_rows[x]+1


    print("横向的投影: "+str(sum_rows))

    for i in range(rows):
        sum_row+=sum_rows[i]

    tag_row = int(sum_row / rows)

    print("mean_sum_rows:  " +  str(tag_row))

    index1 =0
    for i in range(rows):
        if(sum_rows[i]>tag_row/2):
            index1=i-1
            break




    tag_rows=[0 for n in range(rows)]
    # if(index1==0):
    # index1 = (int)(rows/12)
    index2 = (int)(rows*(11/12))
    for i in range(index1,index2):
        if(sum_rows[i]>tag_row-20):
            tag_rows[i]=1
        else:
            tag_rows[i]=0

    print("横向标记分割: "+str(tag_rows))



    # 对投影进行排序
    rows_copy = sum_rows.copy()
    rows_copy.sort()
    # print(rows_copy)

    double = 0
    double_start =0
    double_end = 0
    tag1 = 0
    tag2 =0
    for i in range((int)(rows/4),(int)(rows*3/4)):
        if(sum_rows[i]==0 and sum_rows[i+1]!=0):
            print(" 双排车牌")
            tag1 =1
            double_end = i
        if (sum_rows[i] !=0 and sum_rows[i + 1] == 0):
            print(" 双排车牌")
            tag2 = 1
            double_start = i
    if(tag1 and tag2):
        double=1






    #  对双排车牌的下半部分进行处理,重新进行赋值处理
    if(double==1):
        print("double_start: " + str(double_start))
        print("double_end: " + str(double_end))

        double_avg = (int)((double_start + double_end) / 2)

        print("double_avg: " + str(double_avg))

        cv2.imwrite("/Users/Quantum/Desktop/double_up.jpg", image[range(double_avg + 1), :])
        cv2.imwrite("/Users/Quantum/Desktop/double_down.jpg", image[range((int)(double_avg * 7 / 9), rows), :])
        # cv2.imwrite("/Users/Quantum/Desktop/double_up_1.jpg",
        #             image[range(double_avg + 1), :][:, range((int)(colums * 2 / 10), (int)(colums / 2))])
        # cv2.imwrite("/Users/Quantum/Desktop/double_up_2.jpg",
        #             image[range(double_avg + 1), :][:, range((int)(colums / 2), (int)(colums * 8 / 10))])


        path_file_1 = "/Users/Quantum/Desktop/mjy/" + file[0] + "____" + file+".jpg"
        cv2.imwrite(path_file_1,
                    image[range(double_avg + 1), :][:, range((int)(colums * 2 / 10), (int)(colums / 2))])
        path_file_2 = "/Users/Quantum/Desktop/mjy/" + file[1] + "____" + file+".jpg"
        cv2.imwrite(path_file_2,
                    image[range(double_avg + 1), :][:, range((int)(colums / 2), (int)(colums * 8 / 10))])





        image = cv2.imread("/Users/Quantum/Desktop/double_down.jpg")
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 3)

        sp = image.shape
        rows = sp[0]
        colums = sp[1]

        tag_rows = [0 for n in range(rows)]
        index1 = (int)(rows / 12)
        index2 = (int)(rows * (11 / 12))
        for i in range(index1, index2):
            if (sum_rows[i] > tag_row - 20):
                tag_rows[i] = 1
            else:
                tag_rows[i] = 0
        print("横向标记分割: "+str(tag_rows))

        for y in range(colums):
            num = 0
            for x in range(rows):
                if (gray[x, y] > mean_value - 10):
                    gray[x, y] = 255
                    white_num += 1

                else:
                    gray[x, y] = 0
                    black_num += 1

        sum_row = 0
        sum_rows = [0 for n in range(rows)]

        for x in range(rows):
            num = 0
            for y in range((int)(colums / 12), (int)(colums * 11 / 12)):
                if (gray[x, y] == tag):
                    sum_rows[x] = sum_rows[x] + 1

        print("横向的投影: " + str(sum_rows))








    # import matplotlib.pyplot as plt
    # for i in range(sp[1]):
    #     plt.scatter(i,lst[i])
    # plt.show()





    #  横向分割
    list2 =[]
    num = 0
    start=0
    end=0
    for i in range(rows):
        if(sum_rows[i-1]==0 and sum_rows[i]==1):
            start=i
            num=num+1
        if(sum_rows[i-1]==1 and sum_rows[i]==0):
            end =i
            num=num+1
        if(num==2):
            # cv2.imwrite("/Users/Quantum/Desktop/"+str(i)+".jpg", gray[:,range(start,end+1)] )
            list2.append(start)
            list2.append(end)
            # cv2.imwrite("/Users/Quantum/Desktop/9.jpg", gray[:,range(start,end+1)])
            num=0

    # print("横向分割: "+str(list2))

    # list2.sort()
    #
    # cut_rows =[]
    # for i in range(1,len(list2),2):
    #     cut_rows.append(list2[i]-list2[i-1])
    # print(cut_rows)
    #
    #
    # #  一般在纵向区域会分为三个部分,而字符所在的部分是最大的跨度部分
    # print("max   "+str(max(cut_rows)) )
    # index = cut_rows.index(max(cut_rows))
    #
    # print("index   "+str(index))
    #
    # print(list2[index*2])
    # print(list2[index*2+1])
    #
    # row_start = list2[index*2-1]
    # row_end = list2[index*2+1+1]

    row_start = 0
    row_end = 0

    for i in range(rows):
        if(tag_rows[i]==0 and tag_rows[i+1]==1):
            row_start = i
            break


    for i in range(rows-1,-1,-1):
        if(tag_rows[i]==0 and tag_rows[i-1]==1):
            row_end = i
            break

    # for i in range(rows-1):
    #     if(tag_rows[i]==0 and tag_rows[i+1]==1):
    #         row_start = i
    #     if (tag_rows[i] == 1 and tag_rows[i+1]==0):
    #         row_end = i
    #     if((row_end-row_start)>rows/3):
    #         break

    print("row_start:  "+ str(row_start))
    print("row_end:  "+ str(row_end))








    sum_colum = 0
    sum_colums = [0 for n in range(colums)]
    #  纵向的投影
    for y in range(colums):
        num=0
        for x in range(row_start,row_end+1):
            if(gray[x,y]==tag):
                sum_colums[y]=sum_colums[y]+1

    print("纵向的投影: "+str(sum_colums))

    for i in range(colums):
        sum_colum+=sum_colums[i]
    tag_colum = int(sum_colum/colums)
    print("mean_sum_colum:  " +  str(tag_colum))


    tag_colums=[0 for n in range(colums)]
    index1 = (int)(colums/25)
    index2 = (int)(colums*(24/25))
    for i in range(index1,index2):
        if(sum_colums[i]>5):
            tag_colums[i]=1
        else:
            tag_colums[i]=0

    print("纵向标记分割: "+str(tag_colums))

    # 对投影进行排序
    colums_copy = sum_colums.copy()
    colums_copy.sort()
    # print(colums_copy)



    #   纵向的分割
    list1 =[]
    list_start = []
    list_end = []
    num = 0
    start=0
    end=0
    for i in range(colums):
        # num = 0
        if(tag_colums[i-1]==0 and tag_colums[i]==1):
            start=i
            num=num+1
            list_start.append(i)
            # print(i)
            list1.append(start)
        if(tag_colums[i-1]==1 and tag_colums[i]==0):
            end =i
            num=num+1
            # print(i)
            list1.append(end)
            list_end.append(i)
        # if(num==2):
        #     cv2.imwrite("/Users/Quantum/Desktop/"+str(i)+".jpg", gray[:,range(start,end+1)] )
        #     list1.append(start)
        #     # print(start)
        #     list1.append(end)
        #     # print(end)
        #     # cv2.imwrite("/Users/Quantum/Desktop/9.jpg", gray[:,range(start,end+1)])
        #     num=0

    print("纵向分割: "+str(list1))

    # for i in range(len(list1)):
    #     if (i%2==1 and list1[i]-list1[i-1]>5):
    #         cv2.imwrite("/Users/Quantum/Desktop/"+str(list1[i])+".jpg", gray[:,range(list1[i-1],list1[i]+1)] )




    print("起始坐标点: "+str(list_start))
    print("终止坐标点: "+str(list_end))



    # 存储分割之后的纵向坐标信息
    cut_colums = []
    # 分开存储字符分割之后的图像
    for i in range(0,len(list_start)):
        # if (list_end[i]+colums/40 > list_start[i+1]):
        #     for j in range(i+1,len(list_start)):


        if ( list_end[i]-list_start[i]>3):
            # cv2.imwrite("/Users/Quantum/Desktop/"+str(i)+".jpg", gray[range(row_start,row_end+1),range(list1[i-1],list1[i]+1)] )
            # cv2.imwrite("/Users/Quantum/Desktop/"+str(list1[i]+1)+".jpg", gray[:,range(list1[i-1],list1[i]+1)][range(row_start,row_end+1),:] )
            cut_colums.append(list_start[i])
            cut_colums.append(list_end[i])
            # cv2.imwrite("/Users/Quantum/Desktop/" + str(list_start[i] )+":"+str(list_end[i]) + ".jpg",
            #             image[:, range(list_start[i], list_end[i] + 1)][range(row_start + 3, row_end + 1 - 3), :])


                # print("字符: "+ str(list1[i-1] )+":"+str(list1[i]))
        # if (list_start[i] - list_end[i] > colums / 30):
            # cv2.imwrite("/Users/Quantum/Desktop/"+str(i)+".jpg", gray[range(row_start,row_end+1),range(list1[i-1],list1[i]+1)] )
            # cv2.imwrite("/Users/Quantum/Desktop/"+str(list1[i]+1)+".jpg", gray[:,range(list1[i-1],list1[i]+1)][range(row_start,row_end+1),:] )
            # cv2.imwrite("/Users/Quantum/Desktop/" + str(list_end[i]) + ":" + str(list_start[i]) + ".jpg",
            #             image[:, range(list_end[i], list_start[i] + 1)][range(row_start + 3, row_end + 1 - 3), :])
            # print("字符: " + str(list1[i - 1]) + ":" + str(list1[i]))
        elif(list_end[i]-list_start[i]<0):
            if(i>=1 and list_end[i]-list_start[i-1]>colums/50):
                cut_colums.append(list_start[i-1])
                cut_colums.append(list_end[i])
                # cv2.imwrite("/Users/Quantum/Desktop/" + str(list_start[i-1]) + ":" + str(list_end[i]) + ".jpg",
                #         image[:, range(list_start[i-1], list_end[i] + 1)][range(row_start + 3, row_end + 1 - 3), :])


            # if(i-2<0):
            #     cv2.imwrite("/Users/Quantum/Desktop/"+str(list1[i]+1)+".jpg", image[:,range(list1[0],list1[i+1]+1)][range(row_start+3,row_end+1-3), :])
            #     # cv2.imwrite("/Users/Quantum/Desktop/"+str(list1[i]+1)+".jpg", gray[:,range(list1[0]-3,list1[i+1]+1-3)][range(row_start+3,row_end+1-3), :])
            #     # cv2.imwrite("/Users/Quantum/Desktop/"+str(list1[i]+1)+".jpg", gray[:,range(list1[0],list1[i+1]+1)][range(row_start,row_end+1), :])
            # elif(i+1>len(list1)-1):
            #     cv2.imwrite("/Users/Quantum/Desktop/"+str(list1[i]+1)+".jpg", image[:,range(list1[i-2],list1[len(list1)-1]+1)][range(row_start+3,row_end+1-3),:] )
            #     # cv2.imwrite("/Users/Quantum/Desktop/"+str(list1[i]+1)+".jpg", gray[:,range(list1[i-2]+3,list1[i+1]+1-3)][range(row_start+3,row_end+1-3),:] )
            #     # cv2.imwrite("/Users/Quantum/Desktop/"+str(list1[i]+1)+".jpg", gray[:,range(list1[i-1],list1[i])][range(row_start,row_end),:] )
            # else:
            #     cv2.imwrite("/Users/Quantum/Desktop/"+str(list1[i]+1)+".jpg", image[:,range(list1[i-2],list1[i+1]+1)][range(row_start+3,row_end+1-3),:] )

    print("记录的纵向坐标分割点:  "+str(cut_colums))


    #  下面一部分
    #  处理那些左右两部分的中文文字与八个字符情况下的的分割,还有因为二值化的可能不合理性而缺失的字符


    #  主要处理因为一个汉字分为左右两个部分,会被判定为两个字符的情况,在这里我们使用判断条件,清除里面的不合理分割点
    tag = 0
    for i in range(1,len(cut_colums)-1,2):
        if(cut_colums[i+1] - cut_colums[i]>=colums/50):
            # tag = cut_colums[i]
            tag = i
            break

    print(tag)
    # if(tag):
    #     for i in range(1,tag)):
    cut_colums = cut_colums[:1]+cut_colums[tag:]

    print("切割坐标 :"+str(cut_colums))





    #  具体处理那些汉字分为左右两个部分或者是像川字分为三个部分的问题,通过字符的中位数间隔的比例,我们进行处理
    cut_length = []
    for i in range(1,len(cut_colums),2):
        cut_length.append(cut_colums[i]-cut_colums[i-1])
    print("切割长度坐标: "+str(cut_length))

    copy = cut_length.copy()
    copy.sort()
    median_length = copy[(int)(len(cut_length)/2)]
    # print(copy)
    print("切割长度的中位数值: "+str(median_length))
    if (median_length ==0):
        median_length = colums/8

    cut_again_start = []
    cut_again_end = []
    cut_again_num =[]
    for  i in range(0,len(cut_length)):
        cut_num = (cut_length[i] / (median_length * 3 / 4))
        if(cut_num >=1.5):
            cut_again_start.append((i+1)*2-2)
            cut_again_end.append((i+1)*2-1)
            cut_again_num.append(int(cut_num))
    print("cut_again_start: "+str(cut_again_start))
    print("cut_again_end: "+str(cut_again_end))
    print("cut_again_num: "+str(cut_again_num))


    for i in range(0,len(cut_again_start)):
        if (i >0):
            incre_len = (int)((cut_colums[cut_again_end[i]+cut_again_num[i-1]-1]-cut_colums[cut_again_start[i]+cut_again_num[i-1]-1])/cut_again_num[i])
            # incre_len = (int)((cut_colums[cut_again_end[i]+2*(cut_again_num[i-1]-1)]-cut_colums[cut_again_start[i]+cut_again_num[i-1]-1])/cut_again_num[i])
            print(incre_len)

        else:
            incre_len = (int)((cut_colums[cut_again_end[i]]-cut_colums[cut_again_start[i]])/cut_again_num[i])
            print(incre_len)
        for j in range(1,cut_again_num[i]):
            if(i>0):
                # cut_colums.insert(cut_again_start[i]+j+(cut_again_num[i-1]-1)*2,cut_colums[cut_again_start[i]+cut_again_num[i-1]-1]+j*incre_len)
                num1 =  cut_colums[ cut_again_start[i] + cut_again_num[i - 1] - 1] + j * incre_len
                cut_colums.insert(cut_again_start[i]+j+cut_again_num[i-1]-1,cut_colums[cut_again_start[i]+cut_again_num[i-1]-1]+j*incre_len)
                cut_colums.append(num1)
                print(str(cut_again_start[i]+j+cut_again_num[i-1]-1) + "     " + str(cut_colums[cut_again_start[i]+cut_again_num[i-1]-1] + j * incre_len))
            #
            else:
                num2 = cut_colums[cut_again_start[i]]+j*incre_len
                cut_colums.insert(cut_again_start[i]+j,cut_colums[cut_again_start[i]]+j*incre_len)
                # cut_colums.insert(cut_again_start[i]+j+1,cut_colums[cut_again_start[i]]+j*incre_len)
                cut_colums.append(num2)
                print(str(cut_again_start[i]+j)+"     "+str(cut_colums[cut_again_start[i]]+j*incre_len))

    cut_colums.sort()

    print("cut_cloums: "+str(cut_colums))




    #  处理那些因为二值化不合理而消失的字符,通过过大的字符间隔判定有字符缺失
    if(cut_colums[0]>colums/8):
        cut_colums.insert(0,cut_colums[1])
        cut_colums.insert(0,5)
    if((colums- cut_colums[len(cut_colums)-1])>colums/8):
        cut_colums.insert(len(cut_colums)-1,cut_colums[len(cut_colums)-1])
        cut_colums.append(colums-5)

    print("cut_cloums: "+str(cut_colums))


    #  当铆钉接近字符的时候,会造成字符的联通,铆钉的位置一般在
    #  第二个字符与第三个字符之间,和第五个与第六个之间
    if(double!=1):
        cut1 = 0
        cut2 = 0
        if(cut_colums[3]==cut_colums[4]):
            cut1 = cut_colums[3]

        if (cut_colums[11] == cut_colums[12]):
            cut2 =cut_colums[11]

        if(cut1):
            while cut1 in cut_colums:
                cut_colums.remove(cut1)

        if(cut2):
            while cut1 in cut_colums:
                cut_colums.remove(cut2)


    #  判断剪完之后是不是仍然包括中心的小点



    if(cut_colums[3]-cut_colums[2]>median_length*1.2):
        cut_colums[3]=cut_colums[2]+(int)(median_length*1.2)


    print("cut_cloums: "+str(cut_colums))

    cut_length_last = []
    for i in range(1,len(cut_colums),2):
        cut_length_last.append(cut_colums[i]-cut_colums[i-1])
    print("last切割长度坐标: "+str(cut_length_last))


    #   只在进行提取字符数据的时候使用,为以后的字符识别做准备
    while(len(cut_colums)/2 >len(file)):
        index = cut_length_last.index(min(cut_length_last))
        cut_colums = cut_colums[:index*2]+cut_colums[index*2+2:]
        cut_length_last = []
        for i in range(1, len(cut_colums), 2):
            cut_length_last.append(cut_colums[i] - cut_colums[i - 1])

    print(cut_colums)

    if(double==0):
        for i in range(1,len(cut_colums),2):
            path_file = "/Users/Quantum/Desktop/mjy/"+file[(int)(i/2)]+"____"+file
            cv2.imwrite(path_file  + ".jpg",
                 image[:, range(cut_colums[i-1]-3, cut_colums[i] + 1+3)][range(row_start -3, row_end + 1 +3), :])
            sum_sum+=1
    else:
        for i in range(1, len(cut_colums), 2):
            path_file = "/Users/Quantum/Desktop/mjy/" + file[(int)(i / 2)+2] + "____" + file
            cv2.imwrite(path_file + ".jpg",
                        image[:, range(cut_colums[i - 1] - 3, cut_colums[i] + 1 + 3)][
                        range(row_start - 3, row_end + 1 + 3), :])
            sum_sum += 1


    #   输出分割之后的字符图像
    # for i in range(1,len(cut_colums),2):
    #     cv2.imwrite("/Users/Quantum/Desktop/" + str(cut_colums[i-1]) + ":" + str(cut_colums[i]) + ".jpg",
    #          image[:, range(cut_colums[i-1]-3, cut_colums[i] + 1+3)][range(row_start -3, row_end + 1 +3), :])

    # cv2.waitKey()
    # cv2.waitKey(0)


