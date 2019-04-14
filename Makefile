all:
	# install pycocotools/mask locally
	# copy from https://github.com/pdollar/coco.git
	python2 setup.py build_ext --inplace
	rm -rf build

