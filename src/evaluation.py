

def bbox_iou(bboxA, bboxB):
    # intersection rectangle coords
	xA = max(bboxA[0], bboxB[0])
	yA = max(bboxA[1], bboxB[1])
	xB = min(bboxA[2], bboxB[2])
	yB = min(bboxA[3], bboxB[3])
	# calc intersection rectangle area
	interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)
	# calc ground-truth and prediction rectangle areas
	boxAArea = (bboxA[2] - bboxA[0] + 1) * (bboxA[3] - bboxA[1] + 1)
	boxBArea = (bboxB[2] - bboxB[0] + 1) * (bboxB[3] - bboxB[1] + 1)
	# calc intersection over union
	iou = interArea / float(boxAArea + boxBArea - interArea)
	return iou

