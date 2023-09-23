# 2023.9.18 
# Yzy

import numpy as np
import random
import time
import cv2

color_dict = ["白","粉","黄","蓝"]

class find_best_order(object):
    # img size 6*8
    def __init__(self,input_image):
        self.image = input_image
        self.permanent_img = np.copy(input_image)
        self.finish_flag = False
        self.min_bolck_num = 10000
        self.wipe_order = []
        self.m = self.image.shape[0]
        self.n = self.image.shape[1]
    
    # 返回某一个坐标的所有相邻坐标点
    def get_neighbor_cord(self,cord):
        n_cord = []
        cord1 = [cord[0]-1,cord[1]]
        cord2 = [cord[0]+1,cord[1]]
        cord3 = [cord[0],cord[1]-1]
        cord4 = [cord[0],cord[1]+1]
        if cord1[0]>=0:
            n_cord.append(cord1)
        if cord2[0]<self.m:
            n_cord.append(cord2)
        if cord3[1]>=0:
            n_cord.append(cord3)
        if cord4[1]<self.n:
            n_cord.append(cord4)
        return n_cord
    
    # 返回某一个区域的所有相邻坐标点
    def get_region_neighbor(self,region):
        region_neighbor_list = []
        for cord in region:
            n_cord_list = self.get_neighbor_cord(cord) 
            for n_cord in n_cord_list:
                if n_cord in region or n_cord in region_neighbor_list:
                    continue
                region_neighbor_list.append(n_cord)
        return region_neighbor_list
    
    #将某个区域的数值全部赋值为0
    def wipe_region(self,region):
        for cord in region:
            self.image[cord[0],cord[1]]=0

    # 变化指定位置的数值
    def change_value(self,cord_list):
        for cord in cord_list:
            if self.image[cord[0],cord[1]]==0:
                continue
            self.image[cord[0],cord[1]] += 1
            if self.image[cord[0],cord[1]]==5:
                self.image[cord[0],cord[1]]=1

    # 向连通区域集合中加入坐标点
    # 递归，如果一个点，存在他周围跟他的value一样且不在联通集合中，则将他周围的点加入集合中
    # 每次有点加入集合，重复上述过程，直到无法重复
    def add_cord_to_area(self,used_cord_list,area_list,cord):
        if cord in area_list:
            return used_cord_list,area_list
        area_list.append(cord)
        used_cord_list.append(cord)
        n_cord_list = self.get_neighbor_cord(cord)
        for neighbor_cord in n_cord_list:
            if self.image[neighbor_cord[0],neighbor_cord[1]] == self.image[cord[0],cord[1]]:
                used_cord_list,area_list = self.add_cord_to_area(used_cord_list,area_list,neighbor_cord)
        return used_cord_list,area_list
        
    def calculate_remain_block(self):
        return np.count_nonzero(self.image)



    #记录所有的联通区域
    def region(self):
        region_area_dict = {1:[],2:[],3:[],4:[]}
        used_cord = []
        for i in range(self.m):
            for j in range(self.n):
                if self.image[i,j]==0:
                    continue
                if [i,j] not in used_cord:
                    used_cord, region = self.add_cord_to_area(used_cord,[],[i,j])
                    if len(region)>1:
                        region_area_dict[self.image[i,j]].append(region)
        return region_area_dict
    
    def take_one_step(self):
        # 先找到所有联通区域，从中选取一个【如果没有联通区域就结束】
        # 然后消除掉这部分联通区域，赋值为0
        # 最后将这部分区域周围的区域进行数值变化
        # 至此，one step完成
        region_dict = self.region()
        region_list = region_dict[1]+region_dict[2]+region_dict[3]+region_dict[4]
        if len(region_list)==0:
            self.finish_flag = True
            return []
        # 随机选择联通区域
        #choose_region = min(region_list, key=lambda x: len(x))
        choose_region = region_list[random.randint(0,len(region_list)-1)]
        #choose_region = region_list[int(time.time())%len(region_list)]
        # 消除该联通区域
        self.wipe_region(choose_region)
        # 将周围区域数值进行变化
        region_neighbor = self.get_region_neighbor(choose_region)
        self.change_value(region_neighbor)
        # 一次操作结束
        return choose_region
    
    def take_steps_until_end(self,epoch):
        # 每次完成后，需要记录的内容有
        # 还剩多少方块没消掉
        # 一共消除了多少步
        # 记录消除顺序，每一步分别消除的是哪些区域(以及每次消除时image的状态)
        # 如果剩余方块数量达到历史最低，那么更新步数和消除顺序
        #random.seed(epoch)
        this_wipe_order = []
        while not self.finish_flag:
            choose_region = self.take_one_step()
            this_wipe_order.append(choose_region)
        block_num = self.calculate_remain_block()
        if block_num<self.min_bolck_num:
            self.min_bolck_num = block_num
            self.wipe_order = this_wipe_order
    
    def simulate(self,sim_time=100):
        for i in range(sim_time):
            self.take_steps_until_end(i)
            # 在每次结束后，需要将图像恢复到最初的状态，flag恢复到未完成的状态
            self.image = np.copy(self.permanent_img)
            self.finish_flag = False



