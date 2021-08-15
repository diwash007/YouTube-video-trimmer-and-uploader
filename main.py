from voperator import Operator


if __name__ == "__main__":

	video_loc = input("Enter video location[local/yt]: ")
	op = Operator(video_loc)
	operation = input("Enter number: \n\t 1. Edit only \n\t 2. Edit and Upload \n\t :")
	op.operate(operation)
	op.backup()