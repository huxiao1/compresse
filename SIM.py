#On my honor, I have neither given nor received unauthorized aid on this assignment
from sys import argv

#----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------compression--------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------
""""
Data read and preprocessing
Data write
"""
def read_file_original():
	str = ""
	fp = open("./original.txt")
	content = fp.readlines()
	content2 = []
	len_con = len(content)
	for i in content:
		if i == content[len_con-1]:
			content2.append(i[0:-1])
			continue
		i = i[0:-1]
		content2.append(i)
	return content2

def write_file_original(compressed):
	f = open("cout.txt","a")
	f.write(compressed)
	f.close()

"""
get the dictionary
"""
def get_dict(original):
	dict1 = {}
	list1 = []
	final_list = []
	for i in original:
		if i in dict1.keys():
			dict1[i] += 1
		else:
			dict1[i] = 1

	list1 = sorted(dict1.items(), key=lambda x:x[1],reverse=True)
	for i in range(16):
		final_list.append(list1[i][0])
	return final_list

"""
compressed methods
"""
def direct_match(flag):
	dict_index = '{:04b}'.format(flag[0])
	new_str1 = "111" + dict_index
	return new_str1

def run_length_encoding(str1,tag_i):
	str2 = '{:03b}'.format(tag_i-2)
	new_str1 = "001" + str2
	return new_str1

def bit_mask(str1,final,i):
	loc = final[i][0]
	loc = '{:05b}'.format(loc)
	dict_index = '{:04b}'.format(i)
	dict_str = dictionary[i]
	dict_index_real = '{:04b}'.format(i)
	first_diff_index = final[i][0]
	if first_diff_index <= 28:
		a = str1[first_diff_index:first_diff_index+4]
		b = dict_str[first_diff_index:first_diff_index+4]
		final_bin_str = str_2_bin(a,b)
	else:
		a = str1[-4:]
		b = dict_str[-4:]
		final_bin_str = str_2_bin(a,b)
	new_str1 = "010" + loc + final_bin_str + dict_index_real
	return new_str1


def bit1_mask(final,flag1):
	i = flag1[0]
	loc = final[i][0]
	loc = '{:05b}'.format(loc)
	dict_index = '{:04b}'.format(i)
	new_str1 = "011" + loc + dict_index
	return new_str1

def bit2c_mask(final,i):
	loc = final[i][0]
	loc = '{:05b}'.format(loc)
	dict_index = '{:04b}'.format(i)
	new_str1 = "100" + loc + dict_index
	return new_str1

def bit4c_mask(final,i):
	loc = final[i][0]
	loc = '{:05b}'.format(loc)
	dict_index = '{:04b}'.format(i)
	new_str1 = "101" + loc + dict_index
	return new_str1

def bit2nc_mask(final,i):
	loc1 = final[i][0]
	loc1 = '{:05b}'.format(loc1)
	loc2 = final[i][1]
	loc2 = '{:05b}'.format(loc2)
	dict_index = '{:04b}'.format(i)
	new_str1 = "110" + loc1 + loc2 + dict_index
	return new_str1

"""
sup function
"""
#find the index in the dict priority is str1 in dict
def find_dict_index(str1):
	for i in range(len(dictionary)):
		if dictionary[i] == str1:
			return '{:04b}'.format(i)
#find different location
def find_differnet_loc(str1,dictionary):
	res = []
	for i in range(32):
		if str1[i] != dictionary[i]:
			res.append(i)
	return res
#judge the 4bit con or not con
def bit4_con_jug(final,flag4):
	for i in flag4:
		if ((final[i][1] - final[i][0]) == 1) and ((final[i][2] - final[i][1]) == 1) and ((final[i][3] - final[i][2]) == 1):
			return True
	return False
#judge the 2bit con or not con
def bit2_con_jug(final,flag2):
	for i in flag2:
		if (final[i][1] - final[i][0]) == 1:
			return True
	return False
#judge the bitmask can or cannot  flag2,flag3,flag4
def bitmask_jug(final,flag):
	for i in flag:
		if final[i][-1] - final[i][0] <= 3:
			return i
	return False
#get the bin
def str_2_bin(a,b):
	c = (int(a,2))^(int(b,2))
	d = bin(c)[2:]
	resultd = ""
	if len(d) != 4:
		add0 = 4 - len(d)
		for i in range(add0):
			resultd += '0'
		return resultd + d
	return d