class dig_game(object):
    def __init__(self,input_image,sim_time=10000) -> None:
        self.image = input_image
        self.permanent_img = np.copy(input_image)
        self.m = self.image.shape[0]
        self.n = self.image.shape[1]
        self.real_wipe_order = []
        self.real_image_order = []
        self.sim_time = sim_time
        self.block_list = [[0,0],[5,0],[0,7],[5,7],[0,14],[5,14]]
        # 首先得到11 22的图像
        # 然后，根据左上角8x6的方块计算出最优方法
        # 把最优方法实践到11 22的图像中，得到新的图像
        # 然后，根据左下角8x6的方块计算出最优方法
        # ......以此类推即可
    
    def cut_image(self,cord):
        # cut 6*8 size
        cut_img = self.image[cord[0]:cord[0]+6,cord[1]:cord[1]+8]
        return cut_img
    
    # 返回某一个坐标的所有相邻坐标点
    def get_neighbor_cord(self,cord):
        #print(cord)
        n_cord = []
        cord1 = [cord[0]-1,cord[1]]
        cord2 = [cord[0]+1,cord[1]]
        cord3 = [cord[0],cord[1]-1]
        cord4 = [cord[0],cord[1]+1]
        if cord1[0]>=0:
            n_cord.append(cord1)
        if cord2[0]<self.m:
            n_cord.append(cord2)
        if cord3[1]>=0:
            n_cord.append(cord3)
        if cord4[1]<self.n:
            n_cord.append(cord4)
        return n_cord
    
    # 返回某一个区域的所有相邻坐标点
    def get_region_neighbor(self,region):
        region_neighbor_list = []
        for cord in region:
            #print(cord)
            n_cord_list = self.get_neighbor_cord(cord) 
            for n_cord in n_cord_list:
                if n_cord in region or n_cord in region_neighbor_list:
                    continue
                region_neighbor_list.append(n_cord)
        return region_neighbor_list
    
    #将某个区域的数值全部赋值为0
    def wipe_region(self,region):
        for cord in region:
            self.image[cord[0],cord[1]]=0

    # 变化指定位置的数值
    def change_value(self,cord_list):
        for cord in cord_list:
            if self.image[cord[0],cord[1]]==0:
                continue
            self.image[cord[0],cord[1]] += 1
            if self.image[cord[0],cord[1]]==5:
                self.image[cord[0],cord[1]]=1
    
    # 返回基于某个点对应的联通区域
    # 向连通区域集合中加入坐标点
    # 递归，如果一个点，存在他周围跟他的value一样且不在联通集合中，则将他周围的点加入集合中
    # 每次有点加入集合，重复上述过程，直到无法重复
    def add_cord_to_area(self,area_list,cord):
        if cord in area_list:
            return area_list
        area_list.append(cord)
        n_cord_list = self.get_neighbor_cord(cord)
        for neighbor_cord in n_cord_list:
            if self.image[neighbor_cord[0],neighbor_cord[1]] == self.image[cord[0],cord[1]]:
                area_list = self.add_cord_to_area(area_list,neighbor_cord)
        return area_list
    
    def get_wipe_region_and_take_one_step(self,start_cord):
        cut_img = self.cut_image(start_cord).copy()
        f = find_best_order(cut_img)
        f.simulate(self.sim_time)
        wipe_order = f.wipe_order.copy()
        #print(self.image)
        for wipe in wipe_order:
            if wipe==[]:
                continue
            # 所有要依次消除的区域是wipe_order
            # 每一个要消除的区域是wipe
            # print(wipe_order, wipe)
            wipe_cord = wipe[0]
            wipe_cord = [wipe_cord[0]+start_cord[0],wipe_cord[1]+start_cord[1]]
            #print(wipe_cord)
            real_wipe_region = self.add_cord_to_area([],wipe_cord)
            if len(real_wipe_region)==1:
                self.real_wipe_order = []
                self.real_image_order = []
                self.image = self.permanent_img.copy()
                return "Error"
            
            self.real_image_order.append(self.image.copy())
            region_neighbor_list = self.get_region_neighbor(real_wipe_region)
            self.wipe_region(real_wipe_region)
            self.change_value(region_neighbor_list)
            # print("************************")
            # print(real_wipe_region)
            # print(region_neighbor_list)
            # print(self.image)
            # print("-----------------------")
            self.real_wipe_order.append(real_wipe_region)
            
        return
    def calculate_remain_block(self):
        return np.count_nonzero(self.image)    
    
    def visualize_array(self, array, coordinate_list):
        height, width = self.m, self.n
        result = "     1   2   3   4   5   6   7   8   9   10  11  12  13  14  15  16  17  18  19  20  21  22"
        result += "\n"
        result += "\n"
        for i in range(height):
            result += "{:02d}".format(i+1)
            for j in range(width):
                if [i, j] in coordinate_list:
                    result += "  " + color_dict[int(array[i,j]-1)]
                elif array[i,j] == 0:
                    result += "   X"
                else:
                    result += "   -"#"  %d"%array[i,j]
            if i!= height-1:
                result += "\n"
                result += "\n"
        return result

    def run(self):
        start_time = time.time()
        one_time = True
        for cord in self.block_list:
            a = self.get_wipe_region_and_take_one_step(cord)
            if a=="Error":
                one_time = False
                break
        if not one_time:
            for cord in self.block_list[::-1]:
                a = self.get_wipe_region_and_take_one_step(cord)
                if a=="Error":
                    print("False to solve...")
                    return
        end_time = time.time()
        print("模拟花费时间为",round(end_time-start_time,3))
        print("剩余方块数量为:  ", self.calculate_remain_block())
        print("所需步数为%d,下面将一步步引导操作步骤达成最优情况"%(len(self.real_wipe_order)-1))
        for i in range(len(self.real_wipe_order)):
            if i>0 and i<len(self.real_wipe_order)-1:
                input("现在已经完成第%d / %d步，请敲下Enter键查看下一步操作"%(i,len(self.real_wipe_order)-1))
            if i==len(self.real_wipe_order)-1:
                input("现在已经完成第%d / %d步，请敲下Enter键查看最终结果"%(i,len(self.real_wipe_order)-1))
            print(self.visualize_array(self.real_image_order[i],self.real_wipe_order[i]))
        print("操作全部完成")



