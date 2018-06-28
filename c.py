import cv2

image = cv2.imread("/Users/Quantum/Desktop/4.jpg")
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
for x in range(rows):
    num=0
    for y in range(colums):
        if(gray[x,y]==tag):
            sum_rows[x]=sum_rows[x]+1
print("横向的投影: "+str(sum_rows))

for i in range(rows):
    sum_row+=sum_rows[i]

tag_row = int(sum_row / rows)

print("mean_sum_rows:  " +  str(tag_row))



tag_rows=[0 for n in range(rows)]
index1 = (int)(rows/12)
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



# 存储分割之后的横向坐标信息
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

print("记录的横向坐标分割点:  "+str(cut_colums))

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

if(cut_colums[0]>colums/8):
    cut_colums.insert(0,cut_colums[1])
    cut_colums.insert(0,5)
if((colums- cut_colums[len(cut_colums)-1])>colums/8):
    cut_colums.insert(len(cut_colums)-1,cut_colums[len(cut_colums)-1])
    cut_colums.append(colums-5)

print("cut_cloums: "+str(cut_colums))


for i in range(1,len(cut_colums),2):
    cv2.imwrite("/Users/Quantum/Desktop/" + str(cut_colums[i-1]) + ":" + str(cut_colums[i]) + ".jpg",
         image[:, range(cut_colums[i-1]-3, cut_colums[i] + 1+3)][range(row_start -3, row_end + 1 +3), :])

# cv2.waitKey()
cv2.waitKey(0)