#find difference index of 1 between 00000...
def method_choose(str1):
	flag_0 = False
	flag_1 = False
	flag_2 = False
	flag_3 = False
	flag_4 = False
	flag_n = False

	final = []
	flag0 = []
	flag1 = []
	flag2 = []
	flag3 = []
	flag4 = []
	flagn = []

	for i in range(len(dictionary)):
		res = []
		res = find_differnet_loc(str1,dictionary[i])
		final.append(res)

	#i:num of dic element   final[i]-->correspond diff ele loc 
	#final: [[i],[i+1],[i+2]]
	for i in range(len(final)):
		if len(final[i]) == 1:
			flag_1 = True
			flag1.append(i)
		elif len(final[i]) == 2:
			flag_2 = True
			flag2.append(i)
		elif len(final[i]) == 3:
			flag_3 = True
			flag3.append(i)
		elif len(final[i]) == 4:
			flag_4 = True
			flag4.append(i)
		elif len(final[i]) == 0:
			flag_0 = True
			flag0.append(i)
		else:
			flag_n = True
			flagn.append(i)

	if flag_0 == True:
		result_str = direct_match(flag0)
		return result_str

	elif flag_1 == True:
		result_str = bit1_mask(final,flag1)
		return result_str

	elif (bit2_con_jug(final,flag2) == True) and  (flag_2 == True):
		for i in flag2:
			if final[i][1] - final[i][0] == 1:
				result_str = bit2c_mask(final,i)
				return result_str

	elif (bit4_con_jug(final,flag4) == True) and (flag_4 == True):
		for i in flag4:
			if ((final[i][1] - final[i][0]) == 1) and ((final[i][2] - final[i][1]) == 1) and ((final[i][3] - final[i][2]) == 1):
				result_str = bit4c_mask(final,i)
				return result_str

	elif (bitmask_jug(final,flag2) != False) and (flag_2 == True) and (bitmask_jug(final,flag3) != False) and (flag_3 == True) and (bitmask_jug(final,flag4) != False) and (flag_4 == True):
		i = min(bitmask_jug(final,flag2),bitmask_jug(final,flag3),bitmask_jug(final,flag4))
		result_str = bit_mask(str1,final,i)
		return result_str
	elif (bitmask_jug(final,flag2) != False) and (flag_2 == True) and (bitmask_jug(final,flag3) != False) and (flag_3 == True):
		i = min(bitmask_jug(final,flag2),bitmask_jug(final,flag3))
		result_str = bit_mask(str1,final,i)
		return result_str
	elif (bitmask_jug(final,flag2) != False) and (flag_2 == True) and (bitmask_jug(final,flag4) != False) and (flag_4 == True):
		i = min(bitmask_jug(final,flag2),bitmask_jug(final,flag4))
		result_str = bit_mask(str1,final,i)
		return result_str
	elif (bitmask_jug(final,flag3) != False) and (flag_3 == True) and (bitmask_jug(final,flag4) != False) and (flag_4 == True):
		i = min(bitmask_jug(final,flag3),bitmask_jug(final,flag4))
		result_str = bit_mask(str1,final,i)
		return result_str
	elif (bitmask_jug(final,flag2) != False) and (flag_2 == True):
		i = bitmask_jug(final,flag2)
		result_str = bit_mask(str1,final,i)
		return result_str
	elif (bitmask_jug(final,flag3) != False) and (flag_3 == True):
		i = bitmask_jug(final,flag3)
		result_str = bit_mask(str1,final,i)
		return result_str
	elif (bitmask_jug(final,flag4) != False) and (flag_4 == True):
		i = bitmask_jug(final,flag4)
		result_str = bit_mask(str1,final,i)
		return result_str
	elif (bit2_con_jug(final,flag2) == False) and  (flag_2 == True):
		i = flag2[0]
		result_str = bit2nc_mask(final,i)
		return result_str
	else:
		result_str = "000" + str1
		return result_str