def get_img_array(img_file):
    x_part=11
    y_part=22
    array = cv2.imread(img_file)
    xlen, ylen = array.shape[0], array.shape[1]
    x_cord_list = [int(i * xlen/x_part) for i in range(x_part+1)]
    y_cord_list = [int(i * ylen/y_part) for i in range(y_part+1)]
    new_array = np.zeros([x_part,y_part])
    standard_pixel_value = [[150,150,150],[145,110,185],[90,140,175],[147,135,75]]
    # 实际操作的时候 白作为1 就是 白1 红2 黄3 蓝4
    # 如果像素并非标准像素，自己截图计算均值即可
    def classificate_block(channel_means,standard_pixel_value):
        diff=10000
        for i in range(len(standard_pixel_value)):
            this_diff = sum([abs(channel_means[j]-standard_pixel_value[i][j]) for j in range(3)])
            if this_diff<diff:
                diff=this_diff
                class_result = i+1
        return class_result

    for i in range(x_part):
        for j in range(y_part):
            cut_img = array[x_cord_list[i]:x_cord_list[i+1],y_cord_list[j]:y_cord_list[j+1]]
            channel_means = np.mean(cut_img, axis=(0, 1))
            class_result = classificate_block(channel_means,standard_pixel_value)
            new_array[i,j] = class_result
    return new_array
            

# 截图保存到指定路径，修改文件名
new_array = get_img_array("1.png")
arr = new_array
# #print(arr)
# #print(new_array)

# # 随机生成一个尺寸为 (11, 22) 的数组，元素仅包含 1、2、3、4
# # arr = np.random.choice([1, 2, 3, 4], size=(11, 22))
# # print(arr)

Dig = dig_game(arr,10000)
Dig.run()





