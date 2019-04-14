import refer
from external import mask
import scipy.io as io
import os.path as osp
import os
import json

def generateMasksAndQueries(MASK_DIR, QUERY_FILE_NAME, refer_obj):
	img_sg_counts = {}
	query_file_str = {}
	print "Creating {} mask files..".format(len(refer_obj.data['annotations']))
	actual_processed = 0
	for i,ann in enumerate(refer_obj.data['annotations']):
		if i % 1000 == 0:
			with open(QUERY_FILE_NAME, 'w') as fp:
				json.dump(query_file_str, fp)
			print "On annotation #{}, processed = {}".format(i,actual_processed)
		if ann['iscrowd'] == 1 or ann['id'] not in refer_obj.annToRef:
			continue
		actual_processed += 1
		image = refer_obj.Imgs[ann['image_id']]
		if type(ann['segmentation']) == list: # polygon
			rle = mask.frPyObjects(ann['segmentation'], image['height'], image['width'])
		else:
			rle = ann['segmentation']
		m = mask.decode(rle)
		m = np.sum(m, axis=2)
		matlab_dict = {'segimg_t': m}
		if ann['image_id'] in img_sg_counts:
			img_sg_counts[ann['image_id']] += 1
			filename = "{}_{}".format(ann['image_id'],img_sg_counts[ann['image_id']])
		else:
			img_sg_counts[ann['image_id']] = 1
			filename = "{}_{}".format(ann['image_id'],img_sg_counts[ann['image_id']])
		io.savemat(osp.join(MASK_DIR,filename),matlab_dict)
		ref = refer_obj.annToRef[ann['id']]
		if filename in query_file_str:
			val = query_file_str[filename] 
		else:
			val = []
		for sentence in ref['sentences']:
			val.append(sentence['raw'])
		query_file_str[filename] = val

MASK_DIR = "data/masks/"
QUERY_FILE_NAME = "query_coco.txt"
if __name__ == '__main__':
	rf = refer.REFER("data/",dataset='refcoco', splitBy='google')
	if not osp.exists(MASK_DIR):
		os.makedirs(MASK_DIR)
	generateMasksAndQueries(MASK_DIR,QUERY_FILE_NAME,rf)