"""
main func
"""
def al_compression():
	#set all the position to 0    first rep = 1   second,third....rep = 2,3...
	for i in range(len(original)):
		tag.append(0)

	#find the repeated instrs
	for i in range(len(original)):
		#process the first character
		if i == 0:
			if original[i] == original[i+1]:
				tag[i] = 1
				continue
		#process all the character except the first one
		if (original[i] == original[i-1]):
			if tag[i-1] == 1:
				tag[i] = 2
			elif tag[i-1] == 0:
				tag[i-1] = 1
				tag[i] = 2
			elif tag[i-1] >= 2:
				tag[i] = tag[i-1] + 1
	#process the situation that rep instrs>9
	for i in range(len(tag)):
		if tag[i] == 10:
			tag[i] = 1
		if tag[i] >= 11:
			tag[i] = tag[i] - 9

	#main al
	bit32z = ""

	for i in range(len(original)):
		if tag[i] >= 2:
			if i == len(original) - 1:
				new_str = run_length_encoding(original[i],tag[i])
			if (tag[i+1] == 0) or (tag[i+1] == 1):
				new_str = run_length_encoding(original[i],tag[i])
			else:
				new_str = ""
		else:
			new_str = method_choose(original[i])
		bit32z = bit32z + new_str

	loop = int(len(bit32z)/32)
	more = int(len(bit32z)%32)
	add0 = 32 - more
	
	if loop == 0:
		for i in range(32-len(bit32z)):
			bit32z = bit32z + "0"
		write_file_original(bit32z)
		bit32z = ""
	else:
		if add0 == 32:
			for i in range(loop):
				write_file_original(bit32z[0+32*i:32+32*i])
				write_file_original('\n')
		else:
			for i in range(loop):
				write_file_original(bit32z[0+32*i:32+32*i])
				write_file_original('\n')
			last_line = bit32z[-more:]
			for i in range(add0):
				last_line = last_line + '0'
			write_file_original(last_line)
			write_file_original('\n')
			
	write_file_original("xxxx\n")
	for i in dictionary:
		write_file_original(i)
		write_file_original('\n')
#----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------decompression------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------
""""
Data read and preprocessing
Data write
"""
def read_file_decompressed():
	str = ""
	fp = open("./compressed.txt")
	content = fp.readlines()
	content2 = []
	dictionary = []
	len_con = len(content)
	for i in content:
		if i == content[len_con-1]:
			content2.append(i[0:-1])
			continue
		i = i[0:-1]
		content2.append(i)
	return content2

def write_file_decompressed(compressed):
	f = open("dout.txt","a")
	f.write(compressed)
	f.close()

def reverse(str1):
	new_str1 = ""
	for i in range(len(str1)):
		if str1[i] == '0':
			new_str1 += '1'
		else:
			new_str1 += '0'
	return new_str1

"""
main al
"""
def al_decompression(compressed_data_str):
	i = 0
	list_ready_decomp = []
	while i < len(compressed_data_str):
		if ((i+1) >= len(compressed_data_str)) or ((i+2) >= len(compressed_data_str)):
			break
		
		tmp_head = compressed_data_str[i] + compressed_data_str[i+1] + compressed_data_str[i+2]
		
		if tmp_head == "000" and len(compressed_data_str[i+3:]) < 32:
			break

		if tmp_head == "000":
			final_decomp = compressed_data_str[i:i+35]
			list_ready_decomp.append(final_decomp)
			i = i + 35
			continue
		if tmp_head == "001":
			final_decomp = compressed_data_str[i:i+6]
			list_ready_decomp.append(final_decomp)
			i = i + 6
			continue
		if tmp_head == "010":
			final_decomp = compressed_data_str[i:i+16]
			list_ready_decomp.append(final_decomp)
			i = i + 16
			continue
		if tmp_head == "011":
			final_decomp = compressed_data_str[i:i+12]
			list_ready_decomp.append(final_decomp)
			i = i + 12
			continue
		if tmp_head == "100":
			final_decomp = compressed_data_str[i:i+12]
			list_ready_decomp.append(final_decomp)
			i = i + 12
			continue
		if tmp_head == "101":
			final_decomp = compressed_data_str[i:i+12]
			list_ready_decomp.append(final_decomp)
			i = i + 12
			continue
		if tmp_head == "110":
			final_decomp = compressed_data_str[i:i+17]
			list_ready_decomp.append(final_decomp)
			i = i + 17
			continue
		if tmp_head == "111":
			final_decomp = compressed_data_str[i:i+7]
			list_ready_decomp.append(final_decomp)
			i = i + 7
			continue

	tmp_for_rle = ""

	for i in range(len(list_ready_decomp)):
		if list_ready_decomp[i][0:3] == "000":
			tmp_for_rle = list_ready_decomp[i][3:]
			write_file_decompressed(list_ready_decomp[i][3:])
			write_file_decompressed('\n')
		if list_ready_decomp[i][0:3] == "001":
			loop = int((list_ready_decomp[i][3:]),2)
			for j in range(loop+1):
				write_file_decompressed(tmp_for_rle)
				write_file_decompressed('\n')
		if list_ready_decomp[i][0:3] == "010":
			loc = int(list_ready_decomp[i][3:8],2)
			bitmask = list_ready_decomp[i][8:12]
			dict2 = int(list_ready_decomp[i][12:16],2)
			diction_ele = dict_data[dict2]
			ready_to_pro = diction_ele[loc:loc+4]
			result = str_2_bin(ready_to_pro,bitmask)
			tmp_for_rle = diction_ele[0:loc] + result + diction_ele[loc+4:]
			write_file_decompressed(diction_ele[0:loc] + result + diction_ele[loc+4:])
			write_file_decompressed('\n')
		if list_ready_decomp[i][0:3] == "011":
			loc = int(list_ready_decomp[i][3:8],2)
			dict2 = int(list_ready_decomp[i][8:12],2)
			diction_ele = dict_data[dict2]
			tmp_for_rle = diction_ele[0:loc] + reverse(diction_ele[loc]) + diction_ele[loc+1:]
			write_file_decompressed(diction_ele[0:loc] + reverse(diction_ele[loc]) + diction_ele[loc+1:])
			write_file_decompressed('\n')
		if list_ready_decomp[i][0:3] == "100":
			loc = int(list_ready_decomp[i][3:8],2)
			dict2 = int(list_ready_decomp[i][8:12],2)
			diction_ele = dict_data[dict2]
			tmp_for_rle = diction_ele[0:loc] + reverse(diction_ele[loc:loc+2]) + diction_ele[loc+2:]
			write_file_decompressed(diction_ele[0:loc] + reverse(diction_ele[loc:loc+2]) + diction_ele[loc+2:])
			write_file_decompressed('\n')
		if list_ready_decomp[i][0:3] == "101":
			loc = int(list_ready_decomp[i][3:8],2)
			dict2 = int(list_ready_decomp[i][8:12],2)
			diction_ele = dict_data[dict2]
			tmp_for_rle = diction_ele[0:loc] + reverse(diction_ele[loc:loc+4]) + diction_ele[loc+4:]
			write_file_decompressed(diction_ele[0:loc] + reverse(diction_ele[loc:loc+4]) + diction_ele[loc+4:])
			write_file_decompressed('\n')
		if list_ready_decomp[i][0:3] == "110":
			loc1 = int(list_ready_decomp[i][3:8],2)
			loc2 = int(list_ready_decomp[i][8:13],2)
			dict2 = int(list_ready_decomp[i][13:17],2)
			diction_ele = dict_data[dict2]
			tmp_for_rle = diction_ele[0:loc1] + reverse(diction_ele[loc1]) + diction_ele[loc1+1:loc2] + reverse(diction_ele[loc2]) + diction_ele[loc2+1:]
			write_file_decompressed(diction_ele[0:loc1] + reverse(diction_ele[loc1]) + diction_ele[loc1+1:loc2] + reverse(diction_ele[loc2]) + diction_ele[loc2+1:])
			write_file_decompressed('\n')
		if list_ready_decomp[i][0:3] == "111":
			tmp_for_rle = dict_data[int(list_ready_decomp[i][3:],2)]
			write_file_decompressed(dict_data[int(list_ready_decomp[i][3:],2)])
			write_file_decompressed('\n')

			

if __name__ == '__main__':
	if argv[1] == '1':
		dictionary = []
		original = []
		tag = []
		original = read_file_original()
		dictionary = get_dict(original)
		#main process
		al_compression()
	if argv[1] == '2':
		compressed = []
		compressed_data = []
		dict_data = []
		compressed_data_str = ""
		compressed = read_file_decompressed()
		for i in range(len(compressed)):
			if compressed[i] == "xxxx":
				dict_index = i
				break
			compressed_data.append(compressed[i])
		for i in range(len(compressed)):
			if i >= dict_index + 1:
				dict_data.append(compressed[i])
			else:
				continue
		for i in compressed_data:
			compressed_data_str = compressed_data_str + i
		al_decompression(compressed_data_str)